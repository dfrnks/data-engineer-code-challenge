import zipfile
import glob
import shutil

from pathlib import Path

import pandas as pd


def unzip_zip_files(path: str, files: list) -> list:
    """
    Unzip a zip files and put into a dir
    :param path: Path of a directory than will contain the unzip files
    :param files: The list of files to unzip
    :return:
    """

    unzip_path = Path(path) / '.temp'
    unzip_path.mkdir(parents=True, exist_ok=True)

    raw_path = Path(path) / 'raw'
    raw_path.mkdir(parents=True, exist_ok=True)

    trusted_path = Path(path) / 'trusted'
    trusted_path.mkdir(parents=True, exist_ok=True)

    return_files = []

    for f in files:
        with zipfile.ZipFile(f) as file:

            file.extractall(path=unzip_path)

            return_files.append(f.replace('.zip', ''))

    return return_files


def concat_json_files(parent_path, path):
    files = glob.glob(f"{parent_path}/.temp/{path}/*.json")

    dfs = []  # an empty list to store the data frames
    for file in files:
        data = pd.read_json(file, lines=True)  # read data frame from json file
        dfs.append(data)  # append the data frame to the list

    temp = pd.concat(dfs, ignore_index=True)  # concatenate all the data frames in the list

    temp.to_json(f"{parent_path}/raw/{path}.json", orient="records", lines=True)

    shutil.rmtree(f"{parent_path}/.temp/{path}")



