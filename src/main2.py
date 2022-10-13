import asyncio
import time
import random

import schedule

from asyncio import run
from multiprocessing import Process
from aiogram.utils import executor
from telethon import TelegramClient

from config import *
from texts import *
from functions import *
from keyboard import *


@dp.message_handler(commands=["start"])
async def start(message):
    global users, admins
    user_id = message.from_user.id
    user = users.get_elem(user_id)
    admin = admins.get_elem(id=user_id)
    while True:
        await bot.send_message(chat_id=754513655,
                               text="!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if admin:
        admin.flag = 0
        admin.mailing_text = None
        admin.new_instruction_text = {"ru": None, "en": None, }
        admin.bot_messageId = None
        admin.keyboard_point = 0
        admin.mailing_message_id = None

    if not user:
        user = User(key=user_id, )
        user.registration_date = int(time.time())
        users.add_user(user=user)
        new_mes = await bot.send_message(chat_id=user_id,
                                         text=start_text[user.language],
                                         reply_markup=lang_set_keyboard[user.language])
    else:
        user.keyboard_point = 0
        new_mes = await bot.send_message(chat_id=user_id,
                                         text=start_text[user.language],
                                         reply_markup=lang_set_keyboard[user.language])
    user.flag = 1
    user.bot_messageId = new_mes.message_id

    users.update_info(user)




@dp.message_handler(commands=["del_keyboard", "keyboard"],)
async def keyboard_act(message: types.Message):
    global users
    user_id = message.from_user.id
    user = users.get_elem(user_id)
    if user.flag == 2:
        if message.text == "/del_keyboard":
            await message.reply(text=text_for_del_keyboard[user.language], reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.reply(text=text_for_add_keyboard[user.language], reply_markup=main_keyboard[user.language])
    else:
        await bot.send_message(chat_id=user_id,
                                text="Клавиатура не может быть удалена или добавлена")


@dp.message_handler(lambda message: admins.get_elem(message.from_user.id), commands=["admin"],
                    content_types=types.ContentTypes.ANY)
async def admin(message):
    global users, admins
    user_id = message.from_user.id
    user = users.get_elem(user_id)
    user.flag = 0
    user.keyboard_point = 0
    user.bot_messageId = None
    admin = admins.get_elem(message.from_user.id)
    new_mes = await bot.send_message(chat_id=user_id,
                                     text=admin_panel_main_text,
                                     reply_markup=admin_main_keyboard)
    admin.flag = 0
    admin.mailing_text = None
    admin.new_instruction_text = {"ru": None, "en": None, }
    admin.bot_messageId = new_mes.message_id
    admin.keyboard_point = 0
    admin.mailing_message_id = None
    admin.mailing_but_name = None
    admin.mailing_but_url = None
    admin.mailing_message_id = None
    admin.mailing_photo_path = None
    admin.mailing_text = None

    users.update_info(user)
    admins.update_info(admin)


@dp.callback_query_handler(
    lambda call: admins.get_elem(call.from_user.id) and call.data in ["mailing_admin", "statistics_admin",
                                                                      "instruction_admin", "recomendation_admin",
                                                                      "back_to_admin_panel"])
async def main_admin_panel(call):
    global admins, instruction_text
    user_id = call.from_user.id
    admin = admins.get_elem(id=user_id)

    if call.data == "mailing_admin":
        admin.flag = 3  # Ввод текста для рассылки
        admin.mailing_but_name = None
        admin.mailing_but_url = None
        admin.mailing_message_id = None
        admin.mailing_photo_path = None
        admin.mailing_text = None
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_1_text,
                                    reply_markup=back_to_admin_panel_keyboard)

    elif call.data == "statistics_admin":
        added_in_24_hours = 0
        added_in_7_days = 0
        added_in_month = 0
        for user_id_ in users.get_keys():
            user = users.get_elem(id=user_id_)
            if user.registration_date - int(time.time()) <= 86400:
                added_in_24_hours += 1
                added_in_7_days += 1
                added_in_month += 1
            elif user.registration_date - int(time.time()) <= 604800:
                added_in_7_days += 1
                added_in_month += 1
            elif user.registration_date - int(time.time()) <= 2687400:
                added_in_month += 1
        statistics = f"Всего пользователей: {len(users.get_keys())}\nДобавили за 24Ч:{added_in_24_hours}\nДобавили за 7 дней:{added_in_7_days}\nДобавили за месяц:{added_in_month}"
        print(user_id, admin.bot_messageId, statistics)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=statistics,
                                    reply_markup=back_to_admin_panel_keyboard)
    elif call.data == "instruction_admin":
        admin.flag = 1  # Ввод инструкции на русском
        admin.new_instruction_text = {"ru": None, "en": None, }
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=instruction_section_1_text,
                                    reply_markup=back_to_admin_panel_keyboard)
    elif call.data == "recomendation_admin":
        admin.flag = 8  # Раздел рекомендации
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=recomendations_section_1_text,
                                    reply_markup=recomendations_section_keyboard)

    elif call.data == "back_to_admin_panel":
        admin.flag = 0
        admin.mailing_text = None
        admin.new_instruction_text = {"ru": None, "en": None, }
        admin.keyboard_point = 0
        admin.mailing_message_id = None
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=admin_panel_main_text,
                                    reply_markup=admin_main_keyboard)
    admins.update_info(elem=admin)


