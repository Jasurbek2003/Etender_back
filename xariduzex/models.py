from django.db import models

from etenderuzex.models import type_choices, currency_choices, Category


# Create your models here.

class XariduzexCheck(models.Model):
    tender_id = models.IntegerField(unique=True)
    category = models.TextField()

    def __str__(self):
        return f"{self.tender_id}"

    class Meta:
        verbose_name_plural = 'Xariduzex Checks'


