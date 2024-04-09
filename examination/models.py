from django.db import models

from professional.models import Professional


class Examination(models.Model):
    class Meta:
        db_table = 'examinations'

    date = models.DateTimeField()
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)

