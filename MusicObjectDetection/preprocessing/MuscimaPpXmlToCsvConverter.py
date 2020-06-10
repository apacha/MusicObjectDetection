import os
import re
import shutil
from glob import glob
from typing import List

import pandas as pd
from muscima.cropobject import CropObject
from muscima.io import parse_cropobject_list
from tqdm import tqdm

from MusicObjectDetection.preprocessing.image_color_inverter import ImageColorInverter


class MuscimaPpXmlToCsvConverter(object):

    def copy_and_normalize_images(self, cvc_muscima_directory: str, output_directory: str) -> None:
        os.makedirs(os.path.join(output_directory, "images"), exist_ok=True)

        all_images = glob(cvc_muscima_directory + "/**/*.png", recursive=True)

        for image_path in tqdm(all_images, desc="Copying images"):
            output_path = os.path.join(output_directory, "images", os.path.basename(image_path))
            shutil.copy(image_path, output_path)

        image_inverter = ImageColorInverter()
        image_inverter.invert_images(output_directory, "*.png")

    def normalize_annotations(self, muscima_pp_directory: str, output_directory: str) -> None:

        destination_annotation_file = os.path.join(output_directory, "annotations.csv")

        raw_data_directory = os.path.join(muscima_pp_directory, "v1.0", "data", "cropobjects_withstaff")
        xml_file_paths = [y for x in os.walk(raw_data_directory) for y in glob(os.path.join(x[0], '*.xml'))]
        all_crop_objects = []  # type: List[CropObject]
        for xml_file_path in tqdm(xml_file_paths, desc="Loading annotations from MUSCIMA++ dataset"):
            all_crop_objects.extend(parse_cropobject_list(xml_file_path))
            break

        data = []
        for crop_object in tqdm(all_crop_objects, "Converting annotations"):
            writer = re.search("W-..", crop_object.doc).group()
            page = int(re.search("N-..", crop_object.doc).group()[2:])
            filename = "images/CVC-MUSCIMA_{0}_{1}_D-ideal.png".format(writer, page)
            class_name = crop_object.clsname
            top = crop_object.top
            left = crop_object.left
            bottom = crop_object.bottom
            right = crop_object.right
            data.append((filename, top, left, bottom, right, class_name))

        all_annotations = pd.DataFrame(data=data,
                                       columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])
        all_annotations.to_csv(destination_annotation_file, index=False, float_format="%.0f")

    def remove_unused_images(self, output_directory: str) -> None:

        annotation_file = os.path.join(output_directory, "annotations.csv")
        all_annotations = pd.read_csv(annotation_file)
        used_files = [os.path.basename(path) for path in all_annotations['path_to_image'].unique()]

        for file_path in tqdm(glob(output_directory + "/images/*.png"), desc="Removing unused images"):
            if os.path.basename(file_path) not in used_files:
                os.remove(file_path)
