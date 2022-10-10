import asyncio
import multiprocessing
from threading import Thread

import aioschedule
from flask import request
from telethon import events

from config import *
from texts import *
from keyboard import *
from functions import *
from telethon.tl.functions.channels import JoinChannelRequest
from asyncio import set_event_loop, new_event_loop


@app.route(f'/{API_TOKEN}', methods=["POST", "GET"])
def handle():
    json_string = request.get_data().decode('utf-8')
    # save_data(json_string, 'json_string.json')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/start_client",methods=["POST", "GET"])
def st_client():
    client.loop.run_forever()


async def add_in_channel(link: str, *args):
    # await client(JoinChannelRequest(channel_id))
    # print(100)
    await client(JoinChannelRequest(link))
    return True


async def start_add_in_channel(link: str):
    client.loop.run_until_complete(add_in_channel(link))
    return True


@client.on(events.NewMessage(chats=('https://t.me/test_client_for_aaa', "https://t.me/asasasasasassasadass")))
async def normal_handler(event):
    print(event.message.to_dict()['message'])


@bot.message_handler(commands=["start"])
def start(message):
    global users, admins
    user_id = message.from_user.id
    user = users.get_elem(user_id)
    ###Если пользователя нет в БД
    admin = admins.get_elem(id=user_id)
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
        new_mes = bot.send_message(chat_id=user_id,
                                   text=start_text[user.language],
                                   reply_markup=lang_set_keyboard[user.language])
    else:
        user.keyboard_point = 0
        new_mes = bot.send_message(chat_id=user_id,
                                   text=start_text[user.language],
                                   reply_markup=lang_set_keyboard[user.language])
    user.flag = 1
    user.bot_messageId = new_mes.id

    users.update_info(user)


@bot.message_handler(commands=["admin"], func=lambda message: admins.get_elem(message.from_user.id))
def admin(message):
    global users, admins
    user_id = message.from_user.id
    user = users.get_elem(user_id)
    user.flag = 0
    user.keyboard_point = 0
    user.bot_messageId = None
    admin = admins.get_elem(message.from_user.id)
    new_mes = bot.send_message(chat_id=user_id,
                               text=admin_panel_main_text,
                               reply_markup=admin_main_keyboard)
    admin.flag = 0
    admin.mailing_text = None
    admin.new_instruction_text = {"ru": None, "en": None, }
    admin.bot_messageId = new_mes.id
    admin.keyboard_point = 0
    admin.mailing_message_id = None
    admin.mailing_but_name = None
    admin.mailing_but_url = None
    admin.mailing_message_id = None
    admin.mailing_photo_path = None
    admin.mailing_text = None

    users.update_info(user)
    admins.update_info(admin)


@bot.callback_query_handler(
    func=lambda call: admins.get_elem(call.from_user.id) and call.data in ["mailing_admin", "statistics_admin",
                                                                           "instruction_admin", "recomendation_admin",
                                                                           "back_to_admin_panel"])
def main_admin_panel(call):
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
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_1_text,
                              reply_markup=back_to_admin_panel_keyboard)
    elif call.data == "statistics_admin":
        added_in_24_hours = 0
        added_in_7_days = 0
        added_in_month = 0
        for user_id in users.get_keys():
            user = users.get_elem(id=user_id)
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
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=statistics,
                              reply_markup=back_to_admin_panel_keyboard)
    elif call.data == "instruction_admin":
        admin.flag = 1  # Ввод инструкции на русском
        admin.new_instruction_text = {"ru": None, "en": None, }
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=instruction_section_1_text,
                              reply_markup=back_to_admin_panel_keyboard)
    elif call.data == "recomendation_admin":
        admin.flag = 8  # Раздел рекомендации
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=recomendations_section_1_text,
                              reply_markup=recomendations_section_keyboard)

    elif call.data == "back_to_admin_panel":
        admin.flag = 0
        admin.mailing_text = None
        admin.new_instruction_text = {"ru": None, "en": None, }
        admin.keyboard_point = 0
        admin.mailing_message_id = None
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=admin_panel_main_text,
                              reply_markup=admin_main_keyboard)
    admins.update_info(elem=admin)


