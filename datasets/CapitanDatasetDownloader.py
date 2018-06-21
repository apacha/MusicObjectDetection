import argparse
import os

from omrdatasettools.downloaders.DatasetDownloader import DatasetDownloader


class MensuralDatasetDownloader(DatasetDownloader):
    """ Downloads the Mensural Dataset (Capitan collection)
        https://bitbucket.org/apacha/mensural-detector-database/
    """

    def __init__(self, destination_directory: str):
        """
        Create and initializes a new dataset.
        :param destination_directory: The root directory, into which the data will be copied.
        """
        super().__init__(destination_directory)

    def get_dataset_download_url(self) -> str:
        return "https://owncloud.tuwien.ac.at/index.php/s/hMc6WY64rYO9jcX/download"

    def get_dataset_filename(self) -> str:
        return "mensural-detector-database.zip"

    def download_and_extract_dataset(self):
        if not os.path.exists(self.get_dataset_filename()):
            print("Downloading Mensural Dataset...")
            self.download_file(self.get_dataset_download_url(), self.get_dataset_filename())

        print("Extracting Mensural Dataset...")
        self.extract_dataset(self.destination_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data/mensural",
        help="The directory, where the extracted dataset will be copied to")

    flags, unparsed = parser.parse_known_args()

    dataset = MensuralDatasetDownloader(flags.dataset_directory)
    dataset.download_and_extract_dataset()
