#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author： 刘宣妤
# @file： initializeFunc.py
# datetime： 2021/7/19 9:57 
# ide： PyCharm
from comm.unit.apiMethod import *
from comm.unit.queryDatabase import QueryDB

from config import PROJECT_NAME, AC


def func_header(user=AC[PROJECT_NAME]['user_'], pwd=AC[PROJECT_NAME]['user_pwd']):
    """
    更新header
    """
    login_res = post(headers={'X-Lemonban-Media-Type': 'lemonban.v2'}, address=AC[PROJECT_NAME]['host']+'/member/login',
                     mime_type='application/json', data={'mobile_phone': user,
                                                         'pwd': pwd})[1]
    token = login_res['data']['token_info']['token']
    header = {
        'X-Lemonban-Media-Type': 'lemonban.v2',
        'Authorization': f'Bearer {token}'
    }
    return header


def func_DoSql(sql, count=1, db=None):
    if 'select' in sql or 'SELECT' in sql:
        res_data = QueryDB().main_query(sql, count=count, db=db)
        if res_data:
            if len(res_data[0]) == 1:
                for k, v in res_data[0].items():
                    return v
            else:
                return res_data[0]
    else:
        QueryDB().main_excute(sql)


if __name__ == '__main__':
    c = func_header()
    print(c)

