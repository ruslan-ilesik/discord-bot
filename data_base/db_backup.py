import os
from datetime import date
import time
import discord
from discord.ext import commands
from discord.utils import get

import bot_data 
from __main__ import bot

def backup_db():
    # (--column-statistics=0) add this if ypu use 8 or later version of mysql as a parameter in "cmd"  
    cmd = "mysqldump  -u '%s' -h '%s' -p'%s' --insert-ignore --skip-lock-tables --single-transaction=TRUE '%s' > ./data_base/backups/'%s'_%s.sql" %(bot_data.db_user_name, bot_data.db_local_ip,bot_data.db_password, bot_data.db_base, bot_data.db_base  ,date.today())
    os.system(cmd)

async def send_backup():
    user = get(bot.get_all_members(), id=521291273777446922)
    await user.send(file=discord.File(r'./data_base/backups/%s_%s.sql'%(bot_data.db_base  ,date.today())))
    
async def backupping():
    print('start backupping script')
    start_bacup_time = int(time.time()) 
    backup_db()
    finish_backup_time= int(time.time())
    print ('_________________________________________________')
    print('backup of DB finished'  )
    print('name of file: DS_bot_%s.sql' %(date.today()))
    print ('time to make backup '+ str(finish_backup_time-start_bacup_time)+' seconds')
    print('sending backup to another pc')
    await send_backup()
    print('finish_send')
    return time.time()-start_bacup_time
