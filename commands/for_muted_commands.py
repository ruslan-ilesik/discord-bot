import random
import time

from __main__ import *
import data_base.work_with_db as db
import some_stuff as stuff

avaible = True

#____________for muted commands______________________________
@bot.command(pass_context= True)
async def work_help(ctx):
    if avaible:
        a=  json.loads(''.join(db.select(['work_chanel_ids'],'servers_data',['server_id'],[str(ctx.guild.id)],[' = '],[])[0])) 
        #print(a)
        #print(ctx.channel.id)
        for i in a:
            if ctx.channel.id == i :
            #await ctx.send('В разроботке. а пока сосите бебру')
                await  ctx.send (embed = stuff.embed('чтобы посмотреть сколько вам осталось заданий напишите +tasks_left, что бы получить задание напишите +task_give',Colour.dark_grey()))

@bot.command(pass_context= True)
async def tasks_left(ctx):
    if avaible:
        left = str(db.tuple_to_int(db.select(['amount_of_captcha'],'users_in_mute',['server_id','user_id'],[str(ctx.guild.id), str(ctx.author.id)],['=','='],['AND'])[0]))
        await ctx.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> тебе осталось пройти '+str(left)+' заданий',Colour.dark_grey()))



@bot.command(pass_context= True)
async def task_give(ctx):   
    delay =   time.time() - db.tuple_to_int(db.select(['last_answer_time'],'users_in_mute',['user_id','server_id'],[str(ctx.author.id),str(ctx.guild.id)],['=','='],['AND'])[0])
    time_to_wait  = db.tuple_to_int(db.select(['mute_messages_delay_in_seconds'],'servers_data',['server_id'],[str(ctx.guild.id)],['='],[])[0])
    if delay < time_to_wait: # check that last task was enough time ago
        await ctx.send('вы недавно проходили задание. Вам нужно подождать ещё '+ str( int(time_to_wait - delay))+' секунд')
        return
    symbols = {'*':['*','умножить на '],'/':['/','делить на ','поделить на','разделить на'],'+':['+','прибавить','добавить','плюс'],'-':['-','отнять','минус']}
    a = random.choice(['*',"-",'/','+'])
    # create task and check that it correct
    while True: 
        try:
            first_val = str(random.randint(0,10))
            second_val  = str(random.randint(0,10))
            asnwer = eval( first_val + a + second_val)
            if asnwer % 1 == 0:
                break
        except:
            continue
    await ctx.send(embed = stuff.embed( 'напишите результат выражения: '+first_val+' '+ symbols[a][random.randint(0,len(symbols[a])-1)] + ' '+second_val,Colour.dark_grey()))
    db.update('users_in_mute',['last_answer_time'],[str(int(time.time()))],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
    channel = ctx.channel
    author = ctx.author
    msg = await stuff.command_answer_wait(channel,author)
    if  str(msg.content)  == str(asnwer):
        await msg.channel.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> выполнено успешно',Colour.green()))
        db.update('users_in_mute',['amount_of_captcha'],['amount_of_captcha-1'],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
        # check that user can go out of mute
        user_captcha_left = db.tuple_to_int(db.select(['amount_of_captcha'],'users_in_mute',['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])[0])
        if user_captcha_left <= 0:
            user = get(bot.get_all_members(), id=int(ctx.author.id),guild = ctx.guild)
            role = get(ctx.guild.roles, id = int(db.tuple_to_int(db.select(['mute_role_id'],'servers_data',['server_id'],[ctx.guild.id],['='],[])[0])))
            print('user: ',user,' come out of the mute')
            await user.remove_roles(role)
    else:
        await msg.channel.send(embed = stuff.embed('<@'+str(ctx.author.id)+'> неправильный ответ',Colour.red()))