@bot.callback_query_handler(
    func=lambda call: admins.get_elem(call.from_user.id) and call.data in ["add_rec_channels", "del_rec_channel",
                                                                           "stop_adding_rec_channels"])
def recomendations_section(call):
    global admins, instruction_text
    user_id = call.from_user.id
    admin = admins.get_elem(id=user_id)
    if call.data == "add_rec_channels":
        admin.flag = 9  # Добавление рек канала
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=adding_new_channel_1_text["ru"],
                              reply_markup=adding_new_rec_channel_keyboard)
    elif call.data == "stop_adding_rec_channels":
        admin.flag = 8
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=exit_adding_channel_text["ru"],
                              reply_markup=recomendations_section_keyboard)

    elif call.data == "del_rec_channel":
        if rec_channels.count == 0:
            bot.edit_message_text(chat_id=user_id,
                                  message_id=admin.bot_messageId,
                                  text="Рекомендации отсутствуют")
        else:
            bot.edit_message_text(chat_id=user_id,
                                  message_id=admin.bot_messageId,
                                  text="Рекомендации",
                                  reply_markup=rec_channels.get_channel_keyboard(user_point=admin.keyboard_point,
                                                                                 channel_list=rec_channels.get_keys(),
                                                                                 keyboard_length=count_of_buts_in_keyboard))

    admins.update_info(admin)


@bot.callback_query_handler(
    func=lambda call: admins.get_elem(call.from_user.id) and call.data in ["back_to_writing_en_instruction",
                                                                           "new_instruction_ready"])
def instruction_section(call):
    global admins, instruction_text
    user_id = call.from_user.id
    admin = admins.get_elem(id=user_id)
    if call.data == "back_to_writing_en_instruction":
        admin.flag = 2  # !
        admin.new_instruction_text["en"] = None
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=instruction_section_2_text.format(ru_instruction=admin.new_instruction_text["ru"]),
                              reply_markup=back_to_writing_ru_instruction_keyboard)
    elif call.data == "new_instruction_ready":
        instruction_text = admin.new_instruction_text
        admin.flag = 0
        admin.mailing_text = None
        admin.new_instruction_text = {"ru": None, "en": None, }
        admin.keyboard_point = 0
        admin.mailing_message_id = None
        bot.answer_callback_query(callback_query_id=call.id,
                                  text=notification_instruction_ready,
                                  show_alert=True)
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=admin_panel_main_text,
                              reply_markup=admin_main_keyboard)

    admins.update_info(elem=admin)


@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice"],
                     func=lambda message: users.get_elem(message.from_user.id))
def start_logic(message):
    global users
    user_id = message.from_user.id
    user = users.get_elem(user_id)
    if user.flag == 1:
        if message.text in ["Русский", "Russian"]:
            user.language = "ru"
            user.flag = 2
            bot.send_message(chat_id=user_id,
                             text=after_lang_choose_text[user.language],
                             reply_markup=main_keyboard[user.language])
            bot.send_message(chat_id=user_id,
                             text=instruction_text[user.language],
                             reply_markup=change_lang_keyboard[user.language])

        elif message.text in ["Английский", "English"]:
            user.language = "en"
            user.flag = 2
            bot.send_message(chat_id=user_id,
                             text=after_lang_choose_text[user.language],
                             reply_markup=main_keyboard[user.language])
            bot.send_message(chat_id=user_id,
                             text=instruction_text[user.language],
                             reply_markup=change_lang_keyboard[user.language])
        else:
            pass
    elif user.flag == 2:
        if message.text in ["Инструкция", "Instruction"]:
            bot.send_message(chat_id=user_id,
                             text=instruction_text[user.language],
                             reply_markup=change_lang_keyboard[user.language])
        elif message.text in ["Добавить подписки", "Add"]:
            user.flag = 3
            bot.send_message(chat_id=user_id,
                             text=adding_new_channel_1_text[user.language],
                             reply_markup=adding_new_channel_keyboard[user.language])
        elif message.text in ["Мои подписки", "My"]:
            if len(user.channels) == 0:
                bot.send_message(chat_id=user_id,
                                 text=absense_subcription_text[user.language])
            else:
                bot.send_message(chat_id=user_id,
                                 text=veiw_delete_channel_text[user.language],
                                 reply_markup=channels.get_channel_keyboard(user_point=user.keyboard_point,
                                                                            channel_list=user.channels,
                                                                            keyboard_length=count_of_buts_in_keyboard))
        elif message.text in ["Рекомендации", "Rec"]:
            bot.send_message(chat_id=user_id,
                             text="Рекомендации ещё в разработке")

    elif user.flag == 3:
        if message.text in ["Продолжить", "Continue"]:
            user.flag = 2
            bot.send_message(chat_id=user_id,
                             text=exit_adding_channel_text[user.language],
                             reply_markup=main_keyboard[user.language])
        elif text_is_channel_url(message.forward_from_chat):
            # channel = Channel(key=channels.count)
            # channels.add_channel(channel=channel)
            # user.channels.append(message.text)
            link = f"https://t.me/{message.forward_from_chat.username}"
            print(link)
            check = True

            if check:
                bot.send_message(chat_id=user_id,
                                 text=adding_new_channel_2_text[user.language],
                                 reply_markup=adding_new_channel_keyboard[user.language])
                bot.send_message(chat_id=user_id,
                                 text=adding_new_channel_1_text[user.language],
                                 reply_markup=adding_new_channel_keyboard[user.language])
            else:
                bot.send_message(chat_id=user_id,
                                 text=adding_new_channel_3_text[user.language],
                                 reply_markup=adding_new_channel_keyboard[user.language])
        else:
            bot.send_message(chat_id=user_id,
                             text=adding_new_channel_3_text[user.language],
                             reply_markup=adding_new_channel_keyboard[user.language])
    users.update_info(user)


