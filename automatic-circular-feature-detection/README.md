## Circular Structures Analysis Using MATLAB

The following MATLAB script processes a TIFF image to calculate intensities within detected circular structures, while a PNG image is used for visual representation. The script performs circle detection, intensity calculation, and visualization.

![Example Output](circ_example_output.PNG)

### Summary

1. **Load Images**

    ```matlab
    % Load the TIFF and PNG images
    I_tiff = imread('tri_circ.tiff');
    I_png = imread('tri.png');
    ```

    - `imread('tri_circ.tiff')`: Reads the TIFF image used for intensity calculation.
    - `imread('tri.png')`: Reads the PNG image used for visualization.

2. **Convert to Grayscale**

    ```matlab
    % Convert images to grayscale if they are RGB
    if ndims(I_tiff) == 3
        I_tiff = rgb2gray(I_tiff);
    end
    if ndims(I_png) == 3
        I_png = rgb2gray(I_png);
    end
    ```

    - `rgb2gray(I_tiff)`: Converts the TIFF image to grayscale if it is a color image.
    - `rgb2gray(I_png)`: Converts the PNG image to grayscale if it is a color image.

3. **Calibration**

    ```matlab
    % Calculate the calibration factor
    um_per_pixel = 3.00 / 512;  % 3.00 µm / 512 pixels
    fprintf('Calibration: %.5f µm/pixel\n', um_per_pixel);
    ```

    - The calibration factor is calculated as:

    ```math
    \text{µm per pixel} = \frac{3.00 \, \mu \text{m}}{512 \, \text{pixels}} = 0.00586 \, \mu \text{m/pixel}
    ```

### Calibration Calculation

The calibration factor converts pixel measurements to micrometers (µm).

4. **Hough Transform for Circle Detection**

    ```matlab
    % Detect circles in the PNG image
    [centers, radii] = imfindcircles(I_png, [8 50], 'Sensitivity', 0.9);
    ```

    - `imfindcircles(I_png, [8 50], 'Sensitivity', 0.9)`: Detects circular structures with radii between 8 and 50 pixels.

5. **Visualization**

    ```matlab
    % Display original and annotated images
    figure;
    imshow(I_png, []);
    viscircles(centers, radii, 'EdgeColor', 'g');
    ```

    - `imshow(I_png, [])`: Displays the original PNG image.
    - `viscircles(centers, radii, 'EdgeColor', 'g')`: Overlays detected circles with green edges.

### Circle Detection Visualization

The circles detected by the Hough Transform are visualized with green edges.

6. **Intensity Calculation**

    ```matlab
    % Calculate the average intensity within each circle in the TIFF image
    for i = 1:length(radii)
        mask = createCircularMask(size(I_tiff), centers(i,:), radii(i));
        circle_intensities = I_tiff(mask);
        intensity_values(i) = mean(circle_intensities) * 0.0140;
