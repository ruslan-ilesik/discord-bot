import data_base.work_with_db as db
from discord import Colour
from discord.utils import get
import discord


import some_stuff as stuff

def get_custom_role(server_id,user_id):
    try:
        sub_role = ''.join(db.select(['sub_role_id'],'servers_data',['server_id'],[str(server_id)],['='])[0])
    except:
        sub_role ='-1'
    return db.select(['role_id'],'custom_roles',['server_id','user_id','role_id'],[str(server_id),str(user_id),sub_role],['=','=','!='],['AND','AND'])

def check_that_user_have_custom_role(server_id,user_id):
    if len(get_custom_role(server_id,user_id)) == 0:
        return False
    else:
        return True
        

async def edit_custom_role_color(ctx,color):
    global role
    role_id = get_custom_role(ctx.guild.id,ctx.author.id)
    role = get(ctx.guild.roles, id = int(db.tuple_to_int(role_id[0]))) 
    await role.edit(color = discord.Color(value=int('0x'+color[1::], 16)), reason="")
    await ctx.channel.send(embed = stuff.embed('Успешно изменён цвет роли',Colour.green()))  

async def edit_custom_role_name(ctx,name):
    global role
    role_id = get_custom_role(ctx.guild.id,ctx.author.id)
    role = get(ctx.guild.roles, id = int(db.tuple_to_int(role_id[0]))) 
    await role.edit(name = name, reason="")
    await ctx.channel.send(embed = stuff.embed('Успешно изменено название роли',Colour.green()))

async def edit_custom_role_mention(ctx,what):
    global role
    role_id = get_custom_role(ctx.guild.id,ctx.author.id)
    role = get(ctx.guild.roles, id = int(db.tuple_to_int(role_id[0]))) 
    await role.edit(mentioned  = what, reason="")
    await ctx.channel.send(embed = stuff.embed('Успешно изменена пингабельность роли на: '+str(what),Colour.green()))

async def edit_custom_role_visibility(ctx,is_visible):
    global role
    role_id = get_custom_role(ctx.guild.id,ctx.author.id)
    role = get(ctx.guild.roles, id = int(db.tuple_to_int(role_id[0]))) 

    if is_visible:
        await ctx.guild.get_role(role.id).edit(position=ctx.author.top_role.position+1)
    else:
        await ctx.guild.get_role(role.id).edit(position=1)
    await ctx.channel.send(embed = stuff.embed('Успешно изменена видимость цвета роли на: '+str(is_visible),Colour.green()))

