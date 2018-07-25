import argparse
import os
import random
import pandas as pd


class DatasetSplitter:
    """ Class that can be used to create a reproducible random-split of a dataset into train/validation/test sets """

    def split_annotations_into_training_validation_and_test_set(self, dataset_directory: str,
                                                                train_fraction: float = 0.6,
                                                                validation_fraction: float = 0.2,
                                                                test_fraction: float = 0.2,
                                                                seed: int = 0) -> None:
        if (train_fraction + validation_fraction + test_fraction) != 1.0:
            print("Invalid split requested. Should sum up to 1.0")
            return

        annotations = pd.read_csv(os.path.join(dataset_directory, "annotations.csv"))
        all_file_paths = annotations['path_to_image'].unique()
        all_file_paths.sort()
        dataset_size = all_file_paths.shape[0]

        random.seed(seed)
        all_indices = list(range(0, dataset_size))
        validation_sample_size = int(dataset_size * validation_fraction)
        test_sample_size = int(dataset_size * test_fraction)
        validation_sample_indices = random.sample(all_indices, validation_sample_size)
        test_sample_indices = random.sample((set(all_indices) - set(validation_sample_indices)), test_sample_size)
        training_sample_indices = list(set(all_indices) - set(validation_sample_indices) - set(test_sample_indices))

        print("Splitting annotations for {0} training, {1} validation and {2} test images..."
              .format(len(training_sample_indices), len(validation_sample_indices), len(test_sample_indices)))

        training_file_paths = all_file_paths[training_sample_indices]
        validation_file_paths = all_file_paths[validation_sample_indices]
        test_file_paths = all_file_paths[test_sample_indices]

        training_annotations = annotations.loc[annotations['path_to_image'].isin(training_file_paths)]
        validation_annotations = annotations.loc[annotations['path_to_image'].isin(validation_file_paths)]
        test_annotations = annotations.loc[annotations['path_to_image'].isin(test_file_paths)]

        training_annotations.to_csv(os.path.join(dataset_directory, "training.csv"), index=False, float_format="%.0f")
        validation_annotations.to_csv(os.path.join(dataset_directory, "validation.csv"), index=False,
                                      float_format="%.0f")
        test_annotations.to_csv(os.path.join(dataset_directory, "test.csv"), index=False, float_format="%.0f")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_directory", type=str, default="../data/normalized/deepscores",
                        help="The base directory for the normalized dataset")

    flags, unparsed = parser.parse_known_args()

    datasest = DatasetSplitter()
    datasest.split_annotations_into_training_validation_and_test_set(flags.dataset_directory)
