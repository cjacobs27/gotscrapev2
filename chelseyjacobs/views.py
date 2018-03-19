from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def makesandwich(request):
    return render(request, 'makesandwich.html')
