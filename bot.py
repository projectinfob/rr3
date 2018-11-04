# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
from telebot import types
from pymongo import MongoClient
import threading

client1=os.environ['database']
client=MongoClient(client1)
db=client.channelsbase2
users=db.users
channels=db.channels
buttons=db.buttons
codebuttons=db.codebuttons
bots=db.bots
   
bot=telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])   

@bot.message_handler(commands=['setbutton'])
def setbutton(m):
   if m.from_user.id==682723695 or m.from_user.id==441399484:
      x=m.text.split(' ')
      i=3
      if x[1].lower()=='каналы':
         i=4
      txt=''
      while i<len(x):
         txt+=x[i]
         if i+1!=len(x):
            txt+=' '
         i+=1
      if x[1].lower()=='меню':
         codebuttons.update_one({},{'$set':{'mainmenu.'+x[2]:txt}})
         bot.send_message(m.chat.id, 'Кнопка успешно обновлена!')
      if x[1].lower()=='каналы':
         buttons.update_one({},{'$set':{'channels.'+x[2]:txt}})
         codebuttons.update_one({},{'$set':{'channels.'+x[2]:x[3]}})
         bot.send_message(m.chat.id, 'Кнопка успешно обновлена!')
      

@bot.message_handler(commands=['buttonsinfo'])
def binfo(m):
   x=users.find_one({'id':m.from_user.id})
   u=codebuttons.find_one({})
   text=''
   i=0
   text+='Главное меню:\n'
   for ids in u['codebuttons']['mainmenu']:
      text+='Кнопка '+str(i)+': '+u['codebuttons']['mainmenu'][ids]+'\n'
      i+=1
   i=0
   text+='Каналы:\n'
   for ids in u['codebuttons']['channels']:
      text+='Кнопка '+str(i)+': '+u['codebuttons']['channels'][ids]+'\n'
      i+=1
   bot.send_message(m.chat.id, text)
   
      
      
@bot.message_handler(commands=['start'])
def start(m):
    if users.find_one({'id':m.from_user.id}) is None:
         users.insert_one(createuser(m.from_user.id,m.from_user.first_name,m.from_user.username))
    if m.from_user.id==m.chat.id:
        sendmenu(m.chat.id, m.from_user.id)
        
@bot.message_handler(commands=['addadmin'])
def addadmin(m):
   x=users.find_one({'id':m.from_user.id})
   if x['id']==682723695:
        users.update_one({'id':m.from_user.id},{'$set':{'addingadmin':1}})
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('❌Отмена'))
        bot.send_message(m.chat.id, 'Отправьте id юзера, которого хотите добавить в администраторы бота (id юзера можно '+
                         'получить, переслав его сообщение боту @ForwardInfoBot).')
   
@bot.message_handler(commands=['addchannel'])
def addchannel(m):
    x=users.find_one({'id':m.from_user.id})
    if x['isadmin']==1:
        users.update_one({'id':m.from_user.id},{'$set':{'addingchannel':1}})
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('❌Отмена'))
        bot.send_message(m.chat.id, '''Напишите следующие данные о канале в таком формате (одним сообщением):\n\n
👤Рекламодатель;
📺Канал;
📊Подписчиков;
💶Цена;
💳Скидка (в процентах);
📗Тематика (музыка/блоги/крипта/спорт/интим/цитаты);
🔁Взаимный пиар;
📋Условия.

''',reply_markup=kb)
        
        
@bot.message_handler(commands=['delchannel'])
def dellchannel(m):
    x=users.find_one({'id':m.from_user.id})
    if x['isadmin']==1:
        users.update_one({'id':m.from_user.id},{'$set':{'removingchannel':1}})
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('❌Отмена'))
        bot.send_message(m.chat.id, 'Чтобы удалить канал, напишите его юзернейм (@канал).',reply_markup=kb)


def sendmenu(chatid,userid):
    b=codebuttons.find_one({})
    print(b)
    users.update_one({'id':userid},{'$set':{'currentindex':0}})
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(b['mainmenu'][0]))
    kb.add(types.KeyboardButton(b['mainmenu'][1]),types.KeyboardButton(b['mainmenu'][2]))
    kb.add(types.KeyboardButton(b['mainmenu'][3]),types.KeyboardButton(b['mainmenu'][4]))
    bot.send_message(chatid, '🏡Главное меню',reply_markup=kb)
        
