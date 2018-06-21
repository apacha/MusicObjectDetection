import argparse
import os

from omrdatasettools.downloaders.CvcMuscimaDatasetDownloader import CvcMuscimaDatasetDownloader, CvcMuscimaDataset
from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader

from datasets.MensuralDatasetDownloader import MensuralDatasetDownloader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default=".",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    muscima_pp_directory = os.path.join(flags.dataset_directory, "muscima_pp")
    downloader = MuscimaPlusPlusDatasetDownloader(muscima_pp_directory)
    downloader.download_and_extract_dataset()

    cvc_muscima_directory = os.path.join(flags.dataset_directory, "cvc_muscima")
    downloader = CvcMuscimaDatasetDownloader(cvc_muscima_directory, CvcMuscimaDataset.StaffRemoval)
    downloader.download_and_extract_dataset()

    mensural_directory = os.path.join(flags.dataset_directory, "mensural")
    downloader = MensuralDatasetDownloader(mensural_directory)
    downloader.download_and_extract_dataset()

