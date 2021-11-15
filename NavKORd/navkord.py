import discord
import os
import asyncio
import navdata
import random
import websearch
from dotenv import load_dotenv
from websearch import etok, ktoe
from navdata import find_etok, check_etok, add_user, find_user, update_user, find_ktoe

load_dotenv('know.env')
TOKEN = os.getenv('TOKEN')

# changeable prefix for bot
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
    embed = discord.Embed(title=result_dict["Word"], color=0x00e1ff)
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


def create_embed_stats(user):
    embed = discord.Embed(title=str(user), color=0x1ad132)
    embed.set_author(name="NavKORd")
    embed.set_thumbnail(url=str(user.avatar_url))
    db_user = find_user(user)
    if not db_user:
        add_new_user(user)
        db_user = find_user(user)
    embed.add_field(name="Level", value=db_user["level"], inline=True)
    embed.add_field(name="Exp", value=f'{db_user["exp"]}/{db_user["level"]*100}', inline=True)
    embed.add_field(name="Dictionary Requests", value=db_user["dictreq"], inline=True)
    embed.add_field(name="Daily Corrects", value=db_user["dailycor"], inline=True)
    embed.add_field(name="Gold", value=db_user["gold"], inline=True)
    return embed

def list_to_str_ktoe(list):
    a = ""
    if list:
        for word in list:
            a += word + "\n"
    else:
        a = "None"
    return a


def create_embed_ktoe(result_dict):
    embed = discord.Embed(title=result_dict["word"], color=0x00e1ff)
    embed.set_author(name="Naver Kor-Eng Dictionary", icon_url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
    embed.set_thumbnail(url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
    for key in result_dict:
        if key in ["word"]:
            pass
        else:
            embed.add_field(name=key, value=list_to_str_ktoe(result_dict[key]), inline=False)
    embed.set_footer(text="Copyright Naver 2021")
    return embed


def add_new_user(user, exp_val=0, dict_req=0):
    dic = {
        "user": str(user),
        "level": 1,
        "exp": exp_val,
        "dictreq": dict_req,
        "dailycor": 0,
        "gold": 0
    }
    add_user(dic)


# class holding the bot and its functions
class MyClient(discord.Client):

    # at runtime will show the bot is online
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    # at runtime if a message is sent in the Discord chat, that message is passed in.
    async def on_message(self, message):
        # user who sent the message
        user = str(message.author)
        actual_user = message.author

        mention_users = message.mentions

        # message sent
        content = str(message.content)

        # channel the message was sent in
        channel = str(message.channel.name)

        # Avoids bot reacting/responding to itself
        if user == self.user:
            return

        # returns active message sent in chat to the command-line terminal (not in the Discord chat)
        print('Message from {0.author}: {0.content}'.format(message))

        # Do all Bot functions here, so that the bot only reacts to messages sent in this <channel>: commands
        if channel == 'commands':
            if content.startswith(prefix + "random"):
                response = f'This is your random number: {random.randint(0, 9)}'
                await message.channel.send(response)
                return
            elif content.startswith(prefix + "stats"):
                if len(mention_users) == 1:
                    embed = create_embed_stats(mention_users[0])
                    await message.channel.send(embed=embed)
                elif len(content.split(' ')) > 1:
                    await message.channel.send("Try again. Please use either \"stats\" or \"stats @username\".")
                else:
                    embed = create_embed_stats(actual_user)
                    await message.channel.send(embed=embed)
            elif content.startswith(prefix + "ktoe"):
                search_word = content.split(' ')[1]  # Ex: !ktoe 하다  --> retrieves the korean word
                if search_word.encode().isalpha():
                    await message.channel.send("Try again! Please input a valid Korean word.")
                else:
                    db_user = find_user(actual_user)
                    if not db_user:
                        add_new_user(actual_user, 1, 1)
                    else:
                        update_val = {"$set": {"exp": db_user["exp"] + 1,
                                               "dictreq": db_user["dictreq"] + 1
                                                }}
                        update_user(user, update_val)
                    ktoe_find = find_ktoe(search_word)
                    if ktoe_find:
                        print("from DB")
                        embed = create_embed_ktoe(ktoe_find)
                        await message.channel.send(embed=embed)
                    else:
                        print("from Web")
                        ktoe_re = ktoe(search_word)
                        if type(ktoe_re) == str:
                            await message.channel.send(ktoe_re)
                        else:
                            out = create_embed_ktoe(ktoe_re)
                            await message.channel.send(embed=out)
            elif content.startswith(prefix + "etok"):
                search_word = content.split(' ')[1].lower()  # Ex: !etok blue --> retrieves "blue"
                if not search_word.encode().isalpha():
                    await message.channel.send("Try again! Please input a valid English word.")
                else:
                    db_user = find_user(actual_user)
                    if not db_user:
                        add_new_user(actual_user, 1, 1)
                    else:
                        update_val = {"$set": {"exp": db_user["exp"] + 1,
                                               "dictreq": db_user["dictreq"] + 1
                                               }}
                        update_user(user, update_val)
                    if check_etok(search_word):
                        print("From DB")
                        embed = create_embed_etok(find_etok(search_word))
                        await message.channel.send(embed=embed)
                    else:
                        print("From Web")
                        etok_re = etok(search_word)
                        if type(etok_re) == str:
                            await message.channel.send(etok_re)
                        else:
                            embed = create_embed_etok(etok_re)
                            await message.channel.send(embed=embed)


client = MyClient()
client.run(TOKEN)
