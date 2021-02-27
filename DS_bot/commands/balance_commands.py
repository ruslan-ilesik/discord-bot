import discord
from discord.ext import commands
from discord.utils import get
from discord import Colour

import some_stuff as stuff
import data_base.work_with_db as db
from __main__ import bot

avaible = True


@bot.command(pass_context= True,aliases=['b'])
async def balance(ctx, which = ''):
    if avaible:
        if which == '':
            balance = db.tuple_to_int( db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])[0])
            await ctx.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> ваш баланс: '+str(balance),emoji=':moneybag:'))
        else:
            which = stuff.ping_to_id(which)
            balance = db.tuple_to_int( db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),which],['=','='],['AND'])[0])
            user = get(bot.get_all_members(), id=int(which),guild = ctx.guild)
            await ctx.send(embed = stuff.embed('Баланс '+str(user)+': '+str(balance),emoji=':moneybag:'))


@bot.command(pass_context= True)
async def transfer (ctx, for_who, amount):
    if avaible:
        try:
            for_who = stuff.ping_to_id(for_who)
            if int(for_who) == ctx.author.id :
                await ctx.send(embed = stuff.embed('Вы не можете перечислять деньги самому себе ', Colour.red()))
                return
            if int(for_who) in [i.id for i in ctx.guild.members]: #is guy on server
                if stuff.check_that_you_have_enough_money(ctx.guild.id,ctx.author.id,amount):
                    if len (amount.split('.')) >1: #check that have integer not float
                        raise Exception("Just to send broke message")
                    if int(amount) <=0:#check amount
                        raise Exception("Just to send broke message")

                    # get money from giver
                    db.update('servers_user_data',['balance','money_spent_all_time','transfer_give_times','transfer_money_give_at_all'],['balance-'+amount,'money_spent_all_time+'+amount,'transfer_give_times+1','transfer_money_give_at_all+'+amount],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
                    db.update('servers_user_data',['balance','transfer_take_times','transfer_money_take_at_all'],['balance+'+amount,'transfer_take_times+1','transfer_money_take_at_all+'+amount],['server_id','user_id'],[str(ctx.guild.id),for_who],['=','='],['AND'])
                    await ctx.send(embed = stuff.embed('Успешно переведено '+amount+' коинов на баланс '+str(get(bot.get_all_members(), id=int(for_who),guild = ctx.guild)),Colour.green(),emoji=':white_check_mark:'))
                else:
                    await ctx.send(embed = stuff.embed('У вас нету столько денег чтобы передавать их кому либо',Colour.red()))
            else:
                await ctx.send(embed = stuff.embed('Вы не можете перевести деньги пользователю которого нет на сервере',Colour.red()))
        except:
            await ctx.send(embed = stuff.embed("Что то пошло не так, убедитесь что вы ввели всё правильно",Colour.red()))


