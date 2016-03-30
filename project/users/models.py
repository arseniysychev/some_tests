from datetime import date

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    born = models.DateField()

    def __str__(self):
        return '{name} {age}'.format(
            name=self.name,
            age=self.get_age()
        )

    def get_age(self):
        today = date.today()
        return today.year - self.born.year + (
            (today.month, today.day) < (self.born.month, self.born.day)
        )
