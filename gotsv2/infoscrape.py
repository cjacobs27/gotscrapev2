from bs4 import BeautifulSoup
from django.db import models
from gotsv2.models import Character, Gender

class Infoscrape():
    def __init__(self):
        self.genders = []
        self.unencodedGender = []
        self.dbCharacterObjects = Character.objects.values_list('infobox', flat=True)
        self.html = ''

    def getinfoboxcode(self):
        for item in self.dbCharacterObjects:
            self.html = BeautifulSoup(item, "html.parser")

    def encodegender(self):
        #THERE IS A BUG IN THIS WHICH COULD BE IDENTIFIED IF I COULD FIGURE OUT HOW TO SEE
        #len(self.genders) AFTER IT HAS BEEN POPULATED.
        table_rows = self.html.find_all('tr')
        for row in table_rows:
            header = row.find('th')
            value = row.find('td')
            # print(type(header))
            if "Gender" in str(header):
                gender = value.text
                self.unencodedGender.append(gender)
        for item in self.unencodedGender:
            if "Female" in item:
                self.genders.append("2")
            else:
                self.genders.append("1")
        a = 0
        #GENDERS DOES NOT HAVE ENOUGH LIST ENTRIES
        #SOME ARE BEING MISSED
        #THIS CAUSES AN INDEX ERROR WHEN RUNNING THE BELOW:
        for i in Character.objects.all():
            updategender= i
            if int(self.genders[a]) == 1:
                updategender.gender = Gender(1)
                updategender.save()
            else:
                updategender.gender = Gender(2)
                updategender.save()
            a = a + 1

