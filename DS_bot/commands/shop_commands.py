import json
from discord import Colour
import discord
from discord.utils import get
import time


from __main__ import bot
from data_base import work_with_db as db
import some_stuff as stuff
import custom_roles as cs

avaible = True




def new_shop_product(previos_shop_data,type_of_product,time_in_sec,price,name,description): #type_of_product - cs or sub
    js = {
        'type': type_of_product,   
        'time': time_in_sec,
        'price': price,
        'name': name,
        'description': description
    }
    print(js)
    try:
        previos_shop_data.append(js)
        return previos_shop_data
    except:
        return [js]




    # ___________shop_____________
@bot.command(pass_context= True)
async def shop (ctx):
    shop_data = json.loads(db.tuple_to_array(db.select(['shop'],'servers_data',['server_id'],[str(ctx.guild.id)]))[0][0])
    text = bot.command_prefix+'buy id - чтобы купить товар под номером id  \n :moneybag: | Ваш баланс: '+str(db.tuple_to_int(db.select(['balance'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])[0]))+'\n\n'
    b= 1
    for i in shop_data:
        text += str(b) +') '+str(i['name'])+': ' + str(i['price']) +'\nОписание: '+i['description']+'\n\n'
        b+=1

    await ctx.send ( embed = stuff.embed(text,Colour.gold(),title=':shopping_cart: | МАГАЗИН СЕРВЕРА'))

@bot.command(pass_context= True)
async def buy(ctx, id_or_name,*args):
    shop_data = json.loads(db.tuple_to_array(db.select(['shop'],'servers_data',['server_id'],[str(ctx.guild.id)]))[0][0])

    if len (id_or_name.split('.')) >1 and (int(id_or_name) > len(shop_data) or int(id_or_name)<0): #check that have integer not float
        raise Exception("Just to  broke ")
    id_or_name = int(id_or_name)-1


    if stuff.check_that_you_have_enough_money(ctx.guild.id,ctx.author.id,shop_data[id_or_name]['price']):
        # check that user already has custom role
        if shop_data[id_or_name]['type'] == "cs":# custom roles
            if not cs.check_that_user_have_custom_role(ctx.guild.id,ctx.author.id):                
                colour=Colour.light_grey()
                name = str(ctx.author)
                
                role = await ctx.guild.create_role(colour = colour , name= name)
                await ctx.author.add_roles(role)
                t= time.time()
                db.update('servers_user_data',['balance','money_spent_all_time','amount_of_bought_products','money_spent_in_shop'],['balance - '+str(shop_data[id_or_name]['price']),'money_spent_all_time+'+str(shop_data[id_or_name]['price']),'amount_of_bought_products+1','money_spent_in_shop+'+str(shop_data[id_or_name]['price'])],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
                db.insert('custom_roles',["server_id",'user_id',"role_id","role_time_to_delete_from_user",'time_to_delete_role'],[str(ctx.guild.id),str(ctx.author.id),str(role.id),str(int(t)+int(shop_data[id_or_name]['time'])),str(int(t)+int(shop_data[id_or_name]['time']))])
                await ctx.send (embed = stuff.embed('Покупка совершена успешно',Colour.green()))
            else: 
                await ctx.send(embed = stuff.embed('У вас уже есть кастомная роль',Colour.red()))

        if shop_data [id_or_name] ['type'] == "sub":
            sub_role_id = ''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(ctx.guild.id)],['='])[0])
            if int(sub_role_id) in [i.id for i in ctx.author.roles]: # check that user have sub role  
                await ctx.send(embed = stuff.embed('У вас уже есть роль саба',Colour.red()))
            else:
                role = get(ctx.guild.roles, id = int(sub_role_id)) 
                await ctx.author.add_roles(role)
                t= time.time()
                db.update('servers_user_data',['balance','money_spent_all_time','amount_of_bought_products','money_spent_in_shop'],['balance - '+str(shop_data[id_or_name]['price']),'money_spent_all_time+'+str(shop_data[id_or_name]['price']),'amount_of_bought_products+1','money_spent_in_shop+'+str(shop_data[id_or_name]['price'])],['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND'])
                db.insert('custom_roles',["server_id",'user_id',"role_id","role_time_to_delete_from_user"],[str(ctx.guild.id),str(ctx.author.id),str(role.id),str(int(t)+int(shop_data[id_or_name]['time']))])
                await ctx.send (embed = stuff.embed('Покупка совершена успешно',Colour.green()))
    else:
        await ctx.send(embed = stuff.embed('У вас нет столько коинов',Colour.red()))

