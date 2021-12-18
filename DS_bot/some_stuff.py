from discord import Colour
from discord.utils import get
import discord
import json
import inspect
import re

import data_base.work_with_db as db
from __main__ import bot

def ping_to_id (obj): #if u give id it will just return it
    return re.sub('[^0-9]','', obj)

def check_that_you_have_enough_money(server_id,user_id,price):
    user_balance = db.tuple_to_int(db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(server_id),str(user_id)],['=','='],['AND'])[0])
    return user_balance >= int(price) 

def check_if_user_female(user_id,server_id):
    return bool (db.tuple_to_int( db.select(['is_female'],'servers_user_data',['user_id','server_id'],[str(user_id),str(server_id)],['=','='],['AND'])[0]))


def embed(text,color = Colour.gold(),title ='',emoji = ''):
    if color == Colour.red():
        emoji = ":x:"
    elif color == Colour.green():
        emoji = ":white_check_mark:"
    if len(list(emoji))!=0:
        emoji +='| '
    emb = discord.Embed(description =  emoji+'**'+text+"**" , color = color, title = title)
    return emb

def age_count(t):
    days = int(t / 86400)
    t = t - days * 86400
    hours = int(t / 3600)
    t = t - hours * 3600
    minutes = int (t / 60)
    t = t - minutes * 60
    seconds = int(t)
    return [-days,-hours,-minutes,-seconds]


def is_bot_server_admin(user_id,server_id):
    list_of_admins = json.loads(''.join(db.select(['bot_admins'],'servers_data',['server_id'],[str(server_id)],['='])[0]))
    return  str(user_id) in list_of_admins


def is_bot_server_moderator(user_id,server_id):
    list_of_moderatores = json.loads(''.join(db.select(['bot_moderators'],'servers_data',['server_id'],[str(server_id)],['='])[0]))
    return str(user_id) in list_of_moderatores
 
def is_creator(id):
    return int(id) == 521291273777446922


def input_to_seconds(lenght):
    t_symbol = lenght[len(lenght)-1]
    if t_symbol == 'm':
        lenght = int(lenght[0:len(lenght)-1]) * 60
    elif t_symbol == 'h':
        lenght = int(lenght[0:len(lenght)-1]) * 3600
    elif t_symbol == 'd':
        lenght = int(lenght[0:len(lenght)-1]) * 86400
    elif t_symbol == 'w':
        lenght = int(lenght[0:len(lenght)-1]) * 604800
    elif t_symbol == 'M':
        lenght = int(lenght[0:len(lenght)-1]) * 2592000 
    elif t_symbol == 'y':
        lenght = int(lenght[0:len(lenght)-1]) * 31536000
    else:
        lenght = int(lenght)
    return lenght

def methods_with_decorator(cls, decoratorName = 'bot.command'):
    sourcelines = inspect.getsourcelines(cls)[0]
    for i,line in enumerate(sourcelines):
        line = line.strip()
        if line.split('(')[0].strip() == '@'+decoratorName: # leaving a bit out
            nextLine = sourcelines[i+1]
            name = nextLine.split('def')[1].split('(')[0].strip()
            yield(name)

async def command_answer_wait(channel,author):
    def check(m):
        return  m.channel == channel and m.author == author
    return await bot.wait_for("message", check=check)
