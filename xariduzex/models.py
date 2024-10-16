from django.db import models

from etenderuzex.models import type_choices, currency_choices, Category


# Create your models here.

class XariduzexCheck(models.Model):
    tender_id = models.IntegerField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tender_id} - {self.name}"

    class Meta:
        verbose_name_plural = 'Xariduzex Checks'


