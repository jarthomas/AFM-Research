# Change Color Palette and Generate a 3D View

This Python script automates the process of iterating through data fields in all open containers within the Gwyddion data analysis software. The script modifies the color palette of each data field to "Red" and then displays a 3D view of the current container.

![Console Image](palette-3d-view.png)

### Summary
1. **Iterate Through All Open Containers**

 ```python
for container in gwy.gwy_app_data_browser_get_containers():
    for i in gwy.gwy_app_data_browser_get_data_ids(container):
 ```
2. **Select the Current Data Field**

 ```python
gwy.gwy_app_data_browser_select_data_field(container, i)
 ```

3. **Change the Color Palette of the Scale**
  ```python
Copy code
# Change the color of the scale 
container.set_string_by_name('/' + str(i) + '/base/palette', "Red")
  ```
4. **Display the 3D View of the Current Container**

  ```python
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
gwy.gwy_app_data_browser_show_3d(c, 0)
  ```
