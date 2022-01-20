#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @author： 刘宣妤
# @file： client.py
# datetime： 2022/1/20 17:09 
# ide： PyCharm
import requests

body ={
'file': '20150320010101001',
'fileType': 'PDF',
    'title': "pdf"
}

resp = requests.post('http://127.0.0.1:5000/v2/document/createbyfile', data=body)
print(resp.json())


