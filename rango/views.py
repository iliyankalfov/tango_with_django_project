from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rango.models import Category

def index(request) :
    # Sorts the categories by likes in descending order('-' before likes)
    # and retrieves only the first five
    category_list = Category.objects.order_by('-likes')[:5]

    context_dic = {}
    context_dic['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dic['categories'] = category_list

    return render(request, 'rango/index.html', context=context_dic)

def about(request) :
    return render(request, 'rango/about.html')

