import pandas as pd
import lxml
from lxml import etree


class DeepScoresXmlToCsvConverter(object):
    def convertXmlAnnotationsToCsv(self, annotation_file: str) -> pd.DataFrame:

        root = etree.fromstring(annotation_file)
        filename = root.findtext("filename")
        data = []

        for annotation_object in root.findall("object"):
            class_name = annotation_object.findtext("name")
            top = annotation_object.findtext("bndbox/ymin")
            left = annotation_object.findtext("bndbox/xmin")
            bottom = annotation_object.findtext("bndbox/ymax")
            right = annotation_object.findtext("bndbox/xmax")
            data.append((filename,top, left, bottom, right, class_name))

        converted_output = pd.DataFrame(data=data, columns=["path_to_image","top","left","bottom","right","class_name"])

        return converted_output
