import requests
from django.test import TestCase
from django.test import Client
from .update import Update
from .models import Character
from .infoscrape import Infoscrape
from datetime import datetime
import json
from django.utils.timezone import make_aware
from bs4 import BeautifulSoup
import pandas

class TemplateViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        number_of_objects = 130
        for object_num in range(number_of_objects):
            if object_num % 2 == 0:
                one_or_two = 1
            else:
                one_or_two = 2
            clean_titles = [["title1"],["t2"],["t3"]]
            clean_titles_dict = {}
            clean_titles_dict.update({"titles": clean_titles})
            json_encoded_titles = json.JSONEncoder().encode(clean_titles_dict)
            time = datetime.now()
            a_time = make_aware(time, timezone=None, is_dst=None)
            Character.objects.create(name='Name %s' % object_num, url='URL %s' % object_num, page = one_or_two,
                                     infobox='Infobox HTML %s' % object_num, created_at=a_time, updated_at=a_time,
                                     gender_id= one_or_two, titles=json_encoded_titles, title_strings='title strings %s' % object_num)

    #does the about page display
    def test_about_page_displays(self):
        c = Client()
        response = c.post('/gotsv2/about/')
        self.assertEqual(response.status_code, 200)

    #does the gender-graph page display
    def test_gender_graph_page_displays(self):
        c = Client()
        response = c.post('/gotsv2/gender-graph/')
        self.assertEqual(response.status_code, 200)

    #does the gotsv2 page display
    def test_gotsv2_page_displays(self):
        c = Client()
        response = c.post('/gotsv2/')
        self.assertEqual(response.status_code, 200)

    #does the graph page display
    def test_graph_page_displays(self):
        c = Client()
        response = c.post('/gotsv2/graph/')
        self.assertEqual(response.status_code,200)

    #does the title graph page display
    def test_title_graph_page_displays(self):
        c = Client()
        response = c.post('/gotsv2/title-graph/')
        self.assertEqual(response.status_code,200)


