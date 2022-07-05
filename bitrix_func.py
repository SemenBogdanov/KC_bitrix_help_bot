# import fast_bitrix24
#
#
# def create_new_bitrix_task(title: str, description: str, deadline, response_employer_id: int = 218, group_id: int = 377,
#                            auditors=['16'], creator: int = '2300'):
#     res = bx.call('tasks.task.add',
#                   {'fields': {
#                       'TITLE': title,
#                       'DESCRIPTION': description,
#                       'GROUP_ID': group_id,
#                       'AUDITORS': auditors,
#                       'DEADLINE': deadline,
#                       'RESPONSIBLE_ID': response_employer_id,
#                       'CREATED_BY': creator}
#                   })
#     return res
