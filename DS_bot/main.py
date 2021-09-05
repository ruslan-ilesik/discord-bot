import time
time_to_init = time.time()
import discord
from discord.ext import commands
from discord.utils import get
from discord import Colour
from discord_components import DiscordComponents
import asyncio
import json
import sys
import random
import datetime
import traceback 
import re
import chess.engine


import bot_data

#bot data
intents=discord.Intents.all()
token = bot_data.tocken()
bot = commands.Bot(command_prefix='+',intents=intents)
bot.remove_command('help')
use_shop ={'kick':20,
        'hug':20}


is_windows = hasattr(sys, 'getwindowsversion')

import data_base.work_with_db as db
import data_base.db_backup as db_backup
import some_stuff as stuff
import custom_roles as cs
import events.free_game_distributions as free_games


# values
give = False
tasks=[]



casino_frases = [i[0]  for i in db.tuple_to_array(db.select(['phrase'],'phrases',['type'],['casino'],['=']) ) ]
bot_mention_phrases = [i[0]  for i in db.tuple_to_array(db.select(['phrase'],'phrases',['type'],['bot_mention'],['=']) ) ]


for_alias = {'b':'balance','sub_check':'check_subscriptions','check_sub':'check_subscriptions','subscriptions_check':'check_subscriptions','edit_cs':'edit_custom_role','cs_edit':'edit_custom_role','custom_role_edit':'edit_custom_role'}



@bot.event
async def on_ready():
    DiscordComponents(bot)
    global work_with_commands, ch_engine
    import work_with_commands
    
    print('starting chess engine')
    if is_windows:
        transport, ch_engine = await chess.engine.popen_uci("./data/engines/chess/stockfish/stockfish.exe")
    else:
       transport, ch_engine = await chess.engine.popen_uci("./data/engines/chess/stockfish/stockfish")
    print('chess engine started')

    f= open('log.txt','w')
    f.write('')
    f.close()
    print('im online')
    print('time to init: '+str(time.time()- time_to_init)+' seconds')
    await my_events()
    


@bot.event
async def on_message (ctx,*args): 

    
    global role, give
    #task check
    if (ctx.author.bot):
        return

    # invite links blocking
    if len(re.findall(r"discord.gg/.",ctx.content)) >0:
        await ctx.delete()
        await ctx.channel.send(embed = stuff.embed('Запрещено присылать ссылки/приглашения!!!',Colour.red(),'Нарушение правил'))
        return

    # if someone mentioned bot
    if bot.user.mentioned_in(ctx) and ctx.content[0] != bot.command_prefix:
        #send some phrase
        await ctx.channel.send(embed = stuff.embed(random.choice(bot_mention_phrases),emoji= ':eyes:' ))

    #custom roles check and delete if time left
    t =time.time()
    #get roles that need delete
    customs = db.tuple_to_array(db.select(['*'],'custom_roles',['role_time_to_delete_from_user'],[str(t)],['<'])) # [[server_id, user_id, role_id , role_time_to_delete_from_user, time_to_delete_role],[...],...] 
    for i in customs:
        try:
            guild = bot.get_guild(int(i[0]))
            user = get(bot.get_all_members(), id=int(i[1]),guild  = guild)
            role = get(guild.roles, id = int(i[2]))
            await user.remove_roles(role)

            if t > int(i[4]): #delete role at all if need
                await role.delete()
            db.delete('custom_roles',['server_id','user_id','role_id'],[i[0],i[1],i[2]],['=','=','='],['AND','AND']) 
        except:
            continue


        # check if we can give user money in such channel
    give = False
    try:    
        black_list =  json.loads(''.join(db.select(['black_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),'give_money'],['=','='],['AND'])[0]))
        if len(black_list) == 0 :
            white_list = json.loads(''.join(db.select(['white_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),'give_money'],['=','='],['AND'])[0]))
            if len(white_list) == 0:
                give = True
                
            else:
                if str(ctx.channel.id) in white_list:
                    give = True
        else:
            if not str(ctx.channel.id)  in black_list:
                give = True
    except:
        give = True

    if give:
            #give money for messages
        #check if user exist in DB of this server
        balance_add = random.randint(1,3)
        if len(db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND']))== 0:
            # add new
            db.insert('servers_user_data',['user_id','server_id','balance','last_balance_add_time','kicks_give','kicks_take','hugs_give','hugs_take','money_spent_all_time'],[str(ctx.author.id),str(ctx.guild.id),str(balance_add),str(int(time.time())),'0','0','0','0','0'])
        elif time.time() - db.tuple_to_int(db.select(['last_balance_add_time'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])[0]) >= 180: #check that we can add new to the balance (time)
            db.update('servers_user_data',['balance','last_balance_add_time'],['balance + ' + str(balance_add),str(int(time.time()))],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND']) #adding 
        if ctx.author.id == 784746857489367041:  #bot_id
            return


    # checking that we can use this command 
    if work_with_commands.is_command_avaible(ctx):
            await bot.process_commands(ctx)
     


#@bot.event
#async def on_command_error(ctx,error):
    #f= open('log.txt','a')
    #print(error)
    #print(ctx.message.content)
    #f.write('\n\nERROR: '+str(error)+'\nMessage: '+ctx.message.content+'\n_______________')
    #f.close()



@bot.event
async def on_member_join(member):
    print('new member')
    print('server id :',member.guild.id)
    t=''.join(db.select (['new_member_message'],'servers_data',['server_id'],[member.guild.id],['='],[])[0])
    if len(t) !=0:
        await member.send(embed = stuff.embed(t))



async def my_events():
    
    time_sleep_times = 0
    while True:
        #autho backup of DB
        if time_sleep_times % 24 == 0:
            try:    
                await db_backup.backupping() # makes backup            
            except:
                print('Error make backup')

        #check for new games
        if time_sleep_times%12 == 0:
            await free_games.main()

        #sleep      
        if time_sleep_times == 24:
            time_sleep_times = 0
        time_sleep_times+=1
        await asyncio.sleep(60*60)


bot.run(token)