@bot.callback_query_handler(
    func=lambda call: admins.get_elem(call.from_user.id) and call.data in ["add_photo", "del_photo", "add_url_button",
                                                                           "del_url_button", "mailing_message_ready",
                                                                           "change_mailing_text",
                                                                           "back_to_mailing_section", ])
def mailing_section(call):
    global admins, instruction_text
    user_id = call.from_user.id
    admin = admins.get_elem(id=user_id)
    try:
        bot.delete_message(chat_id=user_id,
                           message_id=admin.mailing_message_id, )
    except:
        pass
    if call.data == "add_photo":
        admin.flag = 5  # Добавление фото для рассылки
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_3_text,
                              reply_markup=back_to_mailing_section_keyboard)
    elif call.data in ["del_photo", "del_url_button"]:
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        if call.data == "del_url_button":
            admin.mailing_but_name = None
            admin.mailing_but_url = None
            mailing_section_keyboard.add(mailing_section_add_url_but)
            if admin.mailing_photo_path == None:
                mailing_section_keyboard.add(mailing_section_add_photo_but)
            else:
                mailing_section_keyboard.add(mailing_section_del_photo_but)
        else:
            admin.mailing_photo_path = None
            mailing_section_keyboard.add(mailing_section_add_photo_but)
            if admin.mailing_but_name == None:
                mailing_section_keyboard.add(mailing_section_add_url_but)
            else:
                mailing_section_keyboard.add(mailing_section_del_url_but)

        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_2_text,
                              reply_markup=mailing_section_keyboard.add(
                                  mailing_section_ready_but).add(
                                  mailing_section_change_mail_text_but))

        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        if tuple_data_for_mailing_mes[2] != None:
            mailing_mes = bot.send_photo(chat_id=user_id,
                                         photo=tuple_data_for_mailing_mes[2],
                                         caption=tuple_data_for_mailing_mes[0],
                                         reply_markup=tuple_data_for_mailing_mes[1])
        else:
            mailing_mes = bot.send_message(chat_id=user_id,
                                           text=tuple_data_for_mailing_mes[0],
                                           reply_markup=tuple_data_for_mailing_mes[1])
        admin.mailing_message_id = mailing_mes.id

    elif call.data == "add_url_button":
        admin.flag = 6  # Добавление кнопки для рассылки(ссылка)
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_4_text,
                              reply_markup=back_to_mailing_section_keyboard)
    elif call.data == "mailing_message_ready":
        # mailing_all_users()
        bot.answer_callback_query(callback_query_id=call.id,
                                  text="Рассылка",
                                  show_alert=True)
        admin.flag = 0
        bot.edit_message_text(chat_id=user_id,
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
            bot.delete_message(chat_id=user_id,
                               message_id=admin.mailing_message_id)
        except:
            pass
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_1_text,
                              reply_markup=back_to_admin_panel_keyboard)
    elif call.data == "back_to_mailing_section":
        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        if admin.mailing_photo_path == None:
            mailing_section_keyboard.add(mailing_section_add_photo_but)
            mailing_mes = bot.send_message(chat_id=user_id,
                                           text=tuple_data_for_mailing_mes[0],
                                           reply_markup=tuple_data_for_mailing_mes[1])
        else:
            mailing_section_keyboard.add(mailing_section_del_photo_but)
            mailing_mes = bot.send_photo(chat_id=user_id,
                                         photo=tuple_data_for_mailing_mes[2],
                                         caption=tuple_data_for_mailing_mes[0],
                                         reply_markup=tuple_data_for_mailing_mes[1])
        admin.mailing_message_id = mailing_mes.id
        if admin.mailing_but_name == None:
            mailing_section_keyboard.add(mailing_section_add_url_but)
        else:
            mailing_section_keyboard.add(mailing_section_del_url_but)
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_2_text,
                              reply_markup=mailing_section_keyboard.add(
                                  mailing_section_ready_but).add(
                                  mailing_section_change_mail_text_but))

    admins.update_info(elem=admin)


