import requests
from django.test import TestCase
from .update import Update


class UpdateMethodTests(TestCase):
    def test_see_if_mainpage_content_returned_successfully(self):
        request = requests.get("https://en.wikipedia.org/wiki/List_of_A_Song_of_Ice_and_Fire_characters")
        self.assertEqual(request.content, Update().get_name_page_content())
