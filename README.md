# Animal Classifier Pipeline

Camera traps are cameras with a motion sensor that take a picture
whenever something moves in front of them. They are often
used as an inexpensive and non-invasive method of observing animals 
in the wild. This has allowed researchers to generate large databases
of animal activity that typically take a long
time to manually sort through before they can be used
in a research project.

This package provides an easy-to-use function that automatically identifies
the species of an animal in a picture. It has the added feature of cropping the images
around the animal and sorting them into folders by species but it also requires that the animals first be 
detected using [MegaDetector](#megadetector) before the program is run.
The function was originally designed to work for a model that
was trained to categorise animals found in Hong Kong, however it should be relatively easy
to adapt it for any model trained with Keras 
(see the section on how to [modify the pipeline](#how-to-modify-the-package-for-a-new-model) 
for details).

The modules in this repository should be seen as the second part of a larger pipeline
for sorting animal images. MegaDetector provides the first step of finding the
animals in the database and this package automates the final step of categorising
those animals.


## How to Run the Animal Classifier

This package can be installed locally using PIP. To do so, download 
the GitHub repository and run the following code, where the folder
given by "path\to\package" should contain the setup.py file

```python
pip install "path\to\package"
```

The other sections of this ReadMe file describe in detail the different
options that you have when running the program. However, if you just
want to quickly get something to work then they can all be safely ignored
and you can just run the following code once the package has been installed.
Although, you will need to [download the trained model](#model) and have [ran MegaDetector](#megadetector)
as described in the [Inputs](#inputs) section.

```python
from classify_animals.main import classify_animals

classify_animals(
    bb_results_path = 'path\to\MegaDetector\output\json\string', 
    image_dir = 'path\to\raw\images',
    model_path = 'path\to\trained\model',
    md_thr=0.1 #Animal Classifier Threshold 
)
```

### Inputs

The function requires the following three files/directories to run.

- **Bounding boxes** - These are the animal detections that were found
    after running MegaDetector (see the section on [using MegaDetector](#megadetector)
    to find out how to get this). The path to this file should be passed
	to bb_results_path.
- **Images** - Uncropped images that were fed into
	MegaDetector. The path passed to image_dir
	should be the same as what was passed into MegaDetector's detection
	function when the bounding boxes were generated.
- **Model** - Model that was trained to classify cropped images of animals.
	It should either be a single file saved in Keras's H5 format or a folder
	containing the saved models and dataset means and standard deviations from the
	[train_image_classifier_al](https://github.com/garethlamb/train_image_classifier_al) package. 
	Additionally, the path to the model file or folder should be passed to model_path.

#### Model

To obtain a copy of the trained model, please contact Dr. Calvin Lee of the Global Ecology 
Lab at the University of Hong Kong at his email address, leeckf@hku.hk. If you
wish to use your own animal classifier for this pipeline then please read the
section on how to [modify the pipeline](#how-to-modify-the-package-for-a-new-model)
before you use your own model.

#### MegaDetector

MegaDetector is an algorithm developed by Microsoft that can automatically
detect and draw a bounding box around an animal in an image.
The function that is provided by this package requires the bounding boxes generated by
the detector in order to work. Instructions on how to install and run MegaDetector can be found on
their [GitHub](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md) 
page.  It should be noted that the
detector requires the installation of Anaconda and the packages, YOLOv5
and ai4eutils, however details of this can be found on their guide.

This program was tested on outputs from MegaDetector v5.0A (MDv5a). It should
work for other versions of the algorithm but a different [threshold for the detections' confidence
rating](#optional-parameters) will likely need to be chosen.


### Outputs

This program has two outputs. The first is a CSV file called 'Animal Labels'
and the second is a folder called 'cropped_images'
that lists the species of each animal. The data
dictionary for the CSV file is as follows:

- **original_image_path** - File path of the original uncropped image
    relative to the directory that was passed into 'image_dir'.
- **cropped_image_path** - File path to the cropped image relative to
    the folder called 'cropped_images'.
- **bb_conf** - Confidence level of bounding box of the animal given
    by MegaDetector.
- **species** - Species of the animal as predicted by the model.
- **class_ent** - Level of uncertainty in the model's prediction for
    the species of the animal.

As you might expect, the folder called 'cropped_images' contains the cropped
images of animals. The images are sorted into subfolders based on the
species of animal that was detected by the algorithm. Additionally, if a threshold value for the
level of uncertainty in the classifications (known as entropy) was set then it will also 
contain a subfolder called 'zz_unknown' for the animals that it could
not classify.

#### Output folder

The function will create a folder within which  both final outputs will be stored.
It will also place all intermediary files that are required to process the data in
this folder, however they will all be deleted once all of the data has been processed.

By default, the folder will be created in the current working directory and be called
'Animal Detections'. To change where the output is stored, pass
the path to the directory to the [optional parameter](#optional-parameters) 'working_data_dir'
of the function.

**Warning** please do not open, move or delete any files in
this directory while the program is still running as this will likely cause
it to crash.

#### Animal Categories

If left unmodified, the program will classify animals into one of 15 categories of species
all of which can be found in Hong Kong. They are either
given by their Latin name or by a common name if they
are a group of species. The full list of categories can be found below.

- Bird
- Canis lupus familiaris
- Eurasian Otter 
- Felis catus
- Herpestes javanicus
- Hystrix brachyura
- Macaca mulatta
- Melogale species
- Muntiacus species
- Other animal
- Paguma larvata
- Prionailurus bengalensis
- Rodent
- Sus scrofa
- Viverricula indica

## Optional Parameters

The following are optional parameters of the main function
that affect the efficiency and accuracy of the classifier.

- **working_data_dir** (string or Python PATH object), default None: Path
	to directory that will contain the temporary files
	that the program needs to use to run and the output of
	the program. if set to None, it will default to creating
	a folder in the current working directory.
	
- **keep_crops** (bool), default True: If True, MegaDetector's animal detections
	will be cropped and saved to the directory given by working_data_dir. If False,
	the cropped images will be deleted after each batch.
	
- **md_thr** (float), default 0.1: Threshold value for the confidence ratings of
	MegaDetector's detections. Only bounding boxes with a confidence
	rating above the threshold will be cropped and analysed. A higher
	threshold means that detections are more likely to be of an animal
	but it also makes it more likely that fewer animals will be detected.
	
- **ent_thr** (float), default NumPy positive infinity: Threshold value for confidence rating in neural network's
	classifications. Confidence rating is Shannon Entropy of the network's
	output and therefore only classifications that have an entropy below the 
	threshold will be assigned to their crops. A lower threshold will likely increase
	the precision of the classifier however it will also mean that more animal
	detections will be labelled as having an unknown species.
	
- **batch_size** (int), default 32: Number of images to process at a time. Lowering this number
	should reduce the program's requirement for memory and storage space. Raising
	this should reduce the overall time it takes for the neural network
	to process the images.

- **classifier_batch_size** (int), default batch_size / 2: Batch size for images as they're processed by the
	neural network classifier. By default, it is half of batch_size 
	rounded up to the nearest integer.

- **use_checkpoints** (bool), default True: If True, the program will start from checkpoints found
	in working_data_dir, which is useful if the program encounters a fatal error during processing. If
	False, the program will start the whole process from the beginning and overwrite all
	checkpoints.
	
- **show_progress_bar** (bool), default True: If True, a progress bar will be displayed.

## How to Modify the Package for a New Model

Even if you do not use the model that can be provided by 
[Dr. Calvin Lee](#model), the function can still be
used as a pipeline for extracting and analysing animal detections
from MegaDetector. The package has been designed so that it can
be tailored to work for any model that is similar to the original
one by running several commands before the function is run. However,
it does require that the new model is a Keras neural network where each
output node represents exactly one category and where the node with the
highest value is the category for a given image.

There are several global variables that will likely need to be
changed to fit a new model. These variables can be accessed
using the 'config' module; an example of which can be seen below.

```python
from classify_animals.main import main as classy_func
from classify_animals.scripts import config

config.IMAGE_SIZE = (100, 100) # Size of images that are inputted to the model

classy_func(
    bb_results_path = 'path\to\MegaDetector\output\json\string', 
    image_dir = 'path\to\raw\images',
    model_path = 'path\to\trained\model',
    md_thr=0.1 #Animal Classifier Threshold 
)
```

Any changes to the global variables must be called before the
main function is executed, otherwise they will not take effect.
The following describes the global variables that can be edited 
by the 'config' module.

- IMAGE_SIZE, 2-tuple of integers - Images are resized to this size
	using bilinear interpolation before being passed to the model.
	Size is measured in pixels and is given by (height, width).
- UNKNOWN_SPECIES_NAME, string - Label that should be assigned to
	the image when the classifier does not know its category (i.e.
	when the entropy of the output is above the threshold). 
	Defaults to 'zz_unknown'.
- SPECIES_CATEGORIES, 1-D NumPy array - Categories that animals
	can be classified into. Must be listed in the same order as
	when the model was trained. Should also be the same length 
	as the number of output nodes in the model.
- WORK_DIR_DEFAULT_NAME, string - Default name for program's
	working directory folder when no directory has been
	passed into the function
- The following global variables are all strings and are
	the column titles of the output CSV.
  - BASE_COL_NAME, default 'original_image_path'
  - CROP_COL_NAME, default 'cropped_image_path'
  - SPECIES_COL_NAME, default 'species'
  - BB_CONF_COL_NAME, default 'bb_conf'
  - ENT_COL_NAME, default 'class_ent'

You can define your own function that pre-processes the images
before they are passed into the model by overwriting the main
function of the 'preprocess_image' module. By default, the function
will pre-process images for the default model and so it is important
that this function be changed should you use your own.

The pre-processesing function must
input and output precisely one TensorFlow image tensor or else it
will likely cause an error. An example of overwriting the pre-processing function 
with one that leaves the tensors unchanged can be seen below.

```python
from classify_animals.scripts import preprocess_image

preprocess_image.main = lambda x : x # Leave images unchanged

classy_func(
    bb_results_path = 'path\to\MegaDetector\output\json\string', 
    image_dir = 'path\to\raw\images',
    model_path = 'path\to\trained\model',
    md_thr=0.1 #Animal Classifier Threshold 
)
```

## How to Cite this Package

In accordance with the [licensing agreement](LICENCE.txt), you must
give appropriate credit to the author, Gareth Lamb, for any work derived from 
this package. When citing this package, please provide the URL of 
this GitHub page, a link to the licence and indicate
if any changes to the source code were made.
You may do this in any reasonable manner, but not in any way that 
suggests the licensor endorses you or your use.

## Acknowledgements 

We would like to thank the many research teams in Hong Kong who
collected the camera trap data that we used to train our model. 
We would also like
to thank the team behind MegaDetector who built the reliable
open-source animal detector and whose paper inspired us to
build this package. Details of their paper can be found below.

Megadetector
- **Title** - Efficient Pipeline for Camera Trap Image Review
- **Author** - Beery, Sara and Morris, Dan and Yang, Siyu
- **Journal** - arXiv preprint arXiv:1907.06772
- **Year** - 2019

We would also like to thank the creators of Keras and TensorFlow
for building the packages that we used to train our model and
construct the pipeline. The following are the citations to their
packages.

Keras
- **Title** - Keras
- **Author** - Chollet, Francois and others
- **Year** - 2015
- **URL** - https://keras.io

Tensorflow
- **Title** - TensorFlow: Large-Scale Machine Learning on Heterogeneous Systems
- **Author** - Martín Abadi et al.
- **URL** - https://www.tensorflow.org/
- **Note** - Software available from tensorflow.org
