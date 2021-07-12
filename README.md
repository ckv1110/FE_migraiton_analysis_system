# Finite Element Migration Analysis System
Tumoursphere migraitory boundaries (TMB) are mapped out using U-Net machine learning (ML) segmentation, and its migration is modelled and quantitatively analysed using finite element (FE) methods.

### THE WORKING PC USED TO RUN THIS SYSTEM:
- AMD R7 3800x CPU
- 16GB 3200MHz RAM
- RTX 2080 GPU
- WINDOWS 10/11

**Note:** The most important aspect of the PC to run the system will most likely be the GPU (for machine learning assisted segmentation) - I primarily utilized the GPU to train the segmentations.

### SOFTWARE USED FOR THIS SYSTEM:
- Python 3.7.7 (main prerequisite modules are as listed below):
  - tensorflow 2.5.0 (For tumorusphere segmentation; General tensorflow installation are outlined in https://www.tensorflow.org/install; For GPU enabled cards, you can follow https://www.tensorflow.org/install/gpu)
  - GIAS 2 (For Host mesh fitting before the resultant mesh is modelled for it's migration; General instructions for the installation can be found here https://gias2-shape-modelling-tutorial.readthedocs.io/en/latest/installation.html. In my experience, python 3.7 still worked just fine)
  - numpy
  - scipy
  - opencv
  - scikit-image
- FEBio (To model and and analyse the migration of the TMB)
- MATLAB (To extract the xyz coordinates of the TMB for host mesh fitting)
- GMSH (To make an initial TMB mesh)

### HOW TO USE THE SYSTEM:
**1.)** The TMB needed to be segmented before it can be modelled, so tensorflow was used to train the images to segment them. To do that, arrange your training folderas outlined below and run train.py in the /U-Net/ folder.
  - The training folder structure should look like **train/[training_number e.g. 19]/[labeled.png], [raw.png]**
  - You can check the accuracy and validation progress using tensorboard to access your ML model (https://www.tensorflow.org/tensorboard/get_started).

**2.)** After segmentation, use MATLAB to extract the xyz coordinates (as a .xyz format) and create a GMSH txt file for initial TMB meshing.

**3.)** Using GMSH, create a 3D mesh 




