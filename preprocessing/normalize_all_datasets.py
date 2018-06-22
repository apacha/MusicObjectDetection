import argparse
import os

from omrdatasettools.downloaders.CvcMuscimaDatasetDownloader import CvcMuscimaDatasetDownloader, CvcMuscimaDataset
from omrdatasettools.downloaders.MuscimaPlusPlusDatasetDownloader import MuscimaPlusPlusDatasetDownloader

from datasets.DeepScoresDatasetDownloader import DeepScoresDatasetDownloader
from datasets.MensuralDatasetDownloader import MensuralDatasetDownloader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data",
        help="The directory, where the datasets can be found")

    flags, unparsed = parser.parse_known_args()

