from django.shortcuts import render
from django.http import HttpResponse
from .models import Character,Gender
from .update import Update
from .infoscrape import Infoscrape


# Create your views here.
def index(request):
    characters = Character.objects.all()
    context = {'characters': characters}
    return render(request, 'gotsv2/index.html', context)


def update(request):
    u = Update()
    u.generatelinks()
    u.linkscrape()
    u.CharacterModelUpdate()
    i = Infoscrape()
    i.encodegender()

    # Only after the scripts have run will a response be sent to the client.
    # This template will be rendered:
    return render(request, 'gotsv2/update.html')
