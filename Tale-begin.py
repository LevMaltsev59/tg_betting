import telebot
from telebot import types
import random
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

token = ()

roll = 0
coins = 1000
bet = 0
gamestart = False
Prize1 = True

@bot.message_handler(content_types=['text'])
def start(message):
    global roll
    global coins
    global bet
    global gamestart
    global Prize1
    global gamestart

    if message.text == '/start':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_game = types.KeyboardButton('/game')
        keyboard.add(key_game)
        key_coins = types.KeyboardButton('/coins')
        keyboard.add(key_coins)
        key_restart = types.KeyboardButton('/restart')
        keyboard.add(key_restart)
        bot.send_message(message.from_user.id, "Добро пожаловать в игру", reply_markup=keyboard)
    elif message.text == '/game':
        if checkuser(message.from_user.id) == False:
            adduser(message.from_user.id)
        bot.send_message(message.from_user.id, "Напиши сумму своей ставки. В начале у тебя 1000 коинов, если ты проиграешь напиши /restart")
        gamestart = True
    elif message.text == '/coins':
        bot.send_message(message.from_user.id, f"У тебя {coins} коинов")


    elif message.text == '/restart':
        coins = 1000
        bot.send_message(message.from_user.id, f"У тебя теперь снова {coins} коинов.")
        Prize1 = True

    elif message.text == '/prize' and Prize1 == True:
        coins += 500
        bot.send_message(message.from_user.id, f"Ты получил 500 монет за секретную команду!")
        Prize1 = False
    elif message.text == '/prize' and Prize1 == False:
        bot.send_message(message.from_user.id, f"Прости, но ты не можешь повторно использовать секретную команду!")


    elif gamestart == True and message.text.isdigit():
        bet = int(message.text)
        if bet > coins:
            bot.send_message(message.from_user.id, "У тебя недостаточно коинов, на данный момент у тебя всего " + str(coins) + " коинов.")
        else:
            roll = random.randint(1, 3)
            keyboard = types.InlineKeyboardMarkup()
            key_one = types.InlineKeyboardButton(text='1', callback_data='1')
            key_two = types.InlineKeyboardButton(text='2', callback_data='2')
            key_three = types.InlineKeyboardButton(text='3', callback_data='3')
            keyboard.add(key_one)
            keyboard.add(key_two)
            keyboard.add(key_three)
            bot.send_message(message.from_user.id, "Давай поиграем. Я загадал число от 1 до 3", reply_markup=keyboard)
    else:
        gamestart = False
        bot.send_message(message.from_user.id, "Необходимо ввести число, напиши заново /game")

@bot.callback_query_handler(func=lambda call: True)
def game(call):
    global roll
    global coins
    global bet
    global conn

    print(roll)
    if int(call.data) == roll:
        coins += bet
        bot.send_message(call.message.chat.id, "Ты угадал, получи " + str(bet) + " коинов. У тебя осталось " + str(coins) + " коинов")
    else:
        coins -= bet
        bot.send_message(call.message.chat.id, "Ты не угадал, ты потерял " + str(bet) + " коинов. У тебя осталось " + str(coins) + " коинов")

    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

def checkuser(id):
   db.execute("SELECT * FROM telegram_bot WHERE user_id = %s", (id,))
   if db.fetchone() is None:
      return False
   else:
      return True

def adduser(id):
   db.execute("INSERT INTO telegram_bot (user_id, coins) VALUES (%s, 1000)", (id,))
   conn.commit()

def getcoins(id):
   db.execute("SELECT coins FROM telegram_bot WHERE user_id = %s", (id,))
   return db.fetchone()[0]

def setcoint(id, coins):
   db.execute("UPDATE telegram_bot SET COINS = %s WHERE user_id = %s", (coins, id,))
   conn.commit()

bot.polling(none_stop=True, interval=0)