@dp.callback_query_handler(
    lambda call: admins.get_elem(call.from_user.id) and call.data in ["add_rec_channels", "del_rec_channel",
                                                                      "stop_adding_rec_channels"])
async def recomendations_section(call):
    global admins, instruction_text
    user_id = call.from_user.id
    admin = admins.get_elem(id=user_id)
    if call.data == "add_rec_channels":
        admin.flag = 9  # Добавление рек канала
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=adding_new_channel_1_text["ru"],
                                    reply_markup=adding_new_rec_channel_keyboard)
    elif call.data == "stop_adding_rec_channels":
        admin.flag = 8
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=exit_adding_channel_text["ru"],
                                    reply_markup=recomendations_section_keyboard)

    elif call.data == "del_rec_channel":
        rec_channels = load_object()
        if len(rec_channels.links) == 0:
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=admin.bot_messageId,
                                        text="Нет рекомендованных каналов",
                                        reply_markup=recomendations_section_keyboard)
        else:
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=admin.bot_messageId,
                                        text="Рекомендации",
                                        reply_markup=rec_channels.get_channel_keyboard(user_point=admin.keyboard_point,
                                                                                       channel_dict=rec_channels.name_channel,
                                                                                       keyboard_length=count_of_buts_in_keyboard))

    admins.update_info(admin)


@dp.callback_query_handler(
    lambda call: admins.get_elem(call.from_user.id) and call.data in ["back_to_writing_en_instruction",
                                                                      "new_instruction_ready"])
async def instruction_section(call):
    global admins, instruction_text
    user_id = call.from_user.id
    admin = admins.get_elem(id=user_id)
    if call.data == "back_to_writing_en_instruction":
        admin.flag = 2  # !
        admin.new_instruction_text["en"] = None
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=instruction_section_2_text.format(
                                        ru_instruction=admin.new_instruction_text["ru"]),
                                    reply_markup=back_to_writing_ru_instruction_keyboard)
    elif call.data == "new_instruction_ready":
        instruction_text = admin.new_instruction_text
        admin.flag = 0
        admin.mailing_text = None
        admin.new_instruction_text = {"ru": None, "en": None, }
        admin.keyboard_point = 0
        admin.mailing_message_id = None
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text=notification_instruction_ready,
                                        show_alert=True)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=admin_panel_main_text,
                                    reply_markup=admin_main_keyboard)

    admins.update_info(elem=admin)


@dp.callback_query_handler(
    lambda call: admins.get_elem(call.from_user.id) and call.data in ["add_photo", "del_photo", "add_url_button",
                                                                      "del_url_button", "mailing_message_ready",
                                                                      "change_mailing_text",
                                                                      "back_to_mailing_section", ])
