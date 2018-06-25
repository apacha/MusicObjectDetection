import os
from glob import glob

from PIL import Image
from tqdm import tqdm


class MensuralNormalizer():

    def copy_and_normalize_images(self, mensural_directory: str, output_directory: str) -> None:
        os.makedirs(os.path.join(output_directory, "images"), exist_ok=True)

        all_images = glob(mensural_directory + "/*.JPG")
        all_annotations = glob(mensural_directory + "/*.txt")

        for image_path in tqdm(all_images, desc="Copying and converting images"):
            image = Image.open(image_path)
            filename = os.path.splitext(os.path.basename(image_path))[0] + ".png"
            output_path = os.path.join(output_directory, "images", filename)
            image.save(output_path)