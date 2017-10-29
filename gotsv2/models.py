from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=500)
    page = models.TextField()
    infobox = models.TextField()
    created_at = models.DateTimeField('created')
    updated_at = models.DateTimeField('last updated')

    def __str__(self):
        return self.name

    #need to create another method here which causes Character model to update

    # def databaseUpdate(self, Update):
    #     for item in Update.namelist:
    #         print(item)




class Gender(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.character