#kb.add(types.KeyboardButton(b['buttons']['0']),types.KeyboardButton(b['buttons']['1']))
#    kb.add(types.KeyboardButton(b['buttons']['2']),types.KeyboardButton(b['buttons']['3']))
#    kb.add(types.KeyboardButton(b['buttons']['4']),types.KeyboardButton(b['buttons']['5']))
   
def showcategory(category,userid,chatid,x):
        b=codebuttons.find_one({})
        if category==b['channels'][0]:
            print(x)
            y=x['channels'][0]
            i=0
        if category==b['channels'][1]:
            y=x['channels'][1]
            i=1
        if category==b['channels'][2]:
            y=x['channels'][2]
            i=2
        if category==b['channels'][3]:
            y=x['channels'][3]
            i=3
        if category==b['channels'][4]:
            y=x['channels'][4]
            i=4
        if category==b['channels'][5]:
            y=x['channels'][5]
            i=5
        channel=0
        text=''
        users.update_one({'id':userid},{'$set':{'currenttheme':i}})
        users.update_one({'id':userid},{'$set':{'currentindex':0}})
        user=users.find_one({'id':userid})
        text+=showchannels(user,y)
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
        kb.add(types.KeyboardButton('🏡Главное меню'))
        try:
            bot.send_message(chatid, text, reply_markup=kb)
        except:
            bot.send_message(chatid, 'В этой категории пока что нет ни одного канала!')
   

def sellchannel(id):
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton('❌Отмена'))
    bot.send_message(id,'Укажите юзернейм вашего канала следующим сообщением.',reply_markup=kb)
    users.update_one({'id':id},{'$push':{'actions':'sc','actions':'sc_name'}})

def showchannelss(id):
    b=buttons.find_one({})
    c=codebuttons.find_one({})
    kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(b['channels'][0]),types.KeyboardButton(b['channels'][1]))
    kb.add(types.KeyboardButton(b['channels'][2]),types.KeyboardButton(b['channels'][3]))
    kb.add(types.KeyboardButton(b['channels'][4]),types.KeyboardButton(b['channels'][5]))
    bot.send_message(id,c['mainmenu'][1], reply_markup=kb) 
   
   
    
