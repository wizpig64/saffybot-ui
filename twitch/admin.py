from django.contrib import admin

from .models import Bot, Room, Command

admin.site.register(Bot)
admin.site.register(Room)
admin.site.register(Command)
