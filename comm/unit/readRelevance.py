# -*- coding:utf-8 -*-
# @Time    : 2021/07/10
# @Author  : Xuanyu Liu
# @File    : readRelevance.py
# ****************************
import logging
import re

__relevance = ""


def get_value(data, value):
    """获取数据中的值

    :param data:
    :param value:
    :return:
    """
    global __relevance
    if isinstance(data, dict):
        if value in data:
            __relevance = data[value]
        else:
            for key in data:
                __relevance = get_value(data[key], value)
    elif isinstance(data, list):
        for key in data:
            if isinstance(key, dict):
                __relevance = get_value(key, value)
                break
    return __relevance


def get_relevance(data, relevance_list, relevance=None):
    """获取关联键值对

    :param data:
    :param relevance_list:
    :param relevance:
    :return:
    """
    # 获取关联键列表
    relevance_list = re.findall(r"\${(.*?)}", str(relevance_list))
    relevance_list = list(set(relevance_list))
    logging.debug("获取关联键列表:\n%s" % relevance_list)
    # 判断关联键和源数据是否有值
    if (not data) or (not relevance_list):
        return relevance

    # 判断是否存在其他关联键对象
    if not relevance:
        relevance = dict()
    # 遍历关联键
    for each in relevance_list:
        if each in relevance:
            pass
            # # 考虑到一个关联键，多个值
            # if isinstance(relevance[each], list):
            #     a = relevance[each]
            #     a.append(relevance_value)
            #     relevance[each] = a
            # else:
            #     a = relevance[each]
            #     b = list()
            #     b.append(a)
            #     b.append(relevance_value)
            #     relevance[each] = b
        else:
            # 从结果中提取关联键的值
            relevance[each] = get_value(data, each)
    logging.debug("提取关联键对象:\n%s" % relevance)
    return relevance


if __name__ == '__main__':
    data = {'code': 0, 'msg': 'OK', 'id': 100100, 'data': {'id': 127409, 'member_id': 1236921938, 'title': '新增一个项目', 'amount': 6300.0, 'loan_rate': 12.0, 'loan_term': 12, 'loan_date_type': 1, 'bidding_days': 5, 'create_time': '2021-10-09 11:05:46.0', 'bidding_start_time': None, 'full_time': None, 'status': 1}, 'copyright': 'Copyright 柠檬班 © 2017-2020 湖南省零檬信息技术有限公司 All Rights Reserved', 'parameter': {'member_id': '1236921938', 'title': '新增一个项目', 'amount': 6300.0, 'loan_rate': 12.0, 'loan_term': 12, 'loan_date_type': 1, 'bidding_days': 5}}
    check_db = [{'check_type': 'check_db', 'execute_sql': "SELECT * FROM loan WHERE id ='${id}'", 'expected_result': [{'amount': '${amount}'}], 'expected_num': 1}]
    __relevance = get_relevance(data, check_db)
    print(__relevance)



