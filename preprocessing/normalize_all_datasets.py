import argparse
import os

from preprocessing.DeepScoreXmlToCsvConverter import DeepScoreXmlToCsvConverter
from preprocessing.MuscimaPpXmlToCsvConverter import MuscimaPpXmlToCsvConverter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data",
        help="The directory, where the datasets can be found")

    flags, unparsed = parser.parse_known_args()

    deep_score_converter = DeepScoreXmlToCsvConverter()
    deep_score_directory = os.path.join(flags.dataset_directory, "deepscores", "deep_scores_dense")
    normalized_deep_score_directory = os.path.join(flags.dataset_directory, "normalized", "deepscores")
    deep_score_converter.convert_and_normalize_deep_scores_dataset(deep_score_directory,
                                                                   normalized_deep_score_directory)

    muscima_pp_converter = MuscimaPpXmlToCsvConverter()
    muscima_pp_converter.copy_and_normalize_images(os.path.join(flags.dataset_directory, "cvc_muscima"),
                                                   os.path.join(flags.dataset_directory, "normalized", "muscima"))
    muscima_pp_converter.normalize_annotations(os.path.join(flags.dataset_directory, "muscima_pp"),
                                               os.path.join(flags.dataset_directory, "normalized", "muscima"))