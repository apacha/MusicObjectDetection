# Datasets Normalization

After [downloading the datasets](../datasets/README.md), you need to make them interoperable with each other. To do so, we setup the following guidelines and procedures to normalize the datasets, before converting them into specific input formats, needed for various detectors:

- Images are stored as color PNG files with white background and black foreground.
- Annotations are stored as CSV files (comma-separated-values), that must contain a header.

The CSV file should look like the following:

```text
path_to_image,top,left,bottom,right,class_name
mensural/0123.png,100,120,130,142,notehead
mensural/0123.png,12,52,20,72,stem
mensural/0124.png,2,42,100,102,stem
```

an empty file (a file that contains no objects) is represented with a single line without an object:

```text
path/to/empty_image.png,,,,,
```

and for detection results, the very same format is used with one additional column:

```text
path_to_image,top,left,bottom,right,class_name,confidence
mensural/0123.png,100,120,130,142,notehead,0.9752
mensural/0123.png,12,52,20,72,stem,0.5623
mensural/0124.png,2,42,100,102,stem,0.9882
```

Once the object detectors produced results in this format, you can use the evaluation utils described [here](../evaluation/README.md).