import os
import shutil
from typing import Tuple

import pandas as pd
from lxml import etree
from tqdm import tqdm


class DeepScoreXmlToCsvConverter(object):
    def _convert_xml_annotations_to_csv(self, annotation_xml_string: str) -> Tuple[pd.DataFrame, int, int]:

        root = etree.fromstring(annotation_xml_string)
        filename = root.findtext("filename")
        image_width = int(root.findtext("size/width"))
        image_height = int(root.findtext("size/height"))
        data = []

        for annotation_object in root.findall("object"):
            class_name = annotation_object.findtext("name")
            top = annotation_object.findtext("bndbox/ymin")
            left = annotation_object.findtext("bndbox/xmin")
            bottom = annotation_object.findtext("bndbox/ymax")
            right = annotation_object.findtext("bndbox/xmax")

            if class_name == "staffLine" or class_name == "combStaff":
                continue  # Skip staffLines or staves ('comb(ined)Staff') from the deep scores dataset

            data.append((filename, top, left, bottom, right, class_name))

        converted_output = pd.DataFrame(data=data,
                                        columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])

        return converted_output, image_width, image_height

    def _convert_relative_to_absolute_coordinates(self, annotations: pd.DataFrame, image_width: int,
                                                  image_height: int) -> pd.DataFrame:

        normalized_annotations = annotations.copy(True)  # type: pd.DataFrame
        normalized_annotations = normalized_annotations.apply(pd.to_numeric, errors='ignore')
        normalized_annotations['left'] *= image_width
        normalized_annotations['right'] *= image_width
        normalized_annotations['top'] *= image_height
        normalized_annotations['bottom'] *= image_height

        # Correct for 0-pixel width / height annotations (caused by rounding issues) by making extending the box by two pixels
        zero_width_rows = normalized_annotations['right'].astype(int) - normalized_annotations['left'].astype(int) < 1
        zero_height_rows = normalized_annotations['bottom'].astype(int) - normalized_annotations['top'].astype(int) < 1
        normalized_annotations['left'] = normalized_annotations['left'] - zero_width_rows.astype(int)
        normalized_annotations['right'] = normalized_annotations['right'] + zero_width_rows.astype(int)
        normalized_annotations['top'] = normalized_annotations['top'] - zero_height_rows.astype(int)
        normalized_annotations['bottom'] = normalized_annotations['bottom'] + zero_height_rows.astype(int)

        return normalized_annotations

    def copy_and_normalize_images(self, deep_scores_directory: str, output_directory: str) -> None:

        os.makedirs(os.path.join(output_directory, "images"), exist_ok=True)

        source_image_directory = os.path.join(deep_scores_directory, "images_png")
        destination_image_directory = os.path.join(output_directory, "images")

        for image_file_name in tqdm(os.listdir(source_image_directory), desc="Copying images"):
            source_path = os.path.join(source_image_directory, image_file_name)
            destination_path = os.path.join(destination_image_directory, image_file_name)
            shutil.copy(source_path, destination_path)

    def normalize_annotations(self, deep_scores_directory: str, output_directory: str) -> None:
        source_annotation_directory = os.path.join(deep_scores_directory, "xml_annotations")
        destination_annotation_file = os.path.join(output_directory, "annotations.csv")

        all_annotations = None
        for annotation_file_name in tqdm(os.listdir(source_annotation_directory), desc="Converting annotations"):
            with open(os.path.join(source_annotation_directory, annotation_file_name), "r") as annotation_file:
                file_content = annotation_file.read()
                annotations, image_width, image_height = self._convert_xml_annotations_to_csv(file_content)
                absolute_annotations = self._convert_relative_to_absolute_coordinates(annotations, image_width,
                                                                                      image_height)
                absolute_annotations['path_to_image'] = absolute_annotations['path_to_image'].apply(
                    lambda x: "images/" + x[:-3] + "png")
                if all_annotations is None:
                    all_annotations = absolute_annotations
                else:
                    all_annotations = pd.concat([all_annotations, absolute_annotations])

        all_annotations.to_csv(destination_annotation_file, index=False, float_format="%.0f")
