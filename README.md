## MATLAB Script for Gradient Magnitude and Canny Edge Detection

The following MATLAB script reads an image, converts it to grayscale, computes the gradient magnitudes using Gaussian derivatives, and applies Canny edge detection with different threshold levels.

```matlab
% Read an image
I = imread('Current_Backward_sample_2_leveled.png');
I = rgb2gray(I); % Convert to grayscale if it's a color image
I = double(I); % Convert to double precision

% Define the standard deviation for Gaussian kernel
sigma = 2;

% Create Gaussian derivative filters
G = fspecial('gaussian', [6*sigma, 6*sigma], sigma);
[Gx, Gy] = gradient(G);

% Apply the filters to the image
Ix = imfilter(I, Gx, 'conv', 'replicate');
Iy = imfilter(I, Gy, 'conv', 'replicate');

% Compute the gradient magnitude
Gmag = sqrt(Ix.^2 + Iy.^2);

% Display the results
figure;
subplot(1,3,1);
imshow(Ix, []);
title('Gradient in X direction');

subplot(1,3,2);
imshow(Iy, []);
title('Gradient in Y direction');

subplot(1,3,3);
imshow(Gmag, []);
title('Gradient Magnitude');
```

### Explanation

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
sigma = 2;
```

- `sigma = 2`: Sets the standard deviation for the Gaussian kernel.

3. **Create Gaussian derivative filters**

```matlab
% Create Gaussian derivative filters
G = fspecial('gaussian', [6*sigma, 6*sigma], sigma);
[Gx, Gy] = gradient(G);
```

- `fspecial('gaussian', [6*sigma, 6*sigma], sigma)`: Creates a Gaussian filter.
- `[Gx, Gy] = gradient(G)`: Computes the gradient of the Gaussian filter in the x and y directions.

4. **Apply the filters to the image and compute the gradient magnitude**

```matlab
% Apply the filters to the image
Ix = imfilter(I, Gx, 'conv', 'replicate');
Iy = imfilter(I, Gy, 'conv', 'replicate');

% Compute the gradient magnitude
Gmag = sqrt(Ix.^2 + Iy.^2);
```

- `imfilter(I, Gx, 'conv', 'replicate')`: Applies the Gaussian derivative filter in the x direction to the image.
- `imfilter(I, Gy, 'conv', 'replicate')`: Applies the Gaussian derivative filter in the y direction to the image.
- `sqrt(Ix.^2 + Iy.^2)`: Computes the gradient magnitude by combining the gradients in the x and y directions.

5. **Display the results**

```matlab
% Display the results
figure;
subplot(1,3,1);
imshow(Ix, []);
title('Gradient in X direction');

subplot(1,3,2);
imshow(Iy, []);
title('Gradient in Y direction');

subplot(1,3,3);
imshow(Gmag, []);
title('Gradient Magnitude');
```

- `figure`: Creates a new figure window.
- `subplot(1,3,1)`: Divides the figure into a 1x3 grid and selects the first subplot.
- `imshow(Ix, [])`: Displays the gradient in the x direction.
- `title('Gradient in X direction')`: Sets the title for the first subplot.
- `subplot(1,3,2)`: Selects the second subplot.
- `imshow(Iy, [])`: Displays the gradient in the y direction.
- `title('Gradient in Y direction')`: Sets the title for the second subplot.
- `subplot(1,3,3)`: Selects the third subplot.
- `imshow(Gmag, [])`: Displays the gradient magnitude.
- `title('Gradient Magnitude')`: Sets the title for the third subplot.
