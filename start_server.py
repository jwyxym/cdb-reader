from flask import Flask, send_from_directory, jsonify, request, Response
from engineio.async_drivers import gevent
from os.path import exists, join, abspath
from os import mkdir, remove, listdir
from shutil import rmtree, copy
from webbrowser import open_new
from io import BytesIO
from time import ctime
import sys

from read_config import read_card_info
import file_manager
import sqlite_cdb
import unpackage


def get_path():
    def get():
        if hasattr(sys, '_MEIPASS'):
            return sys.executable
        else:
            return abspath(__file__)

    path = get().replace('\\', '/')
    return path[: path.rfind('/')]

app = Flask(__name__)

buffer = f'{get_path()}/dist/buffer'
cdb_backup_folder_path = 'cdb_backup'
pics_folder_path = 'pics'
script_folder_path = 'script'
package_folder_path = 'package'

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and exists(join(f'{get_path()}/dist/', path)):
        return send_from_directory(f'{get_path()}/dist/', path)
    else:
        return send_from_directory(f'{get_path()}/dist/', 'index.html')

@app.route('/api/remove_file', methods = ['POST'])
def remove_file():
    data = request.json
    file = data.get('file')
    file_manager.remove_file(buffer, [pics_folder_path, script_folder_path, package_folder_path, cdb_backup_folder_path], file)
    return jsonify(), 200

@app.route('/api/get_cdbs', methods = ['GET'])
def get_cdbs():
    opened_cdbs = []
    if exists(buffer):
        for file in listdir(buffer):
            if file.endswith('.cdb'):
                opened_cdbs.append(file)
    return jsonify(opened_cdbs), 200

@app.route('/api/create_new_cdb', methods = ['POST'])
def create_new_cdb():
    file_manager.initialize_dir_conceal(buffer)
    file = file_manager.get_only_one_file_path(buffer, f'{str(ctime()).replace(" ", "-").replace(":", "-")}.cdb')
    sqlite_cdb.create_cdb(file)
    return jsonify(), 200

@app.route('/api/search_cdb', methods = ['POST'])
def search_cdb():
    data = request.json
    keyword = data.get('keyword')
    cdb = data.get('cdb')
    result = sqlite_cdb.search_cdb(f'{buffer}/{cdb}', keyword)
    return jsonify(result), 200

@app.route('/api/initialize', methods = ['GET'])
def initialize():
    if not exists(f'{get_path()}/config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400
    info = read_card_info(f'{get_path()}/config/cardinfo_chinese.txt')
    return jsonify(info), 200

@app.route('/api/get_file', methods = ['POST'])
def get_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    file_type = file.content_type
    file_name = file.filename
    
    if file_name == '':
        return jsonify({'error': '没有选择文件'}), 400

    if file:
        file_manager.initialize_dir_conceal(buffer)
        file_path = file_manager.get_only_one_file_path(buffer, file_name)
        file.save(file_path)

        if file_name.endswith('.cdb'):
            copy_cdb_result = file_manager.copy_cdb(file_path, buffer, cdb_backup_folder_path)
            if copy_cdb_result:
                return jsonify(file_path[file_path.rfind('/') + 1 : ]), 200
        elif 'image' in file_type:
            pic_result = file_manager.process_pic(file_path, buffer, pics_folder_path)
            if pic_result:
                remove(file_path)
                return jsonify(pic_result), 200
        
    return jsonify([]), 200

@app.route('/api/get_cdb_menu', methods = ['POST'])
def get_cdb_menu():
    data = request.json
    cdb = data.get('cdb')
    cdb_list = sqlite_cdb.read_cdb(f'{buffer}/{cdb}', 'list')
    if len(cdb_list) == 0:
        return jsonify({'message': '无cdb'}), 200
    return jsonify(cdb_list), 200

@app.route('/api/download_cdb', methods = ['POST'])
def download_cdb():
    data = request.json
    cdb = data.get('cdb')
    file_manager.package_file(sqlite_cdb.read_cdb(f'{buffer}/{cdb}', 'list'), buffer, package_folder_path, pics_folder_path, script_folder_path, cdb)
    download = unpackage.start_package(buffer, package_folder_path, cdb, pics_folder_path, script_folder_path)
    with open(f'{buffer}/{download}', 'rb') as f:
        file_obj = BytesIO(f.read())
        response = Response(file_obj, mimetype = 'application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename = {download}'
        
        return response

@app.route('/api/add_cdb', methods = ['POST'])
def add_cdb():
    data = request.json
    cdb = data.get('cdb')
    return jsonify(sqlite_cdb.add_cdb(f'{buffer}/{cdb}')), 200

@app.route('/api/del_cdb', methods = ['POST'])
def del_cdb():
    data = request.json
    code = data.get('code')
    cdb = data.get('cdb')
    sqlite_cdb.delete_cdb(code, f'{buffer}/{cdb}')
    return jsonify(), 200

@app.route('/api/save_cdb', methods = ['POST'])
def save_cdb():
    data = request.json
    card_data = data.get('data')
    code = data.get('code')
    cdb = data.get('cdb')
    result = ''
    if code != card_data[0]:
        sqlite_cdb.delete_cdb(code, f'{buffer}/{cdb}')
        result += 'removed'
    sqlite_cdb.change_cdb(card_data, f'{buffer}/{cdb}')
    return jsonify(result), 200

@app.route('/api/read_card', methods = ['POST'])
def read_card():
    data = request.json
    _id = data.get('id')
    cdb = data.get('cdb')
    if not exists('./config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400

    card_data = sqlite_cdb.read_cdb(f'{buffer}/{cdb}', 'data', _id)
    if len(card_data) == 0:
        return jsonify({'error': '卡片不存在'}), 400

    card_id = card_data[0]
    if exists(f'{buffer}/{pics_folder_path}/{card_id}.jpg'):
        card_data.append(f'{buffer}/{pics_folder_path}/{card_id}.jpg')
    else:
        card_data.append('/cover.png')
    return jsonify(card_data), 200

if __name__ == '__main__':
    rmtree(buffer, ignore_errors = True)
    open_new('http://127.0.0.1:8000/')
    app.run(host='0.0.0.0', port = 8000)

