from django.http import HttpResponse
from django.shortcuts import render


def starting_page(request):
    return render(request, 'blog/index.html')


def posts(request):
    return HttpResponse('Posts')


def post_detail(request):
    return HttpResponse('Post details')
