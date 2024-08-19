function afm_section_viewer_gui
    % Hardcoded TIFF file
    inputFile = 'Current_Backward_sample_2.tiff';
    
    % Output directory for sections
    outputDir = 'AFM_Sections';

    % Check if the hardcoded file exists
    if ~exist(inputFile, 'file')
        errordlg('The specified TIFF file does not exist.', 'Error');
        return;
    end

    % List all TIFF files in the directory
    tiffFiles = dir(fullfile(outputDir, '*.tiff'));
    numSections = length(tiffFiles);

    % Validate if there are TIFF files
    if numSections == 0
        errordlg('No TIFF files found in the specified directory.', 'Error');
        return;
    end

    % Initialize the section counter
    currentSection = 1;

    % Create the main GUI window
    fig = uifigure('Name', 'AFM Section Viewer', 'Position', [100, 100, 1200, 850]);

    % Create axes for displaying the colored TIFF image with heatmap
    tiffAx = uiaxes(fig, 'Position', [50, 450, 500, 350]);

    % Create table for displaying height distribution statistics
    heightDistTable = uitable(fig, 'Position', [650, 450, 500, 350]);

    % Create axes for displaying the 3D volumetric display
    volAx = uiaxes(fig, 'Position', [50, 50, 500, 300]);

    % Create axes for displaying the height distribution histogram
    histAx = uiaxes(fig, 'Position', [650, 50, 500, 300]);

    % Create a label to display the current section number
    sectionLabel = uilabel(fig, 'Position', [550, 800, 100, 30], ...
        'Text', sprintf('Section %d of %d', currentSection, numSections));

    % Create 'Previous' and 'Next' buttons to navigate sections
    prevButton = uibutton(fig, 'push', 'Position', [400, 800, 100, 30], ...
        'Text', 'Previous', 'ButtonPushedFcn', @(btn, event) navigateSection(-1));
    nextButton = uibutton(fig, 'push', 'Position', [700, 800, 100, 30], ...
        'Text', 'Next', 'ButtonPushedFcn', @(btn, event) navigateSection(1));

    % Create an 'Export to PDF' button
    exportButton = uibutton(fig, 'push', 'Position', [950, 800, 100, 30], ...
        'Text', 'Export to PDF', 'ButtonPushedFcn', @(btn, event) exportToPDF());

    % Disable the 'Previous' button initially
    if currentSection == 1
        prevButton.Enable = 'off';
    end

    % Initialize table headers and data for height distribution statistics
    columnNames = {'Mean Height (µm)', 'Std Dev (µm)', 'Min Height (µm)', 'Max Height (µm)'};
    heightDistData = zeros(numSections, length(columnNames));
    heightDistTable.Data = heightDistData;
    heightDistTable.ColumnName = columnNames;

    % Load and display the initial section
    loadAndDisplaySection(currentSection);

    % Function to navigate through sections
    function navigateSection(direction)
        % Update the current section
        currentSection = currentSection + direction;

        % Enable or disable buttons based on current section
        if currentSection <= 1
            currentSection = 1;
            prevButton.Enable = 'off';
        else
            prevButton.Enable = 'on';
        end

        if currentSection >= numSections
            currentSection = numSections;
            nextButton.Enable = 'off';
        else
            nextButton.Enable = 'on';
        end

        % Update the section label
        sectionLabel.Text = sprintf('Section %d of %d', currentSection, numSections);

        % Load and display the new section
        loadAndDisplaySection(currentSection);
    end

    % Function to load and display the current section and update height distribution statistics
    function loadAndDisplaySection(sectionNumber)
        % Get the current TIFF file name
        tiffFileName = fullfile(outputDir, tiffFiles(sectionNumber).name);

        % Load the TIFF image
        tiffImage = imread(tiffFileName);

        % Convert the image to grayscale if it’s RGB
        if size(tiffImage, 3) == 3
            tiffImage = rgb2gray(tiffImage);
        end

        % Define the physical size of the image (1.00 µm x 1.00 µm)
        physicalWidth = 1.00;  % µm
        physicalHeight = 1.00; % µm

        % Define the pixel size in µm/pixel for the 177x177 px size
        pixelSizeX = physicalWidth / 177;  % µm per pixel in x-direction
        pixelSizeY = physicalHeight / 177; % µm per pixel in y-direction

        % Create a spatial referencing object with world limits
        R = imref2d(size(tiffImage), [0 physicalWidth], [0 physicalHeight]);

        % Convert the pixel intensities to height data in micrometers (assuming pixel intensity represents height)
        heightData = double(tiffImage) / 1000;  % Convert from nm to µm

        % Calculate height distribution statistics in µm
        meanHeight = mean(heightData(:));    % Mean height in µm
        stdHeight = std(heightData(:));      % Standard deviation in µm
        minHeight = min(heightData(:));      % Minimum height in µm
        maxHeight = max(heightData(:));      % Maximum height in µm

        % Update the height distribution table with the new values
        heightDistData(sectionNumber, :) = [meanHeight, stdHeight, minHeight, maxHeight];
        heightDistTable.Data = heightDistData;

        % Apply a colormap to the TIFF image based on intensity (heatmap)
        coloredImage = ind2rgb(im2uint8(mat2gray(tiffImage)), jet(256));

        % Display the colored TIFF image with spatial referencing
        imshow(coloredImage, R, 'Parent', tiffAx);
        title(tiffAx, sprintf('Colored TIFF: %s', tiffFiles(sectionNumber).name), 'Interpreter', 'none');
        xlabel(tiffAx, 'X (µm)');
        ylabel(tiffAx, 'Y (µm)');

        % Create a grid for X and Y in µm, matching the real-world dimensions
        [X, Y] = meshgrid(linspace(0, physicalWidth, size(heightData, 2)), ...
                          linspace(0, physicalHeight, size(heightData, 1)));

        % Create a 3D volumetric display (surface plot) of the height data in µm
        surf(volAx, X, Y, heightData, 'EdgeColor', 'none');
        colormap(volAx, jet);  % Apply the same colormap to the surface
        colorbar(volAx);  % Add a colorbar to the plot
        view(volAx, 3);  % Set the view to 3D
        title(volAx, '3D Volumetric Display');
        xlabel(volAx, 'X (µm)');
        ylabel(volAx, 'Y (µm)');
        zlabel(volAx, 'Height (µm)');

        % Create a histogram of the height distribution in µm
        histogram(histAx, heightData(:), 'Normalization', 'probability');
        title(histAx, 'Height Distribution');
        xlabel(histAx, 'Height (µm)');
        ylabel(histAx, 'Probability');
    end

    % Function to export all elements of each section to a multi-page PDF
    function exportToPDF()
        % Specify the PDF file name
        pdfFileName = fullfile(outputDir, 'AFM_Sections_Export.pdf');

        % Iterate through all sections and export each one to a new page in the PDF
        for sectionNumber = 1:numSections
            % Load the current section
            loadAndDisplaySection(sectionNumber);

            % Create a temporary figure to combine elements for export
            tempFig = figure('Visible', 'off', 'Position', [100, 100, 1200, 850]);

            % Copy the elements into the temporary figure
            tiffCopy = copyobj(tiffAx, tempFig);
            set(tiffCopy, 'Position', [50, 450, 500, 350]);

            volCopy = copyobj(volAx, tempFig);
            set(volCopy, 'Position', [50, 50, 500, 300]);

            histCopy = copyobj(histAx, tempFig);
            set(histCopy, 'Position', [650, 50, 500, 300]);

            % Create a table in the temporary figure
            uitable('Data', heightDistTable.Data(sectionNumber, :), 'ColumnName', heightDistTable.ColumnName, ...
                    'Position', [650, 450, 500, 350]);

            % Export the temporary figure to the PDF, appending to it
            exportgraphics(tempFig, pdfFileName, 'Append', true);

            % Close the temporary figure
            close(tempFig);
        end

        % Notify the user
        uialert(fig, 'PDF exported successfully!', 'Export Complete');
    end
end
