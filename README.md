# E-commerce-Opimization

## Notice
This project is is stil in **beta**, please submit any suggestions to [aounlutfi@gmail.com](mailto:aounlutfi.com).

## Description
The aim of this project is to develop a system that automotically score and suggest an optimal website design based on certain design rules. The system contains the following modules:

  1. Website capture
  2. Website classification
  3. Image processing
  4. Modeling
  5. Evaluation
  
Currently the system only supports 5 e-commerce webstie types (Travel, Food, Hotels, Tickets, Generic) and can only identify "continue shopping" buttons and "proceed to checkout" buttons.

## Dependencies
The system requires the following to function fully:

  1. PhantomJS (Bundled for Windows in the source code)
  3. Tesseract OCR (Bundled for Windows in the source code)
  2. NLTK
  3. OpenCV3 with contrib_lib or OpenCV2
  4. networkX
  5. Skimage

## Examples
It is important to note that to ensure the template image and rules.txt are in the same directory 
as the main script. Also, a folder named tests is needed to output the results and src folder has 
to be in the same directory as the main script.

### Imports
```python
import src.web_classification as clas
import src.web_capture as cap
import src.image_processing as im
import src.modeling as m
import src.evaluation as ev
```
### Classification
```python
classification = clas.web_classification(html)
```
### Modeling
```python
elements = im.image_processing(image)
model = m.modeling(elements, image)
```
### Evaluation
```python
score, recommendations = ev.score(model, classification)
```