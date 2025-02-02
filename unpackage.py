from zipfile import ZipFile as ZipOpen
from zipfile import ZIP_DEFLATED
from rarfile import RarFile as RarOpen
from tarfile import open as TarOpen
from py7zr import SevenZipFile as SevenZipOpen
from os import walk
from os.path import join, isfile, isdir, dirname, basename, dirname, relpath

def unzip_file(zip_path, extract_to):
    with ZipOpen(zip_path, 'r') as zip_ref:
        zip_ref.extractall(path = extract_to)

def untar_file(tar_path, extract_to):
    with TarOpen(tar_path, 'r') as tar_ref:
        tar_ref.extractall(path = extract_to)

def unrar_file(rar_path, extract_to):
    with RarOpen(rar_path, 'r') as rar_ref:
        rar_ref.extractall(path = extract_to)

def un7z_file(sevenz_path, extract_to):
    with SevenZipOpen(sevenz_path, mode='r') as sevenz_ref:
        sevenz_ref.extractall(path = extract_to)

def start_unpackage(file_path, extract_to):
    if file_path.endswith(('.zip', 'ypk')):
        unzip_file(file_path, extract_to)
    elif file_path.endswith(('.tar.gz', '.tgz', '.tar')):
        untar_file(file_path, extract_to)
    elif file_path.endswith('.rar'):
        unrar_file(file_path, extract_to)
    elif file_path.endswith('.7z'):
        un7z_file(file_path, extract_to)

def zip_files(zip_path, files_to_zip):
    with ZipOpen(zip_path, 'w', ZIP_DEFLATED) as zip_ref:
        for file in files_to_zip:
            if isfile(file):
                zip_ref.write(file, basename(file))
            elif isdir(file):
                for root, dirs, files in walk(file):
                    for f in files:
                        file_path = join(root, f)
                        arcname = relpath(file_path, start = dirname(file))
                        zip_ref.write(file_path, arcname)

def start_package(buffer, cdb = 'cards.cdb'):
    from start_server import buffer, package_folder_path
    zip_files(join(buffer, f'{cdb.split(".")[0]}.ypk'), [join(package_folder_path, cdb), join(package_folder_path, 'script'), join(package_folder_path, 'pics')])
    return f'{cdb.split(".")[0]}.ypk'