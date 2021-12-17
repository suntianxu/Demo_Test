# -*- coding:utf-8 -*-
# @Time    : 2021/07/10
# @Author  : Xuanyu Liu
# @File    : checkResult.py
# ***************************
import re
import allure
import logging
from jsonpath import jsonpath
from decimal import Decimal
from comm.unit import readRelevance, replaceRelevance
from hamcrest import *


def check_json(src_data, dst_data):
    """
    校验的json  检查json各字段格式是否一致，和关键字是否存在
    :param src_data: 检验内容
    :param dst_data: 接口返回的数据
    :return:
    """
    if isinstance(src_data, list):
        for key in src_data:
            res = jsonpath(dst_data, key[1])
            if res:
                if key[0] == "eq":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果等于{key[2]}", body=f"期望值：{key[2]};实际值：{res[0]}")
                    try:
                        assert_that(res[0], equal_to(key[2]))
                    except AssertionError:
                        raise Exception("关键字校验失败！ jsonPath匹配%s 的结果值 %s ! = %s" % (key[1], res[0], key[2]))
                elif key[0] == "contain":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果包含{key[2]}", body=f"期望值：{key[2]};实际值：{res[0]}")
                    try:
                        assert_that(res[0], contains_string(key[2]))
                    except AssertionError:
                        raise Exception("关键字校验失败！ jsonPath匹配%s 的结果值 %s 不包含 %s" % (key[1], res[0], key[2]))
                elif key[0] == "lt":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果小于{key[2]}", body=f"期望值：{key[2]};实际值：{res[0]}")
                    try:
                        assert_that(res[0], less_than(key[2]))
                    except AssertionError:
                        raise Exception("关键字数值大小校验失败！jsonPath匹配%s 的结果值为 %s 不小于 期望值 %s" % (key[1], res[0], key[2]))
                elif key[0] == "gt":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果大于{key[2]}", body=f"期望值：{key[2]};实际值：{res[0]}")
                    try:
                        assert_that(res[0], greater_than(key[2]))
                    except AssertionError:
                        raise Exception("关键字数值大小校验失败！jsonPath匹配%s 的结果值为 %s 不大于 期望值 %s" % (key[1], res[0], key[2]))
                elif key[0] == "le":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果小于等于{key[2]}", body=f"期望值：{key[2]};实际值：{res[0]}")
                    try:
                        assert_that(res[0], less_than_or_equal_to(key[2]))
                    except AssertionError:
                        raise Exception("关键字数值大小校验失败！jsonPath匹配%s 的结果值为 %s 不小于等于 期望值 %s" % (key[1], res[0], key[2]))
                elif key[0] == "ge":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果大于等于{key[2]}", body=f"期望值：{key[2]};实际值：{res[0]}")
                    try:
                        assert_that(res[0], greater_than_or_equal_to(key[2]))
                    except AssertionError:
                        raise Exception("关键字数值大小校验失败！jsonPath匹配%s 的结果值为 %s 不大于等于 期望值 %s" % (key[1], res[0], key[2]))
                elif key[0] == "ne":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果不等于{key[2]}", body=f"期望值：{key[2]};实际值：{res[0]}")
                    try:
                        assert_that(res[0], is_not(equal_to(key[2])))
                    except AssertionError:
                        raise Exception("关键字数值大小校验失败！jsonPath匹配%s 的结果值为 %s 等于 期望值 %s" % (key[1], res[0], key[2]))
                elif key[0] == "is_none":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果为空", body=f"期望值：为空;实际值：{res[0]}")
                    try:
                        assert_that(res[0], none())
                    except AssertionError:
                        raise Exception("关键字校验失败！ jsonPath匹配%s 的结果值不为空" % (key[1]))
                elif key[0] == "not_none":
                    with allure.step(f"校验条件：{key} 返回参数值校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果不为空", body=f"期望值：不为空;实际值：{res[0]}")
                    try:
                        assert_that(res[0], not_none())
                    except AssertionError:
                        raise Exception("关键字校验失败！ jsonPath匹配%s 的结果值为空" % (key[1]))
                elif key[0] == "=":
                    with allure.step(f"校验条件：{key} 返回参数长度校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果长度值等于{key[2]}", body=f"期望值：{key[2]};实际值：{len(res[0])}")
                    try:
                        assert_that(res[0], has_length(key[2]))
                    except AssertionError:
                        raise Exception("关键字长度校验失败！ jsonPath匹配%s 的结果值长度为 %s 与期望长度 %s 不相等" % (key[1], len(res[0]), key[2]))
                elif key[0] == "<":
                    with allure.step(f"校验条件：{key} 返回参数长度校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果长度值小于{key[2]}", body=f"期望值：{key[2]};实际值：{len(res[0])}")
                    try:
                        assert_that(len(res[0]), less_than(key[2]))
                    except AssertionError:
                        raise Exception("关键字长度校验失败！jsonPath匹配%s 的结果值长度为 %s 不小于 期望长度 %s" % (key[1], len(res[0]), key[2]))
                elif key[0] == ">":
                    with allure.step(f"校验条件：{key} 返回参数长度校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果长度值大于{key[2]}", body=f"期望值：{key[2]};实际值：{len(res[0])}")
                    try:
                        assert_that(len(res[0]), greater_than(key[2]))
                    except AssertionError:
                        raise Exception("关键字长度校验失败！jsonPath匹配%s 的结果值长度为 %s 不大于 期望长度 %s" % (key[1], len(res[0]), key[2]))
                elif key[0] == ">=":
                    with allure.step(f"校验条件：{key} 返回参数长度校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果长度值大于等于{key[2]}", body=f"期望值：{key[2]};实际值：{len(res[0])}")
                    try:
                        assert_that(len(res[0]), greater_than_or_equal_to(key[2]))
                    except AssertionError:
                        raise Exception("关键字长度校验失败！jsonPath匹配%s 的结果值长度为 %s 不大于等于 期望长度 %s" % (key[1], len(res[0]), key[2]))
                elif key[0] == "<=":
                    with allure.step(f"校验条件：{key} 返回参数长度校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果长度值小于等于{key[2]}", body=f"期望值：{key[2]};实际值：{len(res[0])}")
                    try:
                        assert_that(len(res[0]), less_than_or_equal_to(key[2]))
                    except AssertionError:
                        raise Exception("关键字长度校验失败！jsonPath匹配%s 的结果值长度为 %s 不小于等于 期望长度 %s" % (key[1], len(res[0]), key[2]))
                elif key[0] == "!=":
                    with allure.step(f"校验条件：{key} 返回参数长度校验结果"):
                        allure.attach(name=f"{key[1]}的匹配结果长度值不等于{key[2]}", body=f"期望值：{key[2]};实际值：{len(res[0])}")
                    try:
                        assert_that(len(res[0]), is_not(equal_to(key[2])))
                    except AssertionError:
                        raise Exception("关键字长度校验失败！jsonPath匹配%s 的结果值长度为 %s 等于 期望长度 %s" % (key[1], len(res[0]), key[2]))
            else:
                raise Exception("JSON格式校验，关键字 %s 不在返回结果 %s 中！" % (key, dst_data))

    else:
        raise Exception("JSON校验内容非list格式：{}".format(src_data))


