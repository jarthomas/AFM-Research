# AFM TIFF Image Loader, Plotter, and Excel Exporter

This Python script loads an Atomic Force Microscopy (AFM) TIFF image, generates both 2D and 3D visual representations, and exports the data into an Excel file for further analysis. It provides an easy-to-use interface for file selection via a file dialog and offers detailed visualizations of AFM data.

![Example Output](.png)

### Dependencies:

* NumPy
* Pandas
* Matplotlib
* Tifffile
* Tkinter (for file dialogs)

### Script Features
For each AFM TIFF image, the script performs the following operations:

* Load and display the AFM data
* Reads the AFM image from a .tiff file
* 2D and 3D visualization
* Displays a 2D heatmap to represent the surface height
* Renders a 3D surface plot to visualize the surface morphology of the AFM data
* Exports the data to an Excel file for easy manipulation and analysis
