import pymysql
import functools
import itertools


import bot_data as bd



def ping_to_db():
    conn.ping(reconnect=True)

def conect():
    global conn,cur
    try:
        conn = pymysql.connect(bd.db_local_ip, bd.db_user_name, bd.db_password, bd.db_base)
    except:
        conn = pymysql.connect(bd.db_global_ip, bd.db_user_name, bd.db_password, bd.db_base,port = bd.db_global_port)

    conn.autocommit(True)
    cur = conn.cursor()
    return conn,cur


def disconect(cur,conn):
    cur.close()
    conn.close()

def select(what = [] , table= '', where_where = [] , where_what = [],symbol = ['='], and_or = [] ):
    ping_to_db()
    sql = "SELECT ("+",".join(what)+") FROM "+ str(table)+  " WHERE "
    if len(what) == 1:
        sql = "SELECT "+",".join(what)+" FROM "+ str(table)+  " WHERE "
    for i in range (len(where_where)):
        sql+= str(where_where[i]) + str(symbol[i]) +'"'+ str(where_what[i])+'" '
        try:
            sql += and_or[i]+ ' '
        except:
           data =1
                
    #print(sql)
    cur.execute(sql)
    data = cur.fetchall()
    return data



def insert(table = '', what = [], what_what = []):
    ping_to_db()
    sql = 'INSERT INTO '+str(table)+" ("+ ','.join(what)+ ' ) VALUES ("'+'","'.join(what_what)+'")'
    print(sql)
    cur.execute(sql)
    conn.commit()
    return True


def delete(table='', where=[],where_what=[],symbol=[],and_or=[]):
    ping_to_db()
    sql = 'DELETE FROM '+str(table)
    if len (where)>0:
        sql+=" WHERE "
    for i in range(len(where)):
        sql+= str(where[i]) + str(symbol[i]) + str(where_what[i])+' '
        try:
            sql += and_or[i]+ ' '
        except:
            continue
    #print(sql)
    cur.execute(sql)
    conn.commit()



def update(table = '' ,what = [] , what_what = [] , where = [] , where_what = [],symbol =[], and_or = [] ):
    ping_to_db()
    sql = "UPDATE "+ str(table)+' SET '
    for i in range (len(what)):
        sql += ' '+str(what[i]) + ' = '+ str(what_what[i])+ ','
    sql = sql[:len(sql)-1:]
    sql += ' WHERE '
    for i in range (len(where)):
        sql+= str(where[i]) + str(symbol[i]) + str(where_what[i])+' '
        try:
            sql += and_or[i]+ ' '
        except:
            continue
    print(sql)
    cur.execute(sql)
    conn.commit()
    return True

def custom_sql(sql):
    ping_to_db()
    cur.execute(sql)
    conn.commit()
    return True

def tuple_to_int(tuple_obj):
    return functools.reduce(lambda sub, ele: sub * 10 + ele, tuple_obj)

def tuple_to_array(b) :
    a= []
    for i in b:
        a.append( list(i))
    return(a)

conect()
                # examples

#insert('users' , ['sdsede','dedfrf'],['dede','dedrfrf'])
#select(['wwded','frgfrtgf','gtgt'],'users',['dededf',"defr"], ['rfrgt','frgttg'],['>',"<"],["AND"])
#update('users',['dwdew','dedew'],['qqq','www'],['qwsde','wdefr'],['dedefd','edref'],['>','<'],['OR'])
#delete('deede',['dedeed','qwqwq'],['dedede','qwqssws'],['>','<'],['and'])
