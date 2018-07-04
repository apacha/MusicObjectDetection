import os
from glob import glob

from PIL import Image
from tqdm import tqdm
import pandas as pd


class MensuralConverter(object):

    def copy_and_normalize_images(self, mensural_directory: str, output_directory: str) -> None:
        os.makedirs(os.path.join(output_directory, "images"), exist_ok=True)

        all_images = glob(mensural_directory + "/*.JPG")

        for image_path in tqdm(all_images, desc="Copying and converting images"):
            image = Image.open(image_path)
            filename = os.path.splitext(os.path.basename(image_path))[0] + ".png"
            output_path = os.path.join(output_directory, "images", filename)
            image.save(output_path)

    def normalize_annotations(self, mensural_directory: str, output_directory: str) -> None:
        destination_annotation_file = os.path.join(output_directory, "annotations.csv")
        all_annotations = glob(mensural_directory + "/*.txt")

        data = []
        for annotation_path in tqdm(all_annotations, desc="Normalizing annotations"):
            with open(annotation_path, 'r') as gt_file:
                lines = gt_file.read().splitlines()

            filename = "images/{0}.png".format(os.path.basename(annotation_path[-8]))
            for line in lines:
                upper_left, lower_right, ground_truth = line.split(';')
                class_name, staff_line_position = ground_truth.split(':')
                xmin, ymin = upper_left.split(',')
                xmax, ymax = lower_right.split(',')

                top = float(ymin)
                left = float(xmin)
                bottom = float(ymax)
                right = float(xmax)
                data.append((filename, top, left, bottom, right, class_name))

        all_annotations = pd.DataFrame(data=data,
                                       columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])
        all_annotations.to_csv(destination_annotation_file, index=False, float_format="%.0f")
