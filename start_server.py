from flask import Flask, send_from_directory, jsonify, request
from os.path import exists, join
from os import mkdir, remove, listdir
from shutil import rmtree
from ctypes import windll
from webbrowser import open_new
from asyncio import run, get_running_loop

from sqlite_cdb import sql
from read_config import read_card_info

app = Flask(__name__, static_folder='dist')

cache = './dist/cache'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and exists(join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/remove_file', methods = ['POST'])
def remove_file():
    data = request.json
    file = data.get('file')
    if exists(f'{cache}/{file}'):
        remove(f'{cache}/{file}')
    return jsonify(), 200

@app.route('/api/get_cdbs', methods = ['GET'])
def get_cdbs():
    opened_cdbs = []
    if exists(cache):
        for file in listdir(cache):
            if file.endswith('.cdb'):
                opened_cdbs.append(file)
    return jsonify(opened_cdbs), 200

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
        file_path = f'{cache}/{file_name}'

        if not exists(cache):
            mkdir(cache)
            windll.kernel32.SetFileAttributesW(cache, 2)

        i = 1
        while exists(file_path):
            file_path = f'{cache}/{file_name[ : file_name.find(".")]}({i}){file_name[file_name.find(".") : ]}'
            i += 1

        file.save(file_path)

        if file_name.endswith('.cdb'):
            return jsonify([file_path[file_path.rfind('/') + 1 : ]]), 200
        
    return jsonify([]), 200

@app.route('/api/read_cdb', methods = ['POST'])
def read_cdb():
    data = request.json
    cdb = data.get('cdb')
    cdb_list = sql(f'{cache}/{cdb}', 'list')
    if len(cdb_list) == 0:
        return jsonify({'error': '无法读取cdb文件'}), 400
    return jsonify(cdb_list), 200

@app.route('/api/read_card', methods = ['POST'])
def read_card():
    data = request.json
    page = data.get('page')
    card = data.get('card')
    cdb = data.get('cdb')
    if not exists('./config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400

    card_data = sql(f'{cache}/{cdb}', 'data')[int(page)][int(card)]
    if exists(f'{cache}/pics/{card_data[0]}.jpg'):
        card_data.append(f'{cache}/pics/{card_data[0]}.jpg')
    else:
        card_data.append('/cover.png')
    return jsonify(card_data), 200

async def start_server():
    loop = get_running_loop()
    loop.run_in_executor(None, open_new, 'http://127.0.0.1:8000/')

    await app.run(host = '127.0.0.1', port = 8000)

if __name__ == '__main__':
    run(start_server())