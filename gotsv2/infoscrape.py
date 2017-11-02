from bs4 import BeautifulSoup
from django.db import models
from gotsv2.models import Character, Gender

class Infoscrape():
    def __init__(self):
        self.genders = []
        self.unencodedGender = []
        self.dbCharacterObjects = Character.objects.values_list('infobox', flat=True)

    def getInfoboxCode(self):
        for item in self.dbCharacterObjects:
            html = BeautifulSoup(item, "html.parser")
            #gotta scrape html now
            table_rows = html.find_all('tr')
            for row in table_rows:
                header = row.find('th')
                value = row.find('td')
                # print(type(header))
                if "Gender" in str(header):
                    gender = value.text
                    self.unencodedGender.append(gender)
        self.encodeGender()

    def encodeGender(self):
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
        # a = 1
        # for i in self.genders:
        #     updategender = Character.objects.get(pk=1)
        #     updategender.gender = i
        #     updategender.save()
        #     a = a + 1

        # for p in self.genders:
        #     name = Character.objects.filter(pk=a).values('name')
        #     g = Gender(character=p, name=name)
        #     print(g)

        # malecount = len(male)
        # femalecount = len(female)
        # genderPieChart(malecount,femalecount)

