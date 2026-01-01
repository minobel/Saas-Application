import requests
from pathlib import Path

def download_to_local(url:str, dest_out_path:Path,parent_mkdir:bool=True):
    if not isinstance(dest_out_path, Path):
        raise ValueError(f"{dest_out_path} must be a pathlib.Path object")
    if parent_mkdir:
        dest_out_path.parent.mkdir(parents=True, exist_ok=True) 
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        #Write the file out in binary mode to prevent any  newline conversion issues
        dest_out_path.write_bytes(response.content)
        return True
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False