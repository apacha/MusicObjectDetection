# Music Object Detection Collection

This is the accompanying repository for the scientific paper ["A Baseline for General Music Object Detection with Deep Learning"](https://www.mdpi.com/2076-3417/8/9/1488) and contains the source code for downloading, preprocessing and working with the data, as well as the evaluation code to measure the performance of various music object detectors.

If you use code from this repository, please consider citing this work as 

```
@Article{Pacha2018,
  author         = {Pacha, Alexander and Hajič, Jan and Calvo-Zaragoza, Jorge},
  title          = {A Baseline for General Music Object Detection with Deep Learning},
  journal        = {Applied Sciences},
  year           = {2018},
  volume         = {8},
  number         = {9},
  issn           = {2076-3417},
  abstract       = {Deep learning is bringing breakthroughs to many computer vision subfields including Optical Music Recognition (OMR), which has seen a series of improvements to musical symbol detection achieved by using generic deep learning models. However, so far, each such proposal has been based on a specific dataset and different evaluation criteria, which made it difficult to quantify the new deep learning-based state-of-the-art and assess the relative merits of these detection models on music scores. In this paper, a baseline for general detection of musical symbols with deep learning is presented. We consider three datasets of heterogeneous typology but with the same annotation format, three neural models of different nature, and establish their performance in terms of a common evaluation standard. The experimental results confirm that the direct music object detection with deep learning is indeed promising, but at the same time illustrates some of the domain-specific shortcomings of the general detectors. A qualitative comparison then suggests avenues for OMR improvement, based both on properties of the detection model and how the datasets are defined. To the best of our knowledge, this is the first time that competing music object detection systems from the machine learning paradigm are directly compared to each other. We hope that this work will serve as a reference to measure the progress of future developments of OMR in music object detection.},
  article-number = {1488},
  doi            = {10.3390/app8091488},
  url            = {http://www.mdpi.com/2076-3417/8/9/1488},
}
```

## Installing requirements

- Install the requirements by running `pip install -r requirements.txt`
    - If you are running on Windows you might have to install the first two packages using `conda install ...` instead of `pip install ...`. 
- Link this project via pip to avoid import errors by running: `pip install -e .`

## Downloading the datasets

In this repository we link to [relevant datasets](https://apacha.github.io/OMR-Datasets/), that are used for Music Object Detection:
   
   - [DeepScores](https://tuggeluk.github.io/deepscores/)
   - [MUSCIMA++](https://ufal.mff.cuni.cz/muscima)
   - [Capitan Collection](https://bitbucket.org/apacha/mensural-detector-database/src/master/)
   
   To download all datasets, simply run 
   
`python datasets/download_all_datasets.py --dataset_directory ./data`
   
## Dataset normalization
After downloading the datasets, you need to make them interoperable with each other. To do this, call

`python preprocessing/normalize_all_datasets.py --dataset_directory ./data`

### Annotation format 
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

We opted for this simple format, because it can easily be read by humans and by the machine and different object detectors require specific formats anyway, e.g. PASCAL VOC format. By having all datasets normalized into a standard format, one only needs to write one target adapter for each destination format.

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
