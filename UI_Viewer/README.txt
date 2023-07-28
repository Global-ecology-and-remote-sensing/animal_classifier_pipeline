# UI viewer

This UI allows users to review the results from the [Animal Classifier](https://github.com/Global-ecology-and-remote-sensing/animal_classifier_pipeline) and modify the results if needed. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the two required packages.

```bash
pip install tkinter
pip install Pillow
```

## Usage
Users can run the UI.py code to review results. Then a UI should pop out and user can copy the JSON file path and image file path to the corresponding input fields.
*The JSON file is the output from the classifier*

If user's inputs are correct, the image, species name, and the confidence index should show on the UI. User can also change the species name if the result from the classifier was not correct. The "Save" button will create a CSV file that records the modified species and also the progress of labelling. 

