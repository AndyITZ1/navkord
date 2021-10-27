import discord
import os
import asyncio
import navdata
import random
import websearch
from dotenv import load_dotenv
from websearch import etok
from navdata import find_db
from navdata import check_db


load_dotenv('know.env')
TOKEN = os.getenv('TOKEN')

#changeable prefix for bot
prefix = "!"

def list_to_str(list):
    a = ""
    if list:
        for word in list:
            a += word + "\n"
    else:
        a = "None"
    return a

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
                search_word = content.split(' ')[1].lower() #Ex: !etok blue --> retrieves "blue"
                #results = functionHere(search_word) Uncomment this line when you replace functionHere()
                if check_db(search_word):
                    print("From DB")
                    #print(find_db(search_word))
                    results = find_db(search_word)
                    embed=discord.Embed(title=results["Word"], color=0x00e1ff)
                    embed.set_author(name="Naver Eng-Kor Dictionary", icon_url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
                    embed.set_thumbnail(url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
                    if list_to_str(results["Adjective"]) != "None":
                        embed.add_field(name="Adjective", value=list_to_str(results["Adjective"]), inline=False)
                    if list_to_str(results["Noun"]) != "None":
                        embed.add_field(name="Noun", value=list_to_str(results["Noun"]), inline=False)
                    if list_to_str(results["Verb"]) != "None":                    
                        embed.add_field(name="Verb", value=list_to_str(results["Verb"]), inline=False)
                    if list_to_str(results["Interjection"]) != "None":
                        embed.add_field(name="Interjection", value=list_to_str(results["Interjection"]), inline=False)
                    if list_to_str(results["Other"]) != "None":
                        embed.add_field(name="Other", value=list_to_str(results["Other"]), inline=False)
                    embed.set_footer(text="Copyright Naver 2021")
                    await message.channel.send(embed=embed)
                else:
                    print("From Web")
                    #print(etok(search_word))
                    results = etok(search_word)
                    embed=discord.Embed(title=results["Word"], color=0x00e1ff)
                    embed.set_author(name="Naver Eng-Kor Dictionary", icon_url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
                    embed.set_thumbnail(url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
                    if list_to_str(results["Adjective"]) != "None":
                        embed.add_field(name="Adjective", value=list_to_str(results["Adjective"]), inline=False)
                    if list_to_str(results["Noun"]) != "None":
                        embed.add_field(name="Noun", value=list_to_str(results["Noun"]), inline=False)
                    if list_to_str(results["Verb"]) != "None":                    
                        embed.add_field(name="Verb", value=list_to_str(results["Verb"]), inline=False)
                    if list_to_str(results["Interjection"]) != "None":
                        embed.add_field(name="Interjection", value=list_to_str(results["Interjection"]), inline=False)
                    if list_to_str(results["Other"]) != "None":
                        embed.add_field(name="Other", value=list_to_str(results["Other"]), inline=False)
                    embed.set_footer(text="Copyright Naver 2021")
                    await message.channel.send(embed=embed)
                # for testing your functions I recommend do it the way you did it by printing in websearch.py, as I still have to format
                # it to see it on discord and obviously you can't test here because you don't have the "know.env"
                


client = MyClient()
client.run(TOKEN)
