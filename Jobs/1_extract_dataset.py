import os
import zipfile
import subprocess

current_dir = os.path.dirname(os.path.realpath(__file__))

pipeline_dir = os.path.join(current_dir, "..")


data_dir = os.path.join(pipeline_dir, "Data")

nba_dataset_url = "vszymonjwiak/nba-traditional"

download_command = f"kaggle datasets download -d {nba_dataset_url}"

subprocess.run(download_command, shell=True, cwd=data_dir)

zip_file_name = f"{nba_dataset_url.split('/')[1]}.zip"

zip_file_path = os.path.join(data_dir, zip_file_name)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(data_dir)

os.remove(zip_file_path)

print("Conjunto de dados do nba baixado e extraído com sucesso!")
