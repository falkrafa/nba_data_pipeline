import os
import zipfile
import subprocess

current_dir = os.path.dirname(os.path.realpath(__file__))

pipeline_dir = os.path.join(current_dir, "..")

try:
    os.mkdir(pipeline_dir[:-7] + "data")
except:
    pass

data_dir = os.path.join(pipeline_dir, "data")

NBA_DATASET_URL = "szymonjwiak/nba-traditional"

download_dataset = f"kaggle datasets download -d {NBA_DATASET_URL}"

subprocess.run(download_dataset, shell=True, cwd=data_dir)

zip_file_name = f"{NBA_DATASET_URL.split('/')[1]}.zip"

zip_file_path = os.path.join(data_dir, zip_file_name)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(data_dir)

os.remove(zip_file_path)
