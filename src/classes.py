import sqlite3
from dataclasses import dataclass
from pathlib import Path
import json

from aiogram import types
from telethon import types as teletypes


###Класс юзера
# @dataclass
class User:
    def __init__(self, key: int = None, flag: int = 0, bot_messageId: int = 0, language: str = "ru",
                 messages_to_del: list = [], channels: list = [], keyboard_point: int = 0,
                 messages_queue: list = [], registration_date: int = None) -> None:
        self.key = key
        self.flag = flag  # Флаг/логическая ступень
        self.bot_messageId = bot_messageId  # id сообщения от бота
        self.language = language
        self.messages_to_del = messages_to_del
        self.channels = channels
        self.keyboard_point = keyboard_point
        self.messages_queue = messages_queue
        self.registration_date = registration_date

    def get_tuple(self) -> tuple:
        # if self.account == None:
        return (self.key,
                self.flag,
                self.bot_messageId,
                self.language,
                json.dumps(self.messages_to_del),
                json.dumps(self.channels),
                self.keyboard_point,
                json.dumps(self.messages_queue),
                self.registration_date)


# @dataclass
class Admin:
    def __init__(self, key: int = None, flag: int = 0, mailing_text: str = None,
                 new_instruction_text: dict = {"ru": None, "en": None, }, bot_messageId: int = None,
                 keyboard_point: int = None, mailing_message_id: int = None, mailing_photo_path: str = None,
                 mailing_but_name: str = None, mailing_but_url: str = None) -> None:
        self.key = key
        self.flag = flag
        self.mailing_text = mailing_text
        self.new_instruction_text = new_instruction_text
        self.bot_messageId = bot_messageId
        self.keyboard_point = keyboard_point
        self.mailing_message_id = mailing_message_id
        self.mailing_photo_path = mailing_photo_path
        self.mailing_but_name = mailing_but_name
        self.mailing_but_url = mailing_but_url

    def get_tuple(self):
        return (
            self.key,
            self.flag,
            self.mailing_text,
            json.dumps(self.new_instruction_text),
            self.bot_messageId,
            self.keyboard_point,
            self.mailing_message_id,
            self.mailing_photo_path,
            self.mailing_but_name,
            self.mailing_but_url
        )


@dataclass
class Channel:
    def __init__(self, key: int = None, users: list = [], url: str = None, name: str = None,
                 chat_id: int = None, last_id_mes: int = None) -> None:
        self.key = key
        self.users = users
        self.url = url
        self.name = name
        self.chat_id = chat_id
        self.last_id_mes = last_id_mes

    def get_tuple(self):
        return (
            self.key,
            json.dumps(self.users),
            self.url,
            self.name,
            self.chat_id,
            self.last_id_mes
        )


# @dataclass
class Recomended_channel:
    def __init__(self, key: int = None, url: str = None, name: str = None, messages_to_send: list = [],
                 chat_id: int = None) -> None:
        pass
        self.key = key
        self.url = url
        self.name = name
        self.messages_to_send = messages_to_send
        self.chat_id = chat_id

    def get_tuple(self):
        return (
            self.key,
            self.url,
            self.name,
            json.dumps(self.messages_to_send),
            self.chat_id

        )


# class Message_from_rec_channel:
#     def __init__(self, key: int, text: str = None, photo_path: str = None, video_path: str = None,
#                  audio_path: str = None, document_path: str = None, sticker_path: str = None,
#                  video_note_path: str = None, voice_path: str = None, ) -> None:
#         self.key = key
#         self.text = text
#         self.photo_path = photo_path
#         self.video_path = video_path
#         self.audio_path = audio_path
#         self.document_path = document_path
#         self.sticker_path = sticker_path
#         self.video_note_path = video_note_path
#         self.voice_path = voice_path
#
#     def get_tuple(self):
#         return (
#             self.key,
#             self.text,
#             self.photo_path,
#             self.video_path,
#             self.audio_path,
#             self.document_path,
#             self.sticker_path,
#             self.video_note_path,
#             self.voice_path,
#         )


