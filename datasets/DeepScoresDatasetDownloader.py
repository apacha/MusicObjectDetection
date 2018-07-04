import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class DeepScoresDatasetDownloader(DatasetDownloader):
    """ Downloads the condensed deep scores dataset
        https://tuggeluk.github.io/deepscores/
    """

    def get_dataset_download_url(self) -> str:
        # Is neither the full deep scores, nor the condensed version, but simply a partial dataset
        return "https://owncloud.tuwien.ac.at/index.php/s/OfYFuXlQ5CH0zf6/download"

    def get_dataset_filename(self) -> str:
        return "deep-scores-v2_100p.zip"

    def download_and_extract_dataset(self, destination_directory: str):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading DeepScores Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting DeepScores Dataset...")
        self.extract_dataset(os.path.abspath(destination_directory))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/deepscores",
        help="The directory, where the extracted dataset will be copied to")

    flags, _ = parser.parse_known_args()

    dataset = DeepScoresDatasetDownloader()
    dataset.download_and_extract_dataset(flags.dataset_directory)
