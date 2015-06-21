from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Gmina(models.Model):
    nazwa = models.CharField(max_length=200)

    def __unicode__(self):  # __unicode__ on Python 2
        return self.nazwa


class Obwod(models.Model):
    gmina = models.ForeignKey(Gmina)
    adres = models.CharField(max_length=200)
    uprawnionych = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    ileKart = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    wersja = models.PositiveIntegerField(default=0)

    def toDict(self):
        return {
            'id': self.id,
            'upr': self.uprawnionych,
            'ile': self.ileKart,
            'wer': self.wersja,
            'adres': self.adres
        }


    def __unicode__(self):  # __unicode__ on Python 2
        return self.adres + " " + self.id + " " + self.uprawnionych + " " +self.ileKart + " " + self.wersja