from bs4 import BeautifulSoup as bs
import vk_api
import random
import datetime
import os
import urllib.request
from vk_api.longpoll import VkLongPoll, VkEventType
import json
import numpy as np
import pandas as pd
import f9
from traceback import format_exc

class Bot:
    def __init__(self):
        print('bot is working')

    def write_msg(self, user_id, text):
        if(self.keyboard2 != ''):
            self.vk_session.method('messages.send', {'user_id': user_id, 'random_id': random.randint(1, 1000000), 'message': text, 'keyboard': self.keyboard2})
        else:
            self.vk_session.method('messages.send', {'user_id': user_id, 'random_id': random.randint(1, 1000000), 'message': text})

    def create_admin(self, id, admins, n):
        admins[id] = n
        f = open('admins.txt', 'a')
        f.write('\n')
        f.write(str(id) + ' ' + str(n))
        f.close()

    def delete_admin(self, id, admins):
        for i in admins.keys():
            if(admins[i] == id):
                for j in range(i, len(admins) - 1):
                    admins[i] = admins[i + 1]
                break
        f = open('admins.txt', 'r')
        d = []
        for line in f:
            line = line.split()
            if(line[0] != id):
                d.append([line[0], line[1]])
        f.close()
        f = open('admins.txt', 'w')
        for i in range(len(d)):
            f.write(d[i][0] + ' ' + d[i][1])
            f.write('\n')
        f.close()

    def cource_add(self):
        f = open('cources.txt', 'w')
        for id in self.cources.keys():
            s = str(str(id) + ' ' + str(self.cources[id]))
            f.write(s)
            f.write('\n')
        f.close()

    def documents_add(self, name, text):
        f = open('documents.txt', 'a')
        f.write('\n')
        f.write(name)
        f.write('\n')
        f.write(text)
        f.close()

    def documents_delete(self, name):
        f = open('documents.txt', 'r')
        d = []
        tr = True
        for line in f:
            if(line == name):
                tr = False
            elif(line != name and line in self.documents.keys()):
                tr = True
            if(tr):
                d.append(line)
        f.close()
        f = open('documents.txt', 'w')
        for i in range(len(d)):
            f.write(d[i])
            f.write('\n')
        f.close()

    def notifications_add(self, id):
        f = open('notifications.txt', 'a')
        f.write('\n')
        f.write(str(id))
        f.close()

    def notifications_delete(self, user_id):
        f = open('notifications.txt', 'r')
        d = []
        for line in f:
            line = line.split()
            if(line != [] and str(line[0]) != str(user_id)):
                d.append(line[0])
        f.close()
        f = open('notifications.txt', 'w')
        for i in range(len(d)):
            f.write(d[i])
            f.write('\n')
        f.close()

    def keyboard(self):
        keyboard1 = {
            'one_time': False,
            'buttons': [[{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '1'}),
                    'label': 'Дотация',
                },
                'color': 'default'
            },
                {
                    'action': {
                        'type': 'text',
                        'payload': json.dumps({'buttons': '2'}),
                        'label': 'Профилакторий',
                    },
                    'color': 'default'
                },
                {
                    'action': {
                        'type': 'text',
                        'payload': json.dumps({'buttons': '3'}),
                        'label': 'Мат. помощь',
                    },
                    'color': 'default'
                },
                {
                    'action': {
                        'type': 'text',
                        'payload': json.dumps({'buttons': '4'}),
                        'label': 'Ед. выплаты',
                    },
                    'color': 'default'
                }
            ],
            [{
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '2'}),
                    'label': 'Включить',
                },
                'color': 'positive'
            },
                {
                    'action': {
                        'type': 'text',
                        'payload': json.dumps({'buttons': '2'}),
                        'label': 'Выключить',
                    },
                    'color': 'negative'
                }
            ]]
        }
        keyboard1 = json.dumps(keyboard1, ensure_ascii=False).encode('utf-8')
        keyboard1 = str(keyboard1.decode('utf-8'))
        self.keyboard2 = keyboard1

    def start(self):
        while True:
            try:
                global gl
                global d
                self.keyboard2 = ''
                d.table('table.xlsx')
                d.birth('births.xlsx')
                vk_session = vk_api.VkApi(token='xxx')
                self.vk_session = vk_session

                #read .txt files (they are for enable to turn off the bot)
                self.documents = {'ед. выплата': [], 'дотация': [], 'мат. помощь': [], 'алушта': []} # names of all documents
                f = open('documents.txt', 'r', encoding='utf-8')
                s = ''
                for line in f:
                    line2 = line
                    line = line.split()
                    if(line != []):
                        if(len(line) == 1 and str(line[0]) in self.documents.keys()):
                            s = str(line[0])
                        elif(len(line) == 2 and str(line[0]) + ' ' + str(line[1]) in self.documents.keys()):
                            s = str(line[0]) +  ' ' + str(line[1])
                        elif (len(line) == 3 and str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[2]) in self.documents.keys()):
                            s = str(line[0]) + ' ' + str(line[1]) + ' ' + str(line[1])
                        else:
                            self.documents[s].append(''.join(line2))
                f.close()

                self.cources = {}
                f = open('cources.txt', 'r')
                s = ''
                for line in f:
                    line = line.split()
                    if (len(line) > 1):
                        self.cources[line[0]] = line[1]
                f.close()

                admins = {}
                f = open('admins.txt', 'r')
                for line in f:
                    line = line.split()
                    if(len(line) > 1):
                        admins[line[0]] = line[1]
                f.close()

                notifications = {}
                f = open('notifications.txt', 'r')
                for line in f:
                    line = line.split()
                    if (line != []):
                        notifications[line[0]] = 1 #1 - on, 2 - off
                f.close()

                #statics
                longpoll = VkLongPoll(vk_session)
                vk = vk_session.get_api()
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                        if (event.text != ''):
                            text = event.text
                            text = text.lower()
                            user_id = str(event.user_id)
                            gl.keyboard()
                            if (len(text) == 1 and ord(text[0]) >= ord('0') and ord(text[0]) <= ord('9')): #if user write his course
                                gl.write_msg(user_id, 'Запомню')
                                self.cources[str(user_id)] = int(text)
                                gl.cource_add()
                            elif(str(user_id) not in self.cources.keys()):
                                gl.write_msg(user_id, 'Введите ваш курс')
                            elif(str(text) == 'привет'):
                                gl.write_msg(user_id, 'Привет, если не знаешь команды, попробуй ввести хелп')
                            elif(text.split()[0] == 'добавить' and text.split()[1] == 'админа'):
                                if(user_id not in admins or len(text.split()) == 4 and text.split()[3] == 2 and admins[user_id] == 1):
                                    gl.write_msg(user_id, 'У вас недостаточно прав')
                                elif(len(text.split()) != 4):
                                    gl.write_msg(user_id, 'Что-то не так, введите хелп')
                                elif(text.split()[2] in admins):
                                    gl.write_msg(user_id, 'Такой админ уже существеут')
                                else:
                                    gl.create_admin(text.split()[2], admins, text.split()[3])
                                    gl.write_msg(user_id, 'Добавлен')
                            elif(len(text.split()) >= 3 and text.split()[0] == 'добавить' and text.split()[1] == 'документ'):
                                m = []
                                n = 0
                                for i in self.documents.keys():
                                    if(len(i.split()) > 1):
                                        m.append(i.split()[0])
                                if(text.split()[2] in m):
                                    name = text.split()[2] + ' ' + text.split()[3]
                                else:
                                    name = text.split()[2]
                                n = len(name)
                                if(name in self.documents.keys()):
                                    self.documents[name] = text[17 + n:]
                                    gl.documents_delete(name)
                                    gl.documents_add(name, text[17 + n:])
                                else:
                                    self.documents[name] = text[17 + n:]
                                    gl.documents_add(name, text[17 + n:])
                            elif (text.split()[0] == 'удалить' and text.split()[1] == 'админа'):
                                if (len(text.split()) != 3):
                                    gl.write_msg(user_id, 'Что-то не так, введите хелп')
                                elif (user_id not in admins or user_id in admins and admins[user_id] != '2' or admins[text.split()[2]] == 2):
                                    gl.write_msg(user_id, 'У вас недостаточно прав')
                                elif (text.split()[2] not in admins):
                                    gl.write_msg(user_id, 'Такого админа нет')
                                else:
                                    gl.delete_admin(text.split()[2], admins)
                                    gl.write_msg(user_id, 'Удалён')
                            elif(text in ['мат. помощь', 'дотация', 'ед. выплаты', 'алушта', 'профилакторий']):
                                s2 = text[0].title()
                                text = s2 + text[1:]
                                if(str(user_id) in self.cources.keys()):
                                    data = d.date(int(self.cources[user_id]), text)
                                    if(data != '-'):
                                        gl.write_msg(user_id, str(text + ' ' + 'будет' + ' ' + data))
                                    else:
                                        gl.write_msg(user_id, 'Ваш курс введён неверно')
                                else:
                                    gl.write_msg(user_id, 'Введите ваш курс')
                            elif (text == 'уведомления'):
                                if(user_id in notifications.keys() and notifications[user_id] == 0):
                                    gl.write_msg(user_id, 'У вас отключены уведомления, для их включения нажмите кнопку включить')
                                else:
                                    gl.write_msg(user_id, 'У вас включены уведомления, для их отключения нажмите кнопку выключить')
                            elif(text == 'включить'):
                                gl.write_msg(user_id, 'У вас включены уведомления')
                                if(user_id not in notifications or user_id in notifications and notifications[user_id] == 0):
                                    notifications[user_id] = 1
                                    gl.notifications_add(user_id)
                            elif (text == 'выключить'):
                                gl.write_msg(user_id, 'У вас выключены уведомления')
                                if (user_id in notifications and notifications[user_id] == 1):
                                    notifications[user_id] = 0
                                    gl.notifications_delete(user_id)
                            elif (text == 'как отправить файл?'):
                                gl.write_msg(user_id,
                                             'Прикрипите к сообщению нужный файл, если вы отправляете дни рождений, в сообщении напишите дни рождений обновить')
                                gl.write_msg(user_id,
                                             'Если же вы отправляете таблицу рассписаний, то в сообщении напишите рассписание добавить')
                            elif(len(text.split()) > 1 and text.split()[0] == 'документы'):
                                if(text[10:] in self.documents.keys()):
                                    for i in range(len(self.documents[text[10:]])):
                                        gl.write_msg(user_id, str(self.documents[text[10:]][i]))
                                else:
                                    gl.write_msg(user_id, 'Такого документа не существует')
                            elif (text.split()[0] == 'хелп'):
                                gl.write_msg(user_id, 'Команды: Дотация|Мат. Помощь|Ед. выплата|Алушта|Профилакторий')
                                gl.write_msg(user_id, 'Добавить|удалить админа (id человека) (доступ админа: 2 - полный, 1 - ограниченный(без доступа к удалению админов))')
                                doc_names = ''
                                for i in self.documents.keys():
                                    doc_names += str(i + '|')
                                gl.write_msg(user_id, 'Добавить документ' + doc_names + 'текст')
                                gl.write_msg(user_id, 'Уведомления')
                                gl.write_msg(user_id, 'Как добавить файл?')
                                gl.write_msg(user_id, 'Заменить название курс на что заменить')
                            elif (user_id in admins and len(text.split()) == 3 and text == 'даты рождений добавить'):
                                message_id = \
                                vk_session.method('messages.getHistory', {'count': 1, 'user_id': str(event.user_id)})[
                                    'items'][0]['id']
                                url = vk_session.method('messages.getById', {'message_ids': message_id})['items'][0][
                                    'attachments'][0]['doc']['url']
                                path = os.path.abspath("bot_for_mei/births.xlsx")
                                urllib.request.urlretrieve(url, path)
                                d.table('births.xlsx')
                            elif (user_id in admins and len(text.split()) == 2 and text == 'расcписание добавить'):
                                message_id = \
                                    vk_session.method('messages.getHistory',
                                                      {'count': 1, 'user_id': str(event.user_id)})[
                                        'items'][0]['id']
                                url = vk_session.method('messages.getById', {'message_ids': message_id})['items'][0][
                                    'attachments'][0]['doc']['url']
                                path = os.path.abspath("bot_for_mei/table.xlsx")
                                urllib.request.urlretrieve(url, path)
                                d.table('table.xlsx')
                            elif(user_id in admins and len(text.split()) == 4 and text.split()[0] == 'заменить' and user_id in admins):
                                gl.write_msg(user_id, d.rwr(text.split()[2], text.split()[3], text.split()[4]))
                            else:
                                gl.write_msg(user_id, 'Что-то странное..., попробуйте ввести "хелп"')
            except:
                with open('error.txt', 'a') as f:
                    f.write(format_exc())
                    f.write('\n')
                # there you can write your id to get notification about error
                # gl.write_msg(id, 'Some error')

gl = Bot()
d = f9.table()
gl.start()