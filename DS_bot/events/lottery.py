import json
from discord import Colour
from discord.utils import get
import asyncio
import random
import time

import data_base.work_with_db as db
import some_stuff as stuff
import custom_roles as cs

def new_lottery(ctx,lottery_name , participants_amount,money_for_participation,win_type,time_amount):            
    js = {
    'required_participants':int(participants_amount),
    'participation_price':int(money_for_participation),
    'prize':
            {   
                'type':win_type,  
                'amount_time':str(time_amount)
            },
    'participants':[]
         } # participants in ids         #type ==  "cs" -  custom_role  "sub" - sub_role  "cash" - coins
    
    js = json.dumps(js)
    
    db.insert('lotterys',['name','server_id','data'],[lottery_name, str(ctx.guild.id),db.conn.escape_string(js)])#.guild.id



async def add_user_to_lottery(ctx,lottery_data):
    # add user
    if stuff.check_that_you_have_enough_money(ctx.guild.id,ctx.author.id,lottery_data[2]['participation_price']):
        lottery_data[2]["participants"].append(ctx.author.id)
        db.update('lotterys',['data'],['"'+db.conn.escape_string(json.dumps (lottery_data[2]))+'"'],['server_id','name'],[lottery_data[1],'"'+lottery_data[0]+'"'],['=','='],['AND'])
        db.update('servers_user_data',['balance','money_spent_all_time','money_spent_in_lottery','lottery_played_times'],['balance-'+str(lottery_data[2]['participation_price']),'money_spent_all_time+'+str(lottery_data[2]['participation_price']),'money_spent_in_lottery+'+str(lottery_data[2]['participation_price']),'lottery_played_times+1' ],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
        await ctx.send(embed = stuff.embed('Вы успешно добавлены в список участников',Colour.green()))
        await check_lottery_to_play(ctx,lottery_data)

    else:
        await ctx.send(embed = stuff.embed('У вас нет столько коинов!',color= Colour.red()))

async def check_lottery_to_play(ctx,lottery_data):
    if len(set(lottery_data[2]["participants"])) == int(lottery_data[2]["required_participants"]):
        await ctx.send(embed = stuff.embed(', '.join(['<@'+str(i)+'>' for i in set(lottery_data[2]['participants'])])+ ': Розыгрыш начался') )
        m  = await ctx.send(embed = stuff.embed('10'))
        for i in range(9,0,-1):
            await asyncio.sleep(1)
            await m.edit(embed = stuff.embed(str(i)))
        winner  = random.choice(lottery_data[2]['participants'])
        await give_prize_and_change_data(ctx,lottery_data,winner)
        lottery_data[2]['participants']=[]
        db.update('lotterys',['data'],['"'+db.conn.escape_string( json.dumps(lottery_data[2]))+'"'],['name','server_id'],['"'+lottery_data[0]+'"',str(ctx.guild.id)],['=','='],['AND'])
        await m.edit (embed  = stuff.embed('<@'+str(winner)+'>: ты победил и выиграл приз, остальным спасибо за участие'))

async def give_prize_and_change_data(ctx,lottery_data,winner_id):
    # add wins and loses
    for i in set(lottery_data[2]['participants']):
        if int(i) == int(winner_id):
            db.update('servers_user_data',['lottery_win_times'],['lottery_win_times+1'],['server_id','user_id'],[str(ctx.guild.id),str(i)],['=','='],['AND'])
        else:
            db.update('servers_user_data',['lottery_lose_times'],['lottery_lose_times+1'],['server_id','user_id'],[str(ctx.guild.id),str(i)],['=','='],['AND'])

    # give prize
    if lottery_data[2]['prize']['type'] == 'cs':#custom role
        custom_role = cs.get_custom_role(str(ctx.guild.id),str(winner_id))
        if custom_role:
            db.update('custom_roles',['role_time_to_delete_from_user','time_to_delete_role'],['role_time_to_delete_from_user+'+str(lottery_data[2]['prize']['amount_time']),'time_to_delete_role+'+str(lottery_data[2]['prize']['amount_time'])],['server_id','user_id','role_id'],[str(ctx.guild.id),str(winner_id),db.tuple_to_int(custom_role[0])],['=','=','='],['AND','AND'])
        else:
            role = await ctx.guild.create_role(colour = Colour.light_grey() , name= 'custom_role')
            await ctx.author.add_roles(role)
            t= time.time()
            db.insert('custom_roles',["server_id",'user_id',"role_id","role_time_to_delete_from_user",'time_to_delete_role'],[str(ctx.guild.id),str(ctx.author.id),str(role.id),str(int(t)+int(lottery_data[2]['prize']['amount_time'])),str(int(t)+int(lottery_data[2]['prize']['amount_time']))])

    elif lottery_data[2]['prize']['type'] == 'sub': #sub role
        sub_role_id = db.tuple_to_int(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)])[0])
        user_role = db.select(['role_id'],'custom_roles',['user_id','server_id','role_id'],[str(winner_id),str(ctx.guild.id),str(sub_role_id)],['=','=','='],['AND','AND'])
        if user_role:
            db.update('custom_roles',['role_time_to_delete_from_user'],['role_time_to_delete_from_user+'+str(lottery_data[2]['prize']['amount_time'])],['server_id','user_id','role_id'],[str(ctx.guild.id),str(winner_id),str(sub_role_id)],['=','=','='],['AND','AND'])
        else:
            role = get(ctx.guild.roles, id = int(sub_role_id)) 
            await ctx.author.add_roles(role)
            t= time.time()
            db.insert('custom_roles',["server_id",'user_id',"role_id","role_time_to_delete_from_user"],[str(ctx.guild.id),str(ctx.author.id),str(role.id),str(int(t)+int(lottery_data[2]['prize']['amount_time']))])

        
    else: #cash
        db.update('servers_user_data',['balance'],['balance+'+str(lottery_data[2]['prize']['amount_time'])],['server_id','user_id'],[str(ctx.guild.id),str(winner_id)],['=','='],['AND'])
        
    

