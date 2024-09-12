import cv2
import numpy as np
import pywt
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

# Function to open file dialog and let user select a PNG file
def upload_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Open file dialog to select a PNG image
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])

    if file_path:
        # Proceed with the image analysis if a file is selected
        process_image(file_path)
    else:
        print("No file selected.")

# Function to process the image and show analysis
def process_image(file_path):
    # Load the image
    original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    # Normalize the image to [0, 1] range for wavelet transform
    image = original_image / 255.0

    # Perform the 2D Discrete Wavelet Transform (DWT)
    wavelet = 'haar'  # You can change to other wavelets like 'db1', 'coif1'
    coeffs2 = pywt.dwt2(image, wavelet)

    # Extract the approximation and detail coefficients
    cA, (cH, cV, cD) = coeffs2

    # Initialize the mask as None
    mask = None

    # Function to update the threshold and display the result
    def update_threshold(threshold):
        nonlocal mask  # To update mask globally for saving it later

        """Callback for the trackbar to apply thresholding and display results."""
        # Apply thresholding to the detail coefficients
        threshold = threshold / 100.0  # Scale threshold for better control
        cH_thresh = np.where(np.abs(cH) > threshold, cH, 0)
        cV_thresh = np.where(np.abs(cV) > threshold, cV, 0)
        cD_thresh = np.where(np.abs(cD) > threshold, cD, 0)

        # Reconstruct the image with thresholded coefficients
        coeffs_thresh = (cA, (cH_thresh, cV_thresh, cD_thresh))
        image_reconstructed = pywt.idwt2(coeffs_thresh, wavelet)

        # Generate mask by thresholding the reconstructed image
        mask = np.where(image_reconstructed > threshold, 1.0, 0.0)

        # Convert the mask back to the [0, 255] range for display
        mask_display = (mask * 255).astype(np.uint8)

        # Display the original image, thresholded mask, and the reconstructed image
        cv2.imshow("Reconstructed Image", (image_reconstructed * 255).astype(np.uint8))
        cv2.imshow("Mask", mask_display)

    # Function to overlay the black areas of the mask on the original image and display side by side
    def overlay_mask():
        if mask is not None:
            # Invert the mask: black areas become 1 (foreground), and white areas become 0
            inverted_mask = 1.0 - mask

            # Normalize the inverted mask to [0, 255] range and convert to uint8
            normalized_mask = (inverted_mask * 255).astype(np.uint8)

            # Convert the original image to 3 channels (RGB) for overlaying
            color_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)

            # Create an overlay with blue color for the mask
            blue_mask = np.zeros_like(color_image)
            blue_mask[:, :, 0] = normalized_mask  # Add mask to the blue channel

            # Blend the original image with the mask (alpha blending)
            alpha = 0.5  # Transparency factor for the mask
            overlay_image = cv2.addWeighted(color_image, 1.0, blue_mask, alpha, 0)

            # Concatenate the original image and the overlayed image side by side
            original_color_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
            combined_image = np.hstack((original_color_image, overlay_image))

            # Display the original and overlayed image side by side
            cv2.imshow("Original and Overlayed Image", combined_image)

            # Optionally, save the overlay image as a PNG
            cv2.imwrite('overlayed_image.png', overlay_image)
            print("Overlay image saved as 'overlayed_image.png'")

    # Create a window for the GUI
    cv2.namedWindow("Reconstructed Image")
    cv2.namedWindow("Mask")

    # Create a slider for the threshold
    cv2.createTrackbar('Threshold', 'Reconstructed Image', 10, 100, update_threshold)

    # Initialize the GUI by displaying the initial state
    update_threshold(10)

    # Event loop to wait for "Enter" key (key code 13) to save the mask and overlay the image
    while True:
        key = cv2.waitKey(1)

        # If "Enter" (key code 13) is pressed, overlay the mask and show images side by side
        if key == 13:
            overlay_mask()  # Overlay the black areas of the mask on the original image and show side by side
            break  # Exit the loop and close the windows

        # If "Esc" (key code 27) is pressed, just exit without saving
        elif key == 27:
            break

    # Close all windows
    cv2.destroyAllWindows()

# Run the image uploader
if __name__ == "__main__":
    upload_image()