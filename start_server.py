from flask import Flask, send_from_directory, jsonify, request, Response
from os.path import exists, join, abspath
from os import mkdir, remove, listdir, walk
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

    path = get()
    return path[: path.rfind('\\')]

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

buffer = join(get_path(), 'dist\\buffer')
cdb_backup_folder_path = join(buffer, 'cdb_backup')
center_pics_folder_path = join(buffer, 'center_pics')
auto_pics_folder_path = join(buffer, 'auto_pics')
pics_folder_path = join(buffer, 'pics')
script_folder_path = join(buffer, 'script')
package_folder_path = join(buffer, 'package')
unpackage_folder_path = join(buffer, 'unpackage')

@app.route('/', defaults = {'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and exists(join(get_path(), 'dist\\', path)):
        return send_from_directory(join(get_path(), 'dist\\'), path)
    else:
        return send_from_directory(join(get_path(), 'dist\\'), 'index.html')

@app.route('/api/get_pics', methods=['POST'])
def get_pics():
    if 'file' not in request.files:
        return jsonify(), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify(), 400

    file_manager.initialize_dir_conceal(auto_pics_folder_path)
    filepath = join(auto_pics_folder_path, file.filename)
    file.save(filepath)
    
    return jsonify(), 200

@app.route('/api/remove_file', methods = ['POST'])
def remove_file():
    data = request.json
    file = data.get('file')
    file_manager.remove_file(file)
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
    file = file_manager.get_only_one_file_path(f'{str(ctime()).replace(" ", "-").replace(":", "-")}.cdb')
    sqlite_cdb.create_cdb(file)
    return jsonify(), 200

@app.route('/api/search_cdb', methods = ['POST'])
def search_cdb():
    data = request.json
    keyword = data.get('keyword')
    cdb = data.get('cdb')
    result = sqlite_cdb.search_cdb(join(buffer, cdb), keyword)
    return jsonify(result), 200

@app.route('/api/initialize', methods = ['GET'])
def initialize():
    if not exists(join(get_path(), 'config\\cardinfo_chinese.txt')):
        return jsonify({'error': '无法读取卡片信息'}), 400
    info = read_card_info(join(get_path(), 'config\\cardinfo_chinese.txt'))
    return jsonify(info), 200

@app.route('/api/get_center_pic', methods=['POST'])
def get_center_pic():
    file = request.files.get('file')
    if not file:
        return jsonify(), 400

    file_manager.initialize_dir(center_pics_folder_path)
    file.save(join(center_pics_folder_path, file.filename))
    return jsonify(f'./buffer/{center_pics_folder_path[center_pics_folder_path.rfind("\\") + 1 : ]}/{file.filename}'), 200

@app.route('/api/get_file', methods = ['POST'])
def get_file():

    if 'files[]' not in request.files:
        return jsonify({'error': '没有文件'}), 400
    
    files = request.files.getlist('files[]')
    if not files:
        return jsonify({'error': '没有选择文件'}), 400

    file_manager.initialize_dir_conceal(buffer)

    result = []
    for file in files:
        file_type = file.content_type
        file_name = file.filename
        if file_name == '':
            continue

        file_path = file_manager.get_only_one_file_path(file_name)
        file.save(file_path)

        if file_name.lower().endswith('.cdb'):
            result.append(file_manager.copy_cdb(file_path, file_name))
        elif 'image' in file_type:
            result.append(file_manager.process_pic(file_path))
            remove(file_path)
        elif 'text' in file_type or file_name.lower().endswith('.lua'):
            lua_result = file_manager.copy_text(file_path)
            if lua_result:
                remove(lua_result)
        elif file_name.lower().endswith(('.ypk', '.zip', '.tar', '.tgz', '.tar.gz', '.7z', '.rar')):
            unpackage.start_unpackage(file_path, unpackage_folder_path)
            chk = True
            while chk:
                chk = False
                for root, dirs, fs in walk(unpackage_folder_path):
                    for f in fs:
                        if f.lower().endswith('.cdb'):
                            result.append(file_manager.copy_cdb(join(root, f), f))
                            remove(join(root, f))
                        elif f.lower().endswith(('.jpg', '.jpeg', 'png', 'bmp')):
                            result.append(file_manager.process_pic(join(root, f)))
                            remove(join(root, f))
                        elif f.lower().endswith(('.lua', '.txt', '.py', '.c', 'cs', 'js', 'css', 'html', 'ts', 'json')):
                            file_manager.copy_text(join(root, f))
                            remove(join(root, f))
                        elif f.lower().endswith(('.ypk', '.zip', '.tar', '.tgz', '.tar.gz', '.7z', '.rar')):
                            unpackage.start_unpackage(join(root, f), join(unpackage_folder_path))
                            remove(join(root, f))
                            chk = True
            remove(file_path)
            rmtree(unpackage_folder_path, ignore_errors = True)
        
    return jsonify(result), 200

@app.route('/api/get_cdb_menu', methods = ['POST'])
def get_cdb_menu():
    data = request.json
    cdb = data.get('cdb')
    cdb_list = sqlite_cdb.read_cdb(join(buffer, cdb), 'list')
    if len(cdb_list) == 0:
        return jsonify({'message': '无cdb'}), 200
    return jsonify(cdb_list), 200

@app.route('/api/download_cdb', methods = ['POST'])
def download_cdb():
    data = request.json
    cdb = data.get('cdb')
    file_manager.package_file(sqlite_cdb.read_cdb(join(buffer, cdb), 'list'), cdb)
    download = unpackage.start_package(cdb)
    with open(join(buffer, download), 'rb') as f:
        file_obj = BytesIO(f.read())
        response = Response(file_obj, mimetype = 'application/octet-stream')
        response.headers['Content-Disposition'] = f'attachment; filename = {download}'
        
        return response

@app.route('/api/add_cdb', methods = ['POST'])
def add_cdb():
    data = request.json
    cdb = data.get('cdb')
    return jsonify(sqlite_cdb.add_cdb(join(buffer, cdb))), 200

@app.route('/api/del_cdb', methods = ['POST'])
def del_cdb():
    data = request.json
    code = data.get('code')
    cdb = data.get('cdb')
    sqlite_cdb.delete_cdb(code, join(buffer, cdb))
    file_manager.remove_file(f'{code}.jpg')
    file_manager.remove_file(f'c{code}.lua')
    return jsonify(), 200

@app.route('/api/save_cdb', methods = ['POST'])
def save_cdb():
    data = request.json
    card_data = data.get('data')
    code = data.get('code')
    cdb = data.get('cdb')
    result = ''
    if code != card_data[0]:
        sqlite_cdb.delete_cdb(code, join(buffer, cdb))
        file_manager.rename_file(f'{code}.jpg', f'{card_data[0]}.jpg')
        file_manager.rename_file(f'c{code}.lua', f'c{card_data[0]}.lua')
        result += 'removed'
    sqlite_cdb.change_cdb(card_data, join(buffer, cdb))
    return jsonify(result), 200

@app.route('/api/read_card', methods = ['POST'])
def read_card():
    data = request.json
    _id = data.get('id')
    cdb = data.get('cdb')
    if not exists('./config/cardinfo_chinese.txt'):
        return jsonify({'error': '无法读取卡片信息'}), 400

    card_data = sqlite_cdb.read_cdb(join(buffer, cdb), 'data', _id)
    if len(card_data) == 0:
        return jsonify({'error': '卡片不存在'}), 400

    card_id = card_data[0]
    if exists(join(pics_folder_path, f'{card_id}.jpg')):
        card_data.append(f'./buffer/{pics_folder_path[pics_folder_path.rfind("\\") + 1 : ]}/{card_id}.jpg')
    else:
        card_data.append('')

    if exists(join(center_pics_folder_path, f'{card_id}.jpg')):
        card_data.append(f'./buffer/{center_pics_folder_path[center_pics_folder_path.rfind("\\") + 1 : ]}/{card_id}.jpg')
    else:
        card_data.append('')
    return jsonify(card_data), 200

if __name__ == '__main__':
    rmtree(buffer, ignore_errors = True)
    open_new('http://127.0.0.1:8000/')
    app.run(host='0.0.0.0', port = 8000)

