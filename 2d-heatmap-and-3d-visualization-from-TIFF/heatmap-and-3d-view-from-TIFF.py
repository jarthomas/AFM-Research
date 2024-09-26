import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tifffile as tiff
from mpl_toolkits.mplot3d import Axes3D
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def load_afm_tiff(filepath):
    # Read the tiff file
    image = tiff.imread(filepath)
    return image

def save_tiff_to_excel(image, output_path):

    # Convert the image (NumPy array) to a pandas DataFrame
    df = pd.DataFrame(image)

    # Save the DataFrame to an Excel file
    df.to_excel(output_path, index=False, header=False)
    print(f"TIFF data successfully saved to {output_path}")

def plot_afm_data(image):
    # Create a figure with two subplots: one for 2D heatmap and one for 3D surface plot
    fig = plt.figure(figsize=(12, 6))

    # Plot 2D heatmap in the first subplot
    ax1 = fig.add_subplot(1, 2, 1)
    heatmap = ax1.imshow(image, cmap='viridis', extent=[0, 3, 0, 3])
    fig.colorbar(heatmap, ax=ax1, label='Height (nm)')
    ax1.set_title("AFM Surface Height Map")
    ax1.set_xlabel("X (µm)")
    ax1.set_ylabel("Y (µm)")

    # Plot 3D surface plot in the second subplot
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')

    # Create a meshgrid for the X and Y coordinates
    x = np.linspace(0, 3, image.shape[1])
    y = np.linspace(0, 3, image.shape[0])
    X, Y = np.meshgrid(x, y)

    # Plot the surface
    ax2.plot_surface(X, Y, image, cmap='viridis')

    # Add labels and title
    ax2.set_title("3D AFM Surface Plot")
    ax2.set_xlabel("X (µm)")
    ax2.set_ylabel("Y (µm)")
    ax2.set_zlabel("Height (nm)")

    # Show the combined figure with both subplots
    plt.tight_layout()
    plt.show()

def get_file_from_user():
    # Init the Tkinter root window and hide it
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
    """
    Main function to load, plot, and save AFM data.
    """
    # Step 1: Get file from user
    filepath = get_file_from_user()
    
    if filepath is None:
        return  # Exit if no file was selected
    
    # Step 2: Load the TIFF image
    image = load_afm_tiff(filepath)
    
    # Step 3: Visualize the AFM image (2D heatmap and 3D surface plot)
    plot_afm_data(image)

    # Step 4: Save the TIFF data to an Excel file
    output_excel_path = filepath.replace(".tif", "_output.xlsx")
    save_tiff_to_excel(image, output_excel_path)

# Call the main function to run the script
if __name__ == "__main__":
    main()