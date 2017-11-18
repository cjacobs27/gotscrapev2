from bs4 import BeautifulSoup
from gotsv2.models import Character, Gender


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

#right, now let's do the same for titles

    def scrape_titles_and_update_model(self):
        for character in Character.objects.all():
            print(character.name)
            infobox = character.infobox
            html = BeautifulSoup(infobox, "html.parser")
            table_rows = html.find_all('tr')
            for row in table_rows:
                header = row.find('th', {'scope': 'row'}, 'Title')
                try:
                    if 'Title' in header.text:
                        value = row.find('td').text
                        character.titles = value
                        character.save()
                    else:
                        pass
                except AttributeError:
                    pass
