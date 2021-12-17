# -*- coding:utf-8 -*-
# @Time    : 2021/07/10
# @Author  : Xuanyu Liu
# @File    : queryDatabase.py
# **************************
import pymssql

from comm.db.queryKingBase import KingBaseServer
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
    def __query_sqlserver(sql, count=None, db=None):
        """查询SQLserver数据

        :param count: 查询条数
        :param sql: sql查询语句
        :return:
        """
        # 获取配置信息
        timeout = dbcfg['timeout']
        address = dbcfg['sqlServer_info']['address']
        user = dbcfg['sqlServer_info']['user']
        password = dbcfg['sqlServer_info']['password']
        if not db:
            db = dbcfg['sqlServer_info']['db']
        host, port = address.split(':')
        # 初始化连接
        conn = pymssql.connect(host=host, port=int(port), user=user, password=password, database=db)
        cur = conn.cursor(True)
        logging.info('执行查询>>> {}'.format(sql))
        # 循环查询
        for i in range(int(timeout)):
            try:
                cur.execute(sql)
                if count is not None:
                    result = cur.fetchmany(count)
                else:
                    result = cur.fetchall()
                cur.close()
                conn.close()
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
    def __query_hbase(sql, db=None):
        """查询HBase数据

        :param sql: sql查询语句
        :return:
        """
        # 获取配置信息
        timeout = dbcfg['timeout']
        address = dbcfg['hbase_info']['address']
        if not db:
            db = dbcfg['hbase_info']['db']
        # 检索SQL语句
        exp = r"^select .*? from (.*?) where .*?$"
        table = re.findall(exp, sql.strip())[0]
        # 添加数据库
        if '.' not in table:
            sql = sql.strip().replace(table, db+'.'+table)
        # 初始化HBase
        hbase = PhoenixServer(address)
        logging.info('执行查询>>> {}'.format(sql))
        # 循环查询
        for i in range(int(timeout)):
            try:
                result = hbase.query(sql, is_dict=True)
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
    def __query_es(sql, db=None):
        """查询ES数据

        :param sql: sql查询语句
        :return:
        """
        # 获取配置信息
        timeout = dbcfg['timeout']
        address = dbcfg['es_info']['address']
        if not db:
            db = dbcfg['es_info']['db']
        logging.info('执行查询>>> {}'.format(sql))
        # 循环查询
        for i in range(int(timeout)):
            try:
                result = elastic_search(address, db, sql)
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
    def __query_solr(sql):
        """查询solr数据

        :param sql: sql查询语句
        :return:
        """
        # 获取配置信息
        timeout = dbcfg['timeout']
        address = dbcfg['solr_info']['address']
        logging.info('执行查询>>> {}'.format(sql))
        # 循环查询
        for i in range(int(timeout)):
            try:
                result = search_solr(address, sql)
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
    def __query_kingbase(sql, count=None, db=None):
        """
        人大金仓数据库查询
        :param sql:
        :param count:
        :return:
        """
        # 获取配置信息
        timeout = dbcfg['timeout']
        address = dbcfg['kingbase_info']['address']
        user = dbcfg['kingbase_info']['user']
        password = dbcfg['kingbase_info']['password']
        if not db:
            db = dbcfg['kingbase_info']['db']
        # 初始化
        host, port = address.split(':')
        kingbase = KingBaseServer(host, int(port), db, user, password)
        logging.info('执行查询>>> {}'.format(sql))
        # 循环查询
        for i in range(int(timeout)):
            try:
                result = kingbase.query(sql, is_dict=True, count=count)
                kingbase.close()
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
        elif DB_TYPE.upper() == 'SQLSERVER':
            if isinstance(sql, dict):
                res = QueryDB.__query_sqlserver(sql['SS'], count, db=db)
            else:
                res = QueryDB.__query_sqlserver(sql, count, db=db)
        elif DB_TYPE.upper() == 'KINGBASE':
            if isinstance(sql, dict):
                if 'KB' in sql.keys():
                    res = QueryDB.__query_kingbase(sql['KB'], count, db=db)
                else:
                    res = QueryDB.__query_kingbase(sql['MS'], count, db=db)
            else:
                res = QueryDB.__query_kingbase(sql, count, db=db)
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
        elif DB_TYPE.upper() == 'SQLSERVER':
            address = dbcfg['sqlServer_info']['address']
            user = dbcfg['sqlServer_info']['user']
            password = dbcfg['sqlServer_info']['password']
            db = dbcfg['sqlServer_info']['db']
            host, port = address.split(':')
            # 初始化连接
            conn = pymssql.connect(host=host, port=int(port), user=user, password=password, database=db)
            cur = conn.cursor(True)
            logging.info('执行数据库操作>>> {}'.format(sql))
            try:
                if isinstance(sql, str):
                    cur.execute(sql)
                    conn.commit()
                elif isinstance(sql, list):
                    for item in sql:
                        cur.execute(item)
                        conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cur.close()
                conn.close()
        elif DB_TYPE.upper() == 'KINGBASE':
            address = dbcfg['kingbase_info']['address']
            user = dbcfg['kingbase_info']['user']
            password = dbcfg['kingbase_info']['password']
            db = dbcfg['kingbase_info']['db']
            # 初始化
            host, port = address.split(':')
            kingbase = KingBaseServer(host, int(port), db, user, password)
            logging.info('执行数据库操作>>> {}'.format(sql))
            if isinstance(sql, str):
                kingbase.execute(sql)
            elif isinstance(sql, list):
                for item in sql:
                    kingbase.execute(item)
            kingbase.close()
        else:
            raise Exception("无该数据库连接方式%s" % DB_TYPE)


if __name__ == '__main__':
    d = {"sql":"SELECT * FROM seal WHERE owner='2875605597074621188';","db":"ums_me"}
    idss = QueryDB.main_query(**d)
    print(idss)

