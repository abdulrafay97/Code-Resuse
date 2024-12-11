from utils import *
from tqdm import tqdm


path = '/Users/abdulrafay/Desktop/RP/Code_Extraction/data' 

save_json = '/Users/abdulrafay/Desktop/RP/Code_Extraction/Jsons' 

filename = 'jellyash.json'


with open(f"{save_json}/{filename}", "w", encoding="utf-8") as json_file:
    json.dump(create_json(path), json_file, indent=3, ensure_ascii=False)