@bot.message_handler()
def channelselect(m):
  if users.find_one({'id':m.from_user.id}) is not None:
    users.update_one({'id':m.from_user.id},{'$set':{'name':m.from_user.first_name}})
    x=channels.find_one({})
    b=codebuttons.find_one({})
    c=buttons.find_one({})
    user=users.find_one({'id':m.from_user.id})
    if m.text=='▶':
        users.update_one({'id':user['id']},{'$inc':{'currentindex':3}})
        user=users.find_one({'id':m.from_user.id})
        y=x[user['currenttheme']]
        text=showchannels(user,y)
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
        kb.add(types.KeyboardButton('🏡Главное меню'))
        if text!='':
            bot.send_message(m.chat.id, text, reply_markup=kb)
        else:
            users.update_one({'id':user['id']},{'$set':{'currentindex':0}})
            user=users.find_one({'id':m.from_user.id})
            y=x[user['currenttheme']]
            text=showchannels(user,y)
            kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
            kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
            kb.add(types.KeyboardButton('🏡Главное меню'))
            bot.send_message(m.chat.id, text, reply_markup=kb)
            
    elif m.text=='◀':
        users.update_one({'id':user['id']},{'$inc':{'currentindex':-3}})
        user=users.find_one({'id':m.from_user.id})
        if user['currentindex']<0:
            users.update_one({'id':user['id']},{'$set':{'currentindex':0}})
        user=users.find_one({'id':m.from_user.id})
        y=x[user['currenttheme']]
        text=showchannels(user,y)
        kb=types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(types.KeyboardButton('◀'),types.KeyboardButton('▶'))
        kb.add(types.KeyboardButton('🏡Главное меню'))
        bot.send_message(m.chat.id, text, reply_markup=kb)
        
        
    elif m.text==b['mainmenu'][0]:
      sellchannel(m.from_user.id)
        
    elif m.text==b['mainmenu'][1]:
        showchannelss(m.from_user.id)
            
    elif m.text==b['mainmenu'][2]:
      showbots(m.from_user.id)
      
    elif m.text==b['mainmenu'][3]:
      stats(m.from_user.id)
      
    elif m.text==b['mainmenu'][4]:
      ballance(m.from_user.id)
      
      
    elif m.text==c['channels'][0]:
       showcategory(b['channels'][0],m.from_user.id,m.chat.id,x)
       
    elif m.text==c['channels'][1]:
       showcategory(b['channels'][1],m.from_user.id,m.chat.id,x)
           
    elif m.text==c['channels'][2]:
       showcategory(b['channels'][2],m.from_user.id,m.chat.id,x)
     
    elif m.text==c['channels'][3]:
       showcategory(b['channels'][3],m.from_user.id,m.chat.id,x)
     
    elif m.text==c['channels'][4]:
       showcategory(b['channels'][4],m.from_user.id,m.chat.id,x)
     
    elif m.text==c['channels'][5]:
       showcategory(b['channels'][5],m.from_user.id,m.chat.id,x)
      
        
    elif m.text=='❌Отмена':
        users.update_one({'id':m.from_user.id},{'$set':{'actions':[]}})
        sendmenu(m.chat.id, m.from_user.id)
               
    elif m.text=='🏡Главное меню':
        sendmenu(m.chat.id, m.from_user.id)
        
    elif m.text=='📮Продать рекламу':
        bot.send_message(m.chat.id,'Для добавления бота в каталог напишите [администратору](tg://user?id='+str(682723695)+').',parse_mode='markdown')                   
            
    user=users.find_one({'id':m.from_user.id})
    if 'addingchannel' in user['actions']:
      try:
        y=m.text.split('\n')
        print(y)
        reklamodatel=y[0]
        channel=y[1]
        subs=int(y[2])
        cost=int(y[3])
        discount=int(y[4])
        theme=nametotheme(y[5])
        piar=y[6]
        conditions=y[7]
        reklamodatel+=''
        channel+=''
        subs+=0
        cost+=0
        discount+=0
        theme+=''
        piar+=''
        conditions+=''
        channels.update_one({},{'$push':{theme:createchannel(reklamodatel,channel,subs,cost,discount,theme,piar,conditions)}})
        bot.send_message(m.chat.id, 'Канал успешно добавлен!')
        users.update_one({'id':m.from_user.id},{'$pull':{'actions':'addingchannel'}})
        u=users.find({})
        finalcost=round(cost-(cost*(discount*0.01)),1)
        text=''
        text+='👤Рекламодатель: '+reklamodatel+'\n'
        text+='📺Канал: '+channel+'\n'
        text+='📊Подписчиков: '+str(subs)+'\n'
        text+='💶Цена: '+str(cost)+'\n'
        text+='💳Скидка: '+str(discount)+'\n'
        text+='🤑Итоговая цена: '+str(finalcost)+'\n'
        text+='📗Тематика: '+themetoname(theme)+'\n'
        text+='🔁Взаимный пиар: '+piar+'\n'
        text+='📋Условия: '+conditions+'\n'
        text+='ℹДля заказа рекламы тебе стоит написать администратору канала.'
        sendto=0
        for ids in u:
            try:
              bot.send_message(ids['id'], text)
              sendto+=1
            except:
              pass
        bot.send_message(m.chat.id, 'Канал отправлен '+str(sendto)+' подписчикам!')
        sendmenu(m.chat.id, m.from_user.id)
      except:
           bot.send_message(m.chat.id, 'Неправильно введены аргументы для добавления канала!')
            
    elif 'removingchannel' in user['actions']: 
        chn=None
        ii=None
        for ids in x:
          if ids!='_id':
            i=0
            for idss in x[ids]:
                print(ids)
                print(idss)
                if idss['channel']==m.text:
                    chn=idss
                    ii=i
                i+=1
        if chn!=None:
            channels.update_one({},{'$pull':{chn['theme']:chn}})
            bot.send_message(m.chat.id, 'Канал успешно удалён!')
            users.update_one({'id':m.from_user.id},{'$set':{'removingchannel':0}})
            sendmenu(m.chat.id, m.from_user.id)
        else:
            bot.send_message(m.chat.id, 'Такого канала не существует!')
            
    elif 'addingadmin' in user['actions']:
        adm=users.find_one({'id':int(m.text)})
        if adm!=None:
            users.update_one({'id':adm['id']},{'$set':{'isadmin':1}})
            bot.send_message(m.chat.id, 'Новый администратор ('+adm['name']+') успешно добавлен!')
            users.update_one({'id':m.from_user.id},{'$set':{'addingadmin':0}})
        else:
            bot.send_message(m.chat.id, 'Юзер с таким id не регистрировался в боте!')
            
    elif 'removingadmin' in user['actions']:
        adm=users.find_one({'id':int(m.text)})
        if adm!=None:
            users.update_one({'id':adm['id']},{'$set':{'isadmin':0}})
            bot.send_message(m.chat.id, 'Юзер '+adm['name']+' больше не администратор!')
            users.update_one({'id':m.from_user.id},{'$set':{'removingadmin':0}})
        else:
            bot.send_message(m.chat.id, 'Юзер с таким id не регистрировался в боте!')

        
        
  else:
      bot.send_message(m.chat.id, 'Сначала напишите боту /start!')
        
           
                
