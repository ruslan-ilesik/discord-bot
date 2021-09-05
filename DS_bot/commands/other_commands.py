import asyncio
from operator import pos
from os import path
import re
import discord
from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get
from discord import Colour
from discord_components import DiscordComponents, Button, ButtonStyle
from discord_components import component
from discord_components.component import Component
import requests
import json
import random
import time
import html
import tic_tac_toe as ttt
import chess as ch
from PIL import Image, ImageDraw
import io

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
            emb.add_field(name="5) остальное", value="**info, ping, stats, question, tic_tac_toe,chess**", inline=False)
            await ctx.send(embed  = emb)
        else:
            if args[0] == '1':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория развлечения \n", color=Colour.gold())
                emb.add_field(name="hug - обнять пользователя ", value="Принимает: id или пинг пользователя которого вы хотите обнять, стоимость "+ str(use_shop['hug']), inline=False)
                emb.add_field(name="slap - дать ляща пользователю ", value="Принимает: id или пинг пользователя которому вы хотиту дать лящ, стоимость "+ str(use_shop['kick']), inline=False)
                emb.add_field(name="casino - проверьте вашу удачу сделав ставку ", value="Принимает: amount - размер ставки, обязательно целое число больше 0", inline=False)
                emb.add_field(name="change_sex - сменить пол", value='Принимает: значение men или women', inline=False)
                emb.add_field(name="lottery  - показывает доступные лотереи на сервере   ", value=" возращает список лотерей", inline=False)
                await ctx.send(embed  = emb)
            
            elif args[0] == '2':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория магазин и покупки \n", color=Colour.gold())
                emb.add_field(name="shop  - магазин  ", value="Выводит список товаров ", inline=False)
                emb.add_field(name="buy  - купить   ", value="Принимает: id товара из магазина, совершает покупку ", inline=False)
                await ctx.send(embed  = emb)
        
            elif args[0] == '3':
                emb = discord.Embed(title=":robot: | Помощник", description="Категория коины \n", color=Colour.gold())
                emb.add_field(name="balance  - баланс  ", value="Принимает: id пользователя чей баланс вы хотите посмотреть, если не передали ничего то выведится ваш баланс", inline=False)
                emb.add_field(name="transfer  - перевести деньги   ", value="Принимает: id или пинг пользователя которому вы хотите перевести коины, а также сумму которую вы хотите перевести , переводит деньги с одного кошелька на другой ", inline=False)
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
                emb.add_field(name="question  - случайный вопрос ", value="Выводит случайнный вопрос, и варианты отвeта на него. Cможете ответить правильно?", inline=False)
                emb.add_field(name="tic_tac_toe  - игра в крестики нолики с ботом ", value="Выводит случайнный вопрос, и варианты отвeта на него. Cможете ответить правильно?", inline=False)
                emb.add_field(name="chess  - игра в шахматы с ботом ", value="выводит игровое поле и кнопки взаимодейтвия (ориентир по кординатам на краю поля)", inline=False)
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
async def question(ctx):
    from __main__ import bot
    question = json.loads(requests.get('https://opentdb.com/api.php?amount=1').text)['results']
    if len(question) == 0:
        question = json.loads(requests.get('https://opentdb.com/api.php?amount=1').text)['results']
        if len(question) == 0 :
            await ctx.send(embed = stuff.embed('Error to get a question for you',Colour.red()))
            return
    question = question[0]
    question['question'] = html.unescape(question['question'])
    question['correct_answer'] = html.unescape(question['correct_answer'])
    posible_answers = question['incorrect_answers']
    for i in range(len(posible_answers)):
        posible_answers[i] = html.unescape(posible_answers[i])

    posible_answers.append(question['correct_answer'])
    random.shuffle(posible_answers)



    await ctx.send(embed = Embed(title = 'QUIZ (you have 10 seconds for answer)',description = question['question'],color = Colour.gold()
    ),components = [Button(style=ButtonStyle.blue, label=i, id = str(ctx.author.id)+i) for i in posible_answers])

    try:
        while True:
            response = await bot.wait_for("button_click",timeout=10.0)
            if ctx.author == response.user and ctx.channel == response.channel and response.component.label in posible_answers and str(ctx.author.id) in response.component.id : 
                break
    except:
        await ctx.send(embed = stuff.embed('Correct answer was: '+question['correct_answer'],Colour.red(),'TIME OUT'))
        return

    await response.respond(type = 7)
    if response.component.label == question['correct_answer']:
        await ctx.send(embed = stuff.embed('The answer was: '+question['correct_answer'],Colour.green(),'Correct!'))
    else:
        await ctx.send(embed = stuff.embed('The answer was: '+question['correct_answer'],Colour.red(),'Incorrect!'))