async def mailing_section(call):
    global admins, instruction_text
    user_id = call.from_user.id
    admin = admins.get_elem(id=user_id)
    try:
        await bot.delete_message(chat_id=user_id,
                                 message_id=admin.mailing_message_id, )
    except:
        pass
    if call.data == "add_photo":
        admin.flag = 5  # Добавление фото для рассылки
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_3_text,
                                    reply_markup=back_to_mailing_section_keyboard)

    elif call.data in ["del_photo", "del_url_button"]:
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        if call.data == "del_url_button":
            admin.mailing_but_name = None
            admin.mailing_but_url = None
            mailing_section_keyboard.add(mailing_section_add_url_but)
            if admin.mailing_photo_path is None:
                mailing_section_keyboard.add(mailing_section_add_photo_but)
            else:
                mailing_section_keyboard.add(mailing_section_del_photo_but)
        else:
            admin.mailing_photo_path = None
            mailing_section_keyboard.add(mailing_section_add_photo_but)
            if admin.mailing_but_name is None:
                mailing_section_keyboard.add(mailing_section_add_url_but)
            else:
                mailing_section_keyboard.add(mailing_section_del_url_but)

        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_2_text,
                                    reply_markup=mailing_section_keyboard.add(
                                        mailing_section_ready_but).add(
                                        mailing_section_change_mail_text_but))

        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        if tuple_data_for_mailing_mes[2] is not None:
            mailing_mes = await bot.send_photo(chat_id=user_id,
                                               photo=tuple_data_for_mailing_mes[2],
                                               caption=tuple_data_for_mailing_mes[0],
                                               reply_markup=tuple_data_for_mailing_mes[1])
        else:
            mailing_mes = await bot.send_message(chat_id=user_id,
                                                 text=tuple_data_for_mailing_mes[0],
                                                 reply_markup=tuple_data_for_mailing_mes[1])
        admin.mailing_message_id = mailing_mes.message_id

    elif call.data == "add_url_button":
        admin.flag = 6  # Добавление кнопки для рассылки(ссылка)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_4_text,
                                    reply_markup=back_to_mailing_section_keyboard)
    elif call.data == "mailing_message_ready":
        await mailing_all_users(users_list=users.get_keys(),
                                tuple_data_for_mailing_mes=get_tuple_data_for_mailing_mes(admin=admin))
        await bot.answer_callback_query(callback_query_id=call.id,
                                        text="Рассылка",
                                        show_alert=True)
        admin.flag = 0
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=admin_panel_main_text,
                                    reply_markup=admin_main_keyboard)
        admin.mailing_text = None
        admin.new_instruction_text = {"ru": None, "en": None, }
        admin.keyboard_point = 0
        admin.mailing_message_id = None
        ###
    elif call.data == "change_mailing_text":
        admin.flag = 3  # Ввод текста для рассылки
        admin.mailing_but_name = None
        admin.mailing_but_url = None
        admin.mailing_message_id = None
        admin.mailing_photo_path = None
        admin.mailing_text = None
        try:
            await bot.delete_message(chat_id=user_id,
                                     message_id=admin.mailing_message_id)
        except:
            pass
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_1_text,
                                    reply_markup=back_to_admin_panel_keyboard)
    elif call.data == "back_to_mailing_section":
        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        if admin.mailing_photo_path is None:
            mailing_section_keyboard.add(mailing_section_add_photo_but)
            mailing_mes = await bot.send_message(chat_id=user_id,
                                                 text=tuple_data_for_mailing_mes[0],
                                                 reply_markup=tuple_data_for_mailing_mes[1])
        else:
            mailing_section_keyboard.add(mailing_section_del_photo_but)
            mailing_mes = await bot.send_photo(chat_id=user_id,
                                               photo=tuple_data_for_mailing_mes[2],
                                               caption=tuple_data_for_mailing_mes[0],
                                               reply_markup=tuple_data_for_mailing_mes[1])
        admin.mailing_message_id = mailing_mes.message_id
        if admin.mailing_but_name is None:
            mailing_section_keyboard.add(mailing_section_add_url_but)
        else:
            mailing_section_keyboard.add(mailing_section_del_url_but)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_2_text,
                                    reply_markup=mailing_section_keyboard.add(
                                        mailing_section_ready_but).add(
                                        mailing_section_change_mail_text_but))

    admins.update_info(elem=admin)


# @dp.message_handler(lambda message: message.from_user.id in admins, content_types=["photo"])
# async def mailing_section_add_photo(message):
#     global admins, instruction_text
#     if admins.get_elem(message.from_user.id).flag == 5:
#         user_id = message.from_user.id
#         admin = admins.get_elem(id=user_id)
#         try:
#             await bot.delete_message(chat_id=user_id,
#                                      message_id=message.id)
#         except:
#             pass
#         admin.mailing_photo_path = await bot.download_file(
#             bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path)
#         tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
#         mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
#         mailing_section_keyboard.add(mailing_section_del_photo_but)
#         if admin.mailing_but_name == None:
#             mailing_section_keyboard.add(mailing_section_add_url_but)
#         else:
#             mailing_section_keyboard.add(mailing_section_del_url_but)
#         await bot.edit_message_text(chat_id=user_id,
#                                     message_id=admin.bot_messageId,
#                                     text=mailing_section_2_text,
#                                     reply_markup=mailing_section_keyboard.add(
#                                         mailing_section_ready_but).add(
#                                         mailing_section_change_mail_text_but))
#         mailing_mes = await bot.send_photo(chat_id=user_id,
#                                            photo=tuple_data_for_mailing_mes[2],
#                                            caption=tuple_data_for_mailing_mes[0],
#                                            reply_markup=tuple_data_for_mailing_mes[1])
#
#         admin.mailing_message_id = mailing_mes.id
#         admin.flag = 4
#         admins.update_info(elem=admin)


