from PIL import Image
from os.path import exists, join
from os import mkdir, remove, listdir, rename
from shutil import rmtree, copy
from ctypes import windll

def process_pic(pic_path):
    from start_server import buffer, pics_folder_path
    initialize_dir(join(pics_folder_path))
    try:
        pic_name = pic_path[pic_path.rfind("\\") + 1 : pic_path.rfind(".")]
        img = Image.open(pic_path)
        img = img.convert('RGB')
        img = img.resize((400, 583), Image.Resampling.LANCZOS)
        img.save(join(pics_folder_path, f'{pic_name}.jpg'))
        return join('/buffer', pics_folder_path, f'{pic_name}.jpg')
    except:
        return None

def copy_text(text_path):
    from start_server import buffer, script_folder_path
    initialize_dir(join(script_folder_path))
    try:
        if not text_path.endswith('.lua'):
            rename(text_path, f'{text_path[ : text_path.rfind(".")]}.lua')
        copy(f'{text_path[ : text_path.rfind(".")]}.lua', join(script_folder_path))
        return f'{buffer}\\{text_path[text_path.rfind("\\") + 1 : text_path.rfind(".")]}.lua'
    except:
        return None
        
def copy_cdb(cdb_path, cdb_name):
    from start_server import buffer, cdb_backup_folder_path
    if not exists(join(cdb_backup_folder_path)):
        mkdir(join(cdb_backup_folder_path))
    try:
        copy(cdb_path, join(cdb_backup_folder_path))
        if not exists(join(buffer, cdb_name)):
            copy(join(cdb_path), join(buffer, cdb_name))
        return f'{cdb_path[cdb_path.rfind("\\") + 1 : ]}'
    except:
        return None

def initialize_dir_conceal(dir_path):
    if not exists(dir_path):
        mkdir(dir_path)
        windll.kernel32.SetFileAttributesW(dir_path, 2)

def initialize_dir(dir_path):
    if not exists(dir_path):
        mkdir(dir_path)

def get_only_one_file_path(file_name):
    from start_server import buffer
    file_path = join(buffer, file_name)
    i = 1
    while exists(file_path):
        file_path = join(buffer, f'{file_name[ : file_name.find(".")]}({i}){file_name[file_name.find(".") : ]}')
        i += 1
    return file_path

def remove_file(file):
    from start_server import buffer, cdb_backup_folder_path, pics_folder_path, script_folder_path, unpackage_folder_path
    if exists(join(buffer, file)):
        remove(join(buffer, file))
    for path in [pics_folder_path, script_folder_path, unpackage_folder_path, cdb_backup_folder_path]:
        if exists(join(path, file)):
            remove(join(path, file))

def package_file(lists, cdb = 'cards.cdb'):
    from start_server import buffer, pics_folder_path, script_folder_path, package_folder_path
    if exists(package_folder_path): rmtree(package_folder_path)
    initialize_dir(pics_folder_path)
    initialize_dir(script_folder_path)
    initialize_dir(package_folder_path)
    initialize_dir(join(package_folder_path, 'pics'))
    initialize_dir(join(package_folder_path,'script'))
    copy(join(buffer, cdb), join(package_folder_path, cdb))
    for files in lists:
        for file in files:
            f = file.split(' ')[0]
            if exists(join(pics_folder_path, f'{f}.jpg')):
                copy(join(pics_folder_path, f'{f}.jpg'), join(package_folder_path, 'pics', f'{f}.jpg'))
            if exists(join(script_folder_path, f'c{f}.lua')):
                copy(join(script_folder_path, f'c{f}.lua'), join(package_folder_path, 'script', f'c{f}.lua'))
