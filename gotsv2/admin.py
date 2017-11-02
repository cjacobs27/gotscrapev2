# Register your models here.
from django.contrib import admin

from .models import Character, Gender

admin.site.register(Character)
admin.site.register(Gender)
