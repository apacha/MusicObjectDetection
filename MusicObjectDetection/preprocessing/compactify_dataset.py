import argparse
import os
from glob import glob

from PIL import Image
import pandas as pd
from tqdm import tqdm


def compactify_dataset(dataset_directory: str, scale_factor: float) -> None:
    normalized_deep_score_directory = os.path.join(dataset_directory, "normalized", "deepscores")
    image_directory = os.path.join(normalized_deep_score_directory, "images")
    for image_path in tqdm(glob(image_directory + "/*.png"), desc="Resizing images"):
        image = Image.open(image_path)
        width, height = image.size
        resized_width, resized_height = int(width * scale_factor), int(height * scale_factor)
        resized_image = image.resize((resized_width, resized_height), Image.LANCZOS)
        resized_image.save(image_path)

    annotations_path = os.path.join(normalized_deep_score_directory, "annotations.csv")
    annotations = pd.read_csv(annotations_path)
    annotations['left'] *= scale_factor
    annotations['top'] *= scale_factor
    annotations['bottom'] *= scale_factor
    annotations['right'] *= scale_factor
    annotations.to_csv(annotations_path, float_format="%.2f", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_directory", type=str, default="../data",
                        help="The directory, where the datasets can be found")
    parser.add_argument("--scale_factor", type=float, default=0.5,
                        help="The directory, where the datasets can be found")

    flags, unparsed = parser.parse_known_args()

    compactify_dataset(flags.dataset_directory, flags.scale_factor)
