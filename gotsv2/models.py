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

    # get gender split
    def get_gender_split(self):
        number_of_women = Character.objects.filter(gender_id='2').count()
        number_of_men = Character.objects.filter(gender_id = '1').count()
        total_people = number_of_men + number_of_women
        female_percentage = round((number_of_women / total_people)*100, 2)
        male_percentage = round((number_of_men / total_people)*100, 2)
        print(female_percentage,male_percentage)
        percentages = [female_percentage, male_percentage]
        return percentages