@bot.message_handler(content_types=["photo"], func=lambda message: message.from_user.id in admins)
def mailing_section_add_photo(message):
    global admins, instruction_text

    if admins.get_elem(message.from_user.id).flag == 5:

        user_id = message.from_user.id
        admin = admins.get_elem(id=user_id)
        bot.delete_message(chat_id=user_id,
                           message_id=message.id)
        admin.mailing_photo_path = bot.download_file(
            bot.get_file(message.photo[len(message.photo) - 1].file_id).file_path)
        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        mailing_section_keyboard.add(mailing_section_del_photo_but)
        if admin.mailing_but_name == None:
            mailing_section_keyboard.add(mailing_section_add_url_but)
        else:
            mailing_section_keyboard.add(mailing_section_del_url_but)
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_2_text,
                              reply_markup=mailing_section_keyboard.add(
                                  mailing_section_ready_but).add(
                                  mailing_section_change_mail_text_but))
        mailing_mes = bot.send_photo(chat_id=user_id,
                                     photo=tuple_data_for_mailing_mes[2],
                                     caption=tuple_data_for_mailing_mes[0],
                                     reply_markup=tuple_data_for_mailing_mes[1])

        admin.mailing_message_id = mailing_mes.id
        admin.flag = 4
        admins.update_info(elem=admin)


@bot.message_handler(
    func=lambda message: admins.get_elem(message.from_user.id) and users.get_elem(message.from_user.id).flag == 0)