# класс для работы с sqllite3
class Sqlite3_Database():
    def __init__(self, db_file_name: str, args: dict, table_name: str) -> None:
        self.table_name = table_name
        self.db_file_name = db_file_name
        self.args = args
        a = self.creating_table()

    def creating_table(self) -> bool:
        if not self.is_file_exist():
            try:
                self.init_sqlite()
                return True
            except Exception as e:
                return False

        elif not self.is_table_exist():
            try:
                self.init_sqlite()
                return True
            except Exception as e:
                return False
        else:
            return True

    def sqlite_connect(self) -> sqlite3.Connection:  # Создание подключения к БД
        conn = sqlite3.connect(self.db_file_name, check_same_thread=True)
        conn.execute("pragma journal_mode=wal;")
        return conn

    def is_file_exist(self) -> bool:  # Существует ли файл БД
        db = Path(f"./{self.db_file_name}")
        try:
            db.resolve(strict=True)
            return True
        except FileNotFoundError:
            return False

    def is_table_exist(self) -> bool:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f'''SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type="table" AND name="{self.table_name}")''')
        is_exist = curs.fetchone()[0]
        conn.commit()
        conn.close()
        if is_exist:
            return True
        else:
            return False

    def init_sqlite(self) -> None:
        str_for_sql_req = ''
        if len(self.args) != 0:
            count = 1
            for key in self.args:
                if count == 1:
                    str_for_sql_req = str_for_sql_req + key + ' ' + self.args[key] + ' primary key'
                else:
                    str_for_sql_req = str_for_sql_req + key + ' ' + self.args[key]
                if count != len(self.args):
                    str_for_sql_req += ', '
                    count += 1
        conn = self.sqlite_connect()
        curs = conn.cursor()
        print(f'''CREATE TABLE {self.table_name} ({str_for_sql_req})''')
        curs.execute(f'''CREATE TABLE {self.table_name} ({str_for_sql_req})''')
        conn.commit()
        conn.close()

    def get_elem_sqllite3(self, key: int | str) -> tuple:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f'''SELECT * from {self.table_name} where key = {key}''')
        answ = curs.fetchone()
        conn.close()
        return answ

    def __contains__(self, other: int | str) -> bool:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f"SELECT 1 FROM {self.table_name} WHERE key={other}")
        if curs.fetchone() is not None:
            conn.close()
            return True
        else:
            conn.close()
            return False

    def __add_column(self, columns: dict) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        self.args += columns
        for col_name in columns:
            curs.execute(f"""ALTER TABLE {self.table_name} ADD COLUMN {col_name} '{columns[col_name]}'""")
        conn.close()

    def add_row(self, values: tuple) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        insert_vals_str = ''
        for i in range(len(values)):
            insert_vals_str += '?'
            if len(values) - 1 != i:
                insert_vals_str += ', '
        print(f"""INSERT INTO {self.table_name} VALUES ({insert_vals_str})""", values)
        curs.execute(f"""INSERT INTO {self.table_name} VALUES ({insert_vals_str})""", values)
        conn.commit()
        conn.close()

    def del_row(self, key: int | str) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f"""DELETE FROM {self.table_name} WHERE key = {key}""")
        conn.commit()
        conn.close()

    def update_info(self, elem: User | Admin | Channel | Recomended_channel) -> None:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        info = elem.get_tuple()
        count = 0
        for column_name in self.args:
            curs.execute(f"""UPDATE {self.table_name} SET {column_name} = ? WHERE key = ?""", (info[count], elem.key))
            count += 1
        conn.commit()
        conn.close()

    def get_keys(self) -> list:
        conn = self.sqlite_connect()
        curs = conn.cursor()
        curs.execute(f"""SELECT key FROM {self.table_name}""")
        grand_tuple = curs.fetchall()
        conn.commit()
        conn.close()
        keys = [key[0] for key in grand_tuple]
        return keys


