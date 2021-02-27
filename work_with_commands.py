import sys
import json
from inspect import getmembers, isfunction

from __main__ import *
import commands.custom_roles_commands as custom_roles_commands
import commands.fun_commands.fun_comands as fun_comands
import commands.admin_and_owner_commands as admin_and_owner_commands
import commands.for_muted_commands as for_muted_commands
import commands.shop_commands as shop_commands
import commands.balance_commands as balance_commands
import commands.other_commands as other_commands
import some_stuff as stuff
import commands.fun_commands.lottery_commands as lottery_commands
#[o for o in getmembers(my_module) if isfunction(o[1])]

blocked_commands = []


list_of_commands = []
list_of_commands.append( list(stuff.methods_with_decorator(custom_roles_commands)))
list_of_commands.append(list(stuff.methods_with_decorator(fun_comands)))
list_of_commands.append(list(stuff.methods_with_decorator(for_muted_commands)))
list_of_commands.append(list(stuff.methods_with_decorator(shop_commands)))
list_of_commands.append(list(stuff.methods_with_decorator(balance_commands)))
list_of_commands.append(list(stuff.methods_with_decorator(other_commands)))
list_of_commands.append(list(stuff.methods_with_decorator(lottery_commands)))







@bot.command(pass_context= True)
async def enable_category(ctx,directory):
    def delete_from_blocked(val):
        global blocked_commands
        for i in val:
            if i in blocked_commands:
                blocked_commands.remove(i)


    if stuff.is_creator(ctx.author.id):
        await ctx.message.delete()

        if directory == 'custom_roles' or directory == 'cs':
            delete_from_blocked(list(stuff.methods_with_decorator(custom_roles_commands)))
            await ctx.author.send(embed  = stuff.embed('custom_roles_commands enabled',Colour.green()))
        
        elif directory == 'fun' :
            delete_from_blocked(list(stuff.methods_with_decorator(fun_comands)))
            delete_from_blocked(list(stuff.methods_with_decorator(lottery_commands)))
            await ctx.author.send(embed  = stuff.embed('fun_comands enabled',Colour.green()))

        elif directory == 'admin' or directory == 'owner' :
            delete_from_blocked(list(stuff.methods_with_decorator(admin_and_owner_commands)))
            await ctx.author.send(embed  = stuff.embed('admin_and_owner_commands enabled',Colour.green()))
        
        elif directory == 'muted' or directory == 'mute' :
            delete_from_blocked(list(stuff.methods_with_decorator(for_muted_commands)))
            await ctx.author.send(embed  = stuff.embed('for_muted_commands enabled',Colour.green()))    

        elif directory == 'shop' :
            delete_from_blocked(list(stuff.methods_with_decorator(shop_commands)))
            await ctx.author.send(embed  = stuff.embed('shop_commands enabled',Colour.green()))

        elif directory == 'balance' :
            delete_from_blocked(list(stuff.methods_with_decorator(balance_commands)))
            await ctx.author.send(embed  = stuff.embed('balance_commands enabled',Colour.green()))

        elif directory == 'other' :
            delete_from_blocked(list(stuff.methods_with_decorator(other_commands)))
            await ctx.author.send(embed  = stuff.embed('other_commands enabled',Colour.green()))

        elif directory == 'all':
            delete_from_blocked(list(stuff.methods_with_decorator(custom_roles_commands)))
            delete_from_blocked(list(stuff.methods_with_decorator(fun_comands)))
            delete_from_blocked(list(stuff.methods_with_decorator(lottery_commands)))
            delete_from_blocked(list(stuff.methods_with_decorator(admin_and_owner_commands)))
            delete_from_blocked(list(stuff.methods_with_decorator(for_muted_commands)))
            delete_from_blocked(list(stuff.methods_with_decorator(shop_commands)))
            delete_from_blocked(list(stuff.methods_with_decorator(balance_commands)))
            delete_from_blocked(list(stuff.methods_with_decorator(other_commands)))
            await ctx.author.send(embed  = stuff.embed('all_commands enabled',Colour.green()))
        
        else:
            await ctx.author.send(embed  = stuff.embed('unknown what to enable',Colour.red()))

