import discord
from discord import Colour
import datetime
import json


from __main__ import bot
import data_base.work_with_db as db
import some_stuff as stuff
import events.lottery as lottery_stuff

@bot.command(pass_context= True)
async def lottery(ctx,*args):
    data = db.tuple_to_array(db.select(["*"],'lotterys',['server_id'],[str(ctx.guild.id)]))
    if len(args) == 0:      
        emb = discord.Embed(color = Colour.gold() ,title="**:game_die: | Доступные лотереи**",description = '**Лотереи. Что тут обьяснять. несколько участников скидываются и получают шанс выиграть приз. Но победитель только один**\n\n ')
        id = 1
        for i in data:
            #convert to readable time if need
            text = ''
            i[2] = json.loads(i[2])
            if i[2]['prize']['type'] == 'sub' or i[2]['prize']['type'] == 'cs':
                i[2]['prize']['amount_time'] = str(datetime.timedelta(seconds=int(i[2]['prize']['amount_time']))).replace('days',"дней")
                text += 'Шанс выиграть: '+ i[2]['prize']['type'].replace('cs','Кастомну роль').replace('sub','Саб роль')+' на '+ i[2]['prize']['amount_time']
            else:
                text += 'Шанс выиграть: '+ i[2]['prize']['type'].replace('cash','Коинов')+' на сумму '+ i[2]['prize']['amount_time']
            text += '\nСтоимость участия: '+str(i[2]['participation_price']) +' коинов\nНужное количество участников: '+ str(i[2]['required_participants']) +'\nУже участвует: ' +  str(len(set(i[2]['participants'])))+ ' участников'
            emb.add_field(name = '**'+str(id)+') '+i[0]+'**',value=''+text+'',inline= False)
            id+=1
        emb.add_field(name ='**:face_with_monocle: **' ,value='**Хотите поучаствовать? Пишите команду +lottery и имя лотереи или её id**',inline= False)
        await ctx.send(embed = emb)
    else:
        lottery_name = ' '.join(args).lower()
        if (lottery_name in [i[0].lower() for i in data]) or (int(lottery_name) >= 1 and int(lottery_name) <= len(data)) :
            # get data about  lottery user ask
            text =''
            try:
                data = data[int(lottery_name)-1]
            except:
                for ki in data:
                    if ki[0].lower() == lottery_name.lower():
                        data = ki
                        break
            #print(data)
            data[2] = json.loads (data[2])
            text += 'Шанс выиграть: '+ data[2]['prize']['type'].replace('cash','Коинов на сумму ').replace('cs',' на ').replace('sub',' на ')
            if data[2]['prize']['type'] == 'cash':
                text+= str(data[2]['prize']['amount_time'])
            else:
                text += str(datetime.timedelta(seconds=int(data[2]['prize']['amount_time']))).replace('days',"дней")
            text += '\nСтоимость участия: '+str(data[2]['participation_price']) +' коинов\nНужное количество участников: '+ str(data[2]['required_participants']) +'\nУже участвует: ' +  str(len(set(data[2]['participants'])))+ ' участников'
            emb = discord.Embed(color = Colour.gold() ,title="**:game_die: | "+ data[0] +"**",description = text)
            emb.add_field(name = 'Хотите поучаствовать?',value='Напишите "confirm", Если не хотите участвовать напишите "exit"')
            await ctx.send(embed = emb)
            msg = await stuff.command_answer_wait(ctx.channel,ctx.author)
            if msg.content.lower() == 'confirm':
                await lottery_stuff.add_user_to_lottery(ctx,data)
            elif  msg.content.lower() == 'exit':
                pass
            else:
                await ctx.send(embed = stuff.embed('Некоректный ввод',color=Colour.red()))
        else:
            await ctx.send(embed = stuff.embed('Неправильное/Несуществующее имя или id лотереи ',color=Colour.red()))