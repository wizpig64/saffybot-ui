import re
from datetime import date, datetime

from django.contrib.postgres.fields import JSONField
from django.db import models


class Bot(models.Model):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40, help_text='oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    def __str__(self):
        return self.username


class Room(models.Model):
    name = models.CharField(max_length=40, help_text='streamer\'s username, usually.')

    def __str__(self):
        return self.name


class CommandQuerySet(models.QuerySet):
    def from_message(self, message, **kwargs):
        # to respond with a random choice, just make multiple commands, and we'll randomly pick one.
        # todo: this is probably really slow, better ways to go about it.
        for command in self.order_by('?'):
            if re.match(command.pattern, message, flags=re.IGNORECASE):
                return command.render(**kwargs)


class Command(models.Model):
    bot = models.ForeignKey(Bot)
    room = models.ForeignKey(Room)
    pattern = models.CharField(max_length=400, help_text='^!command$')
    response = models.CharField(max_length=1024)
    extra = JSONField(blank=True, null=True)

    objects = CommandQuerySet.as_manager()

    def __str__(self):
        return self.pattern

    def render(self, **kwargs):
        if self.extra:
            kwargs = {**self.extra, **kwargs}
        if 'birthday' in kwargs:
            t = date.today()
            b = datetime.strptime(kwargs['birthday'], '%Y-%m-%d').date()
            kwargs['age'] = t.year - b.year - ((t.month, t.day) < (b.month, b.day))
        return self.response.format(**kwargs)
