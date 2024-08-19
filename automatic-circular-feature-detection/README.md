Circular Structures Analysis from TIFF and PNG Images
This project analyzes circular structures detected in PNG and TIFF images, calculates their intensities, and visualizes the most similar circles based on intensity measurements.

Project Overview
Input: TIFF image (tri_circ.tiff) for intensity calculations and PNG image (tri.png) for circle detection and representation.
Output: Circles detected in the image are highlighted, their mean intensity values are calculated, and a table and box plot of the intensity distributions are generated.
Key Steps
Image Loading:

Convert TIFF and PNG images to grayscale.
Calculate calibration factors for both axes.
Circle Detection:

Use the Hough Transform to detect circles in the PNG image.
Identify and label circles with numbers.
Intensity Calculation:

Calculate the mean intensity within each detected circle in the TIFF image.
Convert the intensity values to nanoamperes (nA).
Similarity Calculation:

Normalize the intensity values and compute pairwise Euclidean distances.
Identify the three circles with the smallest total pairwise distance.
Visualization:

Highlight the most similar circles in red and present the intensity distributions using box plots.
Key Equations
Calibration Factor Calculation
The calibration factor for converting pixel distances to micrometers is calculated as:

Calibration Factor
=
Physical Size in µm
Number of Pixels
Calibration Factor= 
Number of Pixels
Physical Size in µm
​
 
For a 512 px image with a 3.00 µm size:

um_per_pixel
=
3.00
 
µm
512
 
pixels
=
0.00586
 
µm/pixel
um_per_pixel= 
512pixels
3.00µm
​
 =0.00586µm/pixel
Intensity Conversion
The intensity values from the TIFF image are converted to nanoamperes (nA) using the calibration factor:

𝐼
nA
=
𝐼
intensity
×
nA_per_intensity
I 
nA
​
 =I 
intensity
​
 ×nA_per_intensity
Normalization
To normalize the intensity values, we use:

𝐼
norm
=
𝐼
−
min
⁡
(
𝐼
)
max
⁡
(
𝐼
)
−
min
⁡
(
𝐼
)
I 
norm
​
 = 
max(I)−min(I)
I−min(I)
​
 
where 
𝐼
I represents the intensity values.

Pairwise Euclidean Distance
The pairwise Euclidean distances between normalized intensity values are calculated as:

𝑑
(
𝑖
,
𝑗
)
=
(
𝐼
norm
,
𝑖
−
𝐼
norm
,
𝑗
)
2
d(i,j)= 
(I 
norm,i
​
 −I 
norm,j
​
 ) 
2
 
​
 
Similarity Calculation
The circles with the smallest total pairwise distance are identified as:

Total Distance
=
∑
𝑗
=
1
𝑛
𝑑
(
𝑖
,
𝑗
)
Total Distance= 
j=1
∑
n
​
 d(i,j)
Visualization
Detected Circles: Circles detected in the PNG image are highlighted in green.
Intensity Distribution: The box plot shows the distribution of intensity values within each detected circle.
