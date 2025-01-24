from flask import Flask, send_from_directory, jsonify, request
from os.path import exists, join
from os import mkdir, remove, listdir
from shutil import rmtree, copy
from webbrowser import open_new

from sqlite_cdb import sql
from read_config import read_card_info
from file_manager import process_pic, copy_cdb, initialize_dir, get_only_one_file_path

app = Flask(__name__, static_folder='dist')

buffer = './dist/buffer'
cdb_backup_folder_path = 'cdb_backup'
pics_folder_path = 'pics'
script_folder_path = 'script'
package_folder_path = 'package'

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
    if exists(f'{buffer}/{file}'):
        remove(f'{buffer}/{file}')
    return jsonify(), 200

@app.route('/api/get_cdbs', methods = ['GET'])
def get_cdbs():
    opened_cdbs = []
    if exists(buffer):
        for file in listdir(buffer):
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
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    file_type = file.content_type
    file_name = file.filename
    
    if file_name == '':
        return jsonify({'error': '没有选择文件'}), 400

    if file:
        initialize_dir(buffer)
        file_path = get_only_one_file_path(buffer, file_name)
        file.save(file_path)

        if file_name.endswith('.cdb'):
            copy_cdb_result = copy_cdb(file_path, buffer, cdb_backup_folder_path)
            if copy_cdb_result:
                return jsonify(file_path[file_path.rfind('/') + 1 : ]), 200
        elif 'image' in file_type:
            pic_result = process_pic(file_path, buffer, pics_folder_path)
            if pic_result:
                remove(file_path)
                return jsonify(pic_result), 200
        
    return jsonify([]), 200

@app.route('/api/read_cdb', methods = ['POST'])
def read_cdb():
    data = request.json
    cdb = data.get('cdb')
    cdb_list = sql(f'{buffer}/{cdb}', 'list')
    if len(cdb_list) == 0:
        return jsonify({'error': '无法读取cdb文件'}), 400
    return jsonify(cdb_list), 200

@app.route('/api/save_cdb', methods = ['POST'])
def save_cdb():
    data = request.json
    card_data = data.get('data')
    code = data.get('code')
    return jsonify(), 200

@app.route('/api/read_card', methods = ['POST'])
def read_card():
    data = request.json
    page = data.get('page')
    card = data.get('card')
    cdb = data.get('cdb')
    if not exists('./config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400

    card_data = sql(f'{buffer}/{cdb}', 'data')
    if exists(f'{buffer}/pics/{card_data[int(page)][int(card)][0]}.jpg'):
        card_data[int(page)][int(card)].append(f'{buffer}/pics/{card_data[int(page)][int(card)][0]}.jpg')
    else:
        card_data[int(page)][int(card)].append('/cover.png')
    return jsonify([card_data[0], card_data[int(page)][int(card)]]), 200

if __name__ == '__main__':
    rmtree(buffer, ignore_errors = True)
    open_new('http://127.0.0.1:8000/')
    app.run(host = '127.0.0.1', port = 8000)