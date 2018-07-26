import argparse
import os

from omrdatasettools.downloaders.CvcMuscimaDatasetDownloader import CvcMuscimaDatasetDownloader, CvcMuscimaDataset
from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader

from MusicObjectDetection.datasets.DeepScoresDatasetDownloader import DeepScoresDatasetDownloader
from MusicObjectDetection.datasets.MensuralDatasetDownloader import MensuralDatasetDownloader


def download_all_datasets(dataset_directory):
    muscima_pp_directory = os.path.join(dataset_directory, "muscima_pp")
    downloader = MuscimaPlusPlusDatasetDownloader()
    downloader.download_and_extract_dataset(muscima_pp_directory)

    cvc_muscima_directory = os.path.join(dataset_directory, "cvc_muscima")
    downloader = CvcMuscimaDatasetDownloader(CvcMuscimaDataset.StaffRemoval)
    downloader.download_and_extract_dataset(cvc_muscima_directory)

    mensural_directory = os.path.join(dataset_directory, "mensural")
    downloader = MensuralDatasetDownloader()
    downloader.download_and_extract_dataset(mensural_directory)

    deepscores_directory = os.path.join(dataset_directory, "deepscores")
    downloader = DeepScoresDatasetDownloader()
    downloader.download_and_extract_dataset(deepscores_directory)


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
