from PIL import Image
from os.path import exists, join
from os import mkdir, remove, listdir, rename
from shutil import rmtree, copy
from ctypes import windll

def process_pic(pic_path, buffer = './dist/buffer', pics_folder = 'pics'):
    initialize_dir(f'{buffer}/{pics_folder}')
    try:
        pic_name = pic_path[pic_path.rfind('/') + 1 : pic_path.rfind('.')]
        img = Image.open(pic_path)
        img = img.convert('RGB')
        img = img.resize((400, 580), Image.Resampling.LANCZOS)
        img.save(f'{buffer}/{pics_folder}/{pic_name}.jpg')
        return f'{buffer}/{pics_folder}/{pic_name}.jpg'
    except:
        return None

def copy_text(text_path, buffer = './dist/buffer', script = 'script'):
    initialize_dir(f'{buffer}/{script}')
    try:
        if not text_path.endswith('.lua'):
            rename(text_path, f'{text_path[ : text_path.rfind('.')]}.lua')
        copy(f'{text_path[ : text_path.rfind('.')]}.lua', f'{buffer}/{script}')
        return f'{buffer}/{text_path[text_path.rfind('/') + 1 : text_path.rfind('.')]}.lua'
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

def initialize_dir_conceal(dir_path):
    if not exists(dir_path):
        mkdir(dir_path)
        windll.kernel32.SetFileAttributesW(dir_path, 2)

def initialize_dir(dir_path):
    if not exists(dir_path):
        mkdir(dir_path)

def get_only_one_file_path(buffer, file_name):
    file_path = f'{buffer}/{file_name}'
    i = 1
    while exists(file_path):
        file_path = f'{buffer}/{file_name[ : file_name.find(".")]}({i}){file_name[file_name.find(".") : ]}'
        i += 1
    return file_path

def remove_file(buffer, folder_path, file):
    if exists(f'{buffer}/{file}'):
        remove(f'{buffer}/{file}')
    for path in folder_path:
        print(f'{buffer}/{path}/{file}')
        if exists(f'{buffer}/{path}/{file}'):
            remove(f'{buffer}/{path}/{file}')

def package_file(lists, buffer = './dist/buffer', path = 'package', pics = 'pics', script = 'script', cdb = 'cards.cdb'):
    if exists(f'{buffer}/{path}'): rmtree(f'{buffer}/{path}')
    initialize_dir(f'{buffer}/{pics}')
    initialize_dir(f'{buffer}/{script}')
    initialize_dir(f'{buffer}/{path}')
    initialize_dir(f'{buffer}/{path}/{pics}')
    initialize_dir(f'{buffer}/{path}/{script}')
    copy(f'{buffer}/{cdb}', f'{buffer}/{path}/{cdb}')
    for files in lists:
        for file in files:
            f = file.split(' ')[0]
            if exists(f'{buffer}/{pics}/{f}.jpg'):
                copy(f'{buffer}/{pics}/{f}.jpg', f'{buffer}/{path}/{pics}/{f}.jpg')
            if exists(f'{buffer}/{script}/c{f}.lua'):
                copy(f'{buffer}/{script}/c{f}.lua', f'{buffer}/{path}/{script}/c{f}.lua')
