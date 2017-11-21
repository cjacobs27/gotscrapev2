from django.shortcuts import render
from django.http import HttpResponse
from .models import Character,Gender
from .update import Update
from .infoscrape import Infoscrape
import json


# Create your views here.
def index(request):
    characters = Character.objects.all()
    context = {'characters': characters}
    return render(request, 'gotsv2/index.html', context)


def update(request):
    # u = Update()
    # u.generate_links()
    # u.link_scrape()
    # u.character_model_update()
    i = Infoscrape()
    # i.encode_gender_and_update()
    i.scrape_titles_and_update_model()

    # Only after the scripts have run will a response be sent to the client.
    # This template will be rendered:
    return render(request, 'gotsv2/update.html')

def graph(request):
    #call get_gender_split()
    c = Character()
    json_percentages = c.get_gender_split()

    # names = json.dumps(c.get_character_names())
    names = c.get_character_names()
    number_of_titles = c.get_title_numbers()
    context = {
        'percentages': json_percentages,
        # 'names': json.JSONDecoder().decode(names),
        'names': json.JSONDecoder().decode(names),
        # 'names': names,
        'title_numbers': json.JSONDecoder().decode(number_of_titles),
    }
    print(names)
    return render(request, 'gotsv2/graph.html', context)
