from __future__ import print_function, unicode_literals
from distutils.core import setup

setup(
    name='MusicObjectDetection',
    version='0.1',
    packages=['MusicObjectDetection',
              'MusicObjectDetection.tests',
              'MusicObjectDetection.datasets',
              'MusicObjectDetection.evaluation',
              'MusicObjectDetection.preprocessing'],
    url='https://bitbucket.org/apacha/musicobjectdetection',
    license='',
    author='Alexander Pacha, Jorge Calvo-Zaragoza, Jan Hajič jr.',
    author_email='alexander.pacha@tuwien.at, jcalvo@upv.es, hajicj@ufal.mff.cuni.cz',
    description='OMR: Music Object Detection.'
)
