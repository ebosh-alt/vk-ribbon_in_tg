from aiogram import types


lang_set_keyboard = {"ru": types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
                           types.KeyboardButton(text="Русский"), types.KeyboardButton(text="English")),
                     "en": types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
                           types.KeyboardButton(text="Русский"), types.KeyboardButton(text="English"))}


main_keyboard = {"ru": types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(
                       types.KeyboardButton(text="Добавить подписки"), types.KeyboardButton(text="Мои подписки"), 
                       types.KeyboardButton(text="Инструкция")).add(types.KeyboardButton(text="Рекомендации")),
                 "en": types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True).add(
                       types.KeyboardButton(text="Add"), types.KeyboardButton(text="My"), 
                       types.KeyboardButton(text="Instruction")).add(types.KeyboardButton(text="Rec"))}

change_lang_keyboard = {"ru": types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(
                              text="Сменить язык", callback_data="change_lang")),
                        "en": types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(
                              text="Change language", callback_data="change_lang"))}

adding_new_channel_keyboard = {"ru": types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                                                                            types.KeyboardButton(text="Продолжить")),
                                "en": types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(
                                                                            types.KeyboardButton(text="Continue"))}


admin_main_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
      types.InlineKeyboardButton(text="Рассылка", callback_data="mailing_admin")).add(
      types.InlineKeyboardButton(text="Статистика", callback_data="statistics_admin")).add(
      types.InlineKeyboardButton(text="Инструкции", callback_data="instruction_admin")).add(
      types.InlineKeyboardButton(text="Рекомендации", callback_data="recomendation_admin"))

#instruction_section
back_to_admin_panel_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
      types.InlineKeyboardButton(text="Назад", callback_data="back_to_admin_panel"))

back_to_writing_ru_instruction_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
      types.InlineKeyboardButton(text="Назад", callback_data="instruction_admin"))

instruction_section_last_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
      types.InlineKeyboardButton(text="Готово", callback_data="new_instruction_ready")).add(
      types.InlineKeyboardButton(text="Назад", callback_data="back_to_writing_en_instruction"))

#recomendations_section
recomendations_section_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
      types.InlineKeyboardButton(text="Добавить каналы", callback_data="add_rec_channels")).add(
      types.InlineKeyboardButton(text="Удалить канал", callback_data="del_rec_channel")).add(
      types.InlineKeyboardButton(text="Назад", callback_data="back_to_admin_panel"))

adding_new_rec_channel_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
      types.InlineKeyboardButton(text="Продолжить", callback_data="stop_adding_rec_channels"))

#mailing_section
mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1)
mailing_section_add_photo_but = types.InlineKeyboardButton(text="Добавить фото", callback_data="add_photo")
mailing_section_del_photo_but = types.InlineKeyboardButton(text="Удалить фото", callback_data="del_photo")
mailing_section_add_url_but = types.InlineKeyboardButton(text="Добавить кнопку", callback_data="add_url_button")
mailing_section_del_url_but = types.InlineKeyboardButton(text="Удалить кнопку", callback_data="del_url_button")
mailing_section_ready_but = types.InlineKeyboardButton(text="Готово", callback_data="mailing_message_ready")
mailing_section_change_mail_text_but = types.InlineKeyboardButton(text="Назад", callback_data="change_mailing_text")

back_to_mailing_section_keyboard = types.InlineKeyboardMarkup(row_width=1).add(
      types.InlineKeyboardButton(text="Назад", callback_data="back_to_mailing_section"))
