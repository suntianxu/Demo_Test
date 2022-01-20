from flask import abort, jsonify, Flask, request, Response

app = Flask(__name__)
# 增加配置，支持中文显示
app.config['JSON_AS_ASCII'] = False


@app.route('/v2/document/createbyfile', methods=['POST'])
def get_createbyfile():
    title = request.values.get('title')
    fileType = request.values.get('fileType')
    # 获取到参数
    if title and fileType:
        # 判断两个入参是否都传了
        res = {'result': {'documentId': '2920979517649051655'}, 'code': 0, 'message': 'SUCCESS'}
        return jsonify(res)  # 返回结果
    else:  # 如果name或者价格获取不到的话，返回参数错误
        return jsonify({'code': 1000000, 'message': 'Upload Failed'})


@app.route('/contract/createbycategory', methods=['POST'])
def get_createbycategory():
    categoryId = request.values.get('categoryId')
    documents = request.values.get('documents')
    # 获取到参数
    if categoryId and documents:
        # 判断两个入参是否都传了
        res = {'code': 0, 'contractId': '2920979528029954131', 'message': 'SUCCESS'}
        return jsonify(res)  # 返回结果
    else:  # 如果name或者价格获取不到的话，返回参数错误
        return jsonify({'code': 1000000, 'message': 'Create Failed'})


@app.route('/contract/signbyperson', methods=['POST'])
def get_signbyperson():
    contractId = request.values.get('contractId')
    # 获取到参数
    if contractId:
        # 判断两个入参是否都传了
        res = {'code': 0, 'message': 'SUCCESS'}
        return jsonify(res)  # 返回结果
    else:  # 如果name或者价格获取不到的话，返回参数错误
        return jsonify({'code': 0, 'message': 'FAILED'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
