## Steps

### 1. Load Images

Load the TIFF image (`tri_circ.tiff`) for intensity calculation and the PNG image (`tri.png`) for clearer representation.

### 2. Convert to Grayscale

Convert both images to grayscale if they are in RGB format.

### 3. Calibration

Calibrate the pixel size based on a known physical size of 3.00 µm across 512 pixels. The calibration factor is calculated as:

```latex
\text{µm per pixel} = \frac{3.00 \, \mu m}{512 \, \text{pixels}} = 0.00586 \, \mu m/\text{pixel}
