import vk_api
import datetime
import schedule
import random
import pandas as pd
import numpy as np
import f9

def birthday():
    global vk_session
    global name_by_id
    global d
    now = str(datetime.datetime.now())
    d2 = int(now[8:10])
    m = int(now[5:7])
    if (str(d2 + '.' + m) in id_by_data.keys()):
        f = open('admins.txt', 'r')
        l = []
        z = 0
        for line in f:
            line = line.split()
            l.append(str(line))
            z += 1
        f.close()
        z = random.randint(1, z)

        f = open('congratulations.txt', 'r')
        congr = []
        for line in f:
            congr.append(str(line))
        f.close()
        r = random.randint(1, len(congr))
        write_msg(id_by_data[str(d2 + '.' + m)], congr[r])


def write_msg(user_id, text):
    vk_session.method('messages.send', {'user_id': user_id, 'random_id': random.randint(1, 1000000), 'message': text})

def cources():
    now = str(datetime.datetime.now()) #every first September bot update cources
    m = now[5:7]
    day = now[8:10]
    if(m == '09' and day == '01'):
        f = open('cources.txt', 'r')
        d = []
        for line in f:
            line = line.split()
            if (line != []):
                d.append(str(line[0] + ' ' + str(int(line[1]) + 1)))
        f.close()
        f = open('cources.txt', 'w')
        for i in range(len(d)):
            f.write(d[i])
            f.write('\n')
        f.close()


d = f9.table()
vk_session = vk_api.VkApi(token='xxx')
vk_session2 = vk_api.VkApi(token='xxxx') #there must be a key of somebody in vk, because vk does not allow some functions for group's bot
name_of_group = '183231650' #name of group in vk (what users we want to congratulate)
count = vk_session2.method('groups.getMembers', {'group_id': name_of_group})['count']
id_by_data = {}
name_by_id = {}
data_by_name = d.birth('births.xlsx')

z = 0
while(z * 1000 < count):
    r = vk_session2.method('groups.getMembers', {'group_id': name_of_group, 'offset': z * 1000})['items']
    for user in r:
        us = vk_session2.method('users.get', {'user_ids': user, 'lang': 'ru'})[0]
        print(us)
        full_name = str(us['first_name']) + ' ' + str(us['last_name'])
        name_by_id[str(user)] = data_by_name[full_name]
        if(full_name not in id_by_data):
            id_by_data[data_by_name[full_name]] = int(user)
        else:
            id_by_data[data_by_name[full_name]].append(int(user))
    z += 1

schedule.every().day.at("17:34").do(birthday)
schedule.every().day.at("00:00").do(cources)
while True:
    schedule.run_pending()