import argparse
import os

from omrdatasettools import *


def download_all_datasets(dataset_directory):
    muscima_pp_directory = os.path.join(dataset_directory, "muscima_pp")
    downloader = Downloader()
    downloader.download_and_extract_dataset(OmrDataset.MuscimaPlusPlus_V1, muscima_pp_directory)

    mensural_directory = os.path.join(dataset_directory, "mensural")
    mensural_name = "mensural"
    mensural_url = ""
    mensural_filename = "mensural-detector-database.zip"

    if mensural_url is "":
        print("Can't download the Capitan dataset, because no download URL has been specified. Please contact "
              "the authors, if you want to have access to the dataset, before it is publicly released. "
              "Developer Info: https://bitbucket.org/apacha/mensural-detector-database/")
    else:
        downloader.download_and_extract_custom_dataset(mensural_name, mensural_url, mensural_filename,
                                                       mensural_directory)

    deepscores_directory = os.path.join(dataset_directory, "deepscores")
    downloader.download_and_extract_custom_dataset("deep-scores",
                                                   "https://github.com/apacha/OMR-Datasets/releases/download/datasets/deep-scores-v1-extended-100pages.zip",
                                                   "deep-scores-v1-extended-100pages.zip", deepscores_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset_directory = flags.dataset_directory
    download_all_datasets(dataset_directory)
