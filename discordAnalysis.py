import json
from pprint import pprint

class User():

    id = 0
    name = ''
    messages = []

    def __init__(self, name, id):
        self.id = id
        self.name = name

    def add_message(self, message):
        self.messages.append(message)

    def print_all(self):
        for message in self.messages:
            print(message)

class DiscordData():

    users = []
    channels = []

    def __init__(self, file):

        logs = json.load(open(file))

        # populate user list
        for index, id in enumerate(logs['meta']['userindex']): 
            name = logs['meta']['users'][id]['name']
            self.users.insert(index,User(name, id))

        # add channel ids
        self.channels = list(logs['meta']['channels'])

        # add messages to users
        for channel in self.channels:
            for message_id in logs['data'][channel]:
                user = logs['data'][channel][message_id]['u']
                message = logs['data'][channel][message_id]['m']
                self.users[user].add_message(message)

    def print_all(self):
        for user in self.users:
            print(user.name)
            user.print_all()



data = DiscordData('rst.txt')
data.print_all()