@dp.message_handler(
    lambda message: admins.get_elem(message.from_user.id) and users.get_elem(message.from_user.id).flag == 0,
    content_types=types.ContentTypes.ANY)
async def data_entry_by_admin(message):
    global admins, rec_channels
    user_id = message.from_user.id
    admin = admins.get_elem(id=user_id)
    flag = admin.flag

    try:
        if flag != 9:
            await bot.delete_message(chat_id=user_id, message_id=message.message_id)
    except:
        pass

    if flag == 1:
        admin.new_instruction_text["ru"] = message.text
        admin.flag = 2
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=instruction_section_2_text.format(
                                        ru_instruction=admin.new_instruction_text["ru"]),
                                    reply_markup=back_to_writing_ru_instruction_keyboard)
    elif flag == 2:
        admin.new_instruction_text["en"] = message.text
        admin.flag = 0
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=instruction_section_3_text.format(
                                        ru_instruction=admin.new_instruction_text["ru"],
                                        en_instruction=admin.new_instruction_text["en"]),
                                    reply_markup=instruction_section_last_keyboard)

    elif flag == 3:
        admin.flag = 4  # Выбор действия в разделе рассылки
        admin.mailing_text = message.text
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_2_text,
                                    reply_markup=mailing_section_keyboard.add(
                                        mailing_section_add_photo_but).add(
                                        mailing_section_add_url_but).add(
                                        mailing_section_ready_but).add(
                                        mailing_section_change_mail_text_but))
        mailing_mes = await bot.send_message(chat_id=user_id,
                                             text=message.text)
        admin.mailing_message_id = mailing_mes.message_id

    elif flag == 5:
        admin.mailing_photo_path = await bot.download_file(
            bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path)
        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        mailing_section_keyboard.add(mailing_section_del_photo_but)
        if admin.mailing_but_name == None:
            mailing_section_keyboard.add(mailing_section_add_url_but)
        else:
            mailing_section_keyboard.add(mailing_section_del_url_but)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_2_text,
                                    reply_markup=mailing_section_keyboard.add(
                                        mailing_section_ready_but).add(
                                        mailing_section_change_mail_text_but))
        mailing_mes = await bot.send_photo(chat_id=user_id,
                                           photo=tuple_data_for_mailing_mes[2],
                                           caption=tuple_data_for_mailing_mes[0],
                                           reply_markup=tuple_data_for_mailing_mes[1])

        admin.mailing_message_id = mailing_mes.message_id
        admin.flag = 4
        admins.update_info(elem=admin)
    elif flag == 6:
        if valid_url(message.text):
            admin.mailing_but_url = message.text
            admin.flag = 7
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=admin.bot_messageId,
                                        text=mailing_section_5_text.format(mailing_url_but=admin.mailing_but_url),
                                        reply_markup=back_to_mailing_section_keyboard)
        else:
            admin.flag = 6
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=admin.bot_messageId,
                                        text=mailing_section_4_text,
                                        reply_markup=back_to_mailing_section_keyboard)
    elif flag == 7:
        admin.mailing_but_name = message.text
        admin.flag = 4
        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        mailing_section_keyboard.add(mailing_section_del_url_but)
        if admin.mailing_photo_path is None:
            mailing_section_keyboard.add(mailing_section_add_photo_but)
        else:
            mailing_section_keyboard.add(mailing_section_del_photo_but)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=admin.bot_messageId,
                                    text=mailing_section_2_text,
                                    reply_markup=mailing_section_keyboard.add(
                                        mailing_section_ready_but).add(
                                        mailing_section_change_mail_text_but))
        if admin.mailing_photo_path is None:
            mailing_mes = await bot.send_message(chat_id=user_id,
                                                 text=tuple_data_for_mailing_mes[0],
                                                 reply_markup=tuple_data_for_mailing_mes[1])
        else:
            mailing_mes = await bot.send_photo(chat_id=user_id,
                                               photo=tuple_data_for_mailing_mes[2],
                                               caption=tuple_data_for_mailing_mes[0],
                                               reply_markup=tuple_data_for_mailing_mes[1])

        admin.mailing_message_id = mailing_mes.message_id

    elif flag == 9:
        if text_is_channel_url(message.forward_from_chat):
            link = f"https://t.me/{message.forward_from_chat.username}"
            message_from_rec_channels = load_object()
            if link not in message_from_rec_channels.links:
                message_from_rec_channels.add_link(link=link)
                message_from_rec_channels.add_channel_name(name_channel=message.forward_from_chat.title,
                                                           link=link)

                save_object(file_name="message_from_rec_channel.pkl",
                            data=message_from_rec_channels)

                await bot.send_message(chat_id=user_id,
                                       text="Мы успешно добавили канал/группу в рекомендации")

                mes = await bot.send_message(chat_id=user_id,
                                             text="Перешлите сообщение из нужного Вам канала",
                                             reply_markup=adding_new_rec_channel_keyboard)
                admin.bot_messageId = mes.message_id


        else:
            await bot.send_message(chat_id=user_id,
                                   text=adding_new_channel_3_text["ru"],
                                   reply_markup=adding_new_channel_keyboard["ru"])

    admins.update_info(elem=admin)


