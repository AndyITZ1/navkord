import discord
import os
import asyncio
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from websearch import etok_search, ktoe_search
from navdata import UserDB, Ktoe, Etok

load_dotenv('know.env')
TOKEN = os.getenv('TOKEN')

userdb = UserDB()
ktoe = Ktoe()
etok = Etok()

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


def list_to_str_newline(list):
    a = ""
    for word in list:
        a += word + "\n"
    return a

def add_stats_upd_lvl(actual_user, remainder):
    db_user = userdb.find_user(actual_user)
    if not db_user:
        add_new_user(actual_user, 1, 1)
    update_val = {"$set": {"exp": remainder,
                           "level": db_user["level"] + 1
                           }}
    userdb.update_user(str(actual_user), update_val)

def create_embed_stats(user):
    embed = discord.Embed(title=str(user), color=0x1ad132)
    embed.set_author(name="NavKORd")
    embed.set_thumbnail(url=str(user.avatar_url))
    db_user = userdb.find_user(user)
    if not db_user:
        add_new_user(user)
        db_user = userdb.find_user(user)
    if db_user["exp"] >= db_user["level"] * 100:
        remainder = db_user["exp"] - db_user["level"] * 100
        add_stats_upd_lvl(user, remainder)
    embed.add_field(name="Level", value=db_user["level"], inline=True)
    embed.add_field(name="Exp", value=f'{db_user["exp"]}/{db_user["level"] * 100}', inline=True)
    embed.add_field(name="Dictionary Requests", value=db_user["dictreq"], inline=True)
    embed.add_field(name="Daily Corrects", value=db_user["dailycor"], inline=True)
    embed.add_field(name="Gold", value=db_user["gold"], inline=True)
    if db_user["rsw"]:
        rsw_out = ""
        for search in db_user["rsw"]:
            rsw_out += "* " + search + "\n"
        embed.add_field(name="Recently Search Words", value=rsw_out, inline=False)
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
        if not (key in ["word", "_id", "count", "date", "conj"]):
            embed.add_field(name=key, value=list_to_str_ktoe(result_dict[key]), inline=False)
    if "conj" in result_dict.keys():
        embed.add_field(name="Conjugated", value=result_dict["conj"], inline=False)
    embed.set_footer(text="Copyright Naver 2021")
    return embed


def iskor(word):
    final = ""
    space = True
    for letter in word:
        if letter.encode().isalpha():
            final += letter
        elif letter == " ":
            final += " "
        elif letter == ",":
            final += ","
    while space is True:
        if final[:1] == " ":
            final = final[1:]
        else:
            space = False
    if len(final) < 3:
        return False
    if final:
        return final
    else:
        return False


def help_embed():
    embed = discord.Embed(title="NavKORd Help")
    embed.set_thumbnail(url="https://i.ytimg.com/vi/qdjakuMaW_c/hqdefault.jpg")
    embed.add_field(name="!ktoe", value="Converts Korean words to English..", inline=False)
    embed.add_field(name="!etok", value="Converts English words to Korean.", inline=False)
    embed.add_field(name="!random", value="roles a random number.", inline=False)
    embed.add_field(name="!stats", value="displays your stats from NavKORd. use @user to display a users stats. ",
                    inline=False)
    embed.set_footer(text="NavKORd Version 0.0.10a")
    return embed


def add_stats_word(actual_user, search_word):
    db_user = userdb.find_user(actual_user)
    if not db_user:
        add_new_user(actual_user, 1, 1)
    else:
        if len(db_user["rsw"]) >= 5:
            if not (search_word in db_user["rsw"]):  # avoid dup
                db_user["rsw"].pop(0)
                db_user["rsw"].append(search_word)
        else:
            if not (search_word in db_user["rsw"]):  # avoid dup
                db_user["rsw"].append(search_word)
        update_val = {"$set": {"exp": db_user["exp"] + 1,
                               "dictreq": db_user["dictreq"] + 1,
                               "rsw": db_user["rsw"]
                               }}
        userdb.update_user(str(actual_user), update_val)


def add_stats_dq(user):
    db_user = userdb.find_user(user)
    if not db_user:
        add_new_user(user, 1, 1)
    update_val = {"$set": {"exp": db_user["exp"] + 100,
                           "gold": db_user["gold"] + 100
                           }}
    userdb.update_user(str(user), update_val)


def add_new_user(user, exp_val=0, dict_req=0):
    dic = {
        "user": str(user),
        "level": 1,
        "exp": exp_val,
        "dictreq": dict_req,
        "dailycor": 0,
        "gold": 0,
        "rsw": []
    }
    userdb.add_user(dic)


