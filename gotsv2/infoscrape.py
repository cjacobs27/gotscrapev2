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
        self.encodeGender(self.unencodedGender)

    def encodeGender(self,unencodedGender):
        for item in unencodedGender:
            if "Female" in item:
                self.genders.append("1")
            else:
                self.genders.append("1")
        a = 1
        # for p in self.genders:
        #     name = Character.objects.filter(pk=a).values('name')
        #     g = Gender(character=p, name=name)
        #     print(g)

        # malecount = len(male)
        # femalecount = len(female)
        # genderPieChart(malecount,femalecount)

