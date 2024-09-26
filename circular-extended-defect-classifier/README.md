# Cicular and Extended Defect Classifier

![Example Output](Heatmap-3d-output.png)

This Python script is designed to analyze and segment defects in Atomic Force Microscopy (AFM) images. It processes an AFM TIFF image to identify circular and extended defects using edge detection, morphology, and region-based segmentation. The resulting defects are visually highlighted in a color-coded image overlay.

### Dependencies:
* numpy: For numerical operations and image array manipulation.
* matplotlib: For plotting and visualizing the images.
* tifffile: To read TIFF image files
* scikit-image (skimage): For image processing functions like edge detection and morphology.
* tkinter: To create a simple GUI for file selection.

### Script Features
* Edge Detection: The script applies the Sobel filter to detect edges in the AFM image.
* Defect Classification: Defects are classified into two categories:
* Circular Defects: Highlighted in green.
* Extended Defects: Highlighted in red.
* Visualization: The original AFM image is displayed side by side with a segmented version, where circular and extended defects are color-coded.

