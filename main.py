import easyocr
import glob
from pathlib import Path

folder_path = r"./Screenshots/"
file_pattern = r"\*png"
files = glob.glob(folder_path + file_pattern)
print(files)
recent_file = max(files, key=os.path.getctime)

