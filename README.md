# Music Object Detection Collection

This is the accompanying repository for the Music Object Detection paper and contains the source code for downloading, preprocessing and working with the data, as well as the evaluation code to measure the performance of various music object detectors.

## Downloading the datasets

In this repository we link to [relevant datasets](https://apacha.github.io/OMR-Datasets/), that are used for Music Object Detection:
   
   - [DeepScores](https://tuggeluk.github.io/deepscores/)
   - [MUSCIMA++](https://ufal.mff.cuni.cz/muscima)
   - [Capitan Collection](https://bitbucket.org/apacha/mensural-detector-database/src/master/)
   
   To download all datasets, simply run `python download_all_datasets.py`
   
## Dataset normalization
After downloading the datasets, you need to make them interoperable with each other. 

To do this, call `python normalize_all_datasets.py`.

We set up the following guidelines and procedures to normalize the datasets, before converting them into specific input formats, needed for various detectors:

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


## Evaluation

For making fair comparisons of different object detectors, a standard battery of metrics is used, that operates on normalized CSV files.

# License

Published under MIT License,

Copyright (c) 2018 [Alexander Pacha](http://alexanderpacha.com), [Jan Hajič](https://ufal.mff.cuni.cz/jan-hajic-jr) and [Jorge Calvo-Zaragoza](https://grfia.dlsi.ua.es/members.php?id=55)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
