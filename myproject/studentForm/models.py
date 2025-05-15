from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    roll = models.CharField(max_length=20)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return self.name
