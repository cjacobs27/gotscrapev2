from django.db import models
import json


class Gender(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    page = models.TextField()
    infobox = models.TextField()
    created_at = models.DateTimeField('created')
    updated_at = models.DateTimeField('last updated')
    gender = models.ForeignKey(Gender)
    titles = models.TextField(null=True, default=None)
    title_strings = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name

    # get gender split
    def get_gender_split(self):
        number_of_women = Character.objects.filter(gender_id='2').count()
        number_of_men = Character.objects.filter(gender_id='1').count()
        total_people = number_of_men + number_of_women
        female_percentage = round((number_of_women / total_people) * 100, 2)
        male_percentage = round((number_of_men / total_people) * 100, 2)
        json_percentages = json.JSONEncoder().encode([female_percentage, male_percentage])
        return json_percentages

    def get_title_numbers(self):
        number_of_titles_list = []
        for character in Character.objects.all():
            json_object = character.titles
            if json_object == "":
                pass
            elif json_object is None:
                number_of_titles_list.append(0)
            else:
                decoded_character_title = json.JSONDecoder().decode(json_object)
                number_of_titles = len(decoded_character_title.get('titles'))
                number_of_titles_list.append(number_of_titles)
        encoded_number_of_titles_list = json.dumps(number_of_titles_list)
        return encoded_number_of_titles_list

    def get_character_names(self):
        names = []
        for character in Character.objects.all():
            name = character.name
            names.append(name)
        names_encoded = json.dumps(names)
        return names_encoded





