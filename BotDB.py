import logging
from datetime import datetime
import psycopg2
from key import user, password, host, port


class BotDB:

    def __init__(self):
        """Инициализация подключения БД"""
        self.conn = psycopg2.connect(user=user,
                                     password=password,
                                     host=host,
                                     port=port,
                                     dbname='firstbase1')
        self.cur = self.conn.cursor()

    def get_support_user_name_by_chat_id(self, chat_id):
        # print(chat_id)
        """Получить имя пользователя службы поддержки по номеру chat_id"""
        query = "select name_employee from public.tech_support_users where chat_id = %s"
        value = (str(chat_id),)
        try:
            self.cur.execute(query, value)
            res = self.cur.fetchall()[0]
            if len(res) > 0:
                print(True)
                return True
            else:
                print(False)
                return False
        except Exception as e:
            print(f"Ошибка получения информации: {e}")
            return False

    def is_in_progress(self, task_id: int):
        """Определяем в работе заявка или еще нет"""
        query = "select task_status from public.kc_bitrix_bot_tasks where id = %s"
        value = (str(task_id),)
        self.cur.execute(query, value)
        res = self.cur.fetchall()[0][0]
        # print(res)
        if res == 'InProgress':
            return True
        else:
            return False

    def set_task_status_is_done(self, task_id: int):
        """Изменить статус заявки на: в работе"""
        print(str(task_id))

        query1 = "UPDATE public.kc_bitrix_bot_tasks SET task_status = 'Done' WHERE id = %s"

        values1 = (task_id,)
        try:
            # print('Попытка записи в БД')
            self.cur.execute(query1, values1)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при вставке: {e}")
            return False

    def set_task_status_in_progress(self, task_id: int, tech_employee_id: int):
        """Изменить статус заявки на: в работе"""
        # print(str(task_id), str(tech_employee_id))

        query1 = "UPDATE public.kc_bitrix_bot_tasks SET task_status = 'InProgress' WHERE id = %s"
        query2 = "UPDATE public.kc_bitrix_bot_tasks SET employee_from_support = (" \
                 "SELECT id from tech_support_users where chat_id = %s::varchar) where id = %s"

        values1 = (task_id,)
        values2 = (tech_employee_id, task_id,)
        try:
            # print('Попытка записи в БД')
            self.cur.execute(query1, values1)
            self.cur.execute(query2, values2)
            id = self.get_support_user_name_by_task_id(task_id)
            self.conn.commit()
            print(f'Переменная id = {id}')
            return id
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка при вставке: {e}")
            return False

    def get_support_user_name_by_task_id(self, task_id: int):
        """Получить имя исполнителя задачи по ID задачи"""
        query = ''
        if self.is_in_progress(task_id):
            query = """select tsu.name_employee
            from public.kc_bitrix_bot_tasks kbbt
            left join tech_support_users tsu on kbbt.employee_from_support = tsu.id 
            where kbbt.id = %s"""
        values = (str(task_id),)
        self.cur.execute(query, values)
        res = self.cur.fetchall()[0][0]
        return res

    def get_task(self, id):
        """Получить отдельное задание"""
        query = "select * from public.kc_bitrix_bot_tasks where id = %s"
        values = (str(id),)
        self.cur.execute(query, values)
        res = self.cur.fetchall()
        return res

    def add_task_to_db(self, data):
        ddate = datetime.strftime(datetime.strptime(data['timestamp'][0:16], '%Y-%m-%d %H:%M'), '%d.%m.%Y %H:%M')
        # print('Data for record!___________')
        # print(data['system'], data['project'], data['ticket_category'], ddate, data['email'],
        #       data['short_task_description'], data['fio'], data['task_status'], data['user_from_id'])
        # print('__________________________!')
        query = "INSERT INTO public.kc_bitrix_bot_tasks(problem_system, project_name, question_category, date, " \
                "e_mail, problem_description,fio,task_status,user_from_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) " \
                "RETURNING id"
        values = (data['system'], data['project'], data['ticket_category'], str(ddate), data['email'],
                  data['short_task_description'], data['fio'], data['task_status'], data['user_from_id'],)
        try:
            # print('Попытка записи в БД')
            self.cur.execute(query, values)
            id = self.cur.fetchone()[0]
            self.conn.commit()
            return id
        except Exception as e:
            print("Ошибка при вставке {}", e)
            return False

    def get_task_user_from_id(self, task_id: int):
        """Получить user.from_id"""
        query = "select user_from_id from public.kc_bitrix_bot_tasks where id = %s"
        values = (task_id,)
        try:
            self.cur.execute(query, values)
            res = self.cur.fetchall()[0][0]
            print(res)
            return res
        except Exception as e:
            logging.info(f'Проблема в get_task_user_from_id: {e}')
            return False

    def check_allow_user_to_create_new_task(self, user_id: int):
        """Проверить возможность создать новую заявку, если нет, то отправить сообщение в чат исполнителю"""
        query = "select count(id)::int from public.kc_bitrix_bot_tasks " \
                "where user_from_id = %s and task_status in (%s, %s);"
        values = (str(user_id), str('InProgress'), str('New!'), )
        try:
            self.cur.execute(query, values)
            res = self.cur.fetchall()[0][0]
        except:
            return True

        if res > 0:
            return False  # невозможно создать поавторное обращение т.к. заявка уже в работе
        else:
            return True  # можно создать дополнитеьную заявку и мы никому не пересылаем сообщения

    def cnd_redirect(self, user_from_id: int):
        query = "select distinct tsu.chat_id from public.kc_bitrix_bot_tasks kbbt " \
                "join tech_support_users tsu on kbbt.employee_from_support = tsu.id " \
                "where user_from_id = %s and task_status = %s"
        values = (str(user_from_id), 'InProgress',)
        try:
            self.cur.execute(query, values)
            res = self.cur.fetchall()[0][0]
            print("res: " + str(res))
            return res
        except:
            return False

    #
    # def get_colleagues(self):
    #     """Получаем список коллег для проверки дней рождений"""
    #     query = "select persone_name, birthday_date from people p where p.type_persons = '2';"
    #     self.cur.execute(query)
    #     res = self.cur.fetchall()
    #     # print(res)
    #     return res

    # def add_birthday(self, p_name, p_date, p_type):
    #     """Добавляем новую запись о дне рождения в таблицу"""
    #     try:
    #         query = """INSERT INTO people (persone_name, birthday_date, type_persons) values (%s,%s,%s)"""
    #         values = (str(p_name), str(p_date), str(p_type),)
    #         self.cur.execute(query, values)
    #         self.conn.commit()
    #         return True
    #     except Exception as e:
    #         print("Ошибка при вставке {}", e)
    #         return False
    #
    # def del_by_id(self, id):
    #     """Удаляем запись о дне рождении по ID"""
    #     try:
    #         self.cur.execute("delete from people p where p.id = %s", (id,))
    #         self.conn.commit()
    #         return True
    #     except:
    #         return False

    # def find_by_surname(self, surname, tp):
    #     if tp == 2:
    #         self.cur.execute("select * from people p where p.persone_name like %s "
    #                          "and p.type_persons = %s::varchar ", (surname, tp,))
    #         res = self.cur.fetchall()
    #         if res:
    #             return res
    #         else:
    #             return False
    #     elif tp == 1:  # private
    #         self.cur.execute("select * from people p where p.persone_name like %s ", (surname,))
    #         res = self.cur.fetchall()
    #         if res:
    #             return res
    #         else:
    #             return False

    def getinfo(self):
        return self.conn.info

    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()
