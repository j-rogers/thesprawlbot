import discord  # version 0.16.12
import random
import pickle
import argparse
import xml.etree.ElementTree as et
from pbabot.games import *
from collections import namedtuple

# API Token
TOKEN = open("token.txt", 'r').read()
DATA_FILE = "../data/data.pickle"


class Clock:
    def __init__(self, name, time='1200'):
        self.name = name
        self.time = time

    def increase(self):
        if self.time == "1200":
            self.time = "1500"
        elif self.time == "1500":
            self.time = "1800"
        elif self.time == "1800":
            self.time = "2100"
        elif self.time == "2100":
            self.time = "2200"
        elif self.time == "2200":
            self.time = "2300"
        elif self.time == "2300":
            self.time = "0000"
        elif self.time == "0000":
            return '```Clock is already at midnight.```'

    def decrease(self):
        if self.time == "0000":
            self.time = "2300"
        elif self.time == "2300":
            self.time = "2200"
        elif self.time == "2200":
            self.time = "2100"
        elif self.time == "2100":
            self.time = "1800"
        elif self.time == "1800":
            self.time = "1500"
        elif self.time == "1500":
            self.time = "1200"
        elif self.time == "1200":
            return '```Clock is already at 1200.```'


class Contact:
    def __init__(self, name, description):
        self.name = name
        self.description = description


# requires python 3.6.8

# Updates and refreshes data file



# Functions











def f(message):
    msg = "```"

    tree = et.parse('data/personal')
    rip = tree.getroot().find('rip')

    ripMsg = message.split()
    if len(ripMsg) > 1: #specific message
        player = rip.find(ripMsg[1])
        print (player)
        if player:
            for character in list(player):
                msg += f"{character.get('name')}: {character.get('cause')}\n\n"
                
           
    else: #short list
        for player in list(rip):
            msg += f'{player.tag}: '
            for character in list(player):
                msg += f"{character.get('name')}, "
            msg += '\n'

    msg += "```"
    msg = msg.strip()
    return msg




def remember(message):
    # Generates random number to get remember message from  events that have happened.
    min = 1
    max = 280
    member = random.randint(min, max)
    notRandom = message.split()  # puts message into a string array seperated by " "

    if len(notRandom) > 1:  # If more values other than .remember
        number = int(notRandom[1])  # converts stringArray  (['.remember' 'num']) to int
        if number >= min and number <= max:  # Ensures it will exist within the range of .remember
            member = number  # sets member to the number.

    tree = et.parse('data/personal')
    remember = tree.find('remember')

    memories = {}
    for memory in list(remember):
        memories[memory.get('index')] = memory.text

    msg = f"```{memories[str(member)]}```"

    return msg




def chess(message):
    msg = "**```THE\t  TECHSORCIST\n\tIS    THE\nCHESS\t\tMASTER!```**"
    return msg





def answerphone(message):
    min = 1
    max = 1
    member = random.randint(min, max)
    notRandom = message.split()  # puts message into a string array seperated by " "

    if len(notRandom) > 1:  # If more values other than .remember
        number = int(notRandom[1])  # converts stringArray  (['.remember' 'num']) to int
        if number >= min and number <= max:  # Ensures it will exist within the range of .remember
            member = number  # sets member to the number.

    switch = {
        1: """```css
Welcome to the Wii Fit helpline how can I help you?```""",
    }

    return switch[member]














def addcontact(message):
    # Get the contact name and description
    tokens = message.split()
    description = ""
    for i in range(2, len(tokens)):
        description += tokens[i] + " "
    contact = (tokens[1], description)

    # Checks if clock has already been added
    for c in contacts:
        # Case insensitive
        name = c[0].lower()
        inName = tokens[1].lower()

        if name == inName:
            return "```Contact already exists.```"

    # Append to contacts list
    contacts.append(contact)

    # Update and refresh file
    updateAndRefreshData("contacts", contacts)
    print("Contact added to file: {" + tokens[1] + ", " + description + "}")

    # Form message and send
    return "```Contact added: " + tokens[1] + ".```"


