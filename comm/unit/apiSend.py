# -*- coding:utf-8 -*-
# @Time    : 2021/07/10
# @Author  : Xuanyu Liu
# @File    : apiSend.py
# ***********************
import json
import logging
import allure
import time
from config import INTERVAL
from comm.unit import apiMethod


def send_request(test_info, case_data):
    """
    封装请求
    :param test_info: 测试信息
    :param case_data: 用例数据
    :return:
    """
    try:
        # 获取用例基本信息
        host = test_info["host"]
        method = test_info["method"].upper()
        address = test_info["address"]
        mime_type = test_info["mime_type"]
        headers = test_info["headers"]
        cookies = test_info["cookies"]
        file = test_info["file"]
        timeout = test_info["timeout"]
        summary = case_data["summary"]
        parameter = case_data["parameter"]
        if 'download_name' in case_data.keys():
            download_name = case_data["download_name"]
        else:
            download_name = None
    except Exception as e:
        raise KeyError(f'获取用例基本信息失败：{e}')

    request_url = host + address
    logging.info("=" * 150)
    logging.info(f"请求接口：{str(summary)}")
    logging.info(f"请求地址：{request_url}")
    logging.info(f"请求头: {str(headers)}")
    logging.info(f"请求参数: {str(parameter)}")

    # 判断是否保存cookies
    if summary == 'save_cookies':
        with allure.step("保存cookies信息"):
            allure.attach(name="请求接口", body=str(summary))
            allure.attach(name="请求地址", body=request_url)
            allure.attach(name="请求头", body=str(headers))
            allure.attach(name="请求参数", body=str(parameter))
            apiMethod.save_cookie(headers=headers,
                                  address=request_url,
                                  mime_type=mime_type,
                                  data=parameter,
                                  cookies=cookies,
                                  timeout=timeout)
    # 判断接口请求类型
    if method == 'POST':
        logging.info("请求方法: POST")
        # 判断是否上传文件
        if file:
            result = apiMethod.post(headers=headers,
                                    address=request_url,
                                    mime_type=mime_type,
                                    files=case_data["file"],
                                    data=parameter,
                                    cookies=cookies,
                                    timeout=timeout)
            with allure.step("POST上传文件"):
                allure.attach(name="请求接口", body=str(summary))
                allure.attach(name="请求地址", body=request_url)
                allure.attach(name="请求头", body=str(headers))
                allure.attach(name="请求参数", body=str(parameter))
                allure.attach(name="上传的文件", body=str(case_data["file"]))
                allure.attach(name="请求结果", body=str(result[1]))
        else:
            result = apiMethod.post(headers=headers,
                                    address=request_url,
                                    mime_type=mime_type,
                                    data=parameter,
                                    cookies=cookies,
                                    timeout=timeout)
            with allure.step("POST请求接口"):
                allure.attach(name="请求接口", body=str(summary))
                allure.attach(name="请求地址", body=request_url)
                allure.attach(name="请求头", body=str(headers))
                allure.attach(name="请求参数", body=str(parameter))
                allure.attach(name="请求结果", body=str(result[1]))
            logging.info("请求结果: %s" % str(result))
    elif method == 'GET':
        logging.info("请求方法: GET")
        result = apiMethod.get(headers=headers,
                               address=request_url,
                               data=parameter,
                               cookies=cookies,
                               timeout=timeout,
                               downloadName=download_name)

        with allure.step("GET请求接口"):
            allure.attach(name="请求接口", body=str(summary))
            allure.attach(name="请求地址", body=request_url)
            allure.attach(name="请求头", body=str(headers))
            allure.attach(name="请求参数", body=str(parameter))
            allure.attach(name="请求结果", body=str(result[1]))
    elif method == 'PUT':
        logging.info("请求方法: PUT")
        # 判断是否上传文件
        if file:
            with allure.step("PUT上传文件"):
                allure.attach(name="请求接口", body=str(summary))
                allure.attach(name="请求地址", body=request_url)
                allure.attach(name="请求头", body=str(headers))
                allure.attach(name="请求参数", body=str(parameter))
            result = apiMethod.put(headers=headers,
                                   address=request_url,
                                   mime_type=mime_type,
                                   files=parameter,
                                   cookies=cookies,
                                   timeout=timeout)
        else:
            with allure.step("PUT请求接口"):
                allure.attach(name="请求接口", body=str(summary))
                allure.attach(name="请求地址", body=request_url)
                allure.attach(name="请求头", body=str(headers))
                allure.attach(name="请求参数", body=str(parameter))
            result = apiMethod.put(headers=headers,
                                   address=request_url,
                                   mime_type=mime_type,
                                   data=parameter,
                                   cookies=cookies,
                                   timeout=timeout)
    elif method == 'DELETE':
        logging.info("请求方法: DELETE")
        with allure.step("DELETE请求接口"):
            allure.attach(name="请求接口", body=str(summary))
            allure.attach(name="请求地址", body=request_url)
            allure.attach(name="请求头", body=str(headers))
            allure.attach(name="请求参数", body=str(parameter))
        result = apiMethod.delete(headers=headers,
                                  address=request_url,
                                  data=parameter,
                                  cookies=cookies,
                                  timeout=timeout)
    else:
        result = {"code": None, "data": None}
    logging.info("请求结果: %s" % str(result))
    time.sleep(INTERVAL)
    return result
