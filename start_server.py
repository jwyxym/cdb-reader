from flask import Flask, send_from_directory, jsonify, request, Response
from os.path import exists, join
from os import mkdir, remove, listdir
from shutil import rmtree, copy
from webbrowser import open_new
from io import BytesIO
from time import ctime
from sqlite_cdb import read_cdb, change_cdb, delete_cdb, create_cdb
from read_config import read_card_info
import file_manager

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
    file_manager.initialize_dir(buffer)
    file = file_manager.get_only_one_file_path(buffer, f'cards-{str(ctime()).replace(" ", "-").replace(":", "-")}.cdb')
    create_cdb(file)
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
        return jsonify({'error': '没有文件'}), 400
    
    file = request.files['file']
    file_type = file.content_type
    file_name = file.filename
    
    if file_name == '':
        return jsonify({'error': '没有选择文件'}), 400

    if file:
        file_manager.initialize_dir(buffer)
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
    cdb_list = read_cdb(f'{buffer}/{cdb}', 'list')
    if len(cdb_list) == 0:
        return jsonify({'message': '无cdb'}), 200
    return jsonify(cdb_list), 200

@app.route('/api/download_cdb', methods = ['POST'])
def download_cdb():
    data = request.json
    cdb = data.get('cdb')

#没改完
    # download, down_name = package_zip(f'{buffer}/{cdb}')
    download, down_name = '1.ypk', '1'
    with open(f'{buffer}/{download}', 'rb') as f:
        file_obj = BytesIO(f.read())
        response = Response(file_obj, mimetype = 'application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename = {down_name}.ypk'
        
        return response

@app.route('/api/del_cdb', methods = ['POST'])
def del_cdb():
    data = request.json
    code = data.get('code')
    cdb = data.get('cdb')
    delete_cdb(code, f'{buffer}/{cdb}')
    return jsonify(), 200

@app.route('/api/save_cdb', methods = ['POST'])
def save_cdb():
    data = request.json
    card_data = data.get('data')
    code = data.get('code')
    cdb = data.get('cdb')
    result = ''
    if code != card_data[0]:
        delete_cdb(code, f'{buffer}/{cdb}')
        result += 'removed'
    change_cdb(card_data, f'{buffer}/{cdb}')
    return jsonify(result), 200

@app.route('/api/read_card', methods = ['POST'])
def read_card():
    data = request.json
    page = data.get('page')
    card = data.get('card')
    cdb = data.get('cdb')
    if not exists('./config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400

    card_data = read_cdb(f'{buffer}/{cdb}', 'data')

    if exists(f'{buffer}/pics/{card_data[int(page)][int(card)][0]}.jpg'):
        card_data[int(page)][int(card)].append(f'{buffer}/pics/{card_data[int(page)][int(card)][0]}.jpg')
    else:
        card_data[int(page)][int(card)].append('/cover.png')
    return jsonify([card_data[0][0], card_data[int(page)][int(card)]]), 200

if __name__ == '__main__':
    rmtree(buffer, ignore_errors = True)
    open_new('http://127.0.0.1:8000/')
    app.run(host = '0.0.0.0', port = 8000)