def deletecontact(message):
    # Get the clock name
    tokens = message.split()
    name = tokens[1]

    # Find the clock to be deleted
    for c in contacts:
        # Case insensitive
        cName = c[0].lower()
        inName = name.lower()

        if cName == inName:
            contacts.remove(c)

    # Update and refresh file
    updateAndRefreshData("contacts", contacts)
    print("Contact deleted from file: " + tokens[1])

    # Form message and send
    return "```Deleted contact " + name + ".```"


def refresh(message):
    msg = "```"

    try:
        data = pickle.loads(open(filename, "rb").read())
        clocks = data["clocks"]
        contacts = data["contacts"]
        msg += "Data has been refreshed."
        print("Data extracted")
    except EOFError:
        print("No data in file.")
    except FileNotFoundError:
        print("No data file found.")

    msg += "```"

    return msg


def log(message):
    # Get log message from message
    tokens = message.split(".log ")
    log = tokens[1]

    # Write to the file
    file = open("log.txt", "a")
    file.write(log + "\n")
    file.close()
    print("Log saved: \"" + log + "\"")

    # Form and send message
    return "```Log saved.```"



# Discord client functions
@client.event
async def on_message(message):
    msg = ""

    # Prevents bot replying to itself
    if message.author == client.user:
        return

    # Prevents bot responding to regular messages
    if not message.content.startswith("."):
        return

    # determine which game is being played
    if game == 'sprawl':
        msg = sprawl.handle(message)
    elif game == 'apoc':
        msg = apoc.handle(message)

    messageString = message.content
    messageString = messageString.lower()

    switch = {
        # Listing commands
        '.help': help,
        '.links': links,
        '.clocks': showclocks,
        '.contacts': showcontacts,
        '.rememberlist': rememberlist,
        '.answerphone': answerphone,
        # Functional commands
        '.roll': roll,
        '.dice': roll,
        '.addclock': addclock,
        '.deleteclock': deleteclock,
        '.increaseclock': increaseclock,
        '.decreaseclock': decreaseclock,
        '.addcontact': addcontact,
        '.deletecontact': deletecontact,
        # Miscellaneous commands
        '.rip': f,
        '.f': f,
        '.remember': remember,
        # Dev commands
        '.refresh': refresh,
        '.log': log,
        '.chess':chess,
    }
    check = False
    if msg != "":
        check = True
    # print (msg)
    if messageString in switch:
        msg = switch[messageString](messageString)
        check = True
    elif check == False:
        for case in switch:
            if case in messageString:
                msg = switch[case](messageString)

    if not msg: msg = invalid(messageString)

    # Sends the map
    if messageString == ".map":
        await client.send_file(message.channel, "images/map.jpg")

    elif messageString == ".fuckmendle":
        await client.send_file(message.channel, "images/mendle.png")
    elif messageString == ".fridge":
        await client.send_file(message.channel, "images/FRIDGE.jpg")
    elif messageString == ".clones":
        await client.send_file(message.channel, "images/clones.png")

    elif messageString != ".map" and messageString != ".fuckmendle" and messageString != ".factorymap":
        await client.send_message(message.channel, msg.format(message))
    else:
        pass


