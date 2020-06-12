import argparse
import os

from MusicObjectDetection.preprocessing.DeepScoreXmlToCsvConverter import DeepScoreXmlToCsvConverter
from MusicObjectDetection.preprocessing.MensuralConverter import MensuralConverter
from MusicObjectDetection.preprocessing.MuscimaPpXmlToCsvConverter import MuscimaPpXmlToCsvConverter
from MusicObjectDetection.preprocessing.dataset_splitter import DatasetSplitter


def normalize_all_datasets(dataset_directory: str) -> None:
    deep_score_converter = DeepScoreXmlToCsvConverter()
    muscima_pp_converter = MuscimaPpXmlToCsvConverter()
    mensural_converter = MensuralConverter()
    dataset_splitter = DatasetSplitter()

    deep_score_directory = os.path.join(dataset_directory, "deepscores", "deep-scores-v1-extended-100pages")
    normalized_deep_score_directory = os.path.join(dataset_directory, "normalized", "deepscores")
    if os.path.exists(deep_score_directory):
        deep_score_converter.copy_and_normalize_images(deep_score_directory, normalized_deep_score_directory)
        deep_score_converter.normalize_annotations(deep_score_directory, normalized_deep_score_directory)
        dataset_splitter.split_annotations_into_training_validation_and_test_set(normalized_deep_score_directory)

    normalized_muscima_pp_directory = os.path.join(dataset_directory, "normalized", "muscima")
    muscima_directory = os.path.join(dataset_directory, "muscima_pp")
    muscima_pp_converter.copy_and_normalize_images(muscima_directory, normalized_muscima_pp_directory)
    if os.path.exists(muscima_directory):
        muscima_pp_converter.normalize_annotations(muscima_directory,
                                                   normalized_muscima_pp_directory)
        muscima_pp_converter.remove_unused_images(normalized_muscima_pp_directory)
        dataset_splitter.split_annotations_into_training_validation_and_test_set(normalized_muscima_pp_directory)

    normalized_mensural_directory = os.path.join(dataset_directory, "normalized", "mensural")
    mensural_directory = os.path.join(dataset_directory, "mensural")
    if os.path.exists(mensural_directory):
        mensural_converter.copy_and_normalize_images(mensural_directory, normalized_mensural_directory)
        mensural_converter.normalize_annotations(mensural_directory, normalized_mensural_directory)
        dataset_splitter.split_annotations_into_training_validation_and_test_set(normalized_mensural_directory)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data",
        help="The directory, where the datasets can be found")

    flags, unparsed = parser.parse_known_args()

    normalize_all_datasets(flags.dataset_directory)
