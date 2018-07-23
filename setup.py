from __future__ import print_function, unicode_literals
from distutils.core import setup

setup(
    name='musicobjectdetection',
    version='0.1',
    packages=['musicobjectdetection',
              'musicobjectdetection.tests',
              'musicobjectdetection.datasets',
              'musicobjectdetection.evaluation',
              'musicobjectdetection.preprocessing'],
    url='',
    license='',
    author='Alexander Pacha, Jorge Calvo-Zaragoza, Jan Hajič jr.',
    author_email='alexander.pacha@tuwien.at, jcalvo@upv.es, hajicj@ufal.mff.cuni.cz',
    description='OMR: Music Object Detection.'
)
