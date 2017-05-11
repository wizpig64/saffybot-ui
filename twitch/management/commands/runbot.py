import socket

from django.core.management.base import BaseCommand, CommandError

from twitch.models import Bot, Room, Command as BotCommand


class Command(BaseCommand):
    help = 'Runs a specified twitch bot in the specified room'

    def add_arguments(self, parser):
        parser.add_argument('bot')
        parser.add_argument('room')

    def handle(self, *args, **options):
        bot_name = options['bot']
        try:
            self.bot = Bot.objects.get(username=bot_name)
        except Bot.DoesNotExist:
            raise CommandError(f'Bot "{bot_name}" does not exist')

        room_name = options['room']
        try:
            self.room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            raise CommandError(f'Room "{room_name}" does not exist')

        self.commands = BotCommand.objects.filter(bot=self.bot, room=self.room)
        if not self.commands.count():
            raise CommandError(f'There are no commands set up for "{bot_name}" at chat room "{room_name}".')

        self.stdout.write(self.style.SUCCESS(f'Starting bot "{bot_name}" at chat room "{room_name}". Kill with ^C.'))
        self.start()

    def start(self):

        # Set all the variables necessary to connect to Twitch IRC
        read_buffer = ''
        announcements_done = False

        # Connecting to Twitch IRC by passing credentials and joining a certain channel
        s = socket.socket()
        s.connect(('irc.twitch.tv', 6667))
        s.send(f'PASS {self.bot.password}\r\n'.encode())
        s.send(f'NICK {self.bot.username}\r\n'.encode())
        s.send(f'JOIN #{self.room.name} \r\n'.encode())

        while True:
            # todo: replace all this messy string manipulation with regex
            read_buffer = read_buffer + s.recv(1024).decode("utf-8")
            temp = read_buffer.split('\n')
            read_buffer = temp.pop()

            for line in temp:
                # Checks whether the message is PING because its a method of Twitch to check if you're afk
                if line.split()[0] == 'PING':
                    s.send(f'PONG {line[1]}\r\n'.encode())
                    continue

                # Splits the given string so we can work with it better
                parts = line.split(':')

                if 'QUIT' not in parts[1] and 'JOIN' not in parts[1] and 'PART' not in parts[1]:
                    try:
                        # Sets the message variable to the actual message sent
                        message = parts[2][:len(parts[2]) - 1]
                    except:
                        message = ''

                    # Sets the username variable to the actual username
                    username_split = parts[1].split('!')
                    username = username_split[0]

                    # Only works after twitch is done announcing stuff
                    if announcements_done:
                        self.stdout.write(username + ": " + message)

                        response = self.commands.from_message(message, username=username)
                        if response:
                            s.send(f'PRIVMSG #{self.room.name} :{response}\r\n'.encode())
                            self.stdout.write(self.style.SUCCESS(f'{self.bot.username}: {response}'))

                for l in parts:
                    if 'End of /NAMES list' in l:
                        announcements_done = True