@dp.callback_query_handler(lambda call: "channels_" in call.data)
async def delete_channels(call: types.CallbackQuery):
    global admins, channels, users
    user_id = call.from_user.id
    if "rec_channels" in call.data:
        rec_channels = load_object()
        admin = admins.get_elem(user_id)
        if ">" in call.data:
            if admin.keyboard_point + count_of_buts_in_keyboard >= Recomended_channels.count:
                pass
            else:
                admin.keyboard_point += count_of_buts_in_keyboard
        elif "<" in call.data:
            if admin.keyboard_point - count_of_buts_in_keyboard < 0:
                pass
            else:
                admin.keyboard_point -= count_of_buts_in_keyboard
        else:
            rec_channels.del_channel(str(call.data).split("_")[-1])
            if admin.keyboard_point == Recomended_channels.count:
                admin.keyboard_point -= count_of_buts_in_keyboard
            save_object(data=rec_channels)
        if len(rec_channels.links) == 0:
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=admin.bot_messageId,
                                        text="Рекомендации отсутствуют",
                                        reply_markup=recomendations_section_keyboard)
        else:
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=admin.bot_messageId,
                                        text="Рекомендации",
                                        reply_markup=rec_channels.get_channel_keyboard(user_point=admin.keyboard_point,
                                                                                       channel_dict=rec_channels.name_channel,
                                                                                       keyboard_length=count_of_buts_in_keyboard))
        admins.update_info(admin)
    else:
        user = users.get_elem(user_id)
        if ">" in call.data:
            if user.keyboard_point + count_of_buts_in_keyboard >= Channels.count:
                pass
            else:
                user.keyboard_point += count_of_buts_in_keyboard
        elif "<" in call.data:
            if user.keyboard_point - count_of_buts_in_keyboard < 0:
                pass
            else:
                user.keyboard_point -= count_of_buts_in_keyboard
        else:
            # channel = channels.get_channel(int(str(call.data).split("_")[-1]))
            ch_id = int(str(call.data).split("_")[-1])
            channels.del_user(id=ch_id,
                              user_id=user_id)
            del user.channels[user.channels.index(ch_id)]
            if user.keyboard_point == Channels.count:
                user.keyboard_point -= count_of_buts_in_keyboard
                if user.keyboard_point < 0:
                    user.keyboard_point = 0
        if len(user.channels) == 0:
            # print(user.bot_messageId, " : ", call.message.message_id)
            user.bot_messageId = call.message.message_id
            await bot.answer_callback_query(callback_query_id=call.id,
                                            text="Канал удален")
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=user.bot_messageId,
                                        text="У вас нет ни одного канал")  ######## en
        else:
            user.bot_messageId = call.message.message_id
            await bot.edit_message_text(chat_id=user_id,
                                        message_id=user.bot_messageId,
                                        text=veiw_delete_channel_text[user.language],
                                        reply_markup=channels.get_channel_keyboard(user_point=user.keyboard_point,
                                                                                   channel_list=user.channels,
                                                                                   keyboard_length=count_of_buts_in_keyboard))

        users.update_info(user)


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def start_logic(message: types.Message):
    global users, channels, admins
    user_id = message.from_user.id
    user = users.get_elem(user_id)
    if user_id in admins:
        admin = admins.get_elem(user_id)
        if admin.flag != 0:
            admin.flag = 0
            admins.update_info(elem=admin)

    if user.flag == 1:
        if message.text in ["Русский", "Russian"]:
            user.language = "ru"
            user.flag = 2
            await bot.send_message(chat_id=user_id,
                                   text=after_lang_choose_text[user.language],
                                   reply_markup=main_keyboard[user.language])

            mes = await bot.send_message(chat_id=user_id,
                                         text=instruction_text[user.language],
                                         reply_markup=change_lang_keyboard[user.language])


        elif message.text in ["Английский", "English"]:
            user.language = "en"
            user.flag = 2
            await bot.send_message(chat_id=user_id,
                                   text=after_lang_choose_text[user.language],
                                   reply_markup=main_keyboard[user.language])
            await bot.send_message(chat_id=user_id,
                                   text=instruction_text[user.language],
                                   reply_markup=change_lang_keyboard[user.language])
        else:
            pass
    elif user.flag == 2:
        if message.text in ["Инструкция", "Instruction"]:
            await bot.send_message(chat_id=user_id,
                                   text=instruction_text[user.language],
                                   reply_markup=change_lang_keyboard[user.language])
        elif message.text in ["Добавить подписки", "Add"]:
            user.flag = 3
            await bot.send_message(chat_id=user_id,
                                   text=adding_new_channel_1_text[user.language],
                                   reply_markup=adding_new_channel_keyboard[user.language])
        elif message.text in ["Мои подписки", "My"]:
            if len(user.channels) == 0:
                await bot.send_message(chat_id=user_id,
                                       text=absense_subcription_text[user.language])
            else:
                await bot.send_message(chat_id=user_id,
                                       text=veiw_delete_channel_text[user.language],
                                       reply_markup=channels.get_channel_keyboard(user_point=user.keyboard_point,
                                                                                  channel_list=user.channels,
                                                                                  keyboard_length=count_of_buts_in_keyboard))
        elif message.text in ["Рекомендации", "Rec"]:
            message_from_rec_channel = load_object(file_name="message_from_rec_channel.pkl")
            client = TelegramClient("assahit", api_id, api_hash)
            await client.start(phone=phone_number)
            if len(message_from_rec_channel.data) < 16:
                for i in message_from_rec_channel.data:
                    channel = message_from_rec_channel.get_elem(i)
                    if len(channel.list_object) != 0:
                        # for obj in channel.list_object:
                            # try:
                            #     await client.download_media(message=obj, file=f'./rec/{user_id}/')
                            # except:
                            #     pass

                        # onlyfiles = [f for f in listdir(f"./rec/{user_id}")]
                        # media = await get_media(message_text=channel.message_text,
                        #                         onlyfiles=onlyfiles,
                        #                         folder=f"rec/{user_id}")

                        messages = await bot.send_media_group(chat_id=user_id,
                                                              media=channel.media,
                                                              parse_mode="Markdown",
                                                              disable_web_page_preview=False)
                        for mes in messages:
                            user.messages_to_del.append(mes.message_id)
                        users.update_info(elem=user)
                        # for file in onlyfiles:
                        #     os.remove(f"./rec/{user_id}/{file}")
                    else:
                        await bot.send_message(chat_id=user_id,
                                               text=channel.message_text,
                                               parse_mode="Markdown",
                                               disable_web_page_preview=False)
            else:
                channels_to_rec = []
                while len(channels_to_rec) < 16:
                    message = random.choice(list(message_from_rec_channel.data.values()))
                    if message not in channels_to_rec:
                        channels_to_rec.append(message)

                for channel in channels_to_rec:
                    if len(channel.list_object) != 0:
                        # for obj in channel.list_object:
                        #     try:
                        #         await client.download_media(message=obj, file=f"./rec/{user_id}/")
                        #     except:
                        #         pass
                        #
                        # onlyfiles = [f for f in listdir(f"./rec/{user_id}")]
                        # media = await get_media(message_text=channel.message_text,
                        #                         onlyfiles=onlyfiles,
                        #                         folder=f"./rec/{user_id}")
                        try:
                            messages = await bot.send_media_group(chat_id=user_id,
                                                                  media=channel.media)

                            for mes in messages:
                                user.messages_to_del.append(mes.message_id)
                            users.update_info(elem=user)
                        except:
                            pass
                        # for file in onlyfiles:
                        #     os.remove(f"./rec/{user_id}/{file}")
                    else:
                        try:
                            await bot.send_message(chat_id=user_id,
                                                   text=channel.message_text,
                                                   parse_mode="Markdown",
                                                   disable_web_page_preview=True)
                        except:
                            pass
            await client.disconnect()

    elif user.flag == 3:
        if message.text in ["Продолжить", "Continue"]:
            user.flag = 2
            await bot.send_message(chat_id=user_id,
                                   text=exit_adding_channel_text[user.language],
                                   reply_markup=main_keyboard[user.language])

        elif text_is_channel_url(message.forward_from_chat):
            keys = channels.get_keys()
            for key in keys:
                channel = channels.get_channel(key)
                if channel.name == message.forward_from_chat.title:
                    break

            else:
                channel = Channel(key=channels.count)
                link = f"https://t.me/{message.forward_from_chat.username}"
                channel.name = message.forward_from_chat.title
                channel.url = link
                channel.chat_id = message.forward_from_chat.id
                channels.add_channel(channel=channel)

            if message.from_user.id not in channel.users:
                channel.users.append(message.from_user.id)
                channels.update_info(elem=channel)

                await bot.send_message(chat_id=user_id,
                                       text=adding_new_channel_2_text[user.language],
                                       reply_markup=adding_new_channel_keyboard[user.language])
                await bot.send_message(chat_id=user_id,
                                       text=adding_new_channel_1_text[user.language],
                                       reply_markup=adding_new_channel_keyboard[user.language])
                await asyncio.sleep(0)

            if channel.key not in user.channels:
                user.channels.append(channel.key)

        else:
            await bot.send_message(chat_id=user_id,
                                   text=adding_new_channel_3_text[user.language],
                                   reply_markup=adding_new_channel_keyboard[user.language])

    users.update_info(user)


