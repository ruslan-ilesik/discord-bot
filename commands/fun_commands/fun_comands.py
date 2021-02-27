import random
import asyncio
import time

from __main__ import bot, use_shop, Colour,casino_frases
import data_base.work_with_db as db
import some_stuff as stuff



avaible = True
@bot.command(pass_context= True)
async def slap(ctx, for_who):
    if avaible:
        async def give(is_user = True):
            if  is_user:
                sex = int(stuff.check_if_user_female(ctx.author.id,ctx.guild.id))
                    
                kick_messages = [i[0]  for i in db.tuple_to_array(db.select(['phrase'],'phrases',['type','is_for_female'],['slap',str(sex)],['=','='],['AND']) ) ]   # [1], [2] - replace with users ping (1- giver, 2- takes)

                message = random.choice(kick_messages)

                message = message.replace('[1]','<@'+str(ctx.author.id)+'>') #who will give
                message = message.replace('[2]','<@'+str(for_who)+'>') # who will recive
                await ctx.send (embed = stuff.embed( message))
                db.update('servers_user_data',['kicks_take'],['kicks_take+1'],['server_id','user_id'],[str(ctx.guild.id),str(for_who)],['=','='],['AND'])
                db.update('servers_user_data',['balance','kicks_give','money_spent_all_time'],['balance-'+str(use_shop['hug']),'kicks_give+1','money_spent_all_time+'+str(use_shop['hug'])],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
            else:
                await ctx.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> поломал руку ударив, не самое приятное действие',Colour.red()))
                db.update('servers_user_data',['balance','kicks_give','money_spent_all_time'],['balance-'+str(use_shop['hug']),'kicks_give+1','money_spent_all_time+'+str(use_shop['hug'])],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])

        #check that user have enough money
        if stuff.check_that_you_have_enough_money(ctx.guild.id,ctx.author.id,use_shop['kick']) :
            # check that we have id or ping message and convert it
            for_who = stuff.ping_to_id(for_who)
            #check that punched person in base  
            #print(for_who)
            if len (db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id), for_who],['=','='],['AND'])) == 0: #check that user is on server
                if int(for_who) in [i.id for i in ctx.guild.members]: #is guy on server
                    db.insert('servers_user_data',['user_id','server_id','balance','last_balance_add_time','kicks_give','kicks_take','hugs_give','hugs_take','money_spent_all_time'],[str(for_who),str(ctx.guild.id),'0',str(int(time.time())),'0','0','0','0','0'])
                    await give()
                else:
                    await give(False)
                    
            else:
                await give()
        else:
            await ctx.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> настолько беден что у него не хватило даже на лящ...',Colour.red()))

@bot.command(pass_context= True)
async def change_sex(ctx,*args):
    async def change(m):
        if m.lower()  == 'men' and if_women:
            db.update('servers_user_data',['is_female'],['0'],['user_id','server_id'],[str(ctx.author.id),str(ctx.guild.id)],['=','='],['AND'])
            await ctx.send(embed = stuff.embed('Успешно изменён пол на мужской',Colour.green()))
        elif m.lower()  == 'women' and not if_women:
            db.update('servers_user_data',['is_female'],['1'],['user_id','server_id'],[str(ctx.author.id),str(ctx.guild.id)],['=','='],['AND'])
            await ctx.send(embed = stuff.embed('Успешно изменён пол на женский',Colour.green()))
        else:
            await ctx.send(embed = stuff.embed('Что то не так, или вы уже являетесь этим полом', Colour.red()))

    if_women = stuff.check_if_user_female(ctx.author.id,ctx.guild.id)
    if len(args) == 0:
        if if_women:
            await ctx.send(embed = stuff.embed('Если хотите поменять пол на мужской напишите "men"',emoji=':restroom: '))
        else:
            await ctx.send(embed = stuff.embed('Если хотите поменять пол на женский напишите "women"',emoji=':restroom: '))
        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
        await change(m.content)
    else:    
        await change(args[0])


