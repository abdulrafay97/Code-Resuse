import os
import json
import javalang
import subprocess
import shutil
import unicodedata
import logging
import ast

from concurrent.futures import ThreadPoolExecutor
from Java.packages import get_package_name
from Java.imports import get_imports
from Java._class import get_class
from Java.interface import get_interface
from Java.enum import get_enum


from Python.imports import get_python_imports
from Python._class import get_python_classs
from Python.independent_method import get_independent_methods

logging.basicConfig(level=logging.ERROR, filename='/Users/abdulrafay/Desktop/RP/Code_Extraction/Logs/error_log.txt', filemode='a',
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
            java_code = read_code_file(path)
            if java_code is None:
                return
            tree = javalang.parse.parse(java_code)
            lines = java_code.splitlines()
            drive_java(tree, lines, repo_structure)

        elif path.endswith('.py'):
            python_code = read_code_file(path)
            if python_code is None:
                return
            
            parsed_ast = ast.parse(python_code)
            drive_python(parsed_ast, repo_structure)


    except Exception as e:
        logging.error(f"Error processing {path}: {e}")



def read_code_file(file_path):
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



def drive_java(tree, lines, repo_structure):
    get_package_name(tree, repo_structure)
    get_imports(tree, repo_structure)
    drive_the_body(tree, lines, repo_structure)



def drive_python(parsed_ast, repo_structure):
    imports = get_python_imports(parsed_ast)

    repo_structure["imports"] = imports
    repo_structure["independent_methodds"] = get_independent_methods(parsed_ast, imports)
    repo_structure["classes"] = get_python_classs(parsed_ast, imports)



def read_url(file_path):
    try: 
        with open(file_path, 'r') as file:
            data = json.load(file)

        git_path = data['url'] + ".git"
        return git_path
    except Exception as e:
        logging.error(f"Error reading JSON: {e}")