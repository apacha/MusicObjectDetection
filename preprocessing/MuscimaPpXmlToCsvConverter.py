import os
import re
import shutil
from glob import glob

from omrdatasettools.converters.ImageInverter import ImageInverter
from omrdatasettools.image_generators.MuscimaPlusPlusImageGenerator import MuscimaPlusPlusImageGenerator
from tqdm import tqdm
import pandas as pd


class MuscimaPpXmlToCsvConverter(object):

    def copy_and_normalize_images(self, cvc_muscima_directory: str, output_directory: str) -> None:
        os.makedirs(os.path.join(output_directory, "images"), exist_ok=True)

        all_images = glob(cvc_muscima_directory + "/**/ideal/**/image/*.png", recursive=True)

        for image_path in tqdm(all_images, desc="Copying images"):
            writer = re.search("w-..", image_path).group()
            file_name = os.path.basename(image_path)
            output_path = os.path.join(output_directory, "images", writer + "_" + file_name)
            shutil.copy(image_path, output_path)

        image_inverter = ImageInverter()
        image_inverter.invert_images(output_directory, "*.png")

    def normalize_annotations(self, muscima_pp_directory: str, output_directory: str) -> None:

        destination_annotation_file = os.path.join(output_directory, "annotations.csv")

        muscima_pp_image_generator = MuscimaPlusPlusImageGenerator()
        xml_file_paths = muscima_pp_image_generator.get_all_xml_file_paths(muscima_pp_directory)
        all_crop_objects = muscima_pp_image_generator.load_crop_objects_from_xml_files(xml_file_paths)

        data = []
        for crop_object in tqdm(all_crop_objects, "Converting annotations"):
            writer = re.search("W-..", crop_object.doc).group().lower()
            page = int(re.search("N-..", crop_object.doc).group()[2:])
            filename = "images/{0}_p{1:03d}.png".format(writer, page)
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
