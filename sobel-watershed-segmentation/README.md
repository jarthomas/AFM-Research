# Sobel and Watershed Therholding for Segmented 3D Visualizations of AFM Data

This Python script provides a comprehensive pipeline for analyzing Atomic Force Microscopy (AFM) images. It allows users to load, preprocess, segment, and visualize AFM images using watershed segmentation and various image processing techniques. The script includes interactive tools for region selection, 3D visualization, and export functionality to save processed images.

![Example Output](Heatmap-3d-output.png)

### Dependencies:

* numpy: For numerical operations.
* matplotlib: For plotting and visualizing images in 2D and 3D.
* scipy: For image filtering and distance transformation.
* skimage: For image processing, edge detection, and segmentation.
* tifffile: To read TIFF images.
* tkinter: For the file selection dialog.
* mpl_toolkits.mplot3d: For 3D plotting of the AFM image.

### Script Features

* Image Loading: Select and load TIFF format AFM images.
* Preprocessing: Apply smoothing and edge detection to emphasize grain boundaries in AFM images.
* Interactive Region Selection: Use a graphical interface to crop a region of interest (ROI) interactively.
* Watershed Segmentation: Segment the AFM image based on distance maps and edge detection.
* 3D Visualization: Render a 3D plot of the AFM image with color-coded segmented grains.
* Segmentation Overlay: Overlay segmentation results on the original AFM image with consistent colors.
* Image Export: Save original, segmented, and 3D-rendered images to a specified folder.

### Walkthrough

## Step 1 - Define an Area of Interest on Your Sample

![Example Output](sample1.png)

## Step 2 - View 

![Example Output](sample1.png)