@bot.command(pass_context= True)
async def tic_tac_toe(ctx):
    def buttons():
       return [[Button(id = json.dumps([i,b]) ,style=(ButtonStyle.blue if field.get_map()[i][b] =='-' else (ButtonStyle.green if field.get_map()[i][b] == 'x' else ButtonStyle.red)), label=field.get_map()[i][b]) for b in range(len(field.get_map()[i]))] for i in range(3)]

    # generate game and bot 
    field = ttt.Field(clear_place_sign = '-')
    ttt_bot = ttt.Bot(field)
    if not field.is_payer_turn():
        ttt_bot.make_move()
    message = await ctx.send(embed = Embed(title = 'Игра "крестики нолики" (30 секунд на ход)',color = Colour.gold()),
    components = buttons())
    try:
        while True:
            response = await bot.wait_for("button_click",timeout = 30.0)
            if response.component.label != '-':
                await response.respond(type = 4,embed = stuff.embed('Место занято, попробуйте другое',Colour.red(),'Ошибка хода'))
            elif ctx.author == response.user and ctx.channel == response.channel:
                await response.respond(type = 7)
                ch = field.make_move(json.loads(response.component.id))
                if ch:
                    await message.edit(components = buttons())
                    if ch == 'draw':
                        await ctx.send(embed = stuff.embed('Ничья',Colour.green(),'Вы играете на уровне бота'))
                        return
                    await ctx.send(embed = stuff.embed('Поздравляем!!!',Colour.green(),'Вы выиграли'))
                    return
                ch = ttt_bot.make_move()
                if ch:
                    await message.edit(components = buttons())
                    if ch == 'draw':
                        await ctx.send(embed = stuff.embed('Ничья',Colour.green(),'Вы играете на уровне бота'))
                        return
                    await ctx.send(embed = stuff.embed('Сожалеем',Colour.red(),'Вы проиграли'))
                    return
                await message.edit(components = buttons())   
    except:
        await ctx.send(embed = stuff.embed('Игра была закрыта из-за вашей неактивности',Colour.red(),'Время вышло'))


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

