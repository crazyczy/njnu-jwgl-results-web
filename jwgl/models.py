from django.db import models


class Account(models.Model):
    idnum = models.CharField(max_length=20, primary_key=True)
    pwd = models.CharField(max_length=20)

    def __str__(self):
        return self.idnum

class Stunum(models.Model):
    idnum = models.CharField(max_length=20, primary_key=True)
    stunum = models.CharField(max_length=20)

    def __str__(self):
        return self.idnum
