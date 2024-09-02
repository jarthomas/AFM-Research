# Change Color Palette and Generate a 3D View

![Console Image](palette-3d-view.png)

This Python script automates the process of iterating through data fields in all open containers within the Gwyddion data analysis software. It modifies the color palette of each data field to "Red" and then displays a 3D view of the current container.

Summary
Iterate Through All Open Containers
   ```python
for container in gwy.gwy_app_data_browser_get_containers():
    for i in gwy.gwy_app_data_browser_get_data_ids(container):
gwy.gwy_app_data_browser_get_containers(): Retrieves all currently open containers in the Gwyddion data browser.
gwy.gwy_app_data_browser_get_data_ids(container): Retrieves the data field IDs for each container.
Select Each Data Field
'''
