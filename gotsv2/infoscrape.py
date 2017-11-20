from bs4 import BeautifulSoup
from gotsv2.models import Character, Gender
import json
import re


class Infoscrape:
    def __init__(self):
        self.genders = []
        self.unencodedGender = []
        self.titles = []
        self.db_character_infoboxes = Character.objects.values_list('infobox', flat=True)

    def gender_text_scrape(self):
        for item in self.db_character_infoboxes:
            html = BeautifulSoup(item, "html.parser")
            table_rows = html.find_all('tr')
            for row in table_rows:
                header = row.find('th', {'scope': 'row'}, 'Gender')
                value = row.find('td')
                if "Gender" in str(header):
                    gender = value.text
                    self.unencodedGender.append(gender)
                else:
                    pass

    def label_male_and_female(self):
        a = 0
        for i in Character.objects.all():
            update_gender = i
            if self.unencodedGender[a] == "Male":
                update_gender.gender = Gender(1)
                update_gender.save()
            elif self.unencodedGender[a] == "Female":
                update_gender.gender = Gender(2)
                update_gender.save()
            a = a + 1

    def encode_gender_and_update(self):
        self.gender_text_scrape()
        self.label_male_and_female()

# right, now let's do the same for titles (possibly a better way of doing this below

    # def split_titles(self, value):
    #
    # def scrape_titles(self):
    #     for character in Character.objects.all():
    #         print("CHARACTER: ", character.name)
    #         infobox = character.infobox
    #         html = BeautifulSoup(infobox, "html.parser")
    #         table_rows = html.find_all('tr')
    #         for row in table_rows:
    #             header = row.find('th', {'scope': 'row'}, 'Title')
    #             try:
    #                 if 'Title' in header.text:
    #                     value = row.find('td').text
    #                     split_titles(value)
    #
    # def scrape_titles_encode_json_update_model:
    #     scrape_titles()
    #     split_titles()
    #     encode_titles_json()
    #     titles_update_model()

    def scrape_titles_and_update_model(self):
        for character in Character.objects.all():
            print("CHARACTER: ", character.name)
            infobox = character.infobox
            html = BeautifulSoup(infobox, "html.parser")
            table_rows = html.find_all('tr')
            for row in table_rows:
                header = row.find('th', {'scope': 'row'}, 'Title')
                try:
                    if 'Title' in header.text:
                        value = row.find('td').text
                        print("VALUE: ", value)
                        titles_as_items_in_list = value.split("\n")
                        clean_titles = []
                        clean_titles_dict = {}
                        for title in titles_as_items_in_list:
                            if title == "":
                                pass
                            else:
                                clean_titles.append(title)
                        a = 0
                        for item in clean_titles:
                            key = 'title'+str(a)
                            clean_titles_dict.update({key: item})
                            a = a + 1
                        print(clean_titles_dict)
                        print(type(clean_titles_dict))
                        # THESE NEED TO BE JSON OBJECTS NOT STRINGS OTHERWISE CAN'T COUNT THEM FROM DB
                        json_encoded_titles = json.dumps(clean_titles_dict)
                        # this is a string??? I give up
                        print(type(json_encoded_titles))
                        # character.titles = json_encoded_titles
                        # character.save()
                    else:
                        pass
                except AttributeError:
                    pass

