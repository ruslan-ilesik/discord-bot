from bs4 import BeautifulSoup
import requests
import discord
from discord import Colour
import re
import asyncio 

import some_stuff as stuff
import data_base.work_with_db as db
from __main__ import bot

async def main():
    url = 'https://freesteam.ru/'
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    mydivs = soup.findAll("div", {"class": "col-lg-4 col-md-4 three-columns post-box"})
    for n, i in enumerate(mydivs, start=1):
        link = i.find('a',{"class": "thumb-link"})['href']
        break
    # go to page with info about game
    data = requests.get(link).text
    soup = BeautifulSoup(data, 'lxml')
    
    what_game_and_where_text = soup.find('h1',{'class':'entry-title'}).text

    # check that we dont already send message about this game
    try:
        f = open('events/last_game_distribation.txt','r')
        last_game = f.read()
        f.close()   
    except:
        last_game =''
    if what_game_and_where_text != last_game:
        
        print(what_game_and_where_text)

        link_to_get = soup.find('div',{'class':'entry-content'}).a['href'].split('?')[0]
        print(link_to_get)
        
        img_link = soup.find('div',{'class':'post-thumb'}).img['data-src']
        print(img_link)

        #send message in all chennals on all servers
        id = [i[0] for i in db.tuple_to_array(db.select(['channel_to_send_game_distributions'],'servers_data',['server_id'],['0'],['>']))]
        for i in id:
            if i != None:
                channel = discord.utils.get(bot.get_all_channels(), id=int(i))
                emb = stuff.embed('Забирать здесь: '+link_to_get,title=what_game_and_where_text,emoji=':tada:')
                emb.set_thumbnail(url=img_link)
                await channel.send(embed =  emb)
        
        # write our last game we send distribution
        f = open('events/last_game_distribation.txt','w')
        f.write(what_game_and_where_text)
        f.close()
    

