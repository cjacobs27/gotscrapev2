import requests
from django.utils import timezone
import pandas
import re
from bs4 import BeautifulSoup
from .models import Character, Gender


class Update:
    def __init__(self):
        regex = (
        '(House|References|Secondary sources|Val|Craster|Hodor|Osha|Primary sources|Bibliography|External links|Other characters|Royal court and officials|Night\\\'s Watch and wildlings|The Sand Snakes)')
        self.name_page = "https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters"
        self.p = re.compile(regex)
        self.name_list = []
        self.link_list = []
        self.check_list = []
        self.info_list = []

    def get_name_page_content(self):
        return requests.get(self.name_page).content

    def generate_links(self):
        soup = BeautifulSoup(self.get_name_page_content(), "html.parser")
        allnames = soup.find_all("span", {"class": "mw-headline"})
        # for item in allnames[:12]:
        for item in allnames:
            name = item.text
            if self.p.match(name) is None:
                # gotta check for Ned specifically as his char page is Ned_Stark but name listed everywhere as Eddard
                # and TIL Gilly is also an island
                if name == "Eddard Stark":
                    self.name_list.append("Ned Stark")
                    correct_name_to_match_url = "Ned_Stark"
                    url = str("https://en.wikipedia.org/wiki/" + correct_name_to_match_url)
                    self.link_list.append(url)
                elif name == "Gilly":
                    self.name_list.append("Gilly")
                    correct_name_to_match_url = "Gilly_(A_Song_of_Ice_and_Fire)"
                    url = str("https://en.wikipedia.org/wiki/" + correct_name_to_match_url)
                    self.link_list.append(url)
                else:
                    self.name_list.append(name)
                    url_suffix = name.replace(" ", "_")
                    underscore = "_"
                    if url_suffix.endswith(underscore):
                        # takes off the last underscore if present using indexing
                        url_suffix = url_suffix[0:-1]
                        # print(url_suffix)
                    url = str("https://en.wikipedia.org/wiki/" + url_suffix)
                    self.link_list.append(url)
            else:
                pass
        list_for_testing = [self.name_list, self.link_list]
        return list_for_testing

    def link_scrape(self):
        a = 0
        for item in self.link_list:
            request = requests.get(item)
            z = request.content
            global soup2
            soup2 = BeautifulSoup(z, "html.parser")
            if "may refer to" in soup2.text:
                self.try_adding_character_suffix_to_url(item)
            else:
                try:
                    redirected = soup2.find("a", {"class:", "mw-redirect"}).text
                    if redirected == self.name_list[a]:
                        self.check_list.append(0)
                        self.info_list.append("")
                    else:
                        self.get_infobox(item)
                except:
                    self.check_list.append(0)
                    self.info_list.append("")
            print(str(a) + "checked")
            a = a + 1
            print()

    def try_adding_character_suffix_to_url(self, item):
        try:
            request2 = requests.get(str(item) + "_(character)")
            y = request2.content
            soup3 = BeautifulSoup(y, "html.parser")
            infobox2 = soup3.find(("table", {"class:", "infobox"}))
            infobox = infobox2.encode('utf-8').strip()
            if "Male" or "Female" in infobox:
                self.check_list.append(1)
                self.info_list.append(infobox)
            else:
                try:
                    request2 = requests.get(str(item) + "_(A_Song_of_Ice_and_Fire)")
                    y = request2.content
                    soup3 = BeautifulSoup(y, "html.parser")
                    infobox2 = soup3.find(("table", {"class:", "infobox"}))
                    infobox = infobox2.encode('utf-8').strip()
                    if "Male" or "Female" in infobox:
                        self.check_list.append(1)
                        self.info_list.append(infobox)
                except:
                    self.check_list.append(0)
                    self.info_list.append("")
        except:
            self.check_list.append(0)
            self.info_list.append("")

    def get_infobox(self, item):
        try:
            table = soup2.find_all(("table", {"class:", "infobox"}))
            infobox = table[0].encode('utf-8').strip()
            if str(infobox).startswith("b'<table class=\"infobox\""):
                self.check_list.append(1)
                self.info_list.append(infobox)
            else:
                self.refine_infobox(item, table)
        except:
            self.check_list.append(0)
            self.info_list.append("")

    def refine_infobox(self, item, table):
        t = False
        for i in range(4):
            if "infobox" in str(table[i]):
                index = i
                t = True
                break
        while t is True:
            infobox = table[index].encode('utf-8').strip()
            self.check_list.append(1)
            self.info_list.append(infobox)
            break
        if t is False:
            self.check_list.append(0)
            self.info_list.append("")

    def character_model_update(self):
        unordered_df = pandas.DataFrame(
            {'Names': self.name_list,
             'URLs': self.link_list,
             'Pages': self.check_list,
             'Infoboxes': self.info_list})
        df = unordered_df[['Names', 'URLs', 'Pages', 'Infoboxes']]
        a = 0
        for item in df['Names']:
            m = Character(name=df['Names'][a], url=df['URLs'][a], page=df['Pages'][a], infobox=df['Infoboxes'][a], created_at=timezone.now(), updated_at=timezone.now())
            if df['Pages'][a] == 1:
                u = df['URLs'][a]
                if self.check_for_update_duplicates(u) is True:
                    print(u, " already in there    (", item ,")")
                else:
                    print(u, " will be added    (", item ,")")
                    m.save()
            else:
                pass
            a = a + 1

    def gender_foreign_key_init(self):
        gender_foreign_key_1 = Gender(id=1, name='Male')
        gender_foreign_key_2 = Gender(id=2, name='Female')
        gender_foreign_key_1.save()
        gender_foreign_key_2.save()

    def check_for_update_duplicates(self, u):
        try:
            Character.objects.get(url=u)
            return True
        except Character.DoesNotExist:
            return False


