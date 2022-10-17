import datetime
import logging
import pickle

from aiogram import Bot, Dispatcher
from flask import Flask
from classes import *


def save_object(data, file_name="message_from_rec_channel.pkl") -> None:
    with open(file_name, "wb+") as fp:
        pickle.dump(data, fp, protocol=5)


def load_object(file_name="message_from_rec_channel.pkl") -> Message_from_rec_channels:
    with open(file_name, "rb+") as fp:
        data = pickle.load(fp)
    return data


API_TOKEN = "5333826486:AAE7DIzcz6Fv84X453UyLsCpt5MYA2QMaY0"

# bot = telebot.TeleBot(token=API_TOKEN)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
web_path = f"/{API_TOKEN}/"
web_link = f"https://2345-2a00-1370-817e-4c0c-c15f-fcee-4f72-ee42.ngrok.io{web_path}"

app = Flask(__name__)

db_file_name = "db.db"

# users
users_table_name = "users"
users_args = {
    'key': 'integer',
    'flag': 'integer',
    'bot_messageId': 'integer',
    'language': 'text',
    'messages_to_del': "blob",
    'channels': "blob",
    'keyboard_point': 'integer',
    'messages_queue': 'blob',
    'registration_date': 'integer',
}
users = Users(db_file_name=db_file_name, args=users_args, table_name=users_table_name)

# admins
admins_table_name = "admins"
admins_args = {
    'key': 'integer',
    'flag': 'integer',
    'mailing_text': 'text',
    'new_instruction_text': 'blob',
    'bot_messageId': 'integer',
    'keyboard_point': 'integer',
    'mailing_message_id': 'integer',
    'mailing_photo_path': 'text',
    'mailing_but_name': 'text',
    'mailing_but_url': 'text',
}
admins = Admins(db_file_name=db_file_name, args=admins_args, table_name=admins_table_name)

admins_list = [754513655, 943588580, 1540836120, 5471804413, 686171972]
for admin_id in admins_list:
    if admin_id not in admins:
        admin = Admin(key=admin_id)
        admins.add_admin(admin=admin)

# channels
channels_table_name = "channels"
channels_args = {
    'key': 'integer',
    'users': 'blob',
    'url': 'text',
    'name': 'text',
    "chat_id": "integer",
    "last_id_mes": "integer",
}
channels = Channels(db_file_name=db_file_name, args=channels_args, table_name=channels_table_name)
Channels.count = len(channels.get_keys())

# rec_channels
rec_channels_table_name = "rec_channels"
rec_channels_args = {
    'key': 'integer',
    'url': 'text',
    'name': 'text',
    'min_id': 'integer',
}

rec_channels = Recomended_channels(db_file_name=db_file_name, args=rec_channels_args,
                                   table_name=rec_channels_table_name)
Recomended_channels.count = len(rec_channels.get_keys())




messages_from_rec_channels = Message_from_rec_channels()#load_object(file_name="message_from_rec_channel.pkl")


api_id = 18142706
api_hash = 'e9b070e6aee05f5437936312e49b6e45'
phone_number = "+79952605482"

# length_keyboard
count_of_buts_in_keyboard = 7
days_for_mes_rec = datetime.timedelta(days=3)

ban_words = ["регистрируйся", "регистрируюся", "подпишись", "переходи", "ссылка на подписку",
             "жми на кнопочку", "перейди", "огромный ассортимент", "скидки в директе и лс", "держи ссылку",
             "скидка при первом заказе", "множество гарантий и довольных клиентов", "самые отзывчивые менеджеры",
             "помогут подобрать лук", "обзоры вещей в reels", "можем найти почти любую вещь с интернета по фото"]


if __name__ == "__main__":
    channel = Recomended_channel()
    channel.key = 0
    channel.name = "name"
    channel.url = "url"
    rec_channels.add_channel(channel=channel)