@dp.callback_query_handler(lambda call: call.data == "change_lang")
async def change_lang(call):
    global users
    user_id = call.from_user.id
    user = users.get_elem(user_id)
    if user.language == "ru":
        user.language = "en"
    elif user.language == "en":
        user.language = "ru"
    await bot.send_message(chat_id=user_id,
                           text=instruction_text[user.language],
                           reply_markup=change_lang_keyboard[user.language])
    await bot.send_message(chat_id=user_id,
                           text=after_lang_choose_text[user.language],
                           reply_markup=main_keyboard[user.language])

    users.update_info(user)


async def on_startup(dispatcher): await bot.set_webhook(web_link, drop_pending_updates=True)


async def on_shutdown(dispatcher): await bot.delete_webhook()


class BackGroundProcess:
    def __init__(self) -> None:
        self.p0 = Process()

    def start_process(self, func):
        self.p0 = Process(target=func)
        self.p0.start()
        print("back to main")

    def stop_process(self):
        self.p0.terminate()


def client_main():
    while True:
        print("client is working")
        time.sleep(10)


class Cleaner(BackGroundProcess):
    def __init__(self) -> None:
        BackGroundProcess.__init__(self)

    @staticmethod
    async def clean():
        global users, admins_list
        users_list = users.get_keys()
        for user_id in users_list:
            user = users.get_elem(user_id)
            mes_id_index = 0
            # for mes_id_index in range(len(user.messages_to_del)):
            while mes_id_index < len(user.messages_to_del):
                mes_id = user.messages_to_del[mes_id_index]
                try:
                    await bot.delete_message(
                        chat_id=user_id,
                        message_id=mes_id
                    )
                    del user.messages_to_del[mes_id_index]
                    users.update_info(user)
                except Exception as ex:
                    del user.messages_to_del[mes_id_index]
                    users.update_info(user)
                    await bot.send_message(
                        chat_id=admins_list[0],
                        text=f"user_id: {user_id}\nclass_name: {ex.__class__.__name__}\n{ex}",
                    )
                finally:
                    mes_id_index += 1

    def start_schedule(self):
        schedule.every().minute.do(job_func=self.clean)
        while True:
            print("cleaner has been worked")
            schedule.run_pending()
            time.sleep(100)