def createchannel(reklamodatel,channel,subs,cost,discount,theme,piar,conditions):
    fcost=round(cost-(cost*(discount*0.01)),1)
    return{'reklamodatel':reklamodatel,
           'channel':channel,
           'subs':subs,
           'cost':cost,
           'discount':discount,
           'finalcost':fcost,
           'theme':theme,
           'piar':piar,
           'conditions':conditions
          }
    print(fcost)
                
    
def showchannels(user, y):
    channel=user['currentindex']
    text=''
    i=channel+3
    while channel<i:
      print('channel '+str(channel))
      print('i: '+str(i))
      try:
        ch=y[channel]
        text+='👤Рекламодатель: '+ch['reklamodatel']+'\n'
        text+='📺Канал: '+ch['channel']+'\n'
        text+='📊Подписчиков: '+str(ch['subs'])+'\n'
        text+='💶Цена: '+str(ch['cost'])+'\n'
        text+='💳Скидка: '+str(ch['discount'])+'\n'
        text+='🤑Итоговая цена: '+str(ch['finalcost'])+'\n'
        text+='📗Тематика: '+themetoname(ch['theme'])+'\n'
        text+='🔁Взаимный пиар: '+ch['piar']+'\n'
        text+='📋Условия: '+ch['conditions']+'\n'
        text+='ℹДля заказа рекламы тебе стоит написать администратору канала.\n'
        text+='\n'
      except:
            pass
      channel+=1
    return text
    
   
def nametotheme(x):
    z=codebuttons.find_one({})
    if x==z['codebuttons']['0']:
        return 'music'
    elif x==z['codebuttons']['1']:
        return 'blogs'
    elif x==z['codebuttons']['2']:
        return 'crypto'
    elif x==z['codebuttons']['3']:
        return 'sport'
    elif x==z['codebuttons']['4']:
        return 'intim'
    elif x==z['codebuttons']['5']:
        return 'citats'


def themetoname(x):
   z=codebuttons.find_one({})
   if x=='music':
      return z['codebuttons']['0']
   if x=='blogs':
      return z['codebuttons']['1']
   if x=='crypto':
      return z['codebuttons']['2']
   if x=='sport':
      return z['codebuttons']['3']
   if x=='intim':
      return z['codebuttons']['4']
   if x=='citats':
      return z['codebuttons']['5']
   
   
def createuser(id,name,username): 
   if id==682723695 or id==441399484:
       adm=1
   else:
       adm=0
   return{'id':id,
          'name':name,
          'username':username,
          'currenttheme':None,
          'currentindex':0,
          #'addingchannel':0,
          'isadmin':adm,
          #'removingchannel':0,
          #'addingadmin':0,
          #'removingadmin':0,
          #'setcode':0,
          'codenumber':None,
          'actions':[]
         }
      
      
      

if True:
   print('bot is working')
   bot.polling(none_stop=True,timeout=600)