class Users(Sqlite3_Database):
    def __init__(self, db_file_name, args, table_name) -> None:
        Sqlite3_Database.__init__(self, db_file_name, args, table_name)

    # Добавление пользователя
    def add_user(self, user: User) -> None:
        self.add_row(user.get_tuple())

    def get_elem(self, id: int) -> User | bool:
        if id in self:
            user_tuple = self.get_elem_sqllite3(id)
            user = User(key=user_tuple[0],
                        flag=user_tuple[1],
                        bot_messageId=user_tuple[2],
                        language=user_tuple[3],
                        messages_to_del=json.loads(user_tuple[4]),
                        channels=json.loads(user_tuple[5]),
                        keyboard_point=user_tuple[6],
                        messages_queue=json.loads(user_tuple[7]),
                        registration_date=user_tuple[8])
            return user
        else:
            return False


class Channels(Sqlite3_Database):
    count = 0

    def __init__(self, db_file_name, args, table_name) -> None:
        Sqlite3_Database.__init__(self, db_file_name, args, table_name)

    # Добавление пользователя
    def add_channel(self, channel: Channel | Recomended_channel) -> None:
        if self.__class__.__name__ == "Channels":
            Channels.count += 1
        else:
            Recomended_channels.count += 1
        self.add_row(channel.get_tuple())

    def del_channel(self, key: int) -> None:
        if self.__class__.__name__ == "Channels":
            Channels.count -= 1
        else:
            Recomended_channels.count -= 1
        self.del_row(key=key)

    def get_channel(self, id: int) -> Channel | bool:
        if id in self:
            channel_tuple = self.get_elem_sqllite3(id)
            channel = Channel(key=channel_tuple[0],
                              users=json.loads(channel_tuple[1]),
                              url=channel_tuple[2],
                              name=channel_tuple[3],
                              chat_id=channel_tuple[4],
                              last_id_mes=channel_tuple[5])
            return channel
        else:
            return False

    def del_user(self, id: int, user_id: int):
        channel = self.get_channel(id)
        ind = channel.users.index(user_id)
        del channel.users[ind]
        if len(channel.users) == 0:
            self.del_channel(id)
        else:
            self.update_info(elem=channel)

    def get_channel_keyboard(self, user_point: int, channel_list: list,
                             keyboard_length: int) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        callback = ""
        if self.__class__.__name__ == "Channels":
            callback = "channels"
        elif self.__class__.__name__ == "Recomended_channels":
            callback = "rec_channels"
        count = 0
        for i in range(user_point, len(channel_list)):
            if count < keyboard_length:
                print(channel_list, " : ", i)

                ch_id = channel_list[i]
                print(ch_id)
                channel = self.get_channel(id=ch_id)
                print(f"{callback}_{channel.key}")
                keyboard.add(types.InlineKeyboardButton(text=channel.name, callback_data=f"{callback}_{channel.key}"))
            else:
                break
            count += 1
        keyboard.add(
            types.InlineKeyboardButton(text="<", callback_data=f"{callback}_<"),
            types.InlineKeyboardButton(text=">", callback_data=f"{callback}_>")
        )
        if self.__class__.__name__ == "Recomended_channels":
            keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_admin_panel"))
        return keyboard


class Recomended_channels(Channels):
    def __init__(self, db_file_name, args, table_name) -> None:
        Channels.__init__(self, db_file_name, args, table_name)

    def get_channel(self, id: int) -> Recomended_channel | bool:
        if id in self:
            channel_tuple = self.get_elem_sqllite3(id)
            channel = Recomended_channel(key=channel_tuple[0],
                                         url=channel_tuple[1],
                                         name=channel_tuple[2],
                                         messages_to_send=json.loads(channel_tuple[3]),
                                         chat_id=channel_tuple[4])
            return channel
        else:
            return False