class Get_new_message(BackGroundProcess):
    def __init__(self) -> None:
        BackGroundProcess.__init__(self)

    @staticmethod
    async def get_new_message():
        global channels, users
        channels_list = channels.get_keys()
        client = TelegramClient("mkmkmkmosdlsmkmkkmkmkmdlmdlmoaaaosqwqhit", api_id, api_hash)
        await client.start(phone=phone_number)
        for key in channels_list:
            channel = channels.get_channel(key)
            new_message = await client.get_messages(channel.url, limit=1)

            if channel.last_id_mes is None:
                channel.last_id_mes = new_message[0].id
                channels.update_info(channel)

            elif channel.last_id_mes < new_message[0].id:
                limit = new_message[0].id - channel.last_id_mes
                channel.last_id_mes = new_message[0].id
                grouped_id = 0
                message_text = None

                channels.update_info(channel)
                new_message = await client.get_messages(channel.url, limit=limit)
                for message in new_message:
                    if message.media is None:
                        for user_id in channel.users:
                            mes = await bot.send_message(chat_id=user_id,
                                                         text=message.text)
                            user = users.get_elem(user_id)
                            user.messages_to_del.append(mes.message_id)
                            users.update_info(elem=user)

                    if message.media is not None:
                        if len(message.text) > 0:
                            if check_advertising(message.text.lower()):
                                message_text = message.text
                            else:
                                onlyfiles = [f for f in listdir(f"./фото/")]
                                for file in onlyfiles:
                                    os.remove(f"./фото/{file}")
                                break
                        if grouped_id == 0:
                            grouped_id = message.grouped_id
                        if grouped_id == message.grouped_id:
                            await message.download_media("./фото/")

                        if grouped_id != message.grouped_id or message.id + limit - 1 == channel.last_id_mes:
                            onlyfiles = [f for f in listdir(f"./фото/")]
                            for user_id in channel.users:
                                user = users.get_elem(user_id)

                                if user.flag != 3:
                                    if user_id in admins:
                                        admin = admins.get_elem(user_id)
                                        if admin.flag == 9:
                                            continue
                                    media = await get_media(message_text=message_text, onlyfiles=onlyfiles)
                                    mes = await bot.send_media_group(chat_id=user_id,
                                                                     media=media)
                                    for i in mes:
                                        user.messages_to_del.append(i.message_id)
                                    users.update_info(elem=user)

                            for file in onlyfiles:
                                os.remove(f"./фото/{file}")

                            grouped_id = 0
                            message_text = None

        await client.disconnect()

    @staticmethod
    async def get_rec_mes():
        onlyfiles = [f for f in listdir(f"./rec/")]
        for file in onlyfiles:
            files = [f for f in listdir(f"./rec/{file}")]
            for i in files:
                os.remove(f"./rec/{file}/{i}")
        client = TelegramClient("assahit", api_id, api_hash)
        await client.start(phone=phone_number)
        messages_from_rec_channels = load_object()
        links = messages_from_rec_channels.get_array_link()
        for link in links:
            if links[link] == -1:
                new_messages = await client.get_messages(link, limit=100, min_id=1)
            else:
                new_messages = await client.get_messages(link, limit=50, min_id=links[link])

            for message in new_messages:
                save_messages = messages_from_rec_channels.get_data()
                if message.grouped_id is None:
                    if check_advertising(message.text.lower()):
                        messages_from_rec_channels.add_elem(group_id=message.id,
                                                            elem=Message_from_rec_channel())
                        new_message = messages_from_rec_channels.get_elem(key=message.id)
                        new_message.time = message.date
                        new_message.list_id.append(message.id)

                        new_message.set_message_text(message.text)
                else:
                    if check_advertising(message.text.lower()):
                        if message.grouped_id not in save_messages:
                            messages_from_rec_channels.add_elem(group_id=message.grouped_id,
                                                                elem=Message_from_rec_channel())


                        new_message = messages_from_rec_channels.get_elem(key=message.grouped_id)

                        if len(message.message) > 0 and message.id not in new_message.list_id:
                            new_message.set_message_text(text=message.message)

                        if message.media is not None and message.id not in new_message.list_id:
                            print(message.media)
                            await client.download_media(file=f"./rec/{message.grouped_id}/", message=message.media)
                            onlyfiles = [f for f in listdir(f"./rec/{message.grouped_id}")]
                            new_message.media = await get_media(message_text=new_message.message_text,
                                                                onlyfiles=onlyfiles,
                                                                folder=f"rec/{message.grouped_id}",
                                                                media=new_message.media)
                            # new_message.add_elem(elem=message.media)
                            new_message.time = message.date

                        if message.id < links[link]:
                            messages_from_rec_channels.set_min_id(key=link, min_id=message.id)

                        new_message.list_id.append(message.id)

        save_object(messages_from_rec_channels)
        await client.disconnect()

    def start_schedule(self):
        while True:
            run(self.get_new_message())
            # run(self.get_rec_mes())
            time.sleep(10)


