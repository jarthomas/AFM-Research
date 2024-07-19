% Read the TIFF image
I = imread('Current_Backward.tiff');

% Display the image
figure;
imshow(I, []);
title('Draw a Line to Generate a Profile');

% Draw lines interactively using drawline
h = drawline;

addlistener(h, 'ROIClicked', @(src, evt) profileCallback(src, I));

function profileCallback(h, I)
    % Determine position of a line
    pos = h.Position;
    
    % Calculate the intensity profile along the line
    c = improfile(I, pos(:,1), pos(:,2));
    
    % Define the conversion factors
    % For this example, I assume the conversion factors are known:
    nA_conversion_factor = 1;  % Conversion factor to nA
    um_per_pixel = 0.5;  % Conversion factor to µm, for example, 1 pixel = 0.5 µm
    
    % Generate the distance vector for the x-axis in µm
    num_points = length(c);
    distance_um = (0:num_points-1) * um_per_pixel;
    
    % Plot the intensity profile in nA
    figure;
    plot(distance_um, c * nA_conversion_factor);
    title('Intensity Profile');
    xlabel('Distance (\mum)');
    ylabel('Intensity (nA)');
end
