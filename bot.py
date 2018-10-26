# -*- coding: utf-8 -*-
import os
import telebot
import time
import chlenomerconfig
import telebot
import random
from telebot import types
from pymongo import MongoClient
import threading

client1=os.environ['database']
client=MongoClient(client1)
db=client.channelsbase
users=db.users
channels=db.channels

   
    
    
@bot.message_handler(commands=['start'])
def start(m):
    if users.find_one({'id':m.from_user.id}) is None:
         users.insert_one(createuser(m.from_user.id,m.from_user.first_name,m.from_user.username))
    if m.from_user.id==m.chat.id:
        kb=types.ReplyKeyboardMarkup()
        kb.add(types.ReplyKeyboardButton('📮ПРОДАТЬ РЕКЛАМУ'))
        kb.add(types.ReplyKeyboardButton('МУЗЫКА'),types.ReplyKeyboardButton('БЛОГИ'))
        kb.add(types.ReplyKeyboardButton('КАНАЛЫ1'),types.ReplyKeyboardButton('КАНАЛЫ2'))
        kb.add(types.ReplyKeyboardButton('КАНАЛЫ3'),types.ReplyKeyboardButton('КАНАЛЫ4'))
        bot.send_message(m.chat.id, '🏡Главное меню',reply_markup=kb)
        
        

@bot.message_handler()
def channelselect(m):
    x=channels.find_one({})
    user=users.find_one({'id':m.from_user.id})
    if m.text=='Далее':
        users.update_one({'id':user['id']},{'$inc':{'currentindex':3}})
        user=users.find_one({'id':m.from_user.id})
        y=x[user['currenttheme']]
        text=showchannels(user,y)
        kb=types.ReplyKeyboardMarkup()
        kb.add(types.ReplyKeyboardButton('Назад'),types.ReplyKeyboardButton('Далее'))
        bot.send_message(m.chat.id, text, reply_markup=kb)
    if m.text=='Назад':
        users.update_one({'id':user['id']},{'$inc':{'currentindex':-3}})
        user=users.find_one({'id':m.from_user.id})
        if user['currentindex']<0:
            users.update_one({'id':user['id']},{'$set':{'currentindex':0}})
        user=users.find_one({'id':m.from_user.id})
        y=x[user['currenttheme']]
        text=showchannels(user,y)
        kb=types.ReplyKeyboardMarkup()
        kb.add(types.ReplyKeyboardButton('Назад'),types.ReplyKeyboardButton('Далее'))
        bot.send_message(m.chat.id, text, reply_markup=kb)
        
        
    if m.text=='МУЗЫКА':
        y=x['music']
        channel=0
        text=''
        users.update_one({'id':m.from_user.id},{'$set':{'currenttheme':'music'}})
        users.update_one({'id':m.from_user.id},{'$set':{'currentindex':0}})
        user=users.find_one({'id':m.from_user.id})
        
        text+=showchannels(user,y)
        
        kb=types.ReplyKeyboardMarkup()
        kb.add(types.ReplyKeyboardButton('Назад'),types.ReplyKeyboardButton('Далее'))
        bot.send_message(m.chat.id, text, reply_markup=kb)
            
    
def showchannels(user, y):
    channel=user['currentindex']
    i=channel+3
    while channel<i:
      try:
        ch=y[channel]
        text+='Рекламодатель: '+ch['reklamodatel']+'\n'
        text+='Канал: '+ch['channel']+'\n'
        text+='Подписчиков: '+str(ch['subs'])+'\n'
        text+='Цена: '+str(ch['cost'])+'\n'
        text+='Скидка: '+str(ch['discount'])+'\n'
        text+='Итоговая цена: '+str(ch['finalcost'])+'\n'
        text+='Тематика: '+themetoname(ch['theme'])+'\n'
        text+='Взаимный пиар: '+yesno(ch['piar'])+'\n'
        text+='Условия: '+ch['conditions']+'\n'
        text+='Для заказа рекламы тебе стоит написать администратору канала.\n'
        text+='\n'
        channel+=1
      except:
            pass
    return text
    
    
def createuser(id,name,username): 
   return{'id':id,
          'name':name,
          'username':username
         }
      
      
      

if True:
   print('bot is working')
   bot.polling(none_stop=True,timeout=600)