@bot.command(pass_context= True)
async def hug(ctx, for_who):
    if avaible:
        async def give(is_user = True):
            if  is_user:
                sex = int(stuff.check_if_user_female(ctx.author.id,ctx.guild.id))
                hug_messages = [i[0]  for i in db.tuple_to_array(db.select(['phrase'],'phrases',['type','is_for_female'],['hug',sex],['=','='],['AND']) ) ]
                message = random.choice(hug_messages)
                message = message.replace('[1]','<@'+str(ctx.author.id)+'>') #who will give
                message = message.replace('[2]','<@'+str(for_who)+'>') # who will recive
                await ctx.send (embed = stuff.embed(message))
                db.update('servers_user_data',['hugs_take'],['hugs_take+1'],['server_id','user_id'],[str(ctx.guild.id),str(for_who)],['=','='],['AND'])
                db.update('servers_user_data',['balance','hugs_give','money_spent_all_time'],['balance-'+str(use_shop['hug']),'hugs_give+1','money_spent_all_time+'+str(use_shop['hug'])],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
            else:
                await ctx.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> обнял стену, не самое приятное действие',Colour.red()))
                db.update('servers_user_data',['balance','hugs_give','money_spent_all_time'],['balance-'+str(use_shop['hug']),'hugs_give+1','money_spent_all_time+'+str(use_shop['hug'])],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])

        #check that user have enough money
        if stuff.check_that_you_have_enough_money(ctx.guild.id,ctx.author.id,use_shop['hug']) :
            # check that we have id or ping message and convert it
            for_who = stuff.ping_to_id(for_who)
            #check that punched person in base  
            if len (db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id), for_who],['=','='],['AND'])) == 0: #check that user is on server
                if int(for_who) in [i.id for i in ctx.guild.members]: #is guy on server
                    db.insert('servers_user_data',['user_id','server_id','balance','last_balance_add_time','kicks_give','kicks_take','hugs_give','hugs_take','money_spent_all_time'],[str(for_who),str(ctx.guild.id),'0',str(int(time.time())),'0','0','0','0','0'])
                    await give()
                else:
                    await give(False)
                    
            else:
                await give()
        else:
            await ctx.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> настолько беден что у него не хватило даже на обнимашки...',Colour.red()))


@bot.command(pass_context= True)
async def casino (ctx, *args):
    
    if avaible:
        try:
            bet = args[0]
        except:
            await ctx.send(embed = stuff.embed('Вы не ввели ставку',Colour.red()) )
            return
        try:
            if len (bet.split('.')) >1: #check that have integer not float
                raise Exception("Just to send broke message")
            bet = int(bet)
            if bet <=0:#check bet
                raise Exception("Just to send broke message")
            if stuff.check_that_you_have_enough_money(ctx.guild.id,ctx.author.id,bet):# check balance

                message = await ctx.send(embed = stuff.embed(random.choice(casino_frases),emoji= ':notebook_with_decorative_cover: '))
                await asyncio.sleep(1.5)
                for i in range(2):
                    await message.edit(embed = stuff.embed(random.choice(casino_frases),emoji= ':notebook_with_decorative_cover: '))
                    await asyncio.sleep(1.5)
                
                if random.randint(1,100) <= 60: #lose
                    db.update('servers_user_data',['balance','money_spent_all_time','casino_times_played','casino_lose_times','casino_money_lose'],['balance-'+str(bet),'money_spent_all_time+'+str(bet),'casino_times_played+1','casino_lose_times+1','casino_money_lose+'+str(bet)],['server_id','user_id'],[ctx.guild.id,ctx.author.id],['=','='],['AND'])
                    await message.edit(embed = stuff.embed( 'Вы проиграли свою ставку в '+str(bet),Colour.red()))
                else: # win
                    win = str(int(bet*0.75))
                    db.update('servers_user_data',['balance','money_spent_all_time','casino_times_played','casino_win_times','casino_money_win'],['balance+'+win,'money_spent_all_time+'+str(bet),'casino_times_played+1','casino_win_times+1','casino_money_win+'+win],['server_id','user_id'],[ctx.guild.id,ctx.author.id],['=','='],['AND'])
                    await message.edit(embed = stuff.embed( "Вы выиграли "+win,Colour.green()))
            else:# send that user that he dont have enough money
                await ctx.send(embed = stuff.embed('Эй, эй, полегче с азартом! У тебя нет таких денег для ставки',Colour.red()))


        except:
            await ctx.send(embed = stuff.embed('Вроде всё просто и понятно, но всё равно вы умудрились сделать ошибку',Colour.red()) )