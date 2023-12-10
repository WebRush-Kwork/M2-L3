import telebot
from config import token
from random import randint
from logic import *

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! 🔥\nЭто бот для создания своего собственного покемона! ✍️\nСписок доступных команд Вы можете увидеть рядом с кнопкой отправки сообщения! 💻')


def get_logged_users():
    try:
        with open('logged_users.txt', 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []


logged_users = get_logged_users()


@bot.message_handler(commands=['create'])
def create(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1, 3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, 'Вы уже создали себе покемона! 🚀')


@bot.message_handler(commands=['attack'])
def attack_pokemon(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.attack(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(
                message.chat.id, "Сражаться можно только с покемонами 😼")
    else:
        bot.send_message(
            message.chat.id, "Вы не ответили на чье-либо сообщение! 📝")


@bot.message_handler(commands=['pokemon'])
def pokemon(message):
    if message.from_user.username in logged_users:
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.info())


@bot.message_handler(commands=['change'])
def change(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        del Pokemon.pokemons[message.from_user.username]
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, 'Вы еще не создали себе покемона! 🫢')


bot.infinity_polling(none_stop=True)
