from bs4 import BeautifulSoup
from django.db import models
from gotsv2.models import Character, Gender

class Infoscrape():
    def __init__(self):
        self.genders = []
        self.unencodedGender = []
        self.dbCharacterObjects = Character.objects.values_list('infobox', flat=True)

    def encodegender(self):
        for item in self.dbCharacterObjects:
            html = BeautifulSoup(item, "html.parser")
            table_rows = html.find_all('tr')
            for row in table_rows:
                header = row.find('th', {'scope': 'row'}, 'Gender')
                value = row.find('td')
                if "Gender" in str(header):
                    gender = value.text
                    print(header)
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
            updategender= i
            if int(self.genders[a]) == 1:
                updategender.gender = Gender(1)
                updategender.save()
            else:
                updategender.gender = Gender(2)
                updategender.save()
            a = a + 1

