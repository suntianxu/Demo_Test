# -*- coding:utf-8 -*-
# @Time    : 2021/09/07
# @Author  : Xuanyu Liu
# @File    : queryKingBase.py
# **************************
import jaydebeapi
import logging

from config import SOURCE_DIR


class KingBaseServer:
    """
    封装Kingbase常用方法。
    """
    def __init__(self, host, port, db, user, passwd):
        # 初始化数据库
        logging.debug(f'Connect MySQL: host={host}, port={port}, db={db}, user={user}, passwd={passwd}')
        try:
            url = f'jdbc:kingbase8://{host}:{port}/{db}'
            dirver = 'com.kingbase8.Driver'
            jarFile = SOURCE_DIR + 'kingbase8-8.2.0.jar'
            self.conn = jaydebeapi.connect(dirver, url, [user, passwd], jarFile)
        except Exception as e:
            raise Exception('连接异常>>> {}'.format(e))

    # 增加、修改、删除命令语句
    def execute(self, sql):
        try:
            # 创建游标
            curs = self.conn.cursor()
            # 执行sql语句
            curs.execute(sql)
            # 提交事务
            self.conn.commit()
            # 关闭游标
            curs.close()
        except Exception as e:
            # 出错时回滚
            self.conn.rollback()
            raise Exception(f'执行异常>>> {e}')

    # 查询所有数据,多个值
    def query(self, sql, is_dict, count=None):
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            res = cur.fetchall()
            column_name = cur.description
            # 关闭游标
            cur.close()
            if is_dict:
                res_dict = list()
                char = [i[0] for i in column_name]
                for item in res:
                    list_item = list(item)
                    to = dict(zip(char, list_item))
                    res_dict.append(to)
                if count:
                    data = res_dict[0:count]
                    return data
                else:
                    return res_dict
            else:
                return res
        except Exception as e:
            raise Exception(f'查询异常>>> {e}')

    # 关闭数据库连接
    def close(self):
        self.conn.close()


if __name__ == '__main__':
    pass
