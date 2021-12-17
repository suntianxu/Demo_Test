# -*- coding:utf-8 -*-
# @Time    : 2021/07/10
# @Author  : Xuanyu Liu
# @File    : readYaml.py
# ***********************


def read_yaml_data(yaml_file):
	"""读取yaml文件数据

	:param yaml_file: yaml文件地址
	:return:
	"""
	import yaml
	yaml_file = yaml_file.replace('\\', '/')
	with open(yaml_file, 'r', encoding="utf-8") as fr:
		return yaml.load(fr, Loader=yaml.SafeLoader)


def write_yaml_file(yaml_file, obj):
	"""把对象obj写入yaml文件

	:param yaml_file: yaml文件地址
	:param obj: 数据对象
	:return:
	"""
	from ruamel import yaml
	with open(yaml_file, 'w', encoding='utf-8') as fw:
		yaml.dump(obj, fw, Dumper=yaml.RoundTripDumper, allow_unicode=True)


def rewrite_yaml_file(yaml_file, mode,  section, value):
	import yaml
	with open(yaml_file, encoding='utf-8') as fp:
		read_yml_str = fp.read()  # 读出来是字符串
		d = yaml.safe_load(read_yml_str)  # 用load方法转字典
	d[mode][section] = value
	with open(yaml_file, 'w', encoding='utf-8') as f:
		yaml.dump(d, f, allow_unicode=True)


if __name__ == '__main__':
	s = ["aaa", "bbb"]
	case_dict = read_yaml_data(r"D:/pythonProject/ApiTesting_0718/ApiTesting/PyDemo/page" + "/contract_sign/test_ContractSignUrlSend.yaml")
	# rewrite_yaml_file(case_yaml, 'PyDemo', "documentIds", s)
	# rewrite_yaml_file(case_yaml, 'PyDemo', "documentId_1", s[0])
	# case_dict_1 = read_yaml_data(case_yaml)
	print(case_dict)
	# print(case_dict_1)
