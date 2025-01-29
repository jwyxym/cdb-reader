from zipfile import ZipFile as ZipOpen
from zipfile import ZIP_DEFLATED
from rarfile import RarFile as RarOpen
from tarfile import open as TarOpen
from py7zr import SevenZipFile as SevenZipOpen
import os

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
    if file_path.endswith('.zip'):
        unzip_file(file_path, extract_to)
    elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz') or file_path.endswith('.tar'):
        untar_file(file_path, extract_to)
    elif file_path.endswith('.rar'):
        unrar_file(file_path, extract_to)
    elif file_path.endswith('.7z'):
        un7z_file(file_path, extract_to)

def zip_files(zip_path, files_to_zip):
    with ZipOpen(zip_path, 'w', ZIP_DEFLATED) as zip_ref:
        for file in files_to_zip:
            if os.path.isfile(file):
                zip_ref.write(file, os.path.basename(file))
            elif os.path.isdir(file):
                for root, dirs, files in os.walk(file):
                    for f in files:
                        file_path = os.path.join(root, f)
                        arcname = os.path.relpath(file_path, start=os.path.dirname(file))
                        zip_ref.write(file_path, arcname)
            else:
                print(f"文件或目录 {file} 不存在")

def start_package(file_path, package_to):
    zip_files(package_to, file_path)
