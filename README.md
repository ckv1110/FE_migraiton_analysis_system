# Finite Element Migration Analysis System
Tumoursphere migraitory boundaries (TMB) are mapped out using U-Net machine learning (ML) segmentation, and its migration is modelled and quantitatively analysed using finite element (FE) methods.

### THE WORKING PC USED TO RUN THIS SYSTEM:
- AMD R7 3800x CPU
- 16GB 3200MHz RAM
- RTX 2080 GPU
- WINDOWS 10/11 OS

**Note:** The most important aspect of the PC to run the system will most likely be the GPU (for machine learning assisted segmentation) - This system primarily utilized the GPU to train the segmentations.

### SOFTWARE USED FOR THIS SYSTEM:
- Python 3.7.7 (main prerequisite modules are as listed below):
  - tensorflow 2.5.0 (For tumorusphere segmentation; General tensorflow installation are outlined in https://www.tensorflow.org/install; For GPU enabled cards, you can follow https://www.tensorflow.org/install/gpu)
  - GIAS 2 (For Host mesh fitting before the resultant mesh is modelled for it's migration; General instructions for the installation can be found here https://gias2-shape-modelling-tutorial.readthedocs.io/en/latest/installation.html. In my experience, python 3.7 still worked just fine)
  - numpy
  - scipy
  - opencv
  - scikit-image
- FEBio (To model and and analyse the migration of the TMB)
- MATLAB (To extract the TMB xyz coordinates for host mesh fitting)
- GMSH (To make an initial TMB mesh)

### HOW TO OPERATE THE SYSTEM:
**1.)** The TMB needed to be segmented before it can be modelled. In this system, a ML-based approached using the U-Net architecture **_(Ronneberger, Fischer, and Brox. 2015)_** is used to train the images and segment them. To do that, arrange your training folder as outlined below and run train.py in the /U-Net/ folder.
- The training folder structure should look like **train/[training_number e.g. 19]/[labeled.png], [raw.png]**
- Feel free to customize your own folder structure, as long as train.py can read both sets it will work.
- You can check the accuracy and validation progress using tensorboard to access your ML model (https://www.tensorflow.org/tensorboard/get_started).
- A compilation of videos created by DigitalSreeni about U-Net was really helpful in informing on how the architecture works and how it is applied in tensorflow
  - DigitalSreeni's YouTube: https://www.youtube.com/watch?v=azM57JuQpQI&list=PLZsOBAyNTZwbR08R959iCvYT3qzhxvGOE&index=1
  - DigitalSreeni's github: https://github.com/bnsreenu/python_for_microscopists

**2.)** After segmentation, use MATLAB to extract the xyz coordinates (as a .xyz format) and create a GMSH txt file for initial TMB meshing (mesh_maker_part_1.m).
- The GMSH txt file is only required for the initial image to generate the initial mesh to host mesh fit
- Other segmented images should have their xyz coordinates extracted in this step to ensure a more automated process in later steps

**3.)** Using GMSH, create a 3D mesh with the resultant GMSH txt file (Mesh -> Define -> 3D) and remove excess mesh outside of the TMB mesh. The mesh should be saved as an .stl file.
- The code for this process was derived from here: https://au.mathworks.com/matlabcentral/fileexchange/61507-binary-image-to-finite-element-mesh-gmsh-geo-file

**4.)** Export the initial mesh into FEBio and create a cylindrical mesh and align it to the TMB centre of mass. The cylindrical mesh will be host mesh fitted to the initial mesh and modelled after this.
- The cylindrical mesh size should not exceeed the size of the initial mesh.
- The radius and height are important considerations; the closer the cylindrical mesh is to the initial mesh, the more accurate the host mesh fit will be.
- After the cylindrical mesh is generated and aligned, further modifications to the mesh type and its associated parameters can be done to increase or decrease the resolution of the migration analysis (butterfly centre mesh type seems to work very well on the TMB model).
- Once the cylindrical mesh is finalized, the initial mesh can be discarded from the FEBio model as it only served as a reference.
- Material should be set for the cylindrical mesh and prescribed x,y displacements should be applied on the mesh boundary nodes so the TMB migration can be modelled.
- The resultant FEBio model should be saved as a .feb file.

**5.)** xyz coordinates of the FEBio mesh is extracted, fitted to the initial mesh, and the nodal displacements are calculated for the prescribed x,y displacement nodes using the batch_script_abs.py. The nodal displacements are overwritten in the .feb file and the code will run FEBio terminal to model the migration changes.
- This should automate when the timepoints of the segmented images are given.

### ADDITIONAL NOTES:
An examplar is provided so you can have a look at how it works (the 0_1 in the treatment_b example under the modelling folder refers to the host mesh fitting of the cylindrical reference mesh to the initial mesh).
More information can be found in our article (will be posted here when published)

### REFERENCES:
- Ronneberger, O., Fischer, P., & Brox, T. (2015, October). U-net: Convolutional networks for biomedical image segmentation. In International Conference on Medical image computing and computer-assisted intervention (pp. 234-241). Springer, Cham.





