import os
import shutil
from typing import Tuple

import pandas as pd
from lxml import etree
from tqdm import tqdm


class DeepScoreXmlToCsvConverter(object):
    def convert_xml_annotations_to_csv(self, annotation_xml_string: str) -> Tuple[pd.DataFrame, int, int]:

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
            data.append((filename, top, left, bottom, right, class_name))

        converted_output = pd.DataFrame(data=data,
                                        columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])

        return converted_output, image_width, image_height

    def convert_relative_to_absolute_coordinates(self, annotations: pd.DataFrame, image_width: int,
                                                 image_height: int) -> pd.DataFrame:

        normalized_annotations = annotations.copy(True)  # type: pd.DataFrame
        normalized_annotations = normalized_annotations.apply(pd.to_numeric, errors='ignore')
        normalized_annotations['left'] *= image_width
        normalized_annotations['right'] *= image_width
        normalized_annotations['top'] *= image_height
        normalized_annotations['bottom'] *= image_height

        return normalized_annotations

    def convert_and_normalize_deep_scores_dataset(self, path_to_deep_scores: str, output_path: str) -> None:

        os.makedirs(os.path.join(output_path, "images"), exist_ok=True)

        source_image_directory = os.path.join(path_to_deep_scores, "images_png")
        source_annotation_directory = os.path.join(path_to_deep_scores, "xml_annotations")
        destination_image_directory = os.path.join(output_path, "images")
        destination_annotation_file = os.path.join(output_path, "deep_score_annotations.csv")

        for image_file_name in tqdm(os.listdir(source_image_directory), desc="Copying images"):
            source_path = os.path.join(source_image_directory, image_file_name)
            destination_path = os.path.join(destination_image_directory, image_file_name)
            shutil.copy(source_path, destination_path)

        all_annotations = None
        for annotation_file_name in tqdm(os.listdir(source_annotation_directory), desc="Converting annotations"):
            with open(os.path.join(source_annotation_directory, annotation_file_name), "r") as annotation_file:
                file_content = annotation_file.read()
                annotations, image_width, image_height = self.convert_xml_annotations_to_csv(file_content)
                absolute_annotations = self.convert_relative_to_absolute_coordinates(annotations, image_width,
                                                                                     image_height)
                absolute_annotations['path_to_image'] = absolute_annotations['path_to_image'].apply(
                    lambda x: "images/" + x)
                if all_annotations is None:
                    all_annotations = absolute_annotations
                else:
                    all_annotations = pd.concat([all_annotations, absolute_annotations])

        all_annotations.to_csv(destination_annotation_file, index=False, float_format="%.0f")