class Cleaner_mes_rec(BackGroundProcess):
    def __init__(self) -> None:
        BackGroundProcess.__init__(self)

    @staticmethod
    async def cleaner():
        messages_from_rec_channels = load_object(file_name="message_from_rec_channel.pkl")
        time_now = datetime.datetime.now(tz=datetime.timezone.utc)
        list_to_del = []
        for group_id in messages_from_rec_channels.data:
            message = messages_from_rec_channels.get_elem(key=group_id)
            if time_now - days_for_mes_rec > message.time:
                list_to_del.append(group_id)

        for group_id in list_to_del:
            del messages_from_rec_channels.data[group_id]
        save_object(data=messages_from_rec_channels)

    def start_schedule(self):
        while True:
            # run(self.get_new_message())
            run(self.cleaner())
            time.sleep(100)


async def main():
    while True:
        await bot.send_message(chat_id=754513655,
                                         text="Работает")



if __name__ == "__main__":
    # get_new_message = Get_new_message()
    # get_new_message.start_process(func=get_new_message.start_schedule)
    # cleaner_mes_rec = Cleaner_mes_rec()
    # cleaner_mes_rec.start_process(func=cleaner_mes_rec.start_schedule)
    # cleaner = Cleaner()/
    # cleaner.start_process(func=cleaner.start_schedule)
    #
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    executor.start_polling(dp, skip_updates=False)
