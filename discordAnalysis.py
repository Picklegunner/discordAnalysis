import json
import re
from pprint import pprint

class User():


    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def print_all(self):
        for message in self.messages:
            print(message)

    def sum_expression_quoted(self, regex):
        sum = 0
        for message in self.messages:
            length = len(regex.findall(message))
            sum += length
            if(length != 0):
                print(message)
        return sum

    def sum_expression(self, regex):
        sum = 0
        for message in self.messages:
            sum += len(regex.findall(message))
        return sum


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
            if channel in logs['data']:
                for message_id in logs['data'][channel]:
                    user = logs['data'][channel][message_id]['u']
                    message = logs['data'][channel][message_id]['m']
                    if message != '':
                        self.users[user].add_message('-->> ' + message)

    def print_all(self):
        for user in self.users:
            print('user: ' + user.name)
            user.print_all()

    def match_report(self, regex):
        print('matches for {}'.format(regex.pattern))
        for user in self.users:
            # print(user.messages)
            print('user: {} matches: {}'.format(user.name, user.sum_expression(regex)))

    def match_report_quoted(self, regex):
        print('matches for {}'.format(regex.pattern))
        for user in self.users:
            # print(user.messages)
            print('user: {} matches: {}'.format(user.name, user.sum_expression_quoted(regex)))

file = input('Enter file name (dht.txt by default): ')
if(file == ''):
    file = 'dht.txt'
print('Using file ' + file)

regex = input('Enter regular expression (Not escaped): ')
if(regex == ''):
    regex = r'regex'
print('Using regex ' + regex)

pattern = re.compile(regex, re.IGNORECASE)
data = DiscordData('dht.txt')

quoted = input('Quote lines? (Y/n): ')
if(quoted == 'Y' or quoted == 'y'):
    data.match_report_quoted(pattern)
else:
    data.match_report(pattern)
