from django.db import models

# Create your models here.

class JobPositionItem(models.Model):
    Name = models.TextField(unique=True)

    def __str__(self):
        return self.Name

class JobCitySetItem(models.Model):
    City = models.TextField(unique=True)

    def __str__(self):
        return self.City

class JobTypeFind(models.Model):
    Jobtype = models.TextField(unique=True)

    def __str__(self):
        return self.Jobtype

class MaxResultsPerCity(models.Model):
    MaxNumber = models.IntegerField()

    def __str__(self):
        return str(self.MaxNumber)

class Host(models.Model):
    Host = models.TextField(unique=True)

    def __str__(self):
        return self.Host

class JobTransparencyLinks(models.Model):
    TechTrans = models.TextField(unique=True)
    TechTransCheck = models.TextField(unique=True)
    def __str__(self):
        return self.TechTrans
