import discord
from discord.ext import commands
from discord.utils import get
from discord import Colour
import json
import time

import data_base.work_with_db as db
from __main__ import bot,for_alias
import some_stuff as stuff
from data_base import db_backup
import custom_roles as cs
import events.lottery as lottery
import commands.shop_commands as shop_commands

#_____admin commands______________________________
avaible = True


async def send_to_user_balance_change(ctx,user_id,text):
    user = get(bot.get_all_members(), id=int(user_id))
    await user.send(embed = stuff.embed(text+' на сервере "'+ctx.guild.name+'"',Colour.green()))


async def show_ids(ctx,what):
    if what == 'admin':
        list_of_admins = json.loads(''.join(db.select(['bot_admins'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
        try:
            await ctx.send(embed = stuff.embed(', '.join(list_of_admins),emoji= ':eye: '))
        except:
            await ctx.channel.send(embed = stuff.embed(', '.join(list_of_admins),emoji= ':eye: '))
    elif what == 'moder':
        list_of_moderatores = json.loads(''.join(db.select(['bot_moderators'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
        try:
            await ctx.send(embed = stuff.embed(', '.join(list_of_moderatores),emoji= ':eye: '))
        except:
           await  ctx.channel.send(embed = stuff.embed(', '.join(list_of_moderatores),emoji= ':eye: '))

async def show_names(ctx,what):
    if what == 'admin':
        list_of_admins = json.loads(''.join(db.select(['bot_admins'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
        try:
            await ctx.send(embed = stuff.embed(', '.join([str(get(bot.get_all_members(), id=int(i) ,guild = ctx.guild)) for i in list_of_admins]),emoji= ':eye: '))
        except:
            await ctx.channel.send(embed = stuff.embed(', '.join([str(get(bot.get_all_members(), id=int(i) ,guild = ctx.guild)) for i in list_of_admins]),emoji= ':eye: '))
    elif what == 'moder':
        list_of_moderatores = json.loads(''.join(db.select(['bot_moderators'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
        try:
            await ctx.send(embed = stuff.embed(', '.join([str(get(bot.get_all_members(), id=int(i) ,guild = ctx.guild)) for i in list_of_moderatores]),emoji= ':eye: '))
        except:
            await ctx.channel.send(embed = stuff.embed(', '.join([str(get(bot.get_all_members(), id=int(i) ,guild = ctx.guild)) for i in list_of_moderatores]),emoji= ':eye: '))


async def show_ids_and_names(ctx,what):
    if what == 'admin':
        list_of_admins = json.loads(''.join(db.select(['bot_admins'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
        names = [str(get(bot.get_all_members(), id=int(i) ,guild = ctx.guild)) for i in list_of_admins]
        try:
            await ctx.send(embed = stuff.embed('\n'.join([names[i]+': '+list_of_admins[i] for i in range(len(names))]),emoji= ':eye: '))
        except:
            await ctx.channel.send(embed = stuff.embed('\n'.join([names[i]+': '+list_of_admins[i] for i in range(len(names))]),emoji= ':eye: '))
    elif what == 'moder':
        list_of_moderatores = json.loads(''.join(db.select(['bot_moderators'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
        names = [str(get(bot.get_all_members(), id=int(i) ,guild = ctx.guild)) for i in list_of_moderatores]
        try:
            await ctx.send(embed = stuff.embed('\n'.join([names[i]+': '+list_of_moderatores[i] for i in range(len(names))]),emoji= ':eye: '))
        except:
            await ctx.channel.send(embed = stuff.embed('\n'.join([names[i]+': '+list_of_moderatores[i] for i in range(len(names))]),emoji= ':eye: '))



@bot.command(pass_context= True)
async def admin_help(ctx):
    p = bot.command_prefix
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id)):  
        text = '``'+p+'add_to_balance "User" "Amount"`` - добавить User на баланс Amount\n``'+p+'remove_from_balance "User" "Amount"`` - снять Amount с баланса User\n``'+p+'set_balance "User" "Amount"`` - присвоить балансу User значение Amount\n\n'
        text+='``'+p+'add_admin "User"`` - добавить User в администраторы бота\n``+remove_admin "User"`` - удалить администратора бота User\n``'+p+'show_admins`` - показать список администраторов бота\n\n'
        text+='``'+p+'add_moder "User"`` - добавить User в модераторы бота\n``'+p+'remove_moder "User"`` - удалить модератора бота User\n``'+p+'show_moders`` - показать список модераторов бота\n\n'
        text+='``'+p+'add_to_scores_blacklist "Channel"`` -добавить канал в blacklist  (пользователи не будут получать очки за активность в этом канале)\n``'+p+'remove_from_scores_blacklist "Channel"`` - убрать канал из blacklist (пользователи смогут получать там очки)\n``'+p+'show_blacklist`` - показывает blacklist каналов активности\n\n '
        text+='``'+p+'gift_custom_role "User" "Time"`` - подарить User кастомную роль на Time\n``'+p+'remove_roles "User"`` - правильно забрать роль у User\n\n'
        text+='``'+p+'edit_lotterys`` - для работы с лотереями (создание, удаление, редактирование)\n``'+p+'command_permisions`` - редактирование настроек команд (blacklist,whitelist)\n``'+p+'server_settings`` - некоторые базовые настройки\n``'+p+'shop_edit`` - редактирование магазина'
        emb = emb = discord.Embed(title="!!! Админ Команды !!!", description=text, color=Colour.gold())
        await ctx.send(embed = emb)








@bot.command(pass_context= True)
@commands.has_permissions(administrator = True) 
async def mute(ctx, user_id , amount_of_captha , *args):# *args  = reason
    if avaible and stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) :
        await ctx.message.delete()
        await ctx.send ('<@'+user_id+'> был заблокирован '+ctx.author.mention+ ' на '+ str(amount_of_captha)+ ' каптчи. Причина : '+' '.join(args))

        user = get(bot.get_all_members(), id = int(user_id),guild = ctx.guild)

        role = get(ctx.message.guild.roles, id = int(db.tuple_to_int(db.select(['mute_role_id'],'servers_data',['server_id'],[ctx.guild.id],['='],[])[0])))
        print(role)
        print(user)
        await user.add_roles(role)
        await user.send(embed = stuff.embed('Вы были заблокированы за нарушение правил и чтобы быть разблокироваными вы должны выполнять банальные задания на подобии ответ на пример или текст. Чтобы узнать об этом больше напишити +work_help в канале для работы',Colour.red()))
            # adding muted person to DB
        #check if that user was already  in mute on this server
        if len(db.select(['amount_of_captcha'],'users_in_mute',['server_id','user_id'],[str(ctx.guild.id),str(user_id)],['=','='],['AND'])) ==0:
            #new_user
            db.insert('users_in_mute',['user_id','server_id','amount_of_captcha','last_answer_time'],[str(user_id),str(ctx.guild.id),str(amount_of_captha),'0'])
        else:
            #update data
            db.update('users_in_mute',['amount_of_captcha'],[str(amount_of_captha)],['user_id','server_id'],[str(user_id),str(ctx.guild.id),],['=','='],['AND'])




@bot.command(pass_context= True)
async def add_to_balance(ctx,for_who,amount):
    if avaible and stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) :
        try:
            int(amount) # it will throw error if somthing wrong
            for_who = stuff.ping_to_id(for_who)
            int(for_who) # it will throw error if somthing wrong
            #check if user not in base
            if len(db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),for_who],['=','='],['AND'])) == 0:
                # add him
                db.insert('servers_user_data',['server_id','user_id','balance'],[str(ctx.guild.id),for_who,amount])
            else:
                #update his balance
                db.update('servers_user_data',['balance'],['balance+'+amount],['server_id','user_id'],[str(ctx.guild.id),for_who,amount],['=','='],['AND'])
            await ctx.send(embed = stuff.embed('Успешно изменён баланс пользователя',Colour.green(),emoji= ':white_check_mark:'))
            await send_to_user_balance_change(ctx,for_who,'Вам было добавлено '+str(amount)+' Коинов на акаунт')
            
        except:
            await ctx.send(embed = stuff.embed('Ошибка при пополнении баланса, возможно вы не правильно ввели данные',Colour.red(),emoji=':x:'))



@bot.command(pass_context= True)
async def remove_from_balance(ctx,for_who,amount):
    if avaible and stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) :
        try:
            int(amount) # it will throw error if somthing wrong
            for_who = stuff.ping_to_id(for_who)
            int(for_who) # it will throw error if somthing wrong
            #check if user not in base
            if len(db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),for_who],['=','='],['AND'])) == 0:
                # add him
                db.insert('servers_user_data',['server_id','user_id','balance'],[str(ctx.guild.id),for_who,amount])
            else:
                #update his balance
                db.update('servers_user_data',['balance'],['balance-'+amount],['server_id','user_id'],[str(ctx.guild.id),for_who,amount],['=','='],['AND'])
            await ctx.send(embed = stuff.embed('Успешно изменён баланс пользователя',Colour.green(),emoji= ':white_check_mark:'))
            await send_to_user_balance_change(ctx,for_who,'У вас было забрано '+str(amount)+' Коинов с акаунта')
        except:
            await ctx.send(embed = stuff.embed('Ошибка при уменьшении баланса, возможно вы не правильно ввели данные',Colour.red(),emoji= ':x:'))


@bot.command(pass_context= True,aliases=["set_to_b"])
async def set_balance(ctx,for_who,amount):
    if avaible and stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) :
        try:
            int(amount) # it will throw error if somthing wrong
            for_who = stuff.ping_to_id(for_who)
            int(for_who) # it will throw error if somthing wrong
            #check if user not in base
            if len(db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),for_who],['=','='],['AND'])) == 0:
                # add him
                db.insert('servers_user_data',['server_id','user_id','balance'],[str(ctx.guild.id),for_who,amount])
            else:
                #update his balance
                db.update('servers_user_data',['balance'],[amount],['server_id','user_id'],[str(ctx.guild.id),for_who,amount],['=','='],['AND'])
            await ctx.send(embed = stuff.embed('Успешно изменён баланс пользователя',Colour.green(),emoji= ':white_check_mark:'))    
            await send_to_user_balance_change(ctx,for_who,'Ваш новый баланс '+str(amount)+' Коинов')
        except:
            await ctx.send(embed = stuff.embed('Ошибка при пополнении баланса, возможно вы не правильно ввели данные',Colour.red(),emoji= ':x:'))

@bot.command(pass_context= True)
async def add_admin(ctx,for_who):
    if avaible and stuff.is_creator(ctx.author.id):
        try:
            for_who = stuff.ping_to_id(for_who)
            admins_list = json.loads(''.join(db.select(['bot_admins'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
            if  for_who in admins_list:
                await ctx.send (embed = stuff.embed('Пользователь уже администратор бота',Colour.red(),emoji= ':x:'))
            else:
                admins_list.append(for_who)
                db.update('servers_data',['bot_admins'],["'"+json.dumps(admins_list)+"'"],['server_id'],[str(ctx.guild.id)],['='])
                await ctx.send (embed = stuff.embed('Пользователь был добавлен в список администраторов бота',Colour.green(),emoji= ':white_check_mark:'))
        except:
            await ctx.send (embed = stuff.embed('Ошибка при добавлении администратора бота',Colour.red(),emoji= ':x:'))

@bot.command(pass_context= True)
async def remove_admin(ctx,for_who):
    if avaible and stuff.is_creator(ctx.author.id):
        try:
            for_who = stuff.ping_to_id(for_who)
            admins_list = json.loads(''.join(db.select(['bot_admins'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
            if  not for_who in admins_list:
                await ctx.send (embed = stuff.embed('Пользователь и так не администратор бота',Colour.red(),emoji= ':x:'))
            else:
                admins_list.remove(for_who)
                db.update('servers_data',['bot_admins'],["'"+json.dumps(admins_list)+"'"],['server_id'],[str(ctx.guild.id)],['='])
                await ctx.send (embed = stuff.embed('Пользователь был убран из списка администраторов бота',Colour.green()))
        except:
            await ctx.send (embed = stuff.embed('Ошибка при добавлении администратора бота',Colour.red(),emoji= ':x:'))


@bot.command(pass_context= True)
async def show_admins(ctx,*args):
    global tasks
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id)):  
        if len (args) == 0:
            await ctx.send (embed = stuff.embed('Если вы хотите отобразить id пользователей напишите "1" или "id"\nЕсли вы хотите отобразть имена пользователей напишите "2" или "name"\nЕсли вы хотите отобразить и имена и id напишите "3" или "all"'))
            msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
            how_show = msg.content
        else:
            how_show =args[0].lower()

        if how_show == "1" or how_show == 'id':
            await show_ids(ctx,'admin')
        elif how_show == "2" or how_show == 'name':
            await show_names(ctx,'admin')           
        elif how_show == "3" or how_show == '4':
            await show_ids_and_names(ctx,'admin')
        else:
            await ctx.send(embed = stuff.embed('Неправильный ввод',Colour.red()))






@bot.command(pass_context= True)
async def add_moder(ctx,for_who):
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id)):
        try:
            for_who = stuff.ping_to_id(for_who)
            moders_list = json.loads(''.join(db.select(['bot_moderators'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
            if  for_who in moders_list:
                await ctx.send (embed = stuff.embed('Пользователь уже модератор бота',Colour.red()))
            else:
                moders_list.append(for_who)
                db.update('servers_data',['bot_moderators'],["'"+json.dumps(moders_list)+"'"],['server_id'],[str(ctx.guild.id)],['='])
                await ctx.send (embed = stuff.embed('Пользователь был добавлен в список модераторов бота',Colour.green()))
        except:
            await ctx.send (embed = stuff.embed('Ошибка при добавлении модератора бота',Colour.red()))

@bot.command(pass_context= True)
async def remove_moder(ctx,for_who):
    if avaible and  (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id)):
        try:
            for_who = stuff.ping_to_id(for_who)
            moders_list = json.loads(''.join(db.select(['bot_moderators'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0]))
            if  not for_who in moders_list:
                await ctx.send (embed = stuff.embed('Пользователь и так не модератор бота',Colour.red()))
            else:
                moders_list.remove(for_who)
                db.update('servers_data',['bot_moderators'],["'"+json.dumps(moders_list)+"'"],['server_id'],[str(ctx.guild.id)],['='])
                await ctx.send (embed = stuff.embed('Пользователь был убран из списка модератор бота',Colour.green()))
        except:
            await ctx.send (embed = stuff.embed('Ошибка при добавлении модератор бота',Colour.red()))


@bot.command(pass_context= True)
async def show_moders(ctx,*args):
    global tasks
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id)):  
        if len (args) == 0:
            await ctx.send (embed = stuff.embed('Если вы хотите отобразить id пользователей напишите "1" или "id"\nЕсли вы хотите отобразть имена пользователей напишите "2" или "name"\nЕсли вы хотите отобразить и имена и id напишите "3" или "all"'))
            how_show = await stuff.command_answer_wait(ctx.channel,ctx.author)
            how_show = how_show.content
        else:
            how_show=args[0].lower()

        if how_show == "1" or how_show == 'id':
            await show_ids(ctx,'moder')
        elif how_show == "2" or how_show == 'name':
            await show_names(ctx,'moder')           
        elif how_show == "3" or how_show == '4':
            await show_ids_and_names(ctx,'moder')
        else:
            await ctx.send(embed = stuff.embed('Неправильный ввод',Colour.red()))


@bot.command(pass_context= True)
async def add_to_scores_blacklist(ctx,channel_id):
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id)):
        try:
            black_list = json.loads(''.join(db.select(['black_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),'give_money'],['=','='],['AND'])[0]))
            if  channel_id in black_list:
                await ctx.send (embed = stuff.embed('Канал уже в чёрном списке',Colour.red()))
            else:
                black_list.append(channel_id)
                db.update('comands_servers_permisions',['black_list'],["'"+json.dumps(black_list)+"'"],['server_id','command'],[str(ctx.guild.id),'"give_money"'],['=','='],['AND'])
                await ctx.send (embed = stuff.embed('Канала был добавлен в blacklist',Colour.green()))
        except:
            await ctx.send (embed = stuff.embed('Ошибка при добавлении канала в blacklist',Colour.red()))

@bot.command(pass_context= True)
async def remove_from_scores_blacklist(ctx,channel_id):
        if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id)):
            try:
                black_list = json.loads(''.join(db.select(['black_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),'give_money'],['=','='],['AND'])[0]))
                if not  channel_id in black_list:
                    await ctx.send (embed = stuff.embed('Каналa нет в чёрном списке',Colour.red()))
                else:
                    black_list.remove(channel_id)
                    db.update('comands_servers_permisions',['black_list'],["'"+json.dumps(black_list)+"'"],['server_id','command'],[str(ctx.guild.id),'"give_money"'],['=','='],['AND'])
                    await ctx.send (embed = stuff.embed('Канала был убран из чёрного списка',Colour.green()))
            except:
                await ctx.send (embed = stuff.embed('Ошибка при удаления канала из чёрного списка',Colour.red()))

@bot.command(pass_context= True)
async def show_blacklist(ctx):
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id)):
        black_list = json.loads(''.join(db.select(['black_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),'give_money'],['=','='],['AND'])[0]))
        await ctx.send(embed = stuff.embed(', '.join(['<#'+i+">" for i in black_list])))

@bot.command(pass_context= True)
async def gift_custom_role(ctx,for_who,lenght):
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id)):
        for_who = stuff.ping_to_id(for_who)
        lenght = stuff.input_to_seconds(lenght)
        #check if user on server
        if int(for_who) in [i.id for i in ctx.guild.members]:
            t = str(int(time.time()+lenght ))
            if cs.check_that_user_have_custom_role(ctx.guild.id,int(for_who)):
                db.update('custom_roles',['role_time_to_delete_from_user','time_to_delete_role'],[t,t],['user_id','server_id','role_id'],[for_who,str(ctx.guild.id),''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0])],['=','=','!='],['AND','AND'])
            else:
                user = get(bot.get_all_members(), id=int(for_who),guild  = ctx.guild)
                role = await ctx.guild.create_role(colour = Colour.dark_gray() , name= str(user))
                await user.add_roles(role)
                db.insert('custom_roles',["server_id",'user_id',"role_id","role_time_to_delete_from_user",'time_to_delete_role'],[str(ctx.guild.id),for_who,str(role.id),t,t])
            await ctx.send(embed = stuff.embed('Успешно подарена роль',Colour.green()))
        else:
            await ctx.send(embed = stuff.embed('Этого пользователя нет на сервере',Colour.red()))

@bot.command(pass_context= True)
async def remove_roles(ctx,for_who,*args):
    global tasks
    if avaible and (stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id)):        
        cus = ''
        text = ''
        for_who = stuff.ping_to_id(for_who)
        if len(args) == 0:
            roles_ids = db.tuple_to_array(db.select(["role_id"],'custom_roles',['server_id','user_id'],[str(ctx.guild.id),for_who],['=','='],["AND"]))  
            for i in roles_ids:
                if str(i[0]) == str(''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0])):
                    text += 'У пользователя есть саб роль, если вы хотите её убрать напишите "sub"\n'
                else:
                    text+= 'У пользователя есть кастомная роль, если вы хотите её убрать напишите "custom"\n'
                    cus = i[0]
            if text == '':
                await ctx.send(stuff.embed('У пользователя нет ролей которые можно забрать',Colour.red()))
            else: 
                await ctx.send(embed = stuff.embed(text))
                msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
                msg = msg.content     
        else:
            msg =args[0].lower()

        if msg == 'custom':
            user = get(bot.get_all_members(), id=int(for_who),guild  = ctx.guild)
            role = get(ctx.guild.roles, id = int(db.tuple_to_int(cs.get_custom_role(str(ctx.guild.id),for_who)[0])))
            db.delete('custom_roles',['server_id','user_id','role_id'],[str(ctx.guild.id),for_who,db.tuple_to_int(cs.get_custom_role(str(ctx.guild.id),for_who)[0])],['=','=','='],['AND','AND']) 
            await user.remove_roles(role)
            await ctx.send(embed = stuff.embed("Успешно удалена кастомная роль у пользователя",Colour.green()))

        elif msg == 'sub':
            user = get(bot.get_all_members(), id=int(for_who),guild  = ctx.guild)
            role = get(ctx.guild.roles, id = int(''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0])))
            db.delete('custom_roles',['server_id','user_id','role_id'],[str(ctx.guild.id),for_who,''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0])],['=','=','='],['AND','AND']) 
            await user.remove_roles(role)
            await ctx.send(embed = stuff.embed("Успешно удалена саб роль у пользователя",Colour.green()))
        else:
            await ctx.send(embed = stuff.embed("Ошибка ввода, поробуйте ещё раз",Colour.red()))


@bot.command(pass_context= True)
async def edit_lotterys(ctx):
    def delete_all_users_from_lottery(lottery):
        
        for i in lottery[2]['participants']:
            db.update('servers_user_data',['balance','money_spent_all_time','money_spent_in_lottery','lottery_played_times'],['balance+'+str(lottery[2]['participation_price']),'money_spent_all_time-'+str(lottery[2]['participation_price']),'money_spent_in_lottery-'+str(lottery[2]['participation_price']),'lottery_played_times-1'],['server_id','user_id'],[str(lottery[1]),str(i)],['=','='],['AND'])
        lottery[2]['participants'] = []
        return lottery   


    if stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.guild.id,ctx.guild.id):
        try:
            await ctx.send(embed = stuff.embed(title='Выберите что вы хотите сделать',text='1) Для редактирования существующей лотереи \n2) Для создания новой лотереи\n3) Для удаления лотерей'))
            m = await stuff.command_answer_wait(ctx.channel,ctx.author)

            
            selcted_type = m.content
            if  m.content == '1' or m.content == '3':
                #select_lottery:
                text = ''
                lotterys_and_data = db.tuple_to_array(db.select(["*"],'lotterys',['server_id'],[str(ctx.guild.id)]))
                for  i in range(len(lotterys_and_data)):
                    text+= str(i+1)+') '+lotterys_and_data[i][0]+'\n'
                emb = stuff.embed(title='**Выберите лотерею которую хотите редактировать (id)**',text = text)
                await ctx.send(embed  = emb)
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if len(m.content.split('.')) >1:
                    raise Exception("Incorect input")

                lottery = lotterys_and_data[int(m.content)-1]
                #edit lottery

                if selcted_type == '1':
                    while True:
                        lottery[2] = json.loads(lottery[2])
                        await ctx.send (embed = stuff.embed(title='Выберите что вы хотите редактировать\nЕсли закончили редактировать напишите "exit"',text='1) Название лотереи \n2) Тип приза (учасники сбросятся и им вернутся деньги)\n3) Время/сумму выигрыша (учасники сбросятся и им вернутся деньги)\n4) Количество участников (учасники сбросятся и им вернутся деньги)\n5) Стоимость участия (учасники сбросятся и им вернутся деньги)'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                        if len(m.content.split('.')) >1:
                            raise Exception("Incorect input")
                        if m.content.lower() == 'exit':
                            return
                        what_to_edit = int(m.content)

                        if what_to_edit == 1:
                            await ctx.send(embed = stuff.embed('Введите новое название лотереи'))
                            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                            db.update('lotterys',['name'],['"'+m.content+'"'],['server_id','name'],[str(ctx.guild.id),'"'+lottery[0]+'"'],['=','='],['AND'])
                            lottery[0] = m.content
                            await ctx.send(embed = stuff.embed('Успешно изменено название лотереи на '+m.content,Colour.green()))

                        elif what_to_edit == 2:
                            await ctx.send(embed = stuff.embed('Введите новый тип приза ("cs" - кастомная роль,"sub" - саб роль,"cash" - кэш)'))
                            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                            new_type = m.content.lower()
                            if new_type != 'cs' and new_type != 'sub' and new_type != 'cash':
                                raise Exception("Incorect input")
                            
                            lottery = delete_all_users_from_lottery(lottery)
                            lottery[2]['prize']['type'] = new_type
                            lottery[2] = json.dumps(lottery[2])
                            db.update('lotterys',['data'],['"'+db.conn.escape_string(lottery[2])+'"'],['server_id','name'],[str(lottery[1]),'"'+str(lottery[0])+'"'],['=','='],['AND'])
                            await ctx.send(embed = stuff.embed('успешно изменён тип награды на '+new_type,Colour.green()))

                        elif what_to_edit == 3:
                            await ctx.send(embed = stuff.embed('Введите новое/новую время/сумму  приза '))
                            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                            if len(m.content.split('.')) > 1:
                                raise Exception("Incorect input")
                            new_time_amount = int(stuff.input_to_seconds(m.content))
                            lottery = delete_all_users_from_lottery(lottery)
                            lottery[2]['prize']['amount_time'] = new_time_amount
                            lottery[2] = json.dumps(lottery[2])
                            db.update('lotterys',['data'],['"'+db.conn.escape_string(lottery[2])+'"'],['server_id','name'],[str(lottery[1]),'"'+str(lottery[0])+'"'],['=','='],['AND'])
                            await ctx.send(embed = stuff.embed('успешно изменено  время/сумма награды на '+str(new_time_amount),Colour.green()))
                        
                        elif what_to_edit == 4:
                            await ctx.send(embed = stuff.embed('Введите новое количество участников '))
                            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                            if len(m.content.split('.')) > 1:
                                raise Exception("Incorect input")
                            new_amount = int(m.content)
                            lottery = delete_all_users_from_lottery(lottery)
                            lottery[2]['required_participants'] = new_amount
                            lottery[2] = json.dumps(lottery[2])
                            db.update('lotterys',['data'],['"'+db.conn.escape_string(lottery[2])+'"'],['server_id','name'],[str(lottery[1]),'"'+str(lottery[0])+'"'],['=','='],['AND'])
                            await ctx.send(embed = stuff.embed('успешно изменено количество участников на '+str(new_amount),Colour.green()))

                        elif what_to_edit == 5:
                            await ctx.send(embed = stuff.embed('Введите новую цену участия '))
                            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                            if len(m.content.split('.')) > 1:
                                raise Exception("Incorect input")
                            new_amount = int(m.content)
                            lottery = delete_all_users_from_lottery(lottery)
                            lottery[2]['participation_price'] = new_amount
                            lottery[2] = json.dumps(lottery[2])
                            db.update('lotterys',['data'],['"'+db.conn.escape_string(lottery[2])+'"'],['server_id','name'],[str(lottery[1]),'"'+str(lottery[0])+'"'],['=','='],['AND'])
                            await ctx.send(embed = stuff.embed('успешно изменена цена участия на '+str(new_amount),Colour.green()))

                elif  selcted_type == '3':  
                    lottery[2] = json.loads(lottery[2])   
                    await ctx.send(embed = stuff.embed ('**Вы уверены что хотите удалить данную лотерею? Если да напишите "confirm", Или  "exit" если нет**',Colour.dark_grey(),emoji= ':exclamation: '))
                    m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                    if m.content.lower() == 'confirm':
                        delete_all_users_from_lottery(lottery)
                        db.delete('lotterys',['name','server_id'],['"'+lottery[0]+'"',str(lottery[1])],['=','='],['AND'])
                        await ctx.send(embed = stuff.embed('Удаление успешно',Colour.green()))
                    elif m.content.lower() == 'exit':
                        return
                    else:
                        raise Exception('Incorect input')

                else:
                    raise Exception ('Incorect input')
            #new lottery
            elif m.content == '2':
                await ctx.send(embed = stuff.embed(text='Введите название новой лотереи'))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                name = m.content


                await ctx.send(embed = stuff.embed(text='Введите стоимость участия '))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if len(m.content.split('.')) > 1: 
                    raise Exception("Incorect input")
                price = int(m.content)
                if price <=0 :
                    raise Exception("Incorect input")
                
                await ctx.send(embed = stuff.embed(text='Введите количество участников  '))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if len(m.content.split('.')) > 1: 
                    raise Exception("Incorect input")
                required_participants = int(m.content)
                if required_participants <=0 :
                    raise Exception("Incorect input")
                
                await ctx.send(embed = stuff.embed(text='Введите тип приза: "custom"(кастомная роль), "sub"(саб роль), "cash"(коины)'))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                type_of_prize =  m.content.lower()
                if type_of_prize != 'sub' and type_of_prize != 'custom' and type_of_prize != 'cash':
                    raise Exception("Incorect input")
                

                await ctx.send(embed = stuff.embed(text='Введите время/сумму приза'))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if len(m.content.split('.')) > 1: 
                    raise Exception("Incorect input")
                amount_time = stuff.input_to_seconds(m.content)
                try:
                    lottery.new_lottery(ctx,name,required_participants,price,type_of_prize,amount_time)
                except: 
                    await ctx.send('Произошла ошибка при добавлении лотереи, возможно вы ввели уже существующее имя лотереи',Colour.red())
                    return
                await ctx.send(embed = stuff.embed('Успешно добавлена новая лотерея',Colour.green()))

        except:
            await ctx.send(embed = stuff.embed('Ошибка, попробуйте сначала',Colour.red()))


@bot.command(pass_context= True)
async def command_permisions(ctx):
    from __main__ import work_with_commands
    if stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id):
        try:
            await ctx.send(embed = stuff.embed('Введите команду чьи разрешения вы хотите изменить'))
            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
            try:
                command = for_alias [m.content.lower()]
            except:
                command = m.content.lower()
            # generate list of commands
            list_of_commands = []
            for  i in work_with_commands.list_of_commands:
                for j in i:
                    list_of_commands.append(j)
            
            if command in list_of_commands:
                await ctx.send(embed = stuff.embed('1) Изменить blacklist\n 2) Изменить whitelist\n 3) Копировать настройки с другой команды'))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)

                if m.content == '1':
                    try:
                        blacklist = json.loads( ''.join(db.select(['black_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),command],['=','='],['AND'])[0]))
                    except:
                        blacklist = []


                    await ctx.send(embed = stuff.embed('blacklist:'+', '.join(['<#'+str(i)+'>' for i in blacklist])+'\n1) Добавить канал в blacklist\n 2) Удалить канал из blacklist\n'))
                    m = await stuff.command_answer_wait(ctx.channel,ctx.author)

                    if m.content == '1':
                        await ctx.send(embed = stuff.embed('Введите канал который хотите добавить:'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                        if len(m.content.split('.')) >1  :
                            raise Exception ('Incorect input')
                        channel = stuff.ping_to_id(m.content)
                        int(channel)

                        if channel in blacklist:
                            await ctx.send (embed = stuff.embed('Этот канал уже в blacklist',Colour.red()))
                            return

                        blacklist.append(channel)
                        
                        try:
                            db.insert('comands_servers_permisions',['server_id','command','black_list','white_list'],[str(ctx.guild.id),command,    db.conn.escape_string(json.dumps(blacklist)),db.conn.escape_string(json.dumps([]))])
                        except:
                            db.update('comands_servers_permisions',['black_list'],["'"+json.dumps(blacklist)+"'"],['server_id','command'],[str(ctx.guild.id),"'"+command+"'"],['=','='],['AND'])
 
                        await ctx.send(embed  = stuff.embed('Успешно добавлен канал в blacklist',Colour.green()))
                    
                    elif m.content == '2'  :
                        if len(blacklist) ==0:
                            await ctx.send(embed = stuff.embed('У данной команды и так нет ограничений',Colour.red()))
                            return

                        await ctx.send(embed = stuff.embed('Введите канал который хотите удалить из списка, напишите "all" чтобы удалить всё'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)

                        if m.content.lower() == 'all':
                            db.update('comands_servers_permisions',['black_list'],['"'+json.dumps([])+'"'],['server_id','command'],[str(ctx.guild.id),'"'+command+'"'],['=','='],['AND'])
                            await ctx.send(embed = stuff.embed('Удалены все каналы из blacklist',Colour.green()))
                            return

                        if len(m.content.split('.')) >1  :
                            raise Exception ('Incorect input')
                        channel = stuff.ping_to_id(m.content)
                        int(channel)
                        try:
                            blacklist.remove(channel)
                        except:
                            await ctx.send(embed = stuff.embed('Этот канал не находится в блэк листе',Colour.red()))
                            return

                        db.update('comands_servers_permisions',['black_list'],["'"+json.dumps(blacklist)+"'"],['server_id','command'],[str(ctx.guild.id),"'"+command+"'"],['=','='],['AND'])
                        await ctx.send(embed = stuff.embed('Канал успешно удалён из blacklist',Colour.green()))


                    else:
                        raise Exception ('Incorect input')

                elif m.content == '2':
                    try:
                        whitelist = json.loads( ''.join(db.select(['white_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),command],['=','='],['AND'])[0]))
                    except:
                        whitelist = []

                    await ctx.send(embed = stuff.embed('whitelist:'+', '.join(['<#'+str(i)+'>' for i in whitelist])+'\n1) Добавить канал в whitelist\n 2) Удалить канал из whitelist\n'))
                    m = await stuff.command_answer_wait(ctx.channel,ctx.author)

                    if m.content == '1':
                        await ctx.send(embed = stuff.embed('Введите канал который хотите добавить:'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                        if len(m.content.split('.')) >1  :
                            raise Exception ('Incorect input')
                        channel = stuff.ping_to_id(m.content)
                        int(channel)

                        if channel in whitelist:
                            await ctx.send (embed = stuff.embed('Этот канал уже в whitelist',Colour.red()))
                            return

                        whitelist.append(channel)
                        
                        try:
                            db.insert('comands_servers_permisions',['server_id','command','white_list','black_list'],[str(ctx.guild.id),command,    db.conn.escape_string(json.dumps(whitelist)),db.conn.escape_string(json.dumps([]))])
                        except:
                            db.update('comands_servers_permisions',['white_list'],["'"+json.dumps(whitelist)+"'"],['server_id','command'],[str(ctx.guild.id),"'"+command+"'"],['=','='],['AND'])
 
                        await ctx.send(embed  = stuff.embed('Успешно добавлен канал в whitelist',Colour.green()))
                    
                    elif m.content == '2'  :
                        if len(whitelist) ==0:
                            await ctx.send(embed = stuff.embed('У данной команды и так нет ограничений',Colour.red()))
                            return

                        await ctx.send(embed = stuff.embed('Введите канал который хотите удалить из списка, напишите "all" чтобы удалить всё'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)

                        if m.content.lower() == 'all':
                            db.update('comands_servers_permisions',['white_list'],['"'+json.dumps([])+'"'],['server_id','command'],[str(ctx.guild.id),'"'+command+'"'],['=','='],['AND'])
                            await ctx.send(embed = stuff.embed('Удалены все каналы из whitelist',Colour.green()))
                            return

                        if len(m.content.split('.')) >1  :
                            raise Exception ('Incorect input')
                        channel = stuff.ping_to_id(m.content)
                        int(channel)
                        try:
                            whitelist.remove(channel)
                        except:
                            await ctx.send(embed = stuff.embed('Этот канал не находится в whitelist',Colour.red()))
                            return

                        db.update('comands_servers_permisions',['white_list'],["'"+json.dumps(whitelist)+"'"],['server_id','command'],[str(ctx.guild.id),"'"+command+"'"],['=','='],['AND'])
                        await ctx.send(embed = stuff.embed('Канал успешно удалён из whitelist',Colour.green()))


                    else:
                        raise Exception ('Incorect input')
                    

                elif m.content == '3':
                    await ctx.send(embed = stuff.embed('Введите c какой команды вы хотите копировать настройки'))
                    m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                    try:
                        command1 = for_alias [m.content.lower()]
                    except:
                        command1 = m.content.lower()

                    if command1 in list_of_commands:
                        setings = [''.join(i) for i in db.select(['*'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),command1],['=','='],['AND'])[0][2::]]  #whitelist, blacklist
                        try:
                            db.insert('comands_servers_permisions',['server_id','command','white_list','black_list'],[str(ctx.guild.id),"'"+command+"'" ,"'"+setings[0]+"'","'"+setings[1]+"'"])
                        except:
                            db.update('comands_servers_permisions',['white_list','black_list'],["'"+setings[0]+"'","'"+setings[1]+"'"],['server_id','command'],[str(ctx.guild.id),"'"+command+"'"],['=','='],['AND'])
                        await ctx.send (embed = stuff.embed('Настройки успешно скопированы',Colour.green()))
                else:
                    raise Exception ('Incorect input')

            else:
                await ctx.send(embed = stuff.embed('Нет такой команды (админские команды нельзя настраивать)',Colour.red()))
        except:
            await ctx.send(embed = stuff.embed('Неправильный ввод',Colour.red()))


@bot.command(pass_context= True)
async def server_settings(ctx):
    if stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id):
        await ctx.send(embed = stuff.embed('1) Саб роль\n2) Канал для отсылки о раздачах игр'))
        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
        if m.content == '1':
            try:
                role_id = ''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)])[0])
            except:
                role_id = ''
            await ctx.send (embed  =stuff.embed('Введите новую саб роли\nСейчас id саб роли '+role_id))
            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
            role_id = stuff.ping_to_id(m.content)
            try:
                db.insert('servers_data',['sub_role_id'],[role_id])
            except:
                db.update('servers_data',['sub_role_id'],[role_id],['server_id'],[str(ctx.guild.id)],['='])
            await ctx.send(embed = stuff.embed('успешное изменение настроек',Colour.green()))
            
        elif m.content == '2':
            try:
                role_id = ''.join(db.select(['channel_to_send_game_distributions'],'servers_data',['server_id'],[str(ctx.guild.id)])[0])
            except:
                role_id = ''
            await ctx.send (embed  =stuff.embed('Введите id канала для отправки о раздачах игр\n Cейчас id: '+role_id))
            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
            role_id = stuff.ping_to_id(m.content)
            try:
                db.insert('servers_data',['channel_to_send_game_distributions'],[role_id])
            except:
                db.update('servers_data',['channel_to_send_game_distributions'],[role_id],['server_id'],[str(ctx.guild.id)],['='])
            await ctx.send(embed = stuff.embed('успешное изменение настроек',Colour.green()))
        else:
            await ctx.send(embed = stuff.embed('Ошибка ввода',Colour.red()))


@bot.command(pass_context= True)
async def shop_edit(ctx):
    try:
        if stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id):
            await ctx.send (embed = stuff.embed('1) Для создания новых товаров\n  2) Для редактирования товаров\n 3) Для удаления товаров'))
            m = await stuff.command_answer_wait(ctx.channel,ctx.author)
            
            shop_data = json.loads(db.tuple_to_array(db.select(['shop'],'servers_data',['server_id'],[str(ctx.guild.id)]))[0][0])
            
            if m.content == '1':
                await ctx.send (embed = stuff.embed('Введите тип товара ("sub"- саб роль,"cs" - кастомная роль)'))
                product_type = await stuff.command_answer_wait(ctx.channel,ctx.author)
                product_type = product_type.content.lower()
                if product_type != 'sub' and product_type != 'cs':
                    raise Exception("Incorect input")

                await ctx.send (embed = stuff.embed('Введите стоимость товара '))
                price  = await stuff.command_answer_wait(ctx.channel,ctx.author)
                price = price.content

                if len(price.split('.')) > 1 :
                    raise Exception("Incorect input")
                int(price)

                await ctx.send (embed = stuff.embed('Введите время на которое выдастся роль'))
                time_of_product  = await stuff.command_answer_wait(ctx.channel,ctx.author)
                time_of_product = stuff.input_to_seconds(time_of_product.content)

                await ctx.send(embed = stuff.embed('Введите имя товара'))
                name = await stuff.command_answer_wait(ctx.channel,ctx.author)
                name = name.content

                await ctx.send(embed = stuff.embed('Введите описание товара'))
                description = await stuff.command_answer_wait(ctx.channel,ctx.author)
                description = description.content

                shop_data = shop_commands.new_shop_product(shop_data,product_type,time_of_product,price,name,description)
                db.update('servers_data',['shop'],['"'+db.conn.escape_string(json.dumps(shop_data))+'"'],['server_id'],[str(ctx.guild.id)],['='])
                await ctx.send (embed = stuff.embed('Успешно добавлен новый товар',Colour.green()))
            
            elif m.content == '2':
                while True:
                    text = ''
                    for i in range(len(shop_data)):
                        text += str(i+1)+') '+shop_data[i]['name']+'\n'

                    await ctx.send(embed = stuff.embed('Выберите товар для редактирования \n\n'+text))
                    m = await stuff.command_answer_wait(ctx.channel,ctx.author)

                    if len(m.content.split('.')) > 1 :
                        raise Exception("Incorect input")
                    
                    what_product = int(m.content) - 1

                    if what_product > len(shop_data):
                        await ctx.send (embed = stuff.embed('Нет такого товара',Colour.red()))
                        return

                    await ctx.send(embed  = stuff.embed('Выберите что редактировать:\n\n1) Имя товара\n2) Описание товара 3) Тип товара\n4) Продолжительность выдачи \n5) Стоимость товара\n\nВведите "exit" чтобы выйти из режима редактирования ')) 
                    m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                    what_to_edit = m.content

                    if what_to_edit == '1':
                        await ctx.send(embed = stuff.embed('Введите новое имя товара'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                        shop_data[what_product]['name'] = m.content
                        await ctx.send(embed = stuff.embed ('Успешно изменено имя товара',Colour.green()))

                    elif what_to_edit =='2':
                        await ctx.send(embed = stuff.embed('Введите новое описание товара'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                        shop_data[what_product]['description'] = m.content
                        await ctx.send(embed = stuff.embed ('Успешно изменено описание товара',Colour.green()))

                    elif what_to_edit =='3':
                        await ctx.send(embed = stuff.embed('Введите новый тип товара ("cs" - кастомная роль,"sub" - саб роль'))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)

                        if m.content.lower() != 'sub' and m.content.lower() != 'cs':
                            raise Exception("Incorect input")
                        shop_data[what_product]['type'] = m.content.lower()
                        await ctx.send(embed = stuff.embed ('Успешно изменён тип товара',Colour.green()))

                    elif what_to_edit =='4':
                        await ctx.send(embed = stuff.embed('Введите новый продолжительность товара '))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                        time_of = str(stuff.input_to_seconds(m.content))
                        shop_data[what_product]['time'] = time_of
                        await ctx.send(embed = stuff.embed ('Успешно изменена продолжительность товара',Colour.green()))

                    elif what_to_edit =='5':
                        await ctx.send(embed = stuff.embed('Введите новую стоимость товара '))
                        m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                        if len(m.content.split('.')) > 1 and int(m.content) > 0 :
                            raise Exception("Incorect input")
                        
                        shop_data[what_product]['price'] = m.content
                        await ctx.send(embed = stuff.embed ('Успешно изменена стоимость товара',Colour.green()))
                    elif what_to_edit.lower() == 'exit':
                        break

                    else:
                        raise Exception ("Incorect input")

                    db.update('servers_data',['shop'],['"'+db.conn.escape_string(json.dumps(shop_data))+'"'],['server_id'],[str(ctx.guild.id)],['='])
            
            elif m.content == '3':
                text = ''
                for i in range(len(shop_data)):
                    text += str(i+1)+') '+shop_data[i]['name']+'\n'

                await ctx.send(embed = stuff.embed('Выберите товар для удаления \n\n'+text))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if len(m.content.split('.')) > 1 :
                    raise Exception("Incorect input")
                
                what_product = int(m.content) - 1

                if what_product > len(shop_data):
                    await ctx.send (embed = stuff.embed('Нет такого товара',Colour.red()))
                    return
                
                await ctx.send(embed = stuff.embed('напишите "confirm" - чтобы потдвердить удаление или "exit" - чтобы отменить удаление'))
                m = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if m.content.lower() == 'confirm':
                    shop_data.pop(what_product)
                    db.update('servers_data',['shop'],['"'+db.conn.escape_string(json.dumps(shop_data))+'"'],['server_id'],[str(ctx.guild.id)],['='])
                elif m.content.lower() == 'exit':
                    return
                else:
                    raise Exception("Incorect input")
    
    except:
        await ctx.send (embed = stuff.embed('Ошибка ввода',Colour.red()))
