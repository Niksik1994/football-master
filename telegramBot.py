import telebot
import re
from class_bot_futboll_win import *
import emoji

bot_name = "FootballMaster"
bot = telebot.TeleBot('1086309481:AAGsv9-VWYpcasMbhcqQv0RAatc354rJkxo')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую тебя, я бот ' + bot_name + ', каждый день я присылаю предсказания на футбольные матчи. ' +
                     "Обычно это матчи ТОП 5 лиг (Англия, Германия, Испания, Италия, Франция) но, иногда бывают матчи и других лиг. Присаживайся по удобнее и жди наводок. " +
                     "Так же ты можешь прислать мне ссылку на матч с сайта myscore(FlashScore.ru) и через пробел колличество матчей за которое нужно смотреть стсистику(максимум 10), " +
                     "и я сравнив статистику обеих команд сделаю прогноз. \nПример: https://www.flashscore.ru/match/z7bKeorA/#match-summary 5")


@bot.message_handler(content_types=['text'])
def send_text(message):
    check_game_url = r"https:\/\/www\.flashscore\.ru\/match\/\w{8}\/#match-summary"
    response = message.text.split(" ")
    count_match = 5
    if re.match(check_game_url, response[0]) is not None:
        try:
            if(int(response[1]) <= 10):
                count_match = int(response[1])
            else: 
                count_match = 5
        except:
            count_match = 5
        bot.send_message(
            message.chat.id, 'Я получил ссылку, жди, сравнение статистики может занимать до 5 минут.')
        bot_football = Bot_futball(
            response[0], count_match, True, True, True, True, True, True, True, True, False)
        bot_start = bot_football.botStart()
        bot.send_message(message.chat.id, emoji.emojize(
            ":eight_spoked_asterisk: " + bot_start[1], use_aliases=True))
    else:
        bot.send_message(message.chat.id, 'Не корректная ссылка на матч.')


bot.polling()