def check_database(actual, expected, mark=''):
    """校验数据库

    :param actual: 实际结果
    :param expected: 期望结果
    :param mark: 标识
    :return:
    """
    if isinstance(actual, dict) and isinstance(expected, dict):
        result = list()
        logging.info('校验数据库{}>>>'.format(mark))
        content = '\n%(key)-20s%(actual)-40s%(expected)-40s%(result)-10s' \
                % {'key': 'KEY', 'actual': 'ACTUAL', 'expected': 'EXPECTED', 'result': 'RESULT'}
        for key in expected:
            if key in actual:
                actual_value = actual[key]
            else:
                actual_value = None
            expected_value = expected[key]
            if actual_value or expected_value:
                if isinstance(actual_value, (int, float, Decimal)):
                    if int(actual_value) == int(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
                else:
                    if str(actual_value) == str(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
            else:
                rst = 'PASS'
            result.append(rst)
            line = '%(key)-20s%(actual)-40s%(expected)-40s%(result)-10s' \
                % {'key': key, 'actual': str(actual_value) + ' ',
                            'expected': str(expected_value) + ' ', 'result': rst}
            content = content + '\n' + line
        logging.info(content)
        allure.attach(name="校验数据库详情{}".format(mark[-1]), body=str(content))
        if 'FAIL' in result:
            raise AssertionError('校验数据库{}未通过！'.format(mark))

    elif isinstance(actual, list) and isinstance(expected, list):
        result = list()
        logging.info('校验数据库{}>>>'.format(mark))
        content = '\n%(key)-25s%(actual)-35s%(expected)-35s%(result)-10s' \
                % {'key': 'INDEX', 'actual': 'ACTUAL', 'expected': 'EXPECTED', 'result': 'RESULT'}
        for index in range(len(expected)):
            if index < len(actual):
                actual_value = actual[index]
            else:
                actual_value = None
            expected_value = expected[index]
            if actual_value or expected_value:
                if isinstance(actual_value, (int, float, Decimal)):
                    if int(actual_value) == int(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
                else:
                    if str(actual_value) == str(expected_value):
                        rst = 'PASS'
                    else:
                        rst = 'FAIL'
            else:
                rst = 'PASS'
            result.append(rst)
            line = '%(key)-25s%(actual)-35s%(expected)-35s%(result)-10s' \
                % {'key': index, 'actual': str(actual_value) + ' ',
                            'expected': str(expected_value) + ' ', 'result': rst}
            content = content + '\n' + line
        logging.info(content)
        allure.attach(name="校验数据库详情{}".format(mark[-1]), body=str(content))
        if 'FAIL' in result:
            raise AssertionError('校验数据库{}未通过！'.format(mark))

    else:
        logging.info('校验数据库{}>>>'.format(mark))
        logging.info('ACTUAL: {}\nEXPECTED: {}'.format(actual, expected))
        if str(expected) != str(actual):
            raise AssertionError('校验数据库{}未通过！'.format(mark))


def check_result(case_data, code, data):
    """
    校验测试结果
    :param case_data: 用例数据
    :param code: 接口状态码
    :param data: 返回的接口json数据
    :return:
    """
    try:
        # 获取用例检查信息
        check_type = case_data['check_body']['check_type']
        expected_code = case_data['check_body']['expected_code']
        expected_result = case_data['check_body']['expected_result']
    except Exception as e:
        raise KeyError('获取用例检查信息失败：{}'.format(e))

    # 接口数据校验
    if check_type == 'no_check':
        with allure.step("不校验接口结果"):
            pass

    elif check_type == 'check_code':
        with allure.step("仅校验接口状态码"):
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="期望code", body=str(expected_code))
            allure.attach(name='实际data', body=str(data))
        if int(code) != expected_code:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    elif check_type == 'check_json':
        urlpar = r'[a-zA-z]+://[^\s]*\''
        urlR = re.findall(urlpar, str(data))
        if urlR:
            for url in urlR:
                url = url.strip("'")
                allure.dynamic.link(str(url), name='检测到有URL,可点击查看链接')
        with allure.step("JSON格式及参数校验接口"):
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="期望code", body=str(expected_code))
            allure.attach(name='实际data', body=str(data))
            allure.attach(name='期望data', body=str(expected_result))
        if int(code) == expected_code:
            if not data:
                data = "{}"
            check_json(expected_result, data)
        else:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    elif check_type == 'entirely_check':
        with allure.step("完全校验接口结果"):
            allure.attach(name="实际code", body=str(code))
            allure.attach(name="期望code", body=str(expected_code))
            allure.attach(name='实际data', body=str(data))
            allure.attach(name='期望data', body=str(expected_result))
        urlpar = r'[a-zA-z]+://[^\s]*\''
        urlR = re.findall(urlpar, str(data))
        if urlR:
            for url in urlR:
                url = url.strip("'")
                allure.dynamic.link(str(url), name='检测到有URL,可点击查看链接')
        if int(code) == expected_code:
            try:
                assert_that(expected_result, equal_to(data))
            except AssertionError:
                raise Exception("完全校验失败！ %s ! = %s" % (expected_result, data))
        else:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    elif check_type == 'regular_check':
        if int(code) == expected_code:
            try:
                result = ""
                if isinstance(expected_result, list):
                    for i in expected_result:
                        result = re.findall(i.replace("\"", "\""), str(data))
                        allure.attach('校验完成结果\n', str(result))
                else:
                    result = re.findall(expected_result.replace("\"", "\'"), str(data))
                    urlpar = r'[a-zA-z]+://[^\s]*\''
                    urlR = re.findall(urlpar, str(data))
                    if urlR:
                        for url in urlR:
                            url = url.strip("'")
                            allure.dynamic.link(str(url), name='检测到有URL,可点击查看链接')
                    with allure.step("正则校验接口结果"):
                        allure.attach(name="实际code", body=str(code))
                        allure.attach(name="期望code", body=str(expected_code))
                        allure.attach(name='实际data', body=str(data))
                        allure.attach(name='期望data', body=str(expected_result).replace("\'", "\""))
                        allure.attach(name=expected_result.replace("\"", "\'") + '校验完成结果',
                                      body=str(result).replace("\'", "\""))
                if not result:
                    raise Exception("正则未校验到内容！ %s" % expected_result)
            except KeyError:
                raise Exception("正则校验执行失败！ %s\n正则表达式为空时" % expected_result)
        else:
            raise Exception("接口状态码错误！\n %s != %s" % (code, expected_code))

    else:
        raise Exception("无该接口校验方式%s" % check_type)

    # 判断是否存在数据库校验标识
    if 'check_db' in case_data:
        from comm.unit import queryDatabase as qdb
        check_db = case_data['check_db']
        # 获取数据库期望结果：获取期望结果-获取关联值-替换关联值
        data['parameter'] = case_data['parameter']
        __relevance = readRelevance.get_relevance(data, check_db)
        check_db = replaceRelevance.replace(check_db, __relevance)

        # 循环校验数据库
        for each in check_db:
            try:
                check_type = each['check_type']
                execute_sql = each['execute_sql']
                expected_result = each['expected_result']
            except KeyError as e:
                raise KeyError('【check_db】存在错误字段！\n{}'.format(e))
            except TypeError:
                raise KeyError("【check_db】类型错误，期望<class 'list'>，而不是%s！" % type(expected_result))
            if not isinstance(expected_result, list):
                raise KeyError("【expected_result】类型错误，期望<class 'list'>，而不是%s！" % type(expected_result))

            # 检索SQL语句
            exp = r"^select (.*?) from (.*?) where (.*?)$"
            res = re.findall(exp, execute_sql.strip().lower())[0]
            for r in res:
                if not each:
                    msg = '标准格式: ' + exp
                    raise Exception('无效SQL>>> {}\n{}'.format(execute_sql, msg))
            # 判断数据库检查类型
            actual = qdb.QueryDB.main_query(execute_sql)

            # 增加输出并进行数据校验
            mark = check_type.replace('check_', '').upper() + '['+res[1]+']'
            with allure.step("校验数据库{}".format(mark)):
                allure.attach(name="实际结果", body=str(actual))
                allure.attach(name='期望结果', body=str(expected_result))
                if "expected_num" in each.keys():
                    expected_num = each['expected_num']
                    allure.attach(name="实际行数", body=str(len(actual)))
                    allure.attach(name='期望行数', body=str(expected_num))
                    # 验证数据库实际结果数量是否正确
                    if len(actual) != int(expected_num):
                        raise AssertionError('校验数据库{}行数未通过！'.format(mark))
                # 检查实际结果中第一条结果值 ***************
                for index, expected in enumerate(expected_result):
                    try:
                        check_database(actual[index], expected, mark+str(index))
                    except IndexError:
                        raise IndexError('校验数据库{}失败，期望结果超出实际条目！'.format(mark+str(index)))


if __name__ == '__main__':
    dst = {'result': {'id': '2880030815012520156', 'bizId': 'CLOUDOPENaFbf6d984E', 'subject': '发起草稿合同，发企业 2021-09-27 16:54:16', 'sn': '202109270000165', 'tenantName': 'CloudOpenApiAuto注册公司', 'ordinal': True, 'category': {'id': '2875605598081122918', 'name': '默认业务分类'}, 'creator': {'name': '刘宣妤', 'contact': '15823887943', 'contactType': 'MOBILE'}, 'status': 'DRAFT', 'expireTime': '2021-10-27 16:54:14', 'signatories': [{'id': '2880030815280955614', 'tenantType': 'COMPANY', 'status': 'DRAFT', 'tenantName': 'CloudOpenApiAuto注册公司', 'receiver': {'name': '刘宣妤', 'contact': '15823887943', 'contactType': 'MOBILE'}, 'serialNo': 0, 'actions': [{'id': '2880030815314510047', 'type': 'LP', 'status': 'INIT', 'name': '法人签字', 'serialNo': 0}], 'delaySet': False, 'sponsor': True}]}, 'code': 0, 'message': 'SUCCESS'}
    src = {"check_body": {
          "check_type": "check_json",
          "expected_code": 200,
          "expected_result": [
          ["gt", "code", -1],
          ["not_none", "message", "SUCCESS"],
          ["!=", "$..signatories", 2]
          ]}}
    check_result(src, 200, dst)
