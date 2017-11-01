import requests
from django.test import TestCase
from .update import Update
# from django.utils import timezone
# import pandas
# import re
# from bs4 import BeautifulSoup
# from .models import Character

class UpdateMethodTests(TestCase):
    # does initial ASOAF test page request work
    def test_see_if_initial_request_returned(self):
        r = Update.requestNamePage()
#this doesn't do anything yet but at least it runs?
#does initial ASOAF page scrape work

#test for each stage of update.py method functionality