def data_entry_by_admin(message):
    global admins, rec_channels
    user_id = message.from_user.id
    admin = admins.get_elem(id=user_id)
    flag = admin.flag
    bot.delete_message(chat_id=user_id, message_id=message.id)
    if flag == 1:
        admin.new_instruction_text["ru"] = message.text
        admin.flag = 2
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=instruction_section_2_text.format(ru_instruction=admin.new_instruction_text["ru"]),
                              reply_markup=back_to_writing_ru_instruction_keyboard)
    elif flag == 2:
        admin.new_instruction_text["en"] = message.text
        admin.flag = 0
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=instruction_section_3_text.format(ru_instruction=admin.new_instruction_text["ru"],
                                                                     en_instruction=admin.new_instruction_text["en"]),
                              reply_markup=instruction_section_last_keyboard)

    elif flag == 3:
        admin.flag = 4  # Выбор действия в разделе рассылки
        admin.mailing_text = message.text
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_2_text,
                              reply_markup=mailing_section_keyboard.add(
                                  mailing_section_add_photo_but).add(
                                  mailing_section_add_url_but).add(
                                  mailing_section_ready_but).add(
                                  mailing_section_change_mail_text_but))
        mailing_mes = bot.send_message(chat_id=user_id,
                                       text=message.text)
        admin.mailing_message_id = mailing_mes.id

    elif flag == 6:
        if valid_url(message.text):
            admin.mailing_but_url = message.text
            admin.flag = 7
            bot.edit_message_text(chat_id=user_id,
                                  message_id=admin.bot_messageId,
                                  text=mailing_section_5_text.format(mailing_url_but=admin.mailing_but_url),
                                  reply_markup=back_to_mailing_section_keyboard)
        else:
            admin.flag = 6
            bot.edit_message_text(chat_id=user_id,
                                  message_id=admin.bot_messageId,
                                  text=mailing_section_4_text,
                                  reply_markup=back_to_mailing_section_keyboard)
    elif flag == 7:
        admin.mailing_but_name = message.text
        admin.flag = 4
        tuple_data_for_mailing_mes = get_tuple_data_for_mailing_mes(admin=admin)
        mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
        mailing_section_keyboard.add(mailing_section_del_url_but)
        if admin.mailing_photo_path == None:
            mailing_section_keyboard.add(mailing_section_add_photo_but)
        else:
            mailing_section_keyboard.add(mailing_section_del_photo_but)
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text=mailing_section_2_text,
                              reply_markup=mailing_section_keyboard.add(
                                  mailing_section_ready_but).add(
                                  mailing_section_change_mail_text_but))
        if admin.mailing_photo_path == None:
            mailing_mes = bot.send_message(chat_id=user_id,
                                           text=tuple_data_for_mailing_mes[0],
                                           reply_markup=tuple_data_for_mailing_mes[1])
        else:
            mailing_mes = bot.send_photo(chat_id=user_id,
                                         photo=tuple_data_for_mailing_mes[2],
                                         caption=tuple_data_for_mailing_mes[0],
                                         reply_markup=tuple_data_for_mailing_mes[1])

        admin.mailing_message_id = mailing_mes.id

    elif flag == 9:
        channel = Recomended_channel(key=rec_channels.count, )
        channel.url = message.text
        channel.name = message.text
        rec_channels.add_channel(channel=channel)
        bot.edit_message_text(chat_id=user_id,
                              message_id=admin.bot_messageId,
                              text="Здесь уже почти всё готово! Нужен клиент, чтобы добавлять канал" +
                                   adding_new_channel_2_text["ru"],
                              reply_markup=adding_new_rec_channel_keyboard)

    admins.update_info(elem=admin)


@bot.callback_query_handler(func=lambda call: "channels_" in call.data)
def delete_channels(call):
    global admins, rec_channels, channels
    user_id = call.from_user.id
    if "rec_channels" in call.data:
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
        if rec_channels.count == 0:
            bot.edit_message_text(chat_id=user_id,
                                  message_id=admin.bot_messageId,
                                  text="Рекомендации отсутствуют")
        else:
            bot.edit_message_text(chat_id=user_id,
                                  message_id=admin.bot_messageId,
                                  text="Рекомендации",
                                  reply_markup=rec_channels.get_channel_keyboard(user_point=admin.keyboard_point,
                                                                                 channel_list=rec_channels.get_keys(),
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
            channels.del_channel(str(call.data).split("_")[-1])
            if user.keyboard_point == Channels.count:
                user.keyboard_point -= count_of_buts_in_keyboard
        if channels.count == 0:
            bot.edit_message_text(chat_id=user_id,
                                  message_id=user.bot_messageId,
                                  text="Рекомендации отсутствуют")
        else:
            bot.edit_message_text(chat_id=user_id,
                                  message_id=user.bot_messageId,
                                  text="Рекомендации",
                                  reply_markup=channels.get_channel_keyboard(user_point=user.keyboard_point,
                                                                             channel_list=channels.get_keys(),
                                                                             keyboard_length=count_of_buts_in_keyboard))

        users.update_info(user)


@bot.callback_query_handler(func=lambda call: call.data == "change_lang")
def change_lang(call):
    global users
    user_id = call.from_user.id
    user = users.get_elem(user_id)
    if user.language == "ru":
        user.language = "en"
    elif user.language == "en":
        user.language = "ru"
    bot.send_message(chat_id=user_id,
                     text=instruction_text[user.language],
                     reply_markup=change_lang_keyboard[user.language])
    bot.send_message(chat_id=user_id,
                     text=after_lang_choose_text[user.language],
                     reply_markup=main_keyboard[user.language])

    users.update_info(user)


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(client.loop.run_forever(), scheduler())



if __name__ == "__main__":
    bot.infinity_polling()

