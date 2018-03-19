from django.shortcuts import render


def makesandwich(request):
    return render(request, 'makesandwich.html')
