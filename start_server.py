from flask import Flask, send_from_directory, jsonify, request
from os.path import exists, join
from os import mkdir, remove
from shutil import rmtree
from ctypes import windll

from sqlite_cdb import sql
from read_config import read_card_info

app = Flask(__name__, static_folder='dist')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if exists('./uploads'):
        rmtree('./uploads')
    if path != "" and exists(join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/remove_file', methods = ['POST'])
def remove_file():
    data = request.json
    file = data.get('file')
    if exists(f'./uploads/{file}'):
        remove(f'./uploads/{file}')
    return jsonify(), 200

@app.route('/api/initialize', methods = ['GET'])
def initialize():
    if not exists('./config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400
    info = read_card_info('./config/cardinfo_chinese.txt')
    return jsonify(info), 200

@app.route('/api/get_file', methods = ['POST'])
def get_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    file_name = file.filename
    
    if file_name == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = f'./uploads/{file_name}'

        if not exists('./uploads'):
            mkdir('./uploads')
            windll.kernel32.SetFileAttributesW('./uploads', 2)

        i = 1
        while exists(file_path):
            file_path = f'./uploads/{file_name[ : file_name.find(".")]}({i}){file_name[file_name.find(".") : ]}'
            i += 1

        file.save(file_path)

        if file_name.endswith('.cdb'):
            return jsonify([file_path[file_path.rfind('/') + 1 : ]]), 200
        
    return jsonify([]), 200

@app.route('/api/read_cdb', methods = ['POST'])
def read_cdb():
    data = request.json
    cdb = data.get('cdb')
    cdb_list = sql(f'./uploads/{cdb}', 'list')
    if len(cdb_list) == 0:
        return jsonify({'error': '无法读取cdb文件'}), 400
    return jsonify(cdb_list)

@app.route('/api/read_card', methods = ['POST'])
def read_card():
    data = request.json
    page = data.get('page')
    card = data.get('card')
    cdb = data.get('cdb')
    if not exists('./config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400
    return jsonify(sql(f'./uploads/{cdb}', 'data')[int(page)][int(card)])

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
