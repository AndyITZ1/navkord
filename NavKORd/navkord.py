import discord
import os
import asyncio
import navdata
import random
import websearch
from dotenv import load_dotenv

load_dotenv('know.env')
TOKEN = os.getenv('TOKEN')

#changeable prefix for bot
prefix = "!"

# class holding the bot and its functions
class MyClient(discord.Client):

    #at runtime will show the bot is online
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    #at runtime if a message is sent in the Discord chat, that message is passed in.
    async def on_message(self, message):
        #user who sent the message
        user = str(message.author)

        #message sent
        content = str(message.content)

        #channel the message was sent in
        channel = str(message.channel.name)
        
        #returns active message sent in chat to the command-line terminal (not in the Discord chat)
        print('Message from {0.author}: {0.content}'.format(message))

        #Avoids bot reacting/responding to itself
        if user == self.user:
            return

        #Do all Bot functions here, so that the bot only reacts to messages sent in this <channel>: commands
        if channel == 'commands':
            if content.startswith(prefix + "random"):
                response = f'This is your random number: {random.randint(0, 9)}'
                await message.channel.send(response)
                return
            elif content.startswith(prefix + "ktoe"):
                search_word = content.split(' ')[1] #Ex: !ktoe 하다  --> retrieves the korean word
                # for the function make sure it returns the parse format and stores it into the 'results' variable
                # results = functionHere(search_word) Uncomment this line when you replace functionHere()
            elif content.startswith(prefix + "etok"):
                #This command is different from the last because with English words you get numbered lines, with Korean words
                # it might be just one line/list of words that aren't numbered so make sure you have a different parsing function
                search_word = content.split(' ')[1] #Ex: !etok blue --> retrieves "blue"
                #results = functionHere(search_word) Uncomment this line when you replace functionHere()

                # for testing your functions I recommend do it the way you did it by printing in websearch.py, as I still have to format
                # it to see it on discord and obviously you can't test here because you don't have the "know.env"
                


client = MyClient()
client.run(TOKEN)