class Admins(Sqlite3_Database):
    def __init__(self, db_file_name, args, table_name) -> None:
        Sqlite3_Database.__init__(self, db_file_name, args, table_name)

    # Добавление пользователя
    def add_admin(self, admin: Admin) -> None:
        self.add_row(admin.get_tuple())

    def get_elem(self, id: int) -> Admin | bool:
        if id in self:
            admin_tuple = self.get_elem_sqllite3(id)
            admin = Admin(key=admin_tuple[0],
                          flag=admin_tuple[1],
                          mailing_text=admin_tuple[2],
                          new_instruction_text=json.loads(admin_tuple[3]),
                          bot_messageId=admin_tuple[4],
                          keyboard_point=admin_tuple[5],
                          mailing_message_id=admin_tuple[6],
                          mailing_photo_path=admin_tuple[7],
                          mailing_but_name=admin_tuple[8],
                          mailing_but_url=admin_tuple[9], )
            return admin
        else:
            return False


class Message_from_rec_channel:
    def __init__(self):
        self.list_object: list[teletypes.MessageMediaPhoto | teletypes.MessageMediaWebPage] = []
        self.message_text = None
        self.time = None
        self.list_id: list = []
        self.media: types.MediaGroup = types.MediaGroup()

    def add_elem(self, elem):
        self.list_object.append(elem)

    def set_message_text(self, text: str) -> None:
        self.message_text = text


class nsql_database:
    def __init__(self) -> None:
        self.data = {}

    # Получение значения по ключу
    def get_elem(self, key: int | str) -> bool | Message_from_rec_channel:
        if key in self.data:
            return self.data[key]
        else:
            return False

    def __contains__(self, other) -> bool:
        if other in self.data:
            return True
        else:
            return False


class Message_from_rec_channels(nsql_database):
    def __init__(self) -> None:
        super().__init__()
        self.links: dict = {}
        self.name_channel: dict = {}  # channel_name | link_to_channel

    def __contains__(self, item: str) -> bool:
        if item in self.links:
            return True
        else:
            return False

    def add_elem(self, group_id: int, elem: Message_from_rec_channel) -> None:
        self.data[group_id] = elem

    def add_link(self, link: str) -> None:
        self.links[link] = -1

    def add_channel_name(self, name_channel: str, link: str) -> None:
        self.name_channel[name_channel] = link

    def get_array_link(self) -> dict:
        return self.links

    def get_data(self) -> dict:
        return self.data

    def set_min_id(self, key: str, min_id: int) -> None:
        self.links[key] = min_id

    def del_channel(self, channel_name: str) -> None:
        link = self.name_channel[channel_name]
        del self.name_channel[channel_name]
        del self.links[link]

    def get_channel_keyboard(self, user_point: int, channel_dict: dict,
                             keyboard_length: int) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        callback = "rec_channels"
        count = 0
        keys = list(channel_dict.keys())
        for i in range(user_point, len(channel_dict)):
            if count < keyboard_length:
                print(channel_dict, " : ", i)
                channel_name = keys[i]
                # link = channel_dict[channel_name]

                # print(f"{callback}_{link}")
                keyboard.add(types.InlineKeyboardButton(text=channel_name, callback_data=f"{callback}_{channel_name}"))
            else:
                break
            count += 1
        keyboard.add(
            types.InlineKeyboardButton(text="<", callback_data=f"{callback}_<"),
            types.InlineKeyboardButton(text=">", callback_data=f"{callback}_>")
        )
        if self.__class__.__name__ == "Message_from_rec_channels":
            keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data="back_to_admin_panel"))
        return keyboard

    # def get_elem(self, id: int) -> Admin | bool:
    #     if id in self:
    #         message_tuple = self.get_elem_sqllite3(id)
    #         message = Message_from_rec_channel(
    #             key=message_tuple[0],
    #             text=message_tuple[1],
    #             photo_path=message_tuple[2],
    #             video_path=message_tuple[3],
    #             audio_path=message_tuple[4],
    #             document_path=message_tuple[5],
    #             sticker_path=message_tuple[6],
    #             video_note_path=message_tuple[7],
    #             voice_path=message_tuple[8],
    #         )
    #         return message
    #     else:
    #         return False
