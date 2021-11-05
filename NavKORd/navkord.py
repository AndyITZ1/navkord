import discord
import os
import asyncio
import navdata
import random
import websearch
from dotenv import load_dotenv
from websearch import etok
from websearch import ktoe
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
            a += word
    else:
        a = "None"
    return a

def create_embed_etok(result_dict):
    embed=discord.Embed(title=result_dict["Word"], color=0x00e1ff)
    embed.set_author(name="Naver Eng-Kor Dictionary", icon_url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
    embed.set_thumbnail(url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
    if list_to_str(result_dict["Adjective"]) != "None":
        embed.add_field(name="Adjective", value=list_to_str(result_dict["Adjective"]), inline=False)
    if list_to_str(result_dict["Noun"]) != "None":
        embed.add_field(name="Noun", value=list_to_str(result_dict["Noun"]), inline=False)
    if list_to_str(result_dict["Verb"]) != "None":                    
        embed.add_field(name="Verb", value=list_to_str(result_dict["Verb"]), inline=False)
    if list_to_str(result_dict["Interjection"]) != "None":
        embed.add_field(name="Interjection", value=list_to_str(result_dict["Interjection"]), inline=False)
    if list_to_str(result_dict["Other"]) != "None":
        embed.add_field(name="Other", value=list_to_str(result_dict["Other"]), inline=False)
    embed.set_footer(text="Copyright Naver 2021")
    return embed

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
                ktoe(search_word)
            elif content.startswith(prefix + "etok"):
                search_word = content.split(' ')[1].lower() #Ex: !etok blue --> retrieves "blue"
                if check_db(search_word):
                    print("From DB")
                    embed = create_embed_etok(find_db(search_word))
                    await message.channel.send(embed=embed)
                else:
                    print("From Web")
                    embed = create_embed_etok(etok(search_word))
                    await message.channel.send(embed=embed)
                


client = MyClient()
client.run(TOKEN)
