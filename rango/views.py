from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category, Page

def index(request) :
    # Sorts the categories by likes in descending order('-' before likes)
    # and retrieves only the first five
    category_list = Category.objects.order_by('-likes')[:5]
    top_five_most_viewed_pages = Page.objects.order_by('-views')[:5]

    context_dic = {}
    context_dic['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dic['categories'] = category_list
    context_dic['pages'] = top_five_most_viewed_pages

    return render(request, 'rango/index.html', context=context_dic)

def about(request) :
    return render(request, 'rango/about.html')

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

