import logging
from datetime import datetime

# from sqlalchemy import create_engine, Table, MetaData
#
# from key import user, password, host, port
#
# engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/firstbase1")
# metadata_obj = MetaData()


# def addTask():
#     conn = engine.connect()
#     sql = 'INSERT INTO public.kc_bitrix_bot_tasks(problem_system,project_name,question_category,date,e_mail,' \
#           'problem_description,price) VALUES ' \
#           '(\'PM\',\'test\',\'Не удается войти\',\'2022-02-04\',\'semen@mail.ru\',\'problem\',500.0)'
#     bot_tasks_table = Table("kc_bitrix_bot_tasks", metadata_obj, autoload_with=engine)
#     res = conn.execute(sql)
#     conn.close()
#     print(res)



