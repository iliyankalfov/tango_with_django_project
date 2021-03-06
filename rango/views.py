from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request) :
    # Sorts the categories by likes in descending order('-' before likes)
    # and retrieves only the first five
    category_list = Category.objects.order_by('-likes')[:5]
    top_five_most_viewed_pages = Page.objects.order_by('-views')[:5]

    context_dic = {}
    context_dic['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dic['categories'] = category_list
    context_dic['pages'] = top_five_most_viewed_pages

    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dic)
    return response

def about(request) :
    context_dic = {}

    visitor_cookie_handler(request)
    context_dic['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dic)

def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits','1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def show_category(request, category_name_slug):
    context_dic = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dic['pages'] = pages
        context_dic['category'] = category
    except Category.DoesNotExist:
        context_dic['category'] = None
        context_dic['pages'] = None

    return render(request, 'rango/category.html', context=context_dic)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs = {'category_name_slug':category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form' : form, 'category' : category}
    return render(request, 'rango/add_page.html', context=context_dict)

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
