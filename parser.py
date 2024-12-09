from utils import *
from tqdm import tqdm


path = '/home/abra165f/ws_code_reuse/github_crawl/CodeSearchNet/metadata' 
temp_folder = '/home/abra165f/ws_code_reuse/parser/temp' 
save_json = '/home/abra165f/ws_code_reuse/github_crawl/CodeSearchNet/code_with_body' 

files = os.listdir(path)

already_done = os.listdir(save_json)

repo_urls = []

for file in tqdm(files, desc='Processing Repos'):

    if file in already_done:
        print("Already Done. SKIP")
        print("==================================")
    
    else:
        if file.endswith(".json"):
            full_path = os.path.join(path, file)

            clone_and_process_repo(read_url(full_path), file, temp_folder, save_json)
