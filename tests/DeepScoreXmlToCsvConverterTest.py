import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from preprocessing.DeepScoreXmlToCsvConverter import DeepScoresXmlToCsvConverter


class DeepScoreXmlToCsvConverterTest(unittest.TestCase):

    def test_download_and_extract_deepscores_dataset_expect_folder_to_be_created(self):
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

        expected_data = [(
                         "lg-2236887-aug-beethoven--page-2.svg", "0.04028364", "0.66760346", "0.04686767", "0.67829842",
                         "noteheadBlack"),
                         (
                         "lg-2236887-aug-beethoven--page-2.svg", "0.08813473", "0.66760346", "0.09471876", "0.67829842",
                         "noteheadBlack")]
        expected_output = pd.DataFrame(data=expected_data,
                                       columns=["path_to_image", "top", "left", "bottom", "right", "class_name"])

        converter = DeepScoresXmlToCsvConverter()
        csv_output = converter.convertXmlAnnotationsToCsv(sample_annotation_file)
        assert_frame_equal(csv_output, expected_output)


if __name__ == '__main__':
    unittest.main()
