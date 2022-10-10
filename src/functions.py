import os
import pickle
from os import listdir

from aiogram import types
from aiogram.types import Chat

from config import bot
from classes import Admin, Message_from_rec_channels


def text_is_channel_url(name: Chat | None) -> bool:
    try:
        if name.username is not None:
            return True
        else:
            return False
    except:
        return False


def get_tuple_data_for_mailing_mes(admin: Admin) -> tuple:
    text: str = admin.mailing_text
    keyboard: types.InlineKeyboardMarkup = None
    mailing_photo_path: str = None

    if admin.mailing_but_name is not None:
        keyboard = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text=admin.mailing_but_name,
                                                                                          url=admin.mailing_but_url))
    if admin.mailing_photo_path is not None:
        mailing_photo_path = admin.mailing_photo_path
    return text, keyboard, mailing_photo_path


async def mailing_all_users(users_list: list, tuple_data_for_mailing_mes) -> None:
    for user_id in users_list:
        try:
            if tuple_data_for_mailing_mes[2] is not None:
                await bot.send_photo(chat_id=user_id,
                                     photo=tuple_data_for_mailing_mes[2],
                                     caption=tuple_data_for_mailing_mes[0],
                                     reply_markup=tuple_data_for_mailing_mes[1])
            else:
                await bot.send_message(chat_id=user_id,
                                       text=tuple_data_for_mailing_mes[0],
                                       reply_markup=tuple_data_for_mailing_mes[1])
        except:
            pass


def valid_url(url: str) -> bool:
    if "https://" or "http://" in url:
        return True
    else:
        return False


async def get_media(message_text: str | None, onlyfiles: list, folder: str = "фото") -> types.MediaGroup():
    media = types.MediaGroup()

    s = [".mp4", ".mpeg", ".mpg", ".webm"]

    for file in range(len(onlyfiles)):
        if file != (len(onlyfiles)) - 1:
            for i in s:
                if i in onlyfiles[file]:
                    media.attach_video(video=types.InputFile(f"./{folder}/{onlyfiles[file]}"))
                    break
            else:
                media.attach_photo(photo=types.InputFile(f"./{folder}/{onlyfiles[file]}"))
        else:
            for i in s:
                if i in onlyfiles[file]:
                    media.attach_video(video=types.InputFile(f"./{folder}/{onlyfiles[file]}"),
                                       caption=message_text)
                    break
            else:
                media.attach_photo(photo=types.InputFile(f"./{folder}/{onlyfiles[file]}"),
                                   caption=message_text)

    return media


def download_media(self, media_id):
    try:
        msg_media_id = int(media_id)
        output = str('usermedia/{}'.format(msg_media_id))
        print('Downloading media wit   h name {}...'.format(output))
        output = self.client.download_msg_media(
            msg_media_id,
            file_path=output,
            progress_callback=self.client2.download_progress_callback)
        print('Media downloaded to {}!'.format(output))

    except ValueError:
        print('Invalid media ID given!')