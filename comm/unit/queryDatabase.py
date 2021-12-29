# -*- coding:utf-8 -*-
# @Time    : 2021/07/10
# @Author  : Xuanyu Liu
# @File    : queryDatabase.py
# **************************
import pymssql

from comm.utils.readYaml import read_yaml_data
from config import DB_CONFIG, PROJECT_NAME, DB_TYPE
from comm.db import *
import logging
import time
import re

dbcfg = read_yaml_data(DB_CONFIG)[PROJECT_NAME]


class QueryDB:
    @staticmethod
    def __query_mysql(sql, count=None, db=None):
        """查询MySQL数据

        :param count:
        :param sql: sql查询语句
        :return:
        """
        # 获取配置信息
        timeout = dbcfg['timeout']
        address = dbcfg['mysql_info']['address']
        user = dbcfg['mysql_info']['user']
        auth = dbcfg['mysql_info']['auth']
        if not db:
            db = dbcfg['mysql_info']['db']
        # 初始化MySQL
        host, port = address.split(':')
        mysql = MysqlServer(host, int(port), db, user, auth)
        logging.info('执行查询>>> {}'.format(sql))
        # 循环查询
        for i in range(int(timeout)):
            try:
                result = mysql.query(sql, is_dict=True, count=count)
                mysql.close()
                if result:
                    return result
                else:
                    time.sleep(1)
                    raise Exception(f'查询异常>>> 查询sql：{sql} >>无数据返回')
            except Exception as e:
                raise Exception('查询异常>>> {}'.format(e))
        else:
            return []

    @staticmethod
    def main_query(sql, db=None, count=None):
        """
        主查询
        判断工程的DBtype进行不同数据库的链接查询
        :param sql:
        :param count:
        :return:
        """
        if DB_TYPE.upper() == 'MYSQL':
            if isinstance(sql, dict):
                res = QueryDB.__query_mysql(sql['MS'], count, db=db)
            else:
                res = QueryDB.__query_mysql(sql, count, db=db)
        else:
            raise Exception("无该数据库校验方式%s" % DB_TYPE)
        return res

    def main_excute(self, sql):
        """
        主操作
        判断工程的DBtype进行不同数据库的链接操作
        :param sql:
        :param count:
        :return:
        """
        if DB_TYPE.upper() == 'MYSQL':
            # 获取配置信息
            address = dbcfg['mysql_info']['address']
            user = dbcfg['mysql_info']['user']
            auth = dbcfg['mysql_info']['auth']
            db = dbcfg['mysql_info']['db']
            # 初始化MySQL
            host, port = address.split(':')
            mysql = MysqlServer(host, int(port), db, user, auth)
            logging.info('执行数据库操作>>> {}'.format(sql))
            if isinstance(sql, str):
                mysql.execute(sql)
            elif isinstance(sql, list):
                for item in sql:
                    mysql.execute(item)
            mysql.close()


if __name__ == '__main__':
    d = {"sql":"SELECT * FROM seal WHERE owner='2875605597074621188';","db":"ums_me"}
    idss = QueryDB.main_query(**d)
    print(idss)

