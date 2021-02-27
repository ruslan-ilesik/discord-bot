import discord
from discord.ext import commands
from discord.utils import get
from discord import Colour
import time

from __main__ import bot, use_shop
import some_stuff as stuff
import data_base.work_with_db as db

avaible = True
#_______________everyone commands___________________________
@bot.command(pass_context= True) 
async def help(ctx,*args):
    if avaible:
        if len(args) == 0:
            emb = discord.Embed(title=":robot: | Помощник", description="**+help id категории** \n", color=Colour.gold())
            emb.add_field(name="1) развлечения", value="**hug, slap, casino, change_sex, lottery**", inline=False)
            emb.add_field(name="2) магазин и покупки", value="**shop , buy**", inline=False)
            emb.add_field(name="3) коины", value="**balance, transfer**", inline=False)
            emb.add_field(name="4) роли", value="**edit_custom_role, check_subscriptions**", inline=False)
            emb.add_field(name="5) остальное", value="**info, ping, stats**", inline=False)
            await ctx.send(embed  = emb)
        else:
            if args[0] == '1':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория развлечения \n", color=Colour.gold())
                emb.add_field(name="hug - обнять пользователя ", value="ПРИНИМАЕТ: id или пинг пользователя которого вы хотите обнять, стоимость "+ str(use_shop['hug']), inline=False)
                emb.add_field(name="slap - дать ляща пользователю ", value="ПРИНИМАЕТ: id или пинг пользователя которому вы хотиту дать лящ, стоимость "+ str(use_shop['kick']), inline=False)
                emb.add_field(name="casino - проверьте вашу удачу сделав ставку ", value="ПРИНИМАЕТ: amount - размер ставки, обязательно целое число больше 0", inline=False)
                emb.add_field(name="change_sex - сменить пол", value='ПРИНИМАЕТ: значение men или women', inline=False)
                emb.add_field(name="lottery  - показывает доступные лотереи на сервере   ", value=" возращает список лотерей", inline=False)
                await ctx.send(embed  = emb)
            
            elif args[0] == '2':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория магазин и покупки \n", color=Colour.gold())
                emb.add_field(name="shop  - магазин  ", value="Выводит список товаров ", inline=False)
                emb.add_field(name="buy  - купить   ", value="ПРИНИМАЕТ: id товара из магазина, совершает покупку ", inline=False)
                await ctx.send(embed  = emb)
        
            elif args[0] == '3':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория коины \n", color=Colour.gold())
                emb.add_field(name="balance  - баланс  ", value="ПРИНИМАЕТ: id пользователя чей баланс вы хотите посмотреть, если не передали ничего то выведится ваш баланс", inline=False)
                emb.add_field(name="transfer  - перевести деньги   ", value="ПРИНИМАЕТ: id или пинг пользователя которому вы хотите перевести коины, а также сумму которую вы хотите перевести , переводит деньги с одного кошелька на другой ", inline=False)
                await ctx.send(embed  = emb)
                    
            elif args[0] == '4':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория роли \n", color=Colour.gold())
                emb.add_field(name="edit_custom_role  - редактирование кастомной роли  ", value="Редактирует кастомную роль, купить можно в магазине", inline=False)
                emb.add_field(name="check_subscriptions  - проверить статус кастомной/саб ролей   ", value="Выводит остаток времени вашей кастомной роли и сабки если они у вас есть  ", inline=False)
                await ctx.send(embed  = emb)
            
            elif args[0] == '5':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория остальное \n", color=Colour.gold())
                emb.add_field(name="info  - информация о боте   ", value="Возращает немного информации о боте", inline=False)
                emb.add_field(name="ping  - проверить задержку с ботом ", value="Выводит задержку в сообщениях в милисикундах  ", inline=False)
                emb.add_field(name="stats  - немного вашей статистики ", value="Выводит вашу статистику на этом сервере  ", inline=False)
                await ctx.send(embed  = emb)

            else:
                await ctx.send(embed = stuff.embed("Не найден id категории о которой вы спрашиваете",Colour.red(),'Помощник'))



@bot.command(pass_context= True) 
async def info(ctx):
    if avaible:
        await ctx.send(embed = stuff.embed('Бот написан на python3.8.5 пользователем ilesik#0358. Если имеете вопросы пишите мне в личные  сообщения\n\n Отдельная благодарность пользователю Raizyr#1337 за помощь',emoji=':wheelchair: '))


@bot.command(pass_context= True)
async def ping(ctx):
    if avaible:
        t = time.time()
        m =await ctx.send(embed = stuff.embed('pong 🏓',Colour.dark_grey()))
        await m.edit( embed = stuff.embed('ping: '+ str(int((time.time() - t )*1000))+' ms',Colour.blue(),emoji=':ping_pong: '))


@bot.command(pass_context= True)
async def stats(ctx):
    if avaible:
        all_user_data  = db.tuple_to_array(db.select(['*'],'servers_user_data',['server_id','user_id'],[str(ctx.guild.id),str(ctx.author.id)],['=','='],['AND']))[0][4::] # [kicks_give,kicks_take,hugs_give,hugs_take,money_spent_all_time,casino_times_played,casino_win_times,casino_lose_times,casino_money_win,casino_money_lose,transfer_money_give_at_all,transfer_money_take_at_all,transfer_give_times,transfer_take_times, amount_of_bought_products, money_spent_in_shop,is_female,money_spent_in_lottery,lottery_played_times,lottery_win_times,lottery_lose_times]
        #print(all_user_data)
        emb = discord.Embed(title=":scroll: | Статистика", description="ваша статистика на этом сервере \n", color=Colour.gold())
        emb.add_field(name=":peace: | Удары/обнимашки", value="Вы ударили других пользователей "+str(all_user_data[0])+" раз \nВы были ударены другими пользователями "+str(all_user_data[1])+' раз \nВы обняли других пользователей '+str(all_user_data[2])+' раз \nВы были обняты другими пользователями '+str(all_user_data[3])+' раз\n', inline=False)
        emb.add_field(name = ":slot_machine: | Казино",value = 'Вы сыграли в казино '+str(all_user_data[5])+' раз\nВы выиграли в казино '+str(all_user_data[6])+' раз\nВы проиграли в казино '+str(all_user_data[7])+' раз\nВаши выигрыши в сумме составляют '+str(all_user_data[8])+" коинов\nВаш проигрыши в сумме составляют "+str(all_user_data[9])+' коинов\n',inline=False)
        emb.add_field(name = ':moneybag: | Коины', value = 'За всё время вы реализовали '+str(all_user_data[4])+ ' коинов\nВы передали другим пользователям '+str(all_user_data[10])+' коинов\nВам перечислили '+str(all_user_data[11])+' коинов\nВы перечсляли коины '+str(all_user_data[12])+' раз\nВы получали коины '+str(all_user_data[13])+' раз\n',inline=False)
        emb.add_field(name = ':shopping_cart: | Магазин и покупки', value = 'За всё время вы купили  '+str(all_user_data[14])+ ' товаров\nВы потратили '+str(all_user_data[15])+' коинов на покупки\n',inline=False)
        emb.add_field(name = ':game_die: | Лотереи', value = 'За всё время вы потратили  '+str(all_user_data[17])+ ' коинов на участие\nВы участвовали '+str(all_user_data[18])+' раз\nВы выиграли '+str(all_user_data[19])+' раз\nВы проиграли '+str(all_user_data[20])+' раз\n',inline=False)
        await ctx.send(embed = emb)

