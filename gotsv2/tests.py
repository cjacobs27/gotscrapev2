import requests
from django.test import TestCase
from .update import Update
# from bs4 import BeautifulSoup


class UpdateMethodTests(TestCase):
    def test_see_if_main_page_content_returned_successfully(self):
        request = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
        self.assertEqual(request.content, Update().get_name_page_content())

    #generate_links()

    def test_if_name_list_is_a_list(self):
        test_link_list = Update().generate_links()
        self.assertEqual(type(test_link_list[0]), list)

    def test_if_link_list_is_a_list(self):
        test_link_list = Update().generate_links()
        self.assertEqual(type(test_link_list[1]), list)

    def test_if_name_list_populated(self):
        # checks if there's stuff in the list as it could be empty
        test_link_list = Update().generate_links()
        self.assertTrue(len(test_link_list[0]) >= 3)

    def test_if_link_list_populated(self):
        # checks if there's stuff in the list as it could be empty
        test_link_list = Update().generate_links()
        self.assertTrue(len(test_link_list[1]) >= 3)

    def test_if_link_list_and_name_list_same_length(self):
        # if not same length then indicates error with appending either list
        test_link_list = Update().generate_links()
        self.assertEqual(len(test_link_list[0]), len(test_link_list[1]))
