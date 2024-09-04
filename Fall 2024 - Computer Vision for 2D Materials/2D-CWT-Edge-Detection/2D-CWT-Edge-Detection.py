import cv2
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# Upload the necessary images
uploaded = files.upload()

def create_composite(original_img_path, mask_img_path, alpha=0.5, mask_color=(255, 0, 0)):
    
    original_img = cv2.imread(original_img_path, cv2.IMREAD_COLOR)
    mask_img = cv2.imread(mask_img_path, cv2.IMREAD_GRAYSCALE)
    
    # Normalize mask values between 0 and 1 for blending
    mask_img_normalized = mask_img / 255.0

    # Convert the mask to binary (black and white)
    _, mask_img_binary = cv2.threshold(mask_img_normalized, 0.5, 1.0, cv2.THRESH_BINARY)
    
    # Create a colored version of the mask
    mask_colored = np.zeros_like(original_img)
    mask_colored[:, :] = mask_color
    
    # Overlay the mask on the original image
    composite_image = cv2.addWeighted(original_img.astype(float), 1.0, 
                                      (mask_colored * mask_img_binary[..., None]).astype(float), alpha, 0)
    
    return mask_img, composite_image.astype(np.uint8)

# File paths
original_img = '2d.png'        
cwt_mask_1 = 'ctlowmask.png'  
cwt_mask_2 = 'ctmidmask.png'  
cwt_mask_3 = 'cthighmask.png'  

# CWT images
cwt_1 = 'ctlow.png'            
cwt_2 = 'ctmid.png'            
cwt_3 = 'cthigh.png'           

# Colors for the mask overlays (one color per dataset)
colors = [(255, 0, 0),  # Red for Dataset 1
          (0, 255, 0),  # Green for Dataset 2
          (0, 0, 255)]  # Blue for Dataset 3

# Datasets: (CWT image, mask image, description, overlay color)
datasets = [
    (cwt_1, cwt_mask_1, "CWT 1.00px", colors[0]),
    (cwt_2, cwt_mask_2, "CWT 3.50px", colors[1]),
    (cwt_3, cwt_mask_3, "CWT 5.00px", colors[2])
]

# Set up plot layout: 3 columns (CWT image, mask, composite)
plt.figure(figsize=(15, 10))

for i, (cwt_img_path, mask_path, title, color) in enumerate(datasets):
    # Read the CWT image
    cwt_img = cv2.imread(cwt_img_path, cv2.IMREAD_GRAYSCALE)
    
    # Create the composite image
    mask, composite = create_composite(original_img, mask_path, alpha=0.5, mask_color=color)
    
    # Plot CWT image
    plt.subplot(len(datasets), 3, i * 3 + 1)
    plt.title(f"CWT Image {title}")
    plt.imshow(cwt_img, cmap='gray')
    plt.axis('off')
    
    # Plot mask image
    plt.subplot(len(datasets), 3, i * 3 + 2)
    plt.title(f"Mask {title}")
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    
    # Plot composite image
    plt.subplot(len(datasets), 3, i * 3 + 3)
    plt.title(f"Composite {title}")
    plt.imshow(cv2.cvtColor(composite, cv2.COLOR_BGR2RGB))
    plt.axis('off')

# Show the plot
plt.tight_layout()
plt.show()
