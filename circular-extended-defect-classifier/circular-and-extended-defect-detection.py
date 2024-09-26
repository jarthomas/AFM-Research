import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from skimage.filters import sobel
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.segmentation import clear_border

def load_afm_tiff(filepath):
    # Read the tiff file
    image = tiff.imread(filepath)
    return image

def edge_detection(image):
    # Apply the Sobel filter to detect edges
    edges = sobel(image)
    return edges

def classify_defects(edges):
    # Threshold and close the edges
    closed_edges = closing(edges > 0.1, square(4))
    labeled_edges = label(closed_edges)
    labeled_edges = clear_border(labeled_edges)  # Remove artifacts connected to the image border

    circular_mask = np.zeros_like(labeled_edges, dtype=bool)
    extended_mask = np.zeros_like(labeled_edges, dtype=bool)

    # Iterate over the detected regions and classify them based on shape
    for region in regionprops(labeled_edges):
        if region.area >= 30:  # Ignore small regions (adjust threshold as needed)
            # Calculate aspect ratio (extent)
            aspect_ratio = region.major_axis_length / region.minor_axis_length

            # Classify based on aspect ratio: near 1 means circular, higher means extended
            if aspect_ratio < 1.8:
                circular_mask[labeled_edges == region.label] = True
            else:
                extended_mask[labeled_edges == region.label] = True

    return circular_mask, extended_mask

def plot_segmented_defects(image, circular_mask, extended_mask):
    # Create a color overlay: circular defects in green, extended defects in red
    overlay = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.float32)

    # Apply green color to circular defects
    overlay[circular_mask] = [0, 1, 0]  # Green

    # Apply red color to extended defects
    overlay[extended_mask] = [1, 0, 0]  # Red

    # Blend the overlay with the original grayscale image
    alpha = 0.4  # Transparency level
    image_normalized = (image - np.min(image)) / (np.max(image) - np.min(image))  # Normalize image to [0, 1]
    blended = (1 - alpha) * np.stack([image_normalized]*3, axis=-1) + alpha * overlay

    # Plot the original and segmented image side by side
    plt.figure(figsize=(16, 8))

    # Plot original image
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title("Original AFM Image")
    plt.axis('off')

    # Plot segmented image with defects
    plt.subplot(1, 2, 2)
    plt.imshow(blended)
    plt.title("AFM Image with Segmented Defects (Green: Circular, Red: Extended)")
    plt.axis('off')

    plt.show()

def get_file_from_user():
    # Initialize the Tkinter root window and hide it
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window

    # Open the file dialog to select a TIFF file
    file_path = askopenfilename(
        title="Select an AFM TIFF image",
        filetypes=[("TIFF files", "*.tiff *.tif")]
    )
    
    if not file_path:
        print("No file selected. Exiting.")
        return None

    return file_path

def main():
    # Step 1: Get file from user
    filepath = get_file_from_user()
    
    if filepath is None:
        return  # Exit if no file was selected
    
    # Step 2: Load the TIFF image
    image = load_afm_tiff(filepath)
    
    # Step 3: Perform edge detection
    edges = edge_detection(image)

    # Step 4: Classify defects as circular or extended
    circular_mask, extended_mask = classify_defects(edges)

    # Step 5: Plot the original image with classified defects overlaid as colors
    plot_segmented_defects(image, circular_mask, extended_mask)

# Call the main function to run the script
if __name__ == "__main__":
    main()
