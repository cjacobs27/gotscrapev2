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

    # checking other 2 lists
    # commented this out because it takes too long
    # def test_if_check_list_and_info_list_same_length(self):
    #     test_link_list = Update().generate_links()
    #     test_name_list = test_link_list[0]
    #     test_name_list_shorter = test_name_list[:10]
    #     check_list = []
    #     info_list = []
    #     a = 0
    #     for item in test_link_list[1]:
    #         request = requests.get(item)
    #         z = request.content
    #         soup2 = BeautifulSoup(z, "html.parser")
    #         if "may refer to" in soup2.text:
    #             Update().try_adding_character_suffix_to_url(item)
    #         else:
    #             try:
    #                 redirected = soup2.find("a", {"class:", "mw-redirect"}).text
    #                 if redirected == test_name_list_shorter[a]:
    #                     check_list.append(0)
    #                     info_list.append("")
    #                 else:
    #                     Update().get_infobox(item)
    #             except:
    #                 check_list.append(0)
    #                 info_list.append("")
    #         a = a + 1
    #     print(check_list, info_list)
    #     self.assertEqual(len(check_list), len(info_list))

