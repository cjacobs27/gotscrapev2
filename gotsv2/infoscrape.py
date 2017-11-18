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
            update_gender= i
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

    def title_text_scrape(self):
        for character in Character.objects.all():
            infobox = character.infobox
            html = BeautifulSoup(infobox, "html.parser")
            table_rows = html.find_all('tr')
            for row in table_rows:
                header = row.find('th', {'scope': 'row'}, 'Title')
                try:
                    if 'Title' in header.text:
                        # value = row.find('ul')
                        value = row.find('ul').text
                        print(value, "...THAT WAS THE VALUE (their titles)")
                        # code just ignores next line... idk
                        character.titles = value
                        character.save()
                    else:
                        pass
                except AttributeError:
                    pass

# previous idea:
        #         if "Title" in str(header):
        #             try:
        #                 single_character_titles = value.text
        #                 print(single_character_titles)
        #                 self.titles.append(single_character_titles)
        #             except AttributeError:
        #                 # print(value)
        #                 pass
        #         else:
        #             pass
        # print(self.titles)
        # print(len(self.titles))


    # def update_character_model_with_title_lists(self):
    #     a = 0
    #     for i in Character.objects.all():
    #         update_title = self.titles[a]
    #         i.titles = update_title
    #         i.titles.save()


    def scrape_titles_and_update_model(self):
        self.title_text_scrape()
        # self.update_character_model_with_title_lists()
