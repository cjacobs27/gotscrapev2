from django.shortcuts import render
from django.http import HttpResponse
from .models import Character,Gender
from .update import Update
from .infoscrape import Infoscrape
import json
import random


# Create your views here.
def index(request):
    characters = Character.objects.all()
    context = {'characters': characters
                }
    return render(request, 'gotsv2/index.html', context)

def about(request):

    return render(request, 'gotsv2/about.html')

def update(request):
    u = Update()
    u.gender_foreign_key_init()
    u.generate_links()
    u.link_scrape()
    u.character_model_update()
    i = Infoscrape()
    i.encode_gender_and_update()
    i.scrape_titles_and_update_model()

    # Only after the scripts have run will a response be sent to the client.
    print("Updated")
    # This template will be rendered:
    return render(request, 'gotsv2/update.html')

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
    print(json_random_colour_list)
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
    # number_of_titles = c.get_title_numbers()
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
    print(json_random_colour_list)
    context = {
        'names': json.JSONDecoder().decode(names),
        'title_numbers': json.JSONDecoder().decode(number_of_titles),
        'random_colours': json.JSONDecoder().decode(json_random_colour_list)
    }

    return render(request, 'gotsv2/title-graph.html', context)
