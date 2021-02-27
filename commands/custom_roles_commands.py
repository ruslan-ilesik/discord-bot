from __main__ import tasks,Colour,bot
import time
import datetime

import some_stuff as stuff
import custom_roles as cs
import data_base.work_with_db as db
avaible = True
#___________________________custom roles____________________________



@bot.command(pass_context= True,aliases=['sub_check','check_sub','subscriptions_check'])
async def check_subscriptions( ctx, *args ): 

    if len(args) == 0:
        bought_roles_data = db.tuple_to_array(db.select(['role_id'],"custom_roles",['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND']))
        a =db.tuple_to_array(db.select(['role_time_to_delete_from_user'],"custom_roles",['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND']))
        for i in range (len(a)):
            bought_roles_data[i].append(a[i][0])


        sub_role_id = ''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0])
        sub_role_time_to_delete = -1
        custom_role_time_to_delete = -1
        text = ''
        for i in bought_roles_data:

            if int(i[0]) == int(sub_role_id):
                sub_role_time_to_delete = i[1]
            else:
                custom_role_time_to_delete = i[1]
        t = time.time()
        
        if int(sub_role_time_to_delete) > -1:
            sub_role_time_left = t - int(sub_role_time_to_delete) 
            sub_role_time_left = str(datetime.timedelta(seconds= - int(sub_role_time_left)))
            text += 'До окончания саб роли осталось: ' + str(sub_role_time_left.replace('days','дней'))
            text+= '\n\n'
        
        if int(custom_role_time_to_delete) >-1:
            custom_role_time_left = t - int(custom_role_time_to_delete)   
            custom_role_time_left = str(datetime.timedelta(seconds= - int(custom_role_time_left)))
            text += 'До окончания кастомной роли осталось: ' + str(custom_role_time_left.replace('days','дней'))
            text+= '\n\n'
        if text != '':
            await ctx.send(embed = stuff.embed(text,Colour.gold(),':notebook_with_decorative_cover:| Ваши подписки'))
        else:
            await ctx.send(embed = stuff.embed("У вас нет активных подписок, вы можете купить их в магазине (+shop)",Colour.red()))


            #check some one subscriptions (can do only moders and higer)
    elif stuff.is_creator(ctx.author.id) or stuff.is_bot_server_admin(ctx.author.id,ctx.guild.id) or stuff.is_bot_server_moderator(ctx.author.id,ctx.guild.id):
        
        for_who = ''.join(args[0]).lower()
        for_who = stuff.ping_to_id(for_who)
        bought_roles_data = db.tuple_to_array(db.select(['role_id'],"custom_roles",['server_id','user_id'],[str(ctx.guild.id),for_who],['=','='],['AND']))
        a =db.tuple_to_array(db.select(['role_time_to_delete_from_user'],"custom_roles",['server_id','user_id'],[str(ctx.guild.id),for_who],['=','='],['AND']))
        for i in range (len(a)):
            bought_roles_data[i].append(a[i][0])


        sub_role_id = ''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0])
        sub_role_time_to_delete = -1
        custom_role_time_to_delete = -1
        text = ''
        for i in bought_roles_data:

            if int(i[0]) == int(sub_role_id):
                sub_role_time_to_delete = i[1]
            else:
                custom_role_time_to_delete = i[1]
        t = time.time()
        
        if int(sub_role_time_to_delete) > -1:
            sub_role_time_left = t - int(sub_role_time_to_delete) 
            sub_role_time_left = stuff.age_count(sub_role_time_left)
            text += 'До окончания саб роли осталось:' + str(sub_role_time_left[0]) +' дней, '
            for i in sub_role_time_left[1::]:
                text +=  str(i)+': '
            text+= '\n\n'
        
        if int(custom_role_time_to_delete) >-1:
            custom_role_time_left = t - int(custom_role_time_to_delete)   
            custom_role_time_left = stuff.age_count(custom_role_time_left)
            text += 'До окончания кастомной роли осталось:' + str(custom_role_time_left[0]) +' дней, '
            for i in custom_role_time_left[1::]:
                text+= str(i)+':'
            text+= '\n\n'
        if text != '':
            await ctx.send(embed = stuff.embed(text,Colour.gold(),':notebook_with_decorative_cover: | Подписки запрошенгого пользователя'))
        else:
            await ctx.send(embed = stuff.embed("У пользователя нет активных подписок",Colour.red()))



