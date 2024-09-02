for container in gwy.gwy_app_data_browser_get_containers():
	for i in gwy.gwy_app_data_browser_get_data_ids(container):
	
		# Makes this channel current in the data browser
		gwy.gwy_app_data_browser_select_data_field(container, i)
	
		# Change the color of the scale 
		container.set_string_by_name('/' + str(i) + '/base/palette', "Red")
		
c = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
gwy.gwy_app_data_browser_show_3d(c, 0)
