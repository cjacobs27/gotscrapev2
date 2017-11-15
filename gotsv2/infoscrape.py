from bs4 import BeautifulSoup
from django.db import models
from gotsv2.models import Character, Gender

class Infoscrape():
    def __init__(self):
        self.genders = []
        self.unencodedGender = []
        self.dbCharacterObjects = Character.objects.values_list('infobox', flat=True)

    def encode_gender_and_update(self):
        # scrapes infobox text, sorts into male & female, updates Character model
        for item in self.dbCharacterObjects:
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
        for item in self.unencodedGender:
            if "Female" in item:
                self.genders.append("2")
            else:
                self.genders.append("1")
        a = 0
        for i in Character.objects.all():
            update_gender = i
            if int(self.genders[a]) == 1:
                update_gender.gender = Gender(1)
                update_gender.save()
            else:
                update_gender.gender = Gender(2)
                update_gender.save()
            a = a + 1

   # Commented out code is probably a better way of doing this...
   # but not right now

    # def gender_text_scrape(self):
    #     for item in self.dbCharacterObjects:
    #         html = BeautifulSoup(item, "html.parser")
    #         table_rows = html.find_all('tr')
    #         for row in table_rows:
    #             header = row.find('th', {'scope': 'row'}, 'Gender')
    #             value = row.find('td')
    #             if "Gender" in str(header):
    #                 gender = value.text
    #                 self.unencodedGender.append(gender)
    #             else:
    #                 pass
    #
    # def label_male(self):
    #     a = 0
    #     for i in Character.objects.all():
    #         update_gender= i
    #         if self.unencodedGender[a] == "Male":
    #             update_gender.gender = Gender(1)
    #             update_gender.save()
    #         elif self.unencodedGender[a] == "Female":
    #             update_gender.gender = Gender(2)
    #             update_gender.save()
    #         a = a + 1
    # def encode_gender_and_update(self):
    #     gender_text_scrape(self)
    #     label_male(self)


