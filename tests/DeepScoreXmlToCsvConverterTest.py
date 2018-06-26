import os
import shutil
import unittest

import pandas as pd
from hamcrest import assert_that, is_, empty, not_, equal_to
from pandas.util.testing import assert_frame_equal

from datasets.DeepScoresDatasetDownloader import DeepScoresDatasetDownloader
from preprocessing.DeepScoreXmlToCsvConverter import DeepScoreXmlToCsvConverter


class DeepScoreXmlToCsvConverterTest(unittest.TestCase):

    def test_deep_scores_xml_to_csv_conversion(self):
        # Arrange
        sample_annotation_file = \
            """<annotation>
                   <folder>Annotations</folder>
                   <filename>lg-2236887-aug-beethoven--page-2.svg</filename>
                   <size>
                       <width>2707</width>
                       <height>3828</height>
                       <depth>1</depth>
                   </size>
                   <segmented>0</segmented>
                   <object>
                       <name>noteheadBlack</name>
                       <bndbox>
                           <xmin>0.66760346</xmin>
                           <xmax>0.67829842</xmax>
                           <ymin>0.04028364</ymin>
                           <ymax>0.04686767</ymax>
                       </bndbox>
                   </object>
                   <object>
                       <name>noteheadBlack</name>
                       <bndbox>
                           <xmin>0.66760346</xmin>
                           <xmax>0.67829842</xmax>
                           <ymin>0.08813473</ymin>
                           <ymax>0.09471876</ymax>
                       </bndbox>
                   </object>
               </annotation>"""

        expected_data = [
            ("lg-2236887-aug-beethoven--page-2.svg", "0.04028364", "0.66760346", "0.04686767", "0.67829842",
             "noteheadBlack"),
            ("lg-2236887-aug-beethoven--page-2.svg", "0.08813473", "0.66760346", "0.09471876", "0.67829842",
             "noteheadBlack")]
        expected_output = pd.DataFrame(data=expected_data,
                                       columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])

        converter = DeepScoreXmlToCsvConverter()
        csv_output, _, _ = converter._convert_xml_annotations_to_csv(sample_annotation_file)
        assert_frame_equal(csv_output, expected_output)

    def test_convert_relative_to_absolute_coordinates(self):
        data_input = pd.DataFrame(data=[("page-2.svg", "0.01", "0.02", "0.03", "0.04", "noteheadBlack")],
                                  columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])
        expected_output = pd.DataFrame(data=[("page-2.svg", 1.0, 4.0, 3.0, 8.0, "noteheadBlack")],
                                       columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])

        converter = DeepScoreXmlToCsvConverter()
        actual_output = converter._convert_relative_to_absolute_coordinates(data_input, 200, 100)

        assert_frame_equal(actual_output, expected_output)

    def test_deep_scores_normalization_expect_annotations_in_directory(self):
        # Arrange
        dataset_directory = "temp"
        normalized_dataset_directory = "temp/normalized_deep_scores"
        downloader = DeepScoresDatasetDownloader()
        downloader.download_and_extract_dataset(dataset_directory)
        converter = DeepScoreXmlToCsvConverter()

        # Act
        converter.copy_and_normalize_images(os.path.join(dataset_directory, "deep-scores-dense"),
                                            normalized_dataset_directory)
        converter.normalize_annotations(os.path.join(dataset_directory, "deep-scores-dense"),
                                        normalized_dataset_directory)

        # Assert
        assert_that(os.path.exists(normalized_dataset_directory), is_(equal_to(True)))
        assert_that(os.listdir(normalized_dataset_directory), is_(not_(empty())))

        # Cleanup
        shutil.rmtree("temp", True)
        os.remove("deep-scores-dense-mob.zip")


if __name__ == '__main__':
    unittest.main()
