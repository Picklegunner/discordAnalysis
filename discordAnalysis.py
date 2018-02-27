import json
import re
import math
from pprint import pprint

class User():

    def __init__(self, name, id):
        self.id = id
        self.name = name
        self.messages = []


    def add_message(self, message):
        self.messages.append(message)

    def total_messages(self):
        return len(self.messages)

    def print_all(self):
        for message in self.messages:
            print(message)

    def sum_expression(self, regex):
        sum = 0
        unique_sum = 0
        quotes = []
        for message in self.messages:
            length = len(regex.findall(message))
            sum += length
            if length != 0:
                unique_sum += 1
                quotes.append(message)
        return (sum, unique_sum, quotes)

    def __lt__(self, other):
        return self.total_messages() < other.total_messages()
    
    def __eq__(self, other):
        return self.total_messages() == other.total_messages()
    



class DiscordData():

    users = []
    channels = []

    #server stats
    #total

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

        self.max_name_length = 1
        self.max_value = 1
        for user in self.users:
            self.max_name_length = max(self.max_name_length, len(user.name))
            total = user.total_messages()
            if total > 1:
                self.max_value = max(self.max_value, math.ceil(math.log(total,10)))

        self.users.sort(reverse=True)

    def print_all(self):
        for user in self.users:
            print('user: ' + user.name)
            user.print_all()

    def match_report(self, regex, quoted):
        
        results = {}
        total_matches = 0

        for user in self.users:
            result =  user.sum_expression(regex)
            results[user.name] = (user.total_messages(), result[0], result[1], result[2])
            total_matches += result[0]

        print('{} matches for \'{}\' '.format(total_matches, regex.pattern))

        for user in self.users:   
            print('{:{length}}| {:>{max_val}} matches in {:<{max_val}} {percent_user:6.2f}% user messages, {percent_server:6.2f}% of total matches'.format(
                user.name,
                results[user.name][1],
                results[user.name][0],
                percent_user=(100*results[user.name][2]/results[user.name][0]) if results[user.name][0] != 0 else 0.0,
                length = self.max_name_length + 1,
                max_val = self.max_value + 1,
                percent_server=(100*results[user.name][1]/total_matches) if total_matches != 0 else 0.0))
            if quoted:
                for quote in results[user.name][3]:
                    print('>>> ' + quote)


    def message_length(self):

        results = {}
        regex = re.compile(r'.')

        for user in self.users:
            result =  user.sum_expression(regex)
            results[user.name] = (user.total_messages(), result[0], result[1], result[2])

        for user in self.users:   
            print('{:{length}}| used {:>{max_val}} chars in {:<{max_val}} messages, average length: {:<{max_val}.2f}'.format(
                user.name,
                results[user.name][1],
                results[user.name][0],
                results[user.name][1]/results[user.name][0] if results[user.name][0] != 0 else 0.0,
                length = self.max_name_length + 1,
                max_val = self.max_value + 1))

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
data.match_report(pattern, (quoted == 'Y' or quoted == 'y'))
#data.message_length()