@bot.command(pass_context= True)
async def chess(ctx):
    from __main__ import ch_engine
    board = ch.Board('7k/R2R4/8/8/8/8/5K2/8')

    letters = ['a','b','c','d','e','f','g','h']
                        
    emojis = {
        'B':883415614755045397,
        'b':883415614922838016,
        'K':883415619649806337,
        'k':883415619301687337,
        'N':883415619662413854,
        'n':883415619289112667,
        'P':883415619863740466,
        'p':883415619624632390,
        'Q':883415619679182898,
        'q':883415619633025104,
        'R':883415619343622176,
        'r':883415619733688320}

    def generate_buttons_moves(posible_moves,part2 = False):
        buttons = [[]]
        for i in posible_moves:
            k =str(board).replace(' ','').split('\n')
            k = (k[8-int(i[1])][letters.index(i[0])] if len(list(i)) == 2 else i[2].upper())
            if k != '.':
                buttons[-1].append(Button(id = i,label=(i if len(list(i)) == 2 else i[0:-1:1]),style=ButtonStyle.blue,emoji=bot.get_emoji(emojis[k])))
            else:
                buttons[-1].append(Button(id = i,label=(i if len(list(i)) == 2 else i[0:-1:1]),style=ButtonStyle.blue))
            if len(buttons[-1]) > 4:
                if  len(buttons) < 5:
                    buttons.append([])
                else:
                    if part2:
                        last_btn = buttons[-1][-1]
                        last_btn2 = buttons[-1][-2]
                        buttons = [[Button(id = 'back_move',style=ButtonStyle.grey,emoji= '🔙'),last_btn,last_btn2]]
                    else:
                        buttons[-1] = buttons[-1][0:-1:1]
                        buttons[-1][-1] = Button(id = 'next',style=ButtonStyle.grey,emoji= '⏩')
                        break

        if buttons[-1] == []:
            buttons = buttons[0:-1:1]
        if not part2:
            if (len(buttons) > 0 and len(buttons[-1]) > 4) or len(buttons) ==0:
                buttons.append([])
            buttons[-1].append(Button(id = 'back',style=ButtonStyle.red,emoji='🔙'))
        return buttons 

    def generate_buttons_choose_figure():
        buttons = [[]]
        str_board = str(board)
        x = 0
        y = 8
        for i in list(str_board):
            if i == ' ':
                continue

            if i == '\n':
                x = 0
                y -= 1
                continue

            if i !='.' and i.isupper():
                id = letters[x]+str(y)
                if  id in [str(i)[0:2] for i in board.legal_moves]:
                    buttons[-1].append(Button(id = id,style=ButtonStyle.blue,label=id,emoji= bot.get_emoji(emojis[i])))
                if len(buttons[-1]) > 4 :
                    buttons.append([])

            x+=1
        if len(buttons[-1]) == 0:
            buttons = buttons[0:-1:1]
        if (len(buttons) > 0 and len(buttons[-1])>4) or len(buttons) == 0:
            buttons.append([])
        buttons[-1].append(Button(id = 'exit',style=ButtonStyle.red,emoji='🚪'))
        return buttons

    async def make_img(selected_figure = '',posible_moves = []):
        path = './data/texturs/chess/'
        square_size = 125 #px
        img = Image.new('RGBA', Image.open(path+'board.png').size,(0, 0, 0, 0))
        img.paste(Image.open(path+'board.png'), (0,0,img.size[0],img.size[1]))

        if selected_figure:
            y = int(selected_figure[1])-1
            x = letters.index(selected_figure[0])
            sq = Image.open(path+'blue_square.png').convert("RGBA")
            sq.putalpha(128)
            img.paste(sq,(x*square_size+5,y*square_size),sq)

        for i in posible_moves:
            y = 9-int(i[1])-1
            x = letters.index(i[0])
            sq = Image.open(path+'green_square.png').convert("RGBA")
            sq.putalpha(128)
            img.paste(sq,(x*square_size+3,y*square_size-1),sq)


        str_board =  str(board).replace(' ','').split('\n')
        for i in range(len(str_board)):
            for b in range(len(list(str_board[i]))):
                if str_board[i][b] != '.':
                    p_img = Image.open(path + (str_board[i][b] if str_board[i][b].isupper() else str_board[i][b]+'1') +'.png')
                    img.paste(p_img,(b*square_size,i*square_size),p_img)

        with io.BytesIO() as image_binary:
            img.save(image_binary, 'PNG')
            image_binary.seek(0)
            m = await bot.get_channel(883373495260708954).send(file=discord.File(fp=image_binary, filename='image.png'))
            return m.attachments[0].url
        
    message = await ctx.send(embed = stuff.embed('подождите, бот думает'))
    emb = Embed(title = 'Шахматы (2 мин на ход)',description = 'выберите фигуру которой хотите совершить ход')
    emb.set_image(url = await make_img())
    try:
        while True:

            emb = Embed(title = 'Шахматы (2 мин на ход)',description = 'выберите фигуру которой хотите совершить ход')
            emb.set_image(url = await make_img())
            await message.edit(embed = emb,components = generate_buttons_choose_figure())

            t = int(time.time()+100)
            while True:
                try:
                    response = await bot.wait_for("button_click",timeout = t-time.time())
                except:
                    t = time.time()+20
                    await ctx.send(embed = stuff.embed('Осталось 20 секунд для хода',Colour.gold(),'Внимание!!!',':exclamation:'))
                    response = await bot.wait_for("button_click",timeout = t - time.time())

                if ctx.author == response.user and response.message == message :
                    if response.component.id == 'exit':
                        await response.respond(type=7,embed = stuff.embed('Игра закончена преждевременно'),components=[])
                        return

                    await response.respond(type=7,embed = stuff.embed('подождите, бот думает'),components=[])
                    break

            #get posible moves
            from_where = response.component.id
            posible_moves = [str(i)[2::] for i in board.legal_moves if str(i).startswith(from_where)]
            emb.description = 'выберите куда хотите походить'
            emb.set_image(url = await make_img(response.component.id[0]+str(9-int(response.component.id[1])),posible_moves))
            await message.edit(embed = emb,components = generate_buttons_moves(posible_moves))
            
            t = int(time.time()+100)
            while True:
                try:
                    response = await bot.wait_for("button_click",timeout = t-time.time())
                except:
                    t = time.time()+20
                    await ctx.send(embed = stuff.embed('Осталось 20 секунд для хода',Colour.gold(),'Внимание!!!',':exclamation:'))
                    response = await bot.wait_for("button_click",timeout = t - time.time())

                if ctx.author == response.user and response.message == message :
                    if response.component.id == 'next':
                        t = int(time.time()+120)
                        await response.respond(type=7,components = generate_buttons_moves(posible_moves,True))
                    elif response.component.id == 'back_move':
                        t = int(time.time()+120)
                        await response.respond(type=7,components = generate_buttons_moves(posible_moves))
                    else:
                        break
            
            await response.respond(type=7,embed = stuff.embed('подождите, бот думает'),components=[])
            if response.component.id == 'back':
                continue
            
            

            #make move
            
            board.push(ch.Move.from_uci(from_where[0]+from_where[1]+response.component.id))
            if  board.is_game_over():
                break
            result = await ch_engine.play(board, ch.engine.Limit(time=0.1))
            board.push(result.move)
            if  board.is_game_over():
                break

        if board.outcome().termination._value_ == 3: #draw
            emb = stuff.embed(title = 'Ничья',text = 'Это была напряженная игра!!',color=Colour.gold(),emoji = ':woozy_face: ')
        elif not board.outcome().winner: #black
            emb = stuff.embed(title = 'Проигрыш',text= 'Вы глупы, или бот слишком умен, скорее второе xD',color=Colour.red())
        elif board.outcome().winner: #white
            emb = stuff.embed(title = 'Выигрыш',text = 'Да вам просто повезло',color=Colour.green())
        emb.set_image(url = await make_img())
        await message.edit(embed = emb,components = [])
    except TimeoutError:
        await ctx.send(embed = stuff.embed('Вы думали слишком долго',Colour.red(),'Время вышло'))
        return

