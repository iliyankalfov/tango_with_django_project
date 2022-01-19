from django.shortcuts import render
from django.http import HttpResponse

def index(request) :
    context_dic = {'boldmessage':'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context_dic)

def about(request) :
    return HttpResponse('<a href="/rango/">Index</a>')