class PBABot(discord.Client):
    def __init__(self):
        super().__init__()

        # Extract data from file

        self.clocks = []
        self.contacts = []
        try:
            data = pickle.loads(open(DATA_FILE, "rb").read())
            self.clocks = data["clocks"]
            self.contacts = data["contacts"]
            print("Data extracted")
        except EOFError:
            print("No data in file.")
        except FileNotFoundError:
            print("No data file found.")

    async def on_message(self, message):
        response = ''
        images = None

        # Prevents bot replying to itself
        if message.author == self.user:
            return

        # Prevents bot responding to regular messages
        if not message.content.startswith("."):
            return

        # Parse message
        content = message.content
        content = message.lower().split(' ', 1)
        command = content[0]
        args = content[1]

        switch = {
            # Listing commands
            '.help': self._help,
            '.links': self._links,
            '.clocks': self._clocks,
            '.contacts': self._contacts,
            '.rememberlist': self._rememberlist,
            # Functional commands
            '.roll': self._roll,
            '.dice': self._roll,
            '.addclock': self._addclock,
            '.deleteclock': self._deleteclock,
            '.increaseclock': self._increaseclock,
            '.decreaseclock': self._decreaseclock,
            '.addcontact': addcontact,
            '.deletecontact': deletecontact,
            # Miscellaneous commands
            '.rip': f,
            '.f': f,
            '.remember': remember,
            '.chess': chess,
            '.answerphone': answerphone,
            # Dev commands
            '.refresh': refresh,
            '.log': log,

        }

        response = switch.get(command, None)(args)

        if not response:
            response = '```Invalid command. Type ".help" for a list of commands.```'

        await message.channel.send(response, files=images)

    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    def _help(self, message):
        return """```Use \".command\" when using this bot.\n
    .help: Displays this help message.
    .roll: Rolls 2d6 dice.
    .moves: Displays a list of basic moves.
    .playbooks: Displays a list of playbooks.
    .matrix: Displays a list of matrix-specific moves. [SPRAWL ONLY]
    .custom: Displays a list of custom moves.
    .clocks: Displays the current list of clocks.
    .weapons: Displays a list of weapons and their profiles.
    .addclock <clock name>: Adds a clock with a value of 1500.
    .increaseclock <clock name>: Increases a clock by one segment.
    .decreaseclock <clock name>: Decreases a clock by one segment.
    .deleteclock <clock name>: Deletes the specified clock.
    .contacts: Displays the current list of contacts.
    .addcontact <contact name> <description>: Adds a new contact.
    .deletecontact <contact name>: Deletes a contact.
    .drugs: Displays a list of drugs
    .map: Displays a current map
    .ripsprawl1: Detailed deaths from the Sprawl1
    .ripsprawl2: Detailed deaths from Sprawl2 
    .ripapoc: Detailed deaths from Apoc World
    .rip: List all dead characters.
    .rememberlist: Displays rough numbers for specific moments. 
    .remember: Displays a message of a memorable moment.
    .refresh: Reloads the clock and contact data.
    .log <message>: Saves a message to the log file.
    .links: Displays a link to all the PBA games. 
    ```"""

    def _links(self, message):
        msg = """
        **Apocalpyse World:** https://www.dropbox.com/sh/fmsh9kyaiplqhom/AACw1iLMQ7f53Q40FUnMjlz4a?dl=0
        **The Sprawl:** https://www.dropbox.com/sh/9fr35ivzbvfh06p/AACarsYBpNXxBpEUk_-fz_PXa?dl=0
        **Tremulas:** https://www.dropbox.com/sh/tbhk0w0zgihrf2h/AACtvyv9l5ruLBE6UG3XeGfba?dl=0
        **Dungeon World:** https://www.dropbox.com/sh/p61lutt9m6dfpa3/AACTvHhbJa7K1RIHFYVvJqIza?dl=0
        """
        msg = msg.replace("\t", "")
        return msg

    def _clocks(self, message):
        msg = '```'

        switch = {
            '1200': '□□□□ □□□□ □□□□ □ □ □',
            '1500': '■■■■ □□□□ □□□□ □ □ □',
            '1800': '■■■■ ■■■■ □□□□ □ □ □',
            '2100': '■■■■ ■■■■ ■■■■ □ □ □',
            '2200': '■■■■ ■■■■ ■■■■ ■ □ □',
            '2300': '■■■■ ■■■■ ■■■■ ■ ■ □',
            '0000': '■■■■ ■■■■ ■■■■ ■ ■ ■'
        }

        for clock in self.clocks:
            msg += f'{clock.name}: {switch[clock.value]}\n'

        if not self.clocks:
            msg += 'No clocks have been added.'

        msg += '```'

        return msg

    def _contacts(self, message):
        msg = "```"
        for contact in self.contacts:
            name = contact[0]
            desc = contact[1]
            msg += name + ": " + desc + "\n"

        if msg == "```":
            msg += "No contacts have been added."

        msg += "```"

        return msg

    def _rememberlist(self, message):
        msg = """```
        1-9: Christoff focused
        10-13: Laramy focused
        14-19: Seraph focused
        20: I missed a number..
        21-23:  Syntax Terror focused
        24-27: H4KKK3R focused
        28-32: Noor focused
        33-60: Reat of Sprawl campaign 1 (in order things happened after I stopped grouping by character.)
        61-73: Sprawl campaign 2, while Jayden(swarf) was still playing
        74-106: Sprawl 2 while Mercer was still alive.
        107-114: The last of Sprawl 2.
        115-134: First time playing Apoc world, what a mess that was, also lots of pvp.
        135-178: The last of Apoc world campaign 1, lots of weird stuff and overtrowing.
        179-206: Back to the Sprawl, oh how we missed the Sprawls writing. A one shot spanned over a couple of sessions.
        207-219: Apoc world, Tat and Cowboy.
        220-244: Jayden comes back and Tat dies.
        245: The sprawl and pissing on machines... 
        ```"""
        msg = msg.replace("\t", "")
        return msg

    def _roll(self, message):
        # Generate the roll
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        roll = dice1 + dice2
        msg = ""

        # Unique response based on roll
        if roll == 1:
            msg = "```Throwbacks to when Martin's bot could roll a 1 from 2d6. Good times, not for you though, you rolled a 1.```"
        elif roll == 2:
            msg = "```I hope you have a lot of health cause this is gonna hurt. You rolled a 2.```"
        elif roll == 3:
            msg = "```The Thing is going to have fun with this, you rolled a 3.```"
        elif roll == 4:
            msg = "```You rolled the length of your penis, 4 inches.```"
        elif roll == 5:
            msg = "```Maybe you should have taken those drugs, you rolled a 5.```"
        elif roll == 6:
            msg = "```The RNG gods are displeased with you. You rolled a 6.```"
        elif roll == 7:
            msg = "```You know what, it could be worse. You rolled a 7.```"
        elif roll == 8:
            msg = "```Someones going to be sleeping with the fishes, is it going to be you or him with a roll of 8.```"
        elif roll == 9:
            msg = "```Almost hit that sweet spot. You rolled a 9.```"
        elif roll == 10:
            msg = "```Now we're talking, you rolled a 10.```"
        elif roll == 11:
            msg = "```You could fuck up someones day with this. You rolled an 11.```"
        elif roll == 12:
            msg = "```Okay, now THIS is epic. You rolled a 12.```"

        return msg

    def _addclock(self, name):
        # Checks if clock has already been added
        clock = self._getclock(name)

        if clock:
            return f'```Clock {name} already exists.```'
        else:
            # Append to clocks list
            self.clocks.append(Clock(name))

        # Update and refresh file
        self._savedata()
        print(f'Clock added to file: {name} at 1200')

        # Form message and send
        return f'```Clock added to file: {name} at 1200```'

    def _deleteclock(self, name):
        # Find the clock to be deleted
        clock = self._getclock(name)

        if not clock:
            return f'```Clock {name} not found.'
        else:
            self.clocks.remove(clock)

        # Update and refresh file
        self._savedata()
        print('Clock deleted from file: {name}')

        # Form message and send
        return f'```Deleted clock {name}.```'

    def _increaseclock(self, name):
        # Find the clock to be increased
        clock = self._getclock(name)

        # Check if the clock was found
        if not clock:
            return f'```Clock "{name}" not found.```'
        else:
            clock.increase()

        # Update and refresh file
        self._savedata()
        print(f'Clock update reflected in file (INCREASE): ({clock.name} {clock.value})')

        # Form message and send
        return f'```{clock.name} clock increased to {clock.value}.```'

    def _decreaseclock(self, name):
        clock = self._getclock(name)


        if not clock:
            return f'```Clock "{name}" not found.'

        clock.decrease()

        self._savedata()
        return f'```{clock.name} clock decreased to {clock.value}```'




    def _getclock(self, name):
        for clock in self.clocks:
            if name.lower() == clock.name.lower():
                return clock

        return None

    def _savedata(self):
        data = {'clocks': self.clocks, 'contacts': self.contacts}
        file = open(DATA_FILE, "wb")
        file.write(pickle.dumps(data))
        file.close()

        #data = pickle.loads(open(filename, "rb").read())
        #clocks = data["clocks"]
        #contacts = data["contacts"]
        #print("File reloaded")



def main():
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--game', type=str, required=True, choices=['sprawl', 'apoc'])
    args = parser.parse_args()
    game = vars(args)['game']

    client = PBABot()
    client.run(TOKEN)


if __name__ == '__main__':
    main()