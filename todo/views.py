from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homePage(request):
    context = {}
    return render(request,'todo/home.html',context)