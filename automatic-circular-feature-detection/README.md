\section*{Circular Structures Analysis Using MATLAB}

The following MATLAB script processes a TIFF image to calculate intensities within detected circular structures, while a PNG image is used for visual representation. The script performs circle detection, intensity calculation, and visualization.

\includegraphics{circ_example_output.PNG}

\subsection*{Summary}

\begin{enumerate}
    \item \textbf{Load Images}
    
    \begin{verbatim}
    % Load the TIFF and PNG images
    I_tiff = imread('tri_circ.tiff');
    I_png = imread('tri.png');
    \end{verbatim}
    
    \begin{itemize}
        \item \texttt{imread('tri\_circ.tiff')}: Reads the TIFF image used for intensity calculation.
        \item \texttt{imread('tri.png')}: Reads the PNG image used for visualization.
    \end{itemize}
    
    \item \textbf{Convert to Grayscale}
    
    \begin{verbatim}
    % Convert images to grayscale if they are RGB
    if ndims(I_tiff) == 3
        I_tiff = rgb2gray(I_tiff);
    end
    if ndims(I_png) == 3
        I_png = rgb2gray(I_png);
    end
    \end{verbatim}
    
    \begin{itemize}
        \item \texttt{rgb2gray(I\_tiff)}: Converts the TIFF image to grayscale if it is a color image.
        \item \texttt{rgb2gray(I\_png)}: Converts the PNG image to grayscale if it is a color image.
    \end{itemize}
    
    \item \textbf{Calibration}
    
    \begin{verbatim}
    % Calculate the calibration factor
    um_per_pixel = 3.00 / 512;  % 3.00 µm / 512 pixels
    fprintf('Calibration: %.5f µm/pixel\n', um_per_pixel);
    \end{verbatim}
    
    The calibration factor is calculated as:
    
    \[
    \text{µm per pixel} = \frac{3.00 \, \mu \text{m}}{512 \, \text{pixels}} = 0.00586 \, \mu \text{m/pixel}
    \]
    
    \item \textbf{Hough Transform for Circle Detection}
    
    \begin{verbatim}
    % Detect circles in the PNG image
    [centers, radii] = imfindcircles(I_png, [8 50], 'Sensitivity', 0.9);
    \end{verbatim}
    
    \begin{itemize}
        \item \texttt{imfindcircles(I\_png, [8 50], 'Sensitivity', 0.9)}: Detects circular structures with radii between 8 and 50 pixels.
    \end{itemize}
    
    \item \textbf{Visualization}
    
    \begin{verbatim}
    % Display original and annotated images
    figure;
    imshow(I_png, []);
    viscircles(centers, radii, 'EdgeColor', 'g');
    \end{verbatim}
    
    \begin{itemize}
        \item \texttt{imshow(I\_png, [])}: Displays the original PNG image.
        \item \texttt{viscircles(centers, radii, 'EdgeColor', 'g')}: Overlays detected circles with green edges.
    \end{itemize}
    
    \item \textbf{Intensity Calculation}
    
    \begin{verbatim}
    % Calculate the average intensity within each circle in the TIFF image
    for i = 1:length(radii)
        mask = createCircularMask(size(I_tiff), centers(i,:), radii(i));
        circle_intensities = I_tiff(mask);
        intensity_values(i) = mean(circle_intensities) * 0.0140;
    end
    \end{verbatim}
    
    The intensity in nanoamperes (nA) is calculated by multiplying pixel intensity by a calibration factor:
    
    \[
    \text{Intensity (nA)} = \text{Pixel Intensity} \times 0.0140
    \]
    
    \item \textbf{Display Most Similar Circles}
    
    \begin{verbatim}
    % Highlight the three most similar circles
    distances = pdist(normalize(intensity_values));
    dist_matrix = squareform(distances);
    [~, most_similar_idx] = mink(sum(dist_matrix), 3);
    viscircles(centers(most_similar_idx, :), radii(most_similar_idx), 'EdgeColor', 'r');
    \end{verbatim}
    
    The pairwise distance between normalized intensity values is calculated as:
    
    \[
    \text{Distance} = \sqrt{(I_i - I_j)^2}
    \]
    
    where \( I_i \) and \( I_j \) are the normalized intensities of circles \( i \) and \( j \).
    
    \item \textbf{Plot Intensity Distribution}
    
    \begin{verbatim}
    % Plot box plots of intensity distributions
    boxplot(all_intensities, group, 'Labels', arrayfun(@num2str, 1:numCircles, 'UniformOutput', false));
    \end{verbatim}
    
    \begin{itemize}
        \item \texttt{boxplot}: Displays the intensity distribution within detected circles.
    \end{itemize}
    
    \item \textbf{Output Circle Data}
    
    \begin{verbatim}
    % Display circle data in a table
    circle_table = cell2table(circle_data, 'VariableNames', {'Circle Index', 'X Coordinate', 'Y Coordinate', 'Mean Intensity (nA)'});
    disp(circle_table);
    \end{verbatim}
\end{enumerate}

