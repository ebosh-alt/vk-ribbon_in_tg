from os import listdir
import os
from aiogram import types
from aiogram.types import Chat

from config import bot, ban_words, format_file
from classes import Admin, Message_from_rec_channels


# from src.config import messages_from_rec_channels


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
    if "https://" in url or "http://" in url:
        return True
    else:
        return False


async def get_media(message_text: str | None, onlyfiles: list, folder: str = "фото",
                    media: None | types.MediaGroup = None) -> types.MediaGroup():
    if media is None:
        media = types.MediaGroup()

    for file in range(len(onlyfiles)):
        if file != (len(onlyfiles)) - 1:
            for i in format_file:
                if i in onlyfiles[file]:
                    media.attach_video(video=types.InputFile(f"./{folder}/{onlyfiles[file]}"))
                    break
            else:
                media.attach_photo(photo=types.InputFile(f"./{folder}/{onlyfiles[file]}"))
        else:
            for i in format_file:
                if i in onlyfiles[file]:
                    media.attach_video(video=types.InputFile(f"./{folder}/{onlyfiles[file]}"),
                                       caption=message_text,
                                       parse_mode="Markdown")
                    continue
            else:
                media.attach_photo(photo=types.InputFile(f"./{folder}/{onlyfiles[file]}"),
                                   caption=message_text,
                                   parse_mode="Markdown")

    return media


def check_text(text: str):
    if text is not None:
        if len(text) > 1:
            return True


def media_presence_check(messages_from_rec_channels, group_id: int | None, id: str | None, text: str | None) -> bool:
    if group_id is None:
        if id not in messages_from_rec_channels:
            # if check_text(text=text):
            #     if check_advertising(text.lower()):
            return True
    return False


# def clearing_queue(messages_from_rec_channels):
#     if len(messages_from_rec_channels) > 300:
#         del messages_from_rec_channels[list(messages_from_rec_channels.keys())[0]]


def get_check_format(file: str) -> bool:
    for i in format_file:
        if i in file:
            return True

    return False


def check_advertising(text: str):
    for word in ban_words:
        if word in text:
            return False
    return True


def del_folder(needed_folder: str) -> None:
    files = [f for f in listdir(f"./rec/{needed_folder}")]
    for file in files:
        os.remove(f"./rec/{needed_folder}/{file}")
    os.rmdir(f"./rec/{needed_folder}")


def get_media_(needed_folder: str, message_text: str | None) -> types.MediaGroup():
    files = [f for f in listdir(f"./rec/{needed_folder}")]
    if len(files) == 1:

        for i in format_file:
            if i in files[0]:

                return types.InputFile(f"./rec/{needed_folder}/{files[0]}"), "video"
        return types.InputFile(f"./rec/{needed_folder}/{files[0]}"), "photo"

    media = types.MediaGroup()
    for file in range(len(files)):
        if file != (len(files)) - 1:
            for i in format_file:
                if i in files[file]:
                    media.attach_video(video=types.InputFile(f"./rec/{needed_folder}/{files[file]}"))
                    break
            else:
                media.attach_photo(photo=types.InputFile(f"./rec/{needed_folder}/{files[file]}"))
        else:
            for i in format_file:
                if i in files[file]:
                    media.attach_video(video=types.InputFile(f"./rec/{needed_folder}/{files[file]}"),
                                       caption=message_text,
                                       parse_mode="Markdown")
                    break
            else:
                media.attach_photo(photo=types.InputFile(f"./rec/{needed_folder}/{files[file]}"),
                                   caption=message_text,
                                   parse_mode="Markdown")
    return media


def delete_all_channel_folders(channel_key: int, messages_from_rec_channels: Message_from_rec_channels):
    for rec_message_key in messages_from_rec_channels.get_keys():
        if channel_key == rec_message_key.split("+")[0]:
            del messages_from_rec_channels[rec_message_key]
            del_folder(needed_folder=rec_message_key)