class InfoscrapeTests(TestCase):
    def setUp(self):
        # client may not be needed
        self.client = Client()
        # lists for use with Infoscrape methods
        # generating slightly different test db from before due to needing proper infobox data:
        number_of_objects = 130
        test_infobox = open('gotsv2/test_infobox.html')
        infobox_html = BeautifulSoup(test_infobox, "html.parser")
        for object_num in range(number_of_objects):
            if object_num % 2 == 0:
                one_or_two = 1
            else:
                one_or_two = 2
            time = datetime.now()
            a_time = make_aware(time, timezone=None, is_dst=None)
            Character.objects.create(name='Name', url='URL', page = one_or_two,
                                     infobox=str(infobox_html), created_at=a_time, updated_at=a_time,
                                     gender_id= one_or_two, titles= 'titles', title_strings='title strings')

    def test_gender_text_scrape_method_list_complete(self):
        # if the unencodedGender list is 130 items (the number of fake characters in the TestCase)
        # then gender info has been scraped from each page
        self.db_character_infoboxes = Character.objects.values_list('infobox', flat=True)
        i = Infoscrape()
        i.gender_text_scrape()
        genders = i.unencodedGender
        self.assertEqual(len(genders), 130)

    def test_gender_text_scrape_method_list_correct(self):
        # if the unencodedGender list contains anything except 'Male' or 'Female' there's been an error.
        self.db_character_infoboxes = Character.objects.values_list('infobox', flat=True)
        i = Infoscrape()
        i.gender_text_scrape()
        genders = i.unencodedGender

        def check_list_correct():
            for item in genders:
                if 'Male' or 'Female' in item:
                    return True
                else:
                    print(item)
                    return False
        self.assertTrue(check_list_correct(), True)

    def test_label_male_and_female_updates_db(self):
        i = Infoscrape()
        # need to run i.gender_text_scrape() to generate unencodedGender list in TestCase
        i.gender_text_scrape()
        genders = i.unencodedGender
        i.label_male_and_female()
        # as the dummy infoscrape code is for a Male character, all gender_ids should be saved to Male (1)
        # TestCase db alternates gender so half is 1 and half is 2
        test_db_gender_ids = Character.objects.values_list('gender_id', flat=True)
        def check_gender_ids():
            for item in test_db_gender_ids:
                if item == 1:
                    return True
                else:
                    print(item)
                    return False
        # bear in mind that the gender_id for all Test Characters in test db is now 1
        self.assertTrue(check_gender_ids(), True)

    def test_scrape_titles_and_update_model_scrapes_correctly(self):
        # this test checks both the content and type (str as JSON encoded) of this method's output
        i = Infoscrape()
        ned_stark_titles = i.scrape_titles_and_update_model()
        # str below is expected output of above method (changed from dict to str so can be tested)
        # as it's the correct scrape result from dummy infobox
        check_against = {"titles": ["Lord of Winterfell", "Lord Paramount and Warden of the North",
                                        "Hand of the King", "Protector of the Realm", "Lord Regent of the Seven Kingdoms"]}
        # in order for check_against to match this method's output it must be JSON encoded
        # as the titles in the db were already encoded in the real script before being saved
        json_check_against = json.JSONEncoder().encode(check_against)
        self.assertEqual(ned_stark_titles, json_check_against, True)

    def test_scrape_titles_and_update_model_updates_model(self):
        # this looks a little dodge but does work - comment out next two lines and run test suite if
        # momentarily lacking in confidence - all 3 print statements will be called
        i = Infoscrape()
        i.scrape_titles_and_update_model()
        after_method_run = Character.objects.values_list('titles', flat=True)

        def check_titles_populated():
            # setting token to False initially so then it needs to be changed to True to confirm working
            # rather than just remaining True and being changed to False
            token = False
            if len(after_method_run[0]) < 10:
                print("NUMBER 1.....", after_method_run[0])
                token = False
            else:
                token = True
            if len(after_method_run[65]) < 10:
                print("NUMBER 2.....", after_method_run[65])
                token = False
            else:
                token = True
            if len(after_method_run[129]) < 10:
                print("NUMBER 3.....", after_method_run[129])
                token = False
            else:
                token = True

            self.assertTrue(token, True)
        check_titles_populated()




# class UpdateMethodTests(TestCase):
    #all these tests might be a bit dodgy, will come back to these
    #they're currently broken because I've commented out dodgy code in update.py which only seems to
    #be there for testing purposes


    # def test_see_if_main_page_content_returned_successfully(self):
    #     request = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
    #     self.assertEqual(request.content, Update().get_name_page_content())
    #
    # #generate_links()
    #
    # # def test_if_name_list_is_a_list(self):
    # #     test_link_list = Update().generate_links()
    # #     self.assertEqual(type(test_link_list[0]), list)
    # #
    #
    # def test_if_name_list_is_a_list(self):
    #     name_list = Update().generate_links(name_list)
    #     self.assertEqual(type(name_list), list)
    #
    # def test_if_link_list_is_a_list(self):
    #     test_link_list = Update().generate_links()
    #     self.assertEqual(type(test_link_list[1]), list)
    #
    # def test_if_name_list_populated(self):
    #     # checks if there's stuff in the list as it could be empty
    #     test_link_list = Update().generate_links()
    #     self.assertTrue(len(test_link_list[0]) >= 3)
    #
    # def test_if_link_list_populated(self):
    #     # checks if there's stuff in the list as it could be empty
    #     test_link_list = Update().generate_links()
    #     self.assertTrue(len(test_link_list[1]) >= 3)
    #
    # def test_if_link_list_and_name_list_same_length(self):
    #     # if not same length then indicates error with appending either list
    #     test_link_list = Update().generate_links()
    #     self.assertEqual(len(test_link_list[0]), len(test_link_list[1]))
