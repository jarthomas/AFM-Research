import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import gaussian_filter, distance_transform_edt, label, binary_fill_holes
from skimage.morphology import binary_closing, disk
from skimage.filters import sobel
from skimage.segmentation import watershed
import tifffile as tiff
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from matplotlib.widgets import RectangleSelector, Button

# Global variable to store the selected ROI
roi_coords = None

# Load AFM image
def load_afm_image(file_path):
    return tiff.imread(file_path)

# Preprocessing the AFM image to emphasize grain boundaries
def preprocess_image(image, sigma=1):
    smoothed_image = gaussian_filter(image, sigma=sigma)
    edges = sobel(smoothed_image)
    boundary_mask = edges > np.mean(edges)
    closed_boundary = binary_closing(boundary_mask, disk(2))
    cleaned_boundary = binary_fill_holes(closed_boundary)
    return cleaned_boundary

# Create the topographic map for watershed segmentation
def create_topographic_map(boundary_mask):
    distance_map = distance_transform_edt(~boundary_mask)
    topographic_map = -distance_map
    return topographic_map

# Perform watershed segmentation
def watershed_segmentation(topographic_map, boundary_mask):
    markers, _ = label(~boundary_mask)
    segmented_grains = watershed(topographic_map, markers, mask=~boundary_mask)
    return segmented_grains

# Cropping function
def crop_image(image, roi):
    x_start, x_end, y_start, y_end = roi
    cropped_image = image[int(y_start):int(y_end), int(x_start):int(x_end)]
    return cropped_image

# Interactive cropping function using RectangleSelector
def onselect(eclick, erelease):
    global roi_coords
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    roi_coords = (x1, x2, y1, y2)

def interactive_crop(image):
    fig, ax = plt.subplots()
    ax.imshow(image, cmap='gray')
    ax.set_title('Select the region to crop and close the window')
    rect_selector = RectangleSelector(ax, onselect, interactive=True, useblit=True,
                                      button=[1], minspanx=5, minspany=5, spancoords='pixels',
                                      drag_from_anywhere=True)
    plt.show()
    if roi_coords:
        return crop_image(image, roi_coords)
    else:
        return image

# Plot 3D view of AFM image with highlighted segmented grains
def plot_3d_afm_with_segments(ax, image, segmentation, colormap):
    x = np.linspace(0, image.shape[1], image.shape[1])
    y = np.linspace(0, image.shape[0], image.shape[0])
    X, Y = np.meshgrid(x, y)
    normalized_segments = segmentation / np.max(segmentation)
    surf = ax.plot_surface(X, Y, image, facecolors=colormap(normalized_segments),
                           rstride=1, cstride=1, linewidth=0, antialiased=False, alpha=0.8)
    ax.set_title("3D AFM Image with Segmented Grains")
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")
    ax.set_zlabel("Height (nm)")
    ax.view_init(elev=30, azim=120)

# Overlay the segmentation results on the original image with consistent colors
def overlay_segmentation(ax, image, segmentation, colormap):
    ax.imshow(image, cmap='gray', interpolation='none', alpha=0.6)
    normalized_segments = segmentation / np.max(segmentation)
    colored_segments = colormap(normalized_segments)
    ax.imshow(colored_segments, alpha=0.4)
    ax.set_title("Segmented AFM Image (Colored)")
    ax.axis('off')

# Plot the original AFM image
def plot_original_image(ax, image):
    ax.imshow(image, cmap='gray', interpolation='none')
    ax.set_title("Original AFM Image")
    ax.axis('off')

# Function to allow the user to select a file via a file dialog
def get_file_from_user():
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(
        title="Select a TIFF file",
        filetypes=[("TIFF files", "*.tiff *.tif")]
    )
    return file_path

# Save images to a folder
def save_images_to_folder(image, segmentation, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the original image
    original_image_path = os.path.join(output_folder, 'original_afm_image.png')
    plt.imsave(original_image_path, image, cmap='gray')

    # Save the segmentation overlay
    segmented_image_path = os.path.join(output_folder, 'segmented_afm_image.png')
    plt.imsave(segmented_image_path, segmentation, cmap='viridis')

    # Save the 3D plot as an image
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot_3d_afm_with_segments(ax, image, segmentation, plt.cm.viridis)
    three_d_image_path = os.path.join(output_folder, 'afm_3d_image.png')
    plt.savefig(three_d_image_path)

    print(f"Images saved to folder: {output_folder}")

# Button callback to save images to a new folder
def on_export_button_clicked(event, image, segmentation):
    output_folder = "AFM_Segmentation_Images"
    save_images_to_folder(image, segmentation, output_folder)

# Main function to execute the segmentation pipeline
def main():
    global roi_coords
    file_path = get_file_from_user()

    if not file_path:
        print("No file selected. Exiting...")
        return

    image = load_afm_image(file_path)
    cropped_image = interactive_crop(image)
    boundary_mask = preprocess_image(cropped_image)
    topographic_map = create_topographic_map(boundary_mask)
    segmented_grains = watershed_segmentation(topographic_map, boundary_mask)

    colormap = plt.cm.viridis
    fig, axarr = plt.subplots(1, 3, figsize=(18, 6))

    plot_original_image(axarr[0], cropped_image)
    overlay_segmentation(axarr[1], cropped_image, segmented_grains, colormap)

    ax3 = fig.add_subplot(1, 3, 3, projection='3d')
    plot_3d_afm_with_segments(ax3, cropped_image, segmented_grains, colormap)

    plt.tight_layout()

    # Create a button for exporting images
    ax_export = plt.axes([0.81, 0.01, 0.1, 0.05])  # Position for the button
    export_button = Button(ax_export, 'Export to Folder')

    # Set the button click event to trigger export
    export_button.on_clicked(lambda event: on_export_button_clicked(event, cropped_image, segmented_grains))

    plt.show()

if __name__ == "__main__":
    main()