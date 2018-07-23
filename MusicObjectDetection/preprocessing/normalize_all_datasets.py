import argparse
import os

from MusicObjectDetection.preprocessing.DeepScoreXmlToCsvConverter import DeepScoreXmlToCsvConverter
from MusicObjectDetection.preprocessing.MensuralConverter import MensuralConverter
from MusicObjectDetection.preprocessing.MuscimaPpXmlToCsvConverter import MuscimaPpXmlToCsvConverter
from MusicObjectDetection.preprocessing.dataset_splitter import DatasetSplitter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data",
        help="The directory, where the datasets can be found")

    flags, unparsed = parser.parse_known_args()

    deep_score_converter = DeepScoreXmlToCsvConverter()
    deep_score_directory = os.path.join(flags.dataset_directory, "deepscores", "deep_scores_v2_100p")
    normalized_deep_score_directory = os.path.join(flags.dataset_directory, "normalized", "deepscores")
    deep_score_converter.copy_and_normalize_images(deep_score_directory, normalized_deep_score_directory)
    deep_score_converter.normalize_annotations(deep_score_directory, normalized_deep_score_directory)

    muscima_pp_converter = MuscimaPpXmlToCsvConverter()
    normalized_muscima_pp_directory = os.path.join(flags.dataset_directory, "normalized", "muscima")
    muscima_pp_converter.copy_and_normalize_images(os.path.join(flags.dataset_directory, "cvc_muscima"),
                                                   normalized_muscima_pp_directory)
    muscima_pp_converter.normalize_annotations(os.path.join(flags.dataset_directory, "muscima_pp"),
                                               normalized_muscima_pp_directory)
    muscima_pp_converter.remove_unused_images(normalized_muscima_pp_directory)

    mensural_converter = MensuralConverter()
    normalized_mensural_directory = os.path.join(flags.dataset_directory, "normalized", "mensural")
    mensural_directory = os.path.join(flags.dataset_directory, "mensural")
    mensural_converter.copy_and_normalize_images(mensural_directory, normalized_mensural_directory)
    mensural_converter.normalize_annotations(mensural_directory, normalized_mensural_directory)

    dataset_splitter = DatasetSplitter()
    dataset_splitter.split_annotations_into_training_validation_and_test_set(normalized_deep_score_directory)
    dataset_splitter.split_annotations_into_training_validation_and_test_set(normalized_muscima_pp_directory)
    dataset_splitter.split_annotations_into_training_validation_and_test_set(normalized_mensural_directory)
