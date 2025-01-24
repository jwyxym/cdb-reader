from PIL import Image
from os.path import exists, join
from os import mkdir, remove, listdir
from shutil import rmtree, copy
from ctypes import windll

def process_pic(pic_path, buffer = './dist/buffer', pics_folder = 'pics'):
    if not exists(f'{buffer}/{pics_folder_path}'):
        mkdir(f'{buffer}/{pics_folder_path}')
    try:
        pic_name = pic_path[pic_path.rfind('/') + 1 : pic_path.rfind('.')]
        img = Image.open(pic_path)
        img = img.convert('RGB')
        img = img.resize((400, 580), Image.Resampling.LANCZOS)
        img.save(f'{buffer}/{pics_folder}/{pic_name}.jpg')
        return f'{buffer}/{pics_folder}/{pic_name}.jpg'
    except:
        return None

def copy_cdb(cdb_path, buffer = './dist/buffer', cdb_folder = 'cdb_backup'):
    if not exists(f'{buffer}/{cdb_folder}'):
        mkdir(f'{buffer}/{cdb_folder}')
    try:
        copy(cdb_path, f'{buffer}/{cdb_folder}')
        return f'{buffer}/{cdb_folder}/{cdb_path[cdb_path.rfind('/') + 1 : ]}'
    except:
        return None

def initialize_dir(dir_path):
    if not exists(dir_path):
        mkdir(dir_path)
        windll.kernel32.SetFileAttributesW(dir_path, 2)

def get_only_one_file_path(buffer, file_name):
    file_path = f'{buffer}/{file_name}'
    i = 1
    while exists(file_path):
        file_path = f'{buffer}/{file_name[ : file_name.find(".")]}({i}){file_name[file_name.find(".") : ]}'
        i += 1
    return file_path

if __name__ == '__main__':
    name = '2511'
    process_pic(f'./dist/buffer/{name}.jpg')