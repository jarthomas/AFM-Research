% Step 1: Load the TIFF image for intensity calculation
I_tiff = imread('tri_circ.tiff');

% Step 2: Load the PNG image for representation, TIFF output is too pixelated
I_png = imread('tri.png');

% Step 3: Convert both files to grayscale
if ndims(I_tiff) == 3
    I_tiff = rgb2gray(I_tiff);
end
if ndims(I_png) == 3
    I_png = rgb2gray(I_png);
end

% Step 4: Calculate the calibration factors for X and Y axes
% Given that the TIFF image is 512px x 512px and the physical size is 3.00 µm x 3.00 µm - I confirmed these values in Gwyddion.
um_per_pixel = 3.00 / 512;  % 3.00 µm / 512 pixels
fprintf('Calibration: %.5f µm/pixel\n', um_per_pixel);

% Intensity calibration factor - This is an experimental value, needs work...
nA_per_intensity = 0.0140; 

% Step 5: Hough Transform in the PNG image - 8 55 for the pixel range seems to work the best
[centers, radii] = imfindcircles(I_png, [8 50], 'Sensitivity', 0.9);

% Step 6: Create figures - ready
figure('Name', 'Circular Structures Analysis', 'NumberTitle', 'off', 'WindowState', 'maximized');
% Formatting so all 3 images are presented.
t = tiledlayout(2, 3, 'Padding', 'loose', 'TileSpacing', 'loose');

% Step 7: Display the original PNG image
nexttile;
imshow(I_png, []);
title('Original PNG Image');

% Step 8: Display the original PNG image with all detected circles in green and black numbers
nexttile;
imshow(I_png, []);
title('Detected Circular Structures in PNG');
hold on;
viscircles(centers, radii, 'EdgeColor', 'g');  % Green circles
for i = 1:length(radii)
    text(centers(i,1), centers(i,2), num2str(i), 'Color', 'black', ...
        'FontSize', 12, 'FontWeight', 'bold');
end
hold off;

% Step 9: Display the image with the most similar circles highlighted
numCircles = length(radii);
circle_data = cell(numCircles, 4);  % Store Circle Index, X, Y, Mean Intensity
intensity_values = zeros(numCircles, 1);  % To store mean intensity values
all_intensities = [];  % To store all pixel intensities for box plot
group = [];  % Group labels for the box plot

% Step 10: Calculate the average intensity within each detected circle in the TIFF image
for i = 1:numCircles
    % Create a mask for the circle on the TIFF image
    mask = createCircularMask(size(I_tiff), centers(i,:), radii(i));
    
    % Extract all intensity values within the circle
    circle_intensities = I_tiff(mask);  % Extract pixel intensities in the circle
    circle_intensities_nA = circle_intensities * nA_per_intensity;  % Convert to nA
    
    % Calculate the mean intensity within the circle
    intensity_values(i) = mean(circle_intensities_nA);
    
    % Store the intensities for the box plot
    all_intensities = [all_intensities; circle_intensities_nA];  % Concatenate intensity values
    group = [group; repmat(i, length(circle_intensities_nA), 1)];  % Group labels
    
    % Save the circle data in a cell array
    circle_data{i, 1} = i;  % Circle Index
    circle_data{i, 2} = centers(i, 1);  % X coordinate
    circle_data{i, 3} = centers(i, 2);  % Y coordinate
    circle_data{i, 4} = intensity_values(i);  % Mean Intensity in nA
    
    % Display each circle's mean intensity
    fprintf('Circle %d: Mean Intensity = %.2f nA\n', i, intensity_values(i));
end

% Step 11: Normalize the intensity data
intensity_values_norm = normalize(intensity_values);

% Step 12: Calculate pairwise Euclidean distances
features = intensity_values_norm;
distances = pdist(features);

% Step 13: Find the three circles that are most similar (smallest distances)
% Convert distances to a square matrix form
dist_matrix = squareform(distances);

% Identify the three circles with the smallest total pairwise distance
total_distances = sum(dist_matrix);
[~, most_similar_idx] = mink(total_distances, 3);

% Step 14: Display the image with the most similar circles highlighted in red with black numbers
nexttile;
imshow(I_png, []);
title('Most Similar Detected Circles');
hold on;
viscircles(centers(most_similar_idx, :), radii(most_similar_idx), 'EdgeColor', 'r');  % Red circles
for i = 1:length(most_similar_idx)
    text(centers(most_similar_idx(i), 1), centers(most_similar_idx(i), 2), ...
        num2str(most_similar_idx(i)), 'Color', 'black', 'FontSize', 12, 'FontWeight', 'bold');  % Black text
end
hold off;

% Step 15: Plot the box plots of intensity distributions for each circle in a separate figure
figure('Name', 'Intensity Distribution Boxplot', 'NumberTitle', 'off');
boxplot(all_intensities, group, 'Labels', arrayfun(@num2str, 1:numCircles, 'UniformOutput', false));
title('Intensity Distribution within Detected Circles (TIFF Data)');
xlabel('Circle Index');
ylabel('Intensity (nA)');

% Step 16: Display the circle data in a table
circle_table = cell2table(circle_data, 'VariableNames', {'Circle Index', 'X Coordinate', 'Y Coordinate', 'Mean Intensity (nA)'});
disp(circle_table);

% Function to create a circular mask
function mask = createCircularMask(imageSize, center, radius)
    [X, Y] = meshgrid(1:imageSize(2), 1:imageSize(1));
    mask = (X - center(1)).^2 + (Y - center(2)).^2 <= radius^2;
end
