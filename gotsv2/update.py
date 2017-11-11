import requests
from django.utils import timezone
import pandas
import re
from bs4 import BeautifulSoup
from .models import Character


class Update():
    def __init__(self):
        regex = (
        '(House|References|Secondary sources|Val|Craster|Hodor|Osha|Primary sources|Bibliography|External links|Other characters|Royal court and officials|Night\\\'s Watch and wildlings|The Sand Snakes)')
        self.p = re.compile(regex)
        self.namelist = []
        self.linklist = []
        self.checklist = []
        self.infolist = []

    def requestNamePage(self):
        #gets code from URL, returns requested url content
        r = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
        self.c = r.content
        #status required for testing
        status = r.status_code
        return status, self.c

    def generatelinks(self):
        soup = BeautifulSoup(self.c, "html.parser")
        self.allnames = soup.find_all("span", {"class": "mw-headline"})
        # for item in self.allnames[:12]:
        for item in self.allnames:
            name = item.text
            if self.p.match(name) is None:
                # gotta check for Ned specifically as his char page is Ned_Stark but name listed everywhere as Eddard
                #....turns out I have to screen out a few more... not great.
                if name == "Eddard Stark":
                    self.namelist.append("Ned Stark")
                    rightname = "Ned_Stark"
                    url = str("https://en.wikipedia.org/wiki/" + rightname)
                    self.linklist.append(url)
                elif name == "Gilly":
                    self.namelist.append("Gilly")
                    rightname = "Gilly_(A_Song_of_Ice_and_Fire)"
                    url = str("https://en.wikipedia.org/wiki/" + rightname)
                    self.linklist.append(url)
                else:
                    self.namelist.append(name)
                    urlend = name.replace(" ", "_")
                    underscore = "_"
                    if urlend.endswith(underscore):
                        # takes off the last underscore if present using indexing
                        urlend = urlend[0:-1]
                        # print(urlend)
                    url = str("https://en.wikipedia.org/wiki/" + urlend)
                    self.linklist.append(url)
            else:
                pass


                # character page exists checker - scrapes for redirect link text (this is the name of the character if redirected to
                # the 'list of characters' page

    def linkscrape(self):
        a = 0
        for item in self.linklist:
            request = requests.get(item)
            z = request.content
            global soup2
            soup2 = BeautifulSoup(z, "html.parser")
            if "may refer to" in soup2.text:
                self.trychar(request, item)
            else:
                try:
                    redirected = soup2.find("a", {"class:", "mw-redirect"}).text
                    if redirected == self.namelist[a]:
                        self.checklist.append(0)
                        self.infolist.append("")
                    else:
                        self.getinfobox(item)
                except:
                    self.checklist.append(0)
                    self.infolist.append("")
            print(str(a) + "checked")
            a = a + 1

    def trychar(self, request, item):
        try:
            request2 = requests.get(str(item) + "_(character)")
            y = request2.content
            soup3 = BeautifulSoup(y, "html.parser")
            infobox2 = soup3.find(("table", {"class:", "infobox"}))
            infobox = infobox2.encode('utf-8').strip()
            if "Male" or "Female" in infobox:
                self.checklist.append(1)
                self.infolist.append(infobox)
            else:
                try:
                    request2 = requests.get(str(item) + "_(A_Song_of_Ice_and_Fire)")
                    y = request2.content
                    soup3 = BeautifulSoup(y, "html.parser")
                    infobox2 = soup3.find(("table", {"class:", "infobox"}))
                    infobox = infobox2.encode('utf-8').strip()
                    if "Male" or "Female" in infobox:
                        self.checklist.append(1)
                        self.infolist.append(infobox)
                except:
                    self.checklist.append(0)
                    self.infolist.append("")
        except:
            self.checklist.append(0)
            self.infolist.append("")

    def getinfobox(self, item):
        try:
            table = soup2.find_all(("table", {"class:", "infobox"}))
            infobox = table[0].encode('utf-8').strip()
            if str(infobox).startswith("b'<table class=\"infobox\""):
                self.checklist.append(1)
                self.infolist.append(infobox)
            else:
                self.refineinfobox(item, table)
        except:
            self.checklist.append(0)
            self.infolist.append("")

    def refineinfobox(self, item, table):
        t = False
        for i in range(4):
            if "infobox" in str(table[i]):
                index = i
                t = True
                break
        while t is True:
            infobox = table[index].encode('utf-8').strip()
            self.checklist.append(1)
            self.infolist.append(infobox)
            break
        if t is False:
            self.checklist.append(0)
            self.infolist.append("")


    def CharacterModelUpdate(self):
        unordered_df = pandas.DataFrame(
            {'Names': self.namelist,
             'URLs': self.linklist,
             'Pages': self.checklist,
             'Infoboxes': self.infolist})
        df = unordered_df[['Names', 'URLs', 'Pages', 'Infoboxes']]
        a = 0
        for item in df['Names']:
            m = Character(name=df['Names'][a], url=df['URLs'][a], page=df['Pages'][a], infobox=df['Infoboxes'][a], created_at=timezone.now(), updated_at=timezone.now())
            if df['Pages'][a] == 1:
                u = df['URLs'][a]
                if self.CheckForUpdateDuplicates(u) is True:
                    print(u, " already in there")
                    pass
                else:
                    print(u, " will be added")
                    m.save()
            else:
                pass
            a = a + 1

    def CheckForUpdateDuplicates(self,u):
        try:
            Character.objects.get(url=u)
            return True
        except Character.DoesNotExist:
            return False
            pass

