from django.db import models


class Bot(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40, help_text='oauth:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

    def __str__(self):
        return self.username


class Room(models.Model):
    name = models.CharField(max_length=40, help_text='streamer\'s username, usually.')

    def __str__(self):
        return self.name


class Command(models.Model):
    bot = models.ForeignKey(Bot)
    room = models.ForeignKey(Room)
    pattern = models.CharField(max_length=400, help_text='^!command$')
    response = models.CharField(max_length=400)

    def __str__(self):
        return self.pattern
