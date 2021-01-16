from django.db import models

# Create your models here.
class MaxAge(models.Model):
    Age = models.IntegerField()

    def __str__(self):
        return str(self.Age)

class JobPositionItem(models.Model):
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name

class JobCitySetItem(models.Model):
    City = models.CharField(max_length=255)

    def __str__(self):
        return self.City

class JobTypeFind(models.Model):
    Jobtype = models.CharField(max_length=255)

    def __str__(self):
        return self.Jobtype

class MaxResultsPerCity(models.Model):
    MaxNumber = models.IntegerField()

    def __str__(self):
        return str(self.MaxNumber)

class Host(models.Model):
    Host = models.TextField()

    def __str__(self):
        return self.Host

class JobTransparencyLinks(models.Model):
    TechTrans = models.CharField(max_length=500)
    TechTransCheck = models.CharField(max_length=500)
    def __str__(self):
        return self.TechTrans