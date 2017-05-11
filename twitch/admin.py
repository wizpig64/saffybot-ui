from django.contrib import admin

from .models import Bot, Room, Command

admin.site.register(Bot)
admin.site.register(Room)

class CommandAdmin(admin.ModelAdmin):
    list_display = [
        'pattern',
        'bot',
        'room',
        'response',
    ]

admin.site.register(Command, CommandAdmin)
