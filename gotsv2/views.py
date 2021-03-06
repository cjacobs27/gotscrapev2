from django.shortcuts import render
from django.http import HttpResponse
from .models import Character
from .update import Update
from .infoscrape import Infoscrape
import json
import random


# Create your views here.

def gotsv2(request):
    characters = Character.objects.all()

    context = {'characters': characters,
               # 'clean_titles': clean_titles()
               }
    return render(request, 'gotsv2/gotsv2.html', context)


def about(request):

    return render(request, 'gotsv2/about.html')

def graph(request):
    c = Character()
    json_percentages = c.get_gender_split()
    names = c.get_character_names()
    number_of_titles = c.get_title_numbers()
    random_colour_list = []
    for colour in range(50):
        r = lambda: random.randint(0, 255)
        random_colour = '#%02X%02X%02X' % (r(), r(), r())
        random_colour_list.append(random_colour)
    json_random_colour_list = json.dumps(random_colour_list)
    context = {
        'percentages': json_percentages,
        'names': json.JSONDecoder().decode(names),
        'title_numbers': json.JSONDecoder().decode(number_of_titles),
        'random_colours': json.JSONDecoder().decode(json_random_colour_list),
        'gender_graph': render(request, 'gotsv2/gender-graph.html')
    }

    return render(request, 'gotsv2/graph.html', context)


def gender_graph_page(request):
    c = Character()
    json_percentages = c.get_gender_split()
    names = c.get_character_names()
    context = {
        'percentages': json_percentages,
        'names': json.JSONDecoder().decode(names),
    }

    return render(request, 'gotsv2/gender-graph.html', context)

def title_graph_page(request):
    c = Character()
    names = c.get_character_names()
    number_of_titles = c.get_title_numbers()
    random_colour_list = []
    for colour in range(50):
        r = lambda: random.randint(0, 255)
        random_colour = '#%02X%02X%02X' % (r(), r(), r())
        random_colour_list.append(random_colour)
    json_random_colour_list = json.dumps(random_colour_list)
    context = {
        'names': json.JSONDecoder().decode(names),
        'title_numbers': json.JSONDecoder().decode(number_of_titles),
        'random_colours': json.JSONDecoder().decode(json_random_colour_list)
    }

    return render(request, 'gotsv2/title-graph.html', context)
