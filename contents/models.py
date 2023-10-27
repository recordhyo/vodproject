from django.db import models


# class Vod(models.Model) :
#     id = models.AutoField(primary_key=True)
#     apiid = models.IntegerField(max_length=20)
#     bigcategory = models.CharField(max_length=10)
#     smallcategory = models.CharField(max_length=10)
#     category = models.CharField(max_length=10, null=False)
#     name = models.CharField(max_length=50, null=False)
#     actor = models.CharField(max_length=50, null=True)
#     director = models.CharField(max_length=50, null=True)
#     description = models.TextField(max_length=200, null=True)
#     imgpath = models.CharField(max_length=50, null=True)


class vodtest(models.Model):
    id = models.AutoField(primary_key=True)
    apiid = models.IntegerField(max_length=20, null=False)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(max_length=200, null=True)
    imgpath = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=10, null=False)
    actor = models.CharField(max_length=50, null=True)
    director = models.CharField(max_length=50, null=True)
