# Circular Feature Extraction and Intensity Calculation

This repository contains MATLAB code for extracting circular features and calculating their intensities from a given image. The key mathematical concepts and equations used in the code are detailed below.

## Key Equations and Concepts

### 1. Calibration Factor for X and Y Axes
The calibration factor is calculated as follows:

$$
	ext{um\_per\_pixel} = rac{3.00 \, \mu m}{512 \, 	ext{pixels}} = 0.00585 \, \mu m/	ext{pixel}
$$

This equation determines the physical size of each pixel in the image.

### 2. Intensity Calibration Factor
The conversion factor from pixel intensity values to current values in nanoamperes (nA) is given by:

$$
	ext{nA\_per\_intensity} = 0.0140
$$

### 3. Hough Transform for Circle Detection
The Hough Transform is used to detect circular structures:

$$
egin{align*}
[	ext{centers}, 	ext{radii}] &= 	ext{imfindcircles}(I_{	ext{png}}, [8, 50], 	ext{'Sensitivity'}, 0.9)
\end{align*}
$$

### 4. Mean Intensity Calculation within Detected Circles
For each detected circle, the mean intensity is calculated as follows:

$$
egin{align*}
	ext{circle\_intensities} &= I_{	ext{tiff}}(	ext{mask}) \
	ext{circle\_intensities\_nA} &= 	ext{circle\_intensities} 	imes 	ext{nA\_per\_intensity} \
	ext{intensity\_values}(i) &= 	ext{mean}(	ext{circle\_intensities\_nA})
\end{align*}
$$

### 5. Intensity Normalization
The intensity values are normalized to the range [0, 1]:

$$
	ext{intensity\_values\_norm} = 	ext{normalize}(	ext{intensity\_values})
$$

### 6. Pairwise Euclidean Distance Calculation
The pairwise Euclidean distances are calculated using:

$$
egin{align*}
	ext{features} &= 	ext{intensity\_values\_norm} \
	ext{distances} &= 	ext{pdist}(	ext{features}) \
	ext{dist\_matrix} &= 	ext{squareform}(	ext{distances})
\end{align*}
$$

### 7. Identification of the Most Similar Circles
The most similar circles are identified by:

$$
egin{align*}
	ext{total\_distances} &= \sum(	ext{dist\_matrix}) \
[\sim, 	ext{most\_similar\_idx}] &= 	ext{mink}(	ext{total\_distances}, 3)
\end{align*}
$$

