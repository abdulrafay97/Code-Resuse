import os
import json
import javalang
import subprocess
import shutil
import unicodedata
import logging

from concurrent.futures import ThreadPoolExecutor
from Java.packages import get_package_name
from Java.imports import get_imports
from Java._class import get_class
from Java.interface import get_interface
from Java.enum import get_enum

logging.basicConfig(level=logging.ERROR, filename='error_log.txt', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


def sanitize_path(path):
    return unicodedata.normalize('NFKD', path)


def create_json(path):
    repo_structure = {}

    for content in os.listdir(path):
        content_path = sanitize_path(os.path.join(path, content))

        if content == ".DS_Store":
            continue

        if os.path.isfile(content_path):
            repo_structure[content] = {}
            file_router(content_path, repo_structure[content])

        elif os.path.isdir(content_path):
            repo_structure[content] = create_json(content_path)

    return repo_structure


def file_router(path, repo_structure):
    try:
        if path.endswith('.png') or path.endswith('.jpg'):
            repo_structure['size'] = str(os.path.getsize(path)) + " bytes"

        elif path.endswith('.java'):
            java_code = read_java_file(path)
            if java_code is None:
                return
            tree = javalang.parse.parse(java_code)
            lines = java_code.splitlines()
            drive(tree, lines, repo_structure)

    except Exception as e:
        logging.error(f"Error processing {path}: {e}")


def read_java_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except IOError:
        logging.error(f"Could not read file: {file_path}")
        return None


def drive_the_body(tree, lines, repo_structure):
    for _, node in tree:
        if isinstance(node, javalang.tree.ClassDeclaration):
            get_class(node, tree, lines, repo_structure)

        elif isinstance(node, javalang.tree.InterfaceDeclaration):
            get_interface(node, tree, lines, repo_structure)

        elif isinstance(node, javalang.tree.EnumDeclaration):
            get_enum(node, tree, lines, repo_structure)


def drive(tree, lines, repo_structure):
    get_package_name(tree, repo_structure)
    get_imports(tree, repo_structure)
    drive_the_body(tree, lines, repo_structure)


def read_url(file_path):
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)

        git_path = data['url'] + ".git"
        return git_path
    except Exception as e:
        logging.error(f"Error reading JSON: {e}")


def clone_and_process_repo(repo_url, filename, temp_folder, save_json):
    repo_name = filename.replace('json', '')
    clone_dir = f'{temp_folder}/{repo_name}'

    try:
        subprocess.run(['git', 'clone', '--depth', '1', repo_url, clone_dir], check=True)
        print(f"Processing {repo_name}...")

        with open(f"{save_json}/{filename}", "w") as json_file:
            json.dump(create_json(clone_dir), json_file, indent=3, ensure_ascii=False)

        shutil.rmtree(clone_dir)
        print("==================================")
        
    except Exception as e:
        logging.error(f"Error cloning or processing {repo_url}: {e}")