@bot.command(pass_context= True)
async def disable_category(ctx,directory):
    def add_to_blocked(val):
        global blocked_commands
        for i in val:
            if not  i in blocked_commands:
                blocked_commands.append(i)
    if stuff.is_creator(ctx.author.id):
        await ctx.message.delete()

        if directory == 'custom_roles' or directory == 'cs':
            add_to_blocked(list(stuff.methods_with_decorator(custom_roles_commands)))
            await ctx.author.send(embed  = stuff.embed('custom_roles_commands disabled',Colour.green()))
        
        elif directory == 'fun' :
            add_to_blocked(list(stuff.methods_with_decorator(fun_comands)))
            await ctx.author.send(embed  = stuff.embed('fun_comands disabled',Colour.green()))

        elif directory == 'admin' or directory == 'owner' :
            add_to_blocked(list(stuff.methods_with_decorator(admin_and_owner_commands)))
            await ctx.author.send(embed  = stuff.embed('admin_and_owner_commands disabled',Colour.green()))
        
        elif directory == 'muted' or directory == 'mute' :
            add_to_blocked(list(stuff.methods_with_decorator(for_muted_commands)))
            await ctx.author.send(embed  = stuff.embed('for_muted_commands disabled',Colour.green()))    

        elif directory == 'shop' :
            add_to_blocked(list(stuff.methods_with_decorator(shop_commands)))
            await ctx.author.send(embed  = stuff.embed('shop_commands disabled',Colour.green()))

        elif directory == 'balance' :
            add_to_blocked(list(stuff.methods_with_decorator(balance_commands)))
            await ctx.author.send(embed  = stuff.embed('balance_commands disabled',Colour.green()))

        elif directory == 'other' :
            add_to_blocked(list(stuff.methods_with_decorator(other_commands)))
            await ctx.author.send(embed  = stuff.embed('other_commands disabled',Colour.green()))

        elif directory == 'all':
            add_to_blocked(list(stuff.methods_with_decorator(custom_roles_commands)))
            add_to_blocked(list(stuff.methods_with_decorator(fun_comands)))
            add_to_blocked(list(stuff.methods_with_decorator(admin_and_owner_commands)))
            add_to_blocked(list(stuff.methods_with_decorator(for_muted_commands)))
            add_to_blocked(list(stuff.methods_with_decorator(shop_commands)))
            add_to_blocked(list(stuff.methods_with_decorator(balance_commands)))
            add_to_blocked(list(stuff.methods_with_decorator(other_commands)))
            await ctx.author.send(embed  = stuff.embed('all_commands disabled',Colour.green()))
        
        else:
            await ctx.author.send(embed  = stuff.embed('unknown what to disable',Colour.red()))



@bot.command(pass_context= True)
async def disable_command(ctx,*args):
    global blocked_commands
    com = ''
    try:    #check that its not alias of command and get standart name of command if it not
        com = for_alias[args[0]]
    except:
        com = args[0]
    if stuff.is_creator(ctx.author.id):
        #await ctx.message.delete()
        if com in blocked_commands:
            await ctx.author.send(embed = stuff.embed("Command already disabled",Colour.red(),'',':x:'))
        else:
            blocked_commands.append(com)
            await ctx.author.send(embed = stuff.embed("Command "+com+" disabled",Colour.green(),'',':white_check_mark: '))


@bot.command(pass_context= True)
async def enable_command(ctx,*args):
    global blocked_commands
    if stuff.is_creator(ctx.author.id):
        await ctx.message.delete()
        if not args[0] in blocked_commands:
            await ctx.author.send(embed = stuff.embed("Command not disable",Colour.red(),'',':x:'))
        else:
            blocked_commands.remove(args[0])
            await ctx.author.send(embed = stuff.embed("Command "+args[0]+" enabled",Colour.green(),'',':white_check_mark: '))

@bot.command(pass_context= True)
async def show_disabled_commands(ctx):
    global blocked_commands
    if stuff.is_creator(ctx.author.id):
        await ctx.author.send(embed = stuff.embed(', '.join(blocked_commands),emoji=':eye: '))


@bot.command(pass_context= True)
async def fast_backup(ctx):
    if stuff.is_creator(ctx.author.id):
        db_backup.backup_db()
        await db_backup.send_backup()

def is_command_avaible(ctx,*args):
    global blocked_commands
   
    if ctx.content[0] == bot.command_prefix:
        try: #check that its not alias of command and get standart name of command if it 
            com = for_alias [ctx.content.split(' ')[0][1::]]
        except:
            com = ctx.content.split(' ')[0][1::]
        if not com in blocked_commands:
            #chanel check
            try:    
                black_list =  json.loads(''.join(db.select(['black_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),com],['=','='],['AND'])[0]))
                if len(black_list) == 0 :
                    white_list = json.loads(''.join(db.select(['white_list'],'comands_servers_permisions',['server_id','command'],[str(ctx.guild.id),com],['=','='],['AND'])[0]))
                    if len(white_list) == 0:
                        return True
                    
                    else:
                        if str(ctx.channel.id) in white_list:
                            return True
                        else:
                            return False
                else:
                    if not str(ctx.channel.id)  in black_list:
                        return True
                    else:
                        return False
            except:
                return True
        else:
            return False    






