import argparse
import os

from preprocessing.DeepScoreXmlToCsvConverter import DeepScoreXmlToCsvConverter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_directory",
        type=str,
        default="../data",
        help="The directory, where the datasets can be found")

    flags, unparsed = parser.parse_known_args()

    deep_score_converter = DeepScoreXmlToCsvConverter()
    deep_score_directory = os.path.join(flags.dataset_directory, "deepscores", "deep-scores-200")
    normalized_deep_score_directory = os.path.join(flags.dataset_directory, "normalized", "deepscores")
    deep_score_converter.convert_and_normalize_deep_scores_dataset(deep_score_directory,
                                                                   normalized_deep_score_directory)