@bot.command(pass_context= True,aliases=['edit_cs','cs_edit','custom_role_edit'])
async def edit_custom_role( ctx,*args ):  
    async def what_edit_check(what,*args):
        if what == '1' or what.lower() == 'color':#color editing
            async def edit_color(color):
                try:
                    await cs.edit_custom_role_color(ctx,''.join(color))
                except:
                    await ctx.channel.send(embed = stuff.embed('Ошибка, попробуйте сначала', Colour.red()))
                
            if args[0]:
                await edit_color(args[0])                    
            else:                   
                await ctx.channel.send (embed = stuff.embed(':notebook_with_decorative_cover: | Введите новый цвет роли в палитре HEX пример: #00BFFF'))    
                msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
                await edit_color(msg.content.split(' ')[0])

        elif what == '2' or what.lower() == 'name':
            async def edit_name(name):
                try:
                    await cs.edit_custom_role_name(ctx,name)
                except:
                    await ctx.channel.send(embed = stuff.embed('Ошибка, попробуйте сначала', Colour.red())) 

            if args[0]:
                await edit_name([' '.join(i) for i in args][0])
            else:                 
                await ctx.channel.send (embed = stuff.embed(':notebook_with_decorative_cover: | введите новое имя роли'))    
                msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
                await edit_name(msg.content)

        elif what == '3' or what.lower() == 'mention':
            async def mention_edit(to_what):
                try:
                    await cs.edit_custom_role_mention(ctx,to_what)
                except:
                    await ctx.channel.send(embed = stuff.embed('Ошибка, попробуйте сначала', Colour.red()))

            if args[0]:
                if ''.join(args[0]).lower() == 'true' or ''.join(args[0]) == '1':
                    await mention_edit(True) 
                elif  ''.join(args[0]).lower() == 'false' or ''.join(args[0]) == '0':
                    await mention_edit(False)  
                else:
                    await ctx.channel.send(embed = stuff.embed('Ошибка, попробуйте сначала', Colour.red()))
            else:                 
                await ctx.channel.send (embed = stuff.embed(':notebook_with_decorative_cover: | Введите "true" или "1" чтобы сделать роль пингабельной, а также "false" или "0" чтобы непингабельной соответствено'))    
                msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if msg.content.lower() == 'true' or msg.content == '1':
                    await mention_edit(True) 
                elif  msg.content.lower() == 'false' or msg.content == '0':
                    await mention_edit(False)  
                else:
                    await ctx.channel.send(embed = stuff.embed('Ошибка, попробуйте сначала', Colour.red()))

        elif what == '4' or what.lower() == 'visibility':
            async def visibility_edit(to_what):
                try:
                    await cs.edit_custom_role_visibility(ctx,to_what)
                except:
                    await ctx.channel.send(embed = stuff.embed('Ошибка, попробуйте сначала', Colour.red())) 
            if args[0]:
                if ''.join(args[0]).lower() == 'true' or ''.join(args[0]) == '1':
                   await visibility_edit(True)

                elif  ''.join(args[0]).lower() == 'false' or ''.join(args[0]) == '0':
                    await visibility_edit(False) 
            else:
                await ctx.channel.send (embed = stuff.embed(':notebook_with_decorative_cover: | Введите "1" или "true" чтобы сделать цвет роли видимым , а также "false" или "0" чтобы сделать роль цвета невидимой соответствено'))    
                msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
                if msg.content.lower() == 'true' or msg.content == '1':
                    await visibility_edit(True) 
                elif  msg.content.lower() == 'false' or msg.content == '0':
                    await visibility_edit(False)  
                else:
                    await ctx.channel.send(embed = stuff.embed('Ошибка, попробуйте сначала', Colour.red()))



    if cs.check_that_user_have_custom_role(ctx.guild.id,ctx.author.id):
        if len(args) > 0:
            await what_edit_check(args[0],args[1::])

        else:#ask what edit
            await ctx.send(embed = stuff.embed('1) Для редактирования цвета напишите "color" или "1"\n2) Для редактирования названия роли  введите "name" или "2"\n3) Для изминения пингабельности напишите "mention" или "3"\n4) Для изменения видимости цвета роли напишите "visibility" или "4"'))
            msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
            msg = msg.content.split(' ')
            await what_edit_check(msg[0],msg[1::])

    else:#no custom_role
        await ctx.send(embed = stuff.embed('У вас нет кастомной роли, вы можете купить её в магазине сервера ( +shop )',Colour.red()))
        
