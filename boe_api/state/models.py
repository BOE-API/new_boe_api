# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects
    """
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None



# Create your models here.
class Partido(models.Model):

    nombre = models.CharField(max_length=200)

    class Meta:
        app_label = "state"

    def __unicode__(self):
        return self.nombre


class Legislatura(models.Model):
    inicio = models.DateField()
    final = models.DateField(null=True, blank=True)
    partido = models.ForeignKey("Partido")
    presidente = models.CharField(max_length=300)
    nombre_legislatura = models.CharField(max_length=600)


    objects = GetOrNoneManager()
    class Meta:
        ordering = ['inicio']
        app_label = "state"

    def __unicode__(self):
        return self.nombre_legislatura


