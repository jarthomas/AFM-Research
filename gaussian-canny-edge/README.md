## Gradient Magnitude Canny Edge Detection Using MATLAB

The following MATLAB script reads an image, converts it to grayscale, computes the gradient magnitudes using Gaussian x & y derivatives, and applies Canny edge detection with different threshold levels.

![Example Output](exampleOutput.PNG)

### Summary

1. **Read an image and convert to grayscale and double precision**

```matlab
% Read an image
I = imread('Current_Backward_sample_2_leveled.png');
I = rgb2gray(I); % Convert to grayscale if it's a color image
I = double(I); % Convert to double precision
```

- `imread('Current_Backward_sample_2_leveled.png')`: Reads the image file.
- `rgb2gray(I)`: Converts the image to grayscale if it is a color image.
- `double(I)`: Converts the image to double precision for further processing.

2. **Define the standard deviation for Gaussian kernel**

```matlab
% Define the standard deviation for Gaussian kernel
sigma = 1;
```

`sigma = 1`: Sets the standard deviation for the Gaussian kernel.

3. **Create Gaussian derivative filters**

```matlab
% Create Gaussian derivative filters
G = fspecial('gaussian', [6*sigma, 6*sigma], sigma);
[Gx, Gy] = gradient(G);
```

- `fspecial('gaussian', [6*sigma, 6*sigma], sigma)`: Creates a Gaussian filter.
- `[Gx, Gy] = gradient(G)`: Computes the gradient of the Gaussian filter in the x and y directio
