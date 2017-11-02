from django.db import models


class Gender(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    page = models.TextField()
    infobox = models.TextField()
    created_at = models.DateTimeField('created')
    updated_at = models.DateTimeField('last updated')
    gender = models.ForeignKey(Gender, default=1)

    def __str__(self):
        return self.name


