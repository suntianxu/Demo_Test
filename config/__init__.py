# -*- coding:utf-8 -*-
# @Time    : 2020/12/03
# @Author  : Leo Zhang
# @File    : __init__.py
# ***********************
from pathlib import Path

from comm.utils.readYaml import read_yaml_data
import os

# 获取主目录路径
ROOT_DIR = str(os.path.realpath(__file__)).split('config')[0].replace('\\', '/')

# 获取配置文件路径
API_CONFIG = ROOT_DIR+'config/apiConfig.yml'    # ip header等
PARAM_CONFIG = ROOT_DIR+'config/paramConfig.yml'    # 替换参数等
RUN_CONFIG = ROOT_DIR+'config/runConfig.yml'    # 用例目录 用例执行机制等
DB_CONFIG = ROOT_DIR+'config/dbConfig.yml'      # 数据库配置
REQUEST_CONFIG = ROOT_DIR+'config/requestConfig.yml'    # 请求替换参数关连池

# 获取运行配置信息
RC = read_yaml_data(RUN_CONFIG)
AC = read_yaml_data(API_CONFIG)
INTERVAL = RC['interval']    # 接口调用间隔时间
PROJECT_NAME = RC['project_name']     # 运行项目名称
# 工程使用数据库类型
DB_TYPE = AC[PROJECT_NAME]['dbType'].upper()
SQL_CONFIG = ROOT_DIR + 'config/sql.yaml'
SC = read_yaml_data(SQL_CONFIG)

if Path(ROOT_DIR+PROJECT_NAME).is_dir():
    # 接口数据目录(.chlsj文件)
    DATA_DIR = ROOT_DIR+PROJECT_NAME+'/data'
    # 测试数据目录(test_xxxxx.yaml)
    PAGE_DIR = ROOT_DIR+PROJECT_NAME+'/page'
    # 测试脚本目录(test.py)
    TEST_DIR = ROOT_DIR+PROJECT_NAME+'/testcase'
else:
    # 接口数据目录(.chlsj文件)
    DATA_DIR = ROOT_DIR+'PyDemo'+'/data'
    # 测试数据目录(test_xxxxx.yaml)
    PAGE_DIR = ROOT_DIR+'PyDemo'+'/page'
    # 测试脚本目录(test.py)
    TEST_DIR = ROOT_DIR+'PyDemo'+'/testcase'

# 测试报告目录(xml|html)
REPORT_DIR = ROOT_DIR + 'report'
# 上传文件目录(用于需要上传文件的接口存放文件)
UPLOAD_DIR = ROOT_DIR + 'data_warehouse/upload/'
# 下载文件存放目录
DOWNLOAD_DIR = ROOT_DIR + 'data_warehouse/download/'
# 资源存放目录
SOURCE_DIR = ROOT_DIR + 'data_warehouse/source/'


if __name__ == '__main__':
    print(RC)