# class holding the bot and its functions
class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.guild_dq_bool = {}
        self.guild_daily_q_ans = {}
        self.dq_active_bool = False
        self.dqt = self.loop.create_task(self.run_at("21:23:00", self.daily_question()))

        # self.bg_hello = self.loop.create_task(self.print_hello())

    # at runtime will show the bot is online
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        for server in self.guilds:
            self.guild_daily_q_ans[server.name] = []
            self.guild_dq_bool[server.name] = False

    async def on_guild_join(self):
        for server in self.guilds:
            if server.name not in self.guild_dq_bool.keys():
                self.guild_daily_q_ans[server.name] = []
                self.guild_dq_bool[server.name] = False

    # at runtime if a message is sent in the Discord chat, that message is passed in.
    async def on_message(self, message):
        # user who sent the message
        user = str(message.author)
        actual_user = message.author
        mention_users = message.mentions
        server = message.guild.name
        actual_server = message.guild

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
            elif content.startswith(prefix + "ping"):
                await message.channel.send("Pong2")
            elif content.startswith(prefix + "stats"):
                if len(mention_users) == 1:
                    embed = create_embed_stats(mention_users[0])
                    await message.channel.send(embed=embed)
                elif len(content.split(' ')) > 1:
                    await message.channel.send("Try again. Please use either \"stats\" or \"stats @username\".")
                else:
                    embed = create_embed_stats(actual_user)
                    await message.channel.send(embed=embed)
            elif content.startswith(prefix + "help"):
                await message.channel.send(embed=help_embed())
            elif content.startswith(prefix + "ktoe"):
                search_word = content.split(' ')[1]  # Ex: !ktoe 하다  --> retrieves the korean word
                if self.dq_active_bool:
                    if self.guild_daily_q_ans[server][1] == search_word:
                        await message.channel.send(
                            "Nice Try. We cant give you the definition while daily question is active.")
                else:
                    if search_word.encode().isalpha():
                        await message.channel.send("Try again! Please input a valid Korean word.")
                    else:
                        ktoe_find = ktoe.find(search_word)
                        if ktoe_find:
                            print("from DB")
                            add_stats_word(actual_user, search_word)
                            embed = create_embed_ktoe(ktoe_find)
                            await message.channel.send(embed=embed)
                        else:
                            print("from Web")
                            ktoe_re = ktoe_search(search_word)
                            if type(ktoe_re) == str:
                                await message.channel.send(ktoe_re)
                            else:
                                add_stats_word(actual_user, search_word)
                                out = create_embed_ktoe(ktoe_re)
                                await message.channel.send(embed=out)
            elif content.startswith(prefix + "etok"):
                search_word = content.split(' ')[1].lower()  # Ex: !etok blue --> retrieves "blue"
                if self.dq_active_bool:
                    if self.guild_daily_q_ans[server][1] == search_word:
                        await message.channel.send(
                            "Nice Try. We can't give you the definition while daily question is active.")
                else:
                    if not search_word.encode().isalpha():
                        await message.channel.send("Try again! Please input a valid English word.")
                    else:
                        add_stats_word(actual_user, search_word)
                        if etok.check(search_word):
                            print("From DB")
                            embed = create_embed_etok(etok.find(search_word))
                            await message.channel.send(embed=embed)
                        else:
                            print("From Web")
                            etok_re = etok_search(search_word)
                            if type(etok_re) == str:
                                await message.channel.send(etok_re)
                            else:
                                embed = create_embed_etok(etok_re)
                                await message.channel.send(embed=embed)

    # async def print_hello(self):
    #     await self.wait_until_ready()
    #     print("hello")
    #     channel = self.get_channel(729825675120214099)
    #     await channel.send("hello")
    #     return await asyncio.sleep(5)
    #     # while not self.is_closed():
    #     #     await channel.send("hello")
    #     #     await asyncio.sleep(5)

    async def wait_until_hour(self, hour_val):
        dt = datetime.now()
        td = datetime.strptime(str(datetime.now().date()) + " " + hour_val, "%Y-%m-%d %H:%M:%S")
        if td < dt:
            print("Schedule time is passed, adding a day")
            td = td + timedelta(days=1)
        print((td - dt).seconds)
        await asyncio.sleep((td - dt).seconds)

    # DONT TOUCH THIS
    async def run_at(self, hour_val, coro):
        await self.wait_until_ready()
        await self.wait_until_hour(hour_val)
        return await coro

    # FIGURE THIS OUT LATER WHEN YOU ARE DONE
    async def daily_question(self):
        # 1 min timer
        while not self.is_closed():
            self.dq_active_bool = True
            print("run bi")
            for server in self.guilds:
                channel = discord.utils.get(server.channels, name="commands")
                # channel = self.get_channel(729825675120214099)
                # e_k_bool = random.choice([True, False])
                e_k_bool = False
                if e_k_bool:
                    print("k")
                    db_data = ktoe.random(4)
                    count = 1
                    # for list in db_data:
                    #     for key in list:
                    #         if key in ["conj"]:
                    #             print("conj found")
                    #             error = 0
                    #             dup_loop = True
                    #             inde = db_data.index(list)
                    #             old = db_data[inde]
                    #             print(db_data[inde])
                    #             db_data[inde] = ktoe.random(1)
                    #             while dup_loop:
                    #                 if db_data[inde] == old or db_data[inde] in db_data:
                    #                     error += 1
                    #                     db_data[inde] = ktoe.random(1)
                    #                     print("changed to " + db_data[inde])
                    #                 elif error <= 5:
                    #                     dup_loop = False
                    #                 else:
                    #                     # kills loop when word is different.
                    #                     dup_loop = False
                    #             # print(db_data)
                    #             # print(db_data[inde])
                    answer_num = random.randint(0, len(db_data) - 1)
                    self.guild_daily_q_ans[server.name].append(answer_num + 1)
                    embed = discord.Embed(title="Daily Question:",
                                          description="What is the English word for " + db_data[answer_num][
                                              "word"] + "?",
                                          color=0x00e1ff)
                    for list in db_data:
                        loop_break = False
                        for key in list:
                            if loop_break:
                                break
                            if key in ["conj"]:
                                break
                            if key not in ["word", "_id", "count", "date"]:
                                for word in list[key]:
                                    if iskor(word):
                                        # print(word)
                                        embed.add_field(name=str(count), value=iskor(word), inline=False)
                                        count += 1
                                        loop_break = True
                                        break
                    self.guild_daily_q_ans[server.name].append(db_data[answer_num]["word"])
                    await channel.send(embed=embed)
                else:
                    print("e")
                    db_data = etok.random(4)
                    answer_num = random.randint(0, 3)
                    self.guild_daily_q_ans[server.name].append(answer_num + 1)
                    embed = discord.Embed(title="Daily Question:",
                                          description="What is the Korean word for " + db_data[answer_num][
                                              "Word"] + "?", color=0x00e1ff)
                    count = 1
                    for x in db_data:
                        # print(x)
                        for key in x:
                            if key not in ["Word", "_id", "count", "date", "conj"]:
                                if x[key]:
                                    # print(x[key][0])
                                    val = x[key][0]
                                    if "Number" in val:
                                        val = val.split("Number, ")[1]
                                    elif "→" in val:
                                        val = val.split(" (→")[0]
                                    else:
                                        val = val.split(",")[0]
                                    print(val)
                                    embed.add_field(name=str(count), value=val, inline=False)
                                    count += 1
                                    break
                    await channel.send(embed=embed)
                    self.guild_daily_q_ans[server.name].append(db_data[answer_num]["Word"])
                    print("Supposedly sent embed")
            end_time = datetime.now() + timedelta(seconds=30.0)
            now = datetime.now()
            server_comp = len(self.guild_daily_q_ans.keys())
            actual_comp = 0

            def check_ans(m):
                return m.content in ["1", "2", "3", "4"]

            while now < end_time:
                now = datetime.now()
                print(now)
                if actual_comp == server_comp:
                    break
                else:
                    try:
                        msg = await self.wait_for('message', check=check_ans, timeout=(end_time - now).total_seconds())
                    except asyncio.TimeoutError:
                        break
                    if int(msg.content) == self.guild_daily_q_ans[msg.guild.name][0] and not self.guild_dq_bool[
                        msg.guild.name]:
                        await msg.channel.send(
                            f'Congratulations {msg.author}! You get 100 experience points and 100 gold!')
                        # ADD FUNCTION HERE TO UPDATE STATS FOR GOLD AND EXP
                        print("It works")
                        add_stats_dq(msg.author)
                        self.guild_dq_bool[msg.guild.name] = True
                        actual_comp += 1
            for server in self.guilds:
                if not self.guild_dq_bool[server.name]:
                    channel = discord.utils.get(server.channels, name="commands")
                    await channel.send(
                        f"Times up! Daily question is over! The answer was {self.guild_daily_q_ans[server.name][0]}.")
                self.guild_dq_bool[server.name] = False
            self.dq_active_bool = False
            await self.run_at("20:10:00", self.daily_question())


client = MyClient()
client.run(TOKEN)
