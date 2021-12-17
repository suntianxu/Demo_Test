#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author： 刘宣妤
# @file： contract_hook.py
# datetime： 2021/10/18 17:27 
# ide： PyCharm

from comm.utils.getGlobalData import GlobalData


def login_hook():
    login = "这是登陆后的值"
    setattr(GlobalData, 'login', login)
