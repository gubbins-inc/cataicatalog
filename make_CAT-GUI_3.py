# this version of the script will generate the CSV file based on the
# data in the data.csv files in each chapter folder. It will also
# append the units of measure to the keywords (read from CSV headers)
# it can handle 2 folder structures:

#root (folder)
#	chapter 1 (folder)
#		part 1 (folder)
#			part 1 (product and parts)
#		part 2 (folder)
#			part 2 (product and parts)
#		data.csv
#	chapter 2 (folder)
#		part 3 (folder)
#			part 3 (product and parts)
#		part 4 (folder)
#			part 4 (product and parts)
#		data.csv

# OR

#root (folder)
#	chapter 1 (folder)
#		part 1 (catia part)
#		part 2 (catia part)
#		part 3 (catia part)
#		data.csv
#	chapter 2 (folder)
#		part 4 (catia part)
#		part 5 (catia part)
#		part 6 (catia part)
#		data.csv

# none of the 'metadata' is hard coded in to the script, it is all read in from the data.csv file but must follow this format:

# row 1 - keyword names
# row 2 - data type
# row 3 - UOM to be appended to the keyword name in brackets
# row 4 - HEADER END
# rows 6 onwards - the data

#Clamp Name,	Holding Force,	Plunger Stroke,	Handle Opens,	Weight,	Spindle Supplied,	Flanged Washers Supplied,	Arm Opens
#string,	real,		real,		real,		real,	string,			string,				real
#None,		kg,		mm,		degrees,	Kg,	None,		        None,				degrees	
#HEADER END									
#GH-36202M,	91,		20.3,		,		0.113,	SA-064010,              N/A,                            
#SP-36202-MSS,	,		20.3,		,	        0.113,	SA-085010, 		N/A,


import os
import csv
import configparser
import PySimpleGUI as sg
import ccf2root
import ccplanning
import ccmback

# Read the settings from the INI file
config = configparser.ConfigParser()
config.read('catia_catalog_settings.ini')

# Define the layout for the GUI
sg.theme('Reddit')
layout = [
    [sg.Text('Root Directory', size=(20, 1), justification='right'), sg.Input(config.get('planning', 'root_dir'), key='root_dir', size=(80, 1)), sg.FolderBrowse()],
    [sg.Text('Associations File Path', size=(20, 1), justification='right'), sg.Input(config.get('planning', 'assoc_file'), key='assocs_file_path', size=(80, 1)), sg.FileBrowse(file_types=(('Text Files', '*.txt'),))],
    [sg.Text('Planning File Output Path', size=(20, 1), justification='right'), sg.Input(config.get('planning', 'output_file'), key='planning_file_path', size=(80, 1)), sg.FileSaveAs(file_types=(('JSON Files', '*.json'),))],
    [sg.Button('Save current paths'), sg.Button('Copy Files to Root'), sg.Button('Create Planning File'), sg.Button('Move Back')],  # Place the buttons on the same row
    [sg.Text('Base Directory', size=(20, 1), justification='right'), sg.Input(config.get('make_cat_csv', 'base_dir'), key='base_dir', size=(80, 1)), sg.FolderBrowse()],
    [sg.Text('CSV File Path', size=(20, 1), justification='right'), sg.Input(config.get('make_cat_csv', 'csv_file_path'), key='csv_file_path', size=(80, 1)), sg.FileSaveAs(file_types=(('CSV Files', '*.csv'),))],
    [sg.Button('Generate CSV for Catia batch Catalog'), sg.Button('Create Cat Script file')],
    [sg.Text('Cat Script File Path', size=(20, 1), justification='right'), sg.Input(config.get('catalog', 'script_filepath'), key='script_filepath', size=(80, 1)), sg.FileSaveAs(file_types=(('CATScript Files', '*.CATScript'),))],
    [sg.Text('Catalog Output Path', size=(20, 1), justification='right'), sg.Input(config.get('catalog', 'cat_path'), key='cat_path', size=(80, 1)), sg.FolderBrowse()],
    [sg.Text('Catalog Output Name', size=(20, 1), justification='right'), sg.Input(config.get('catalog', 'cat_name'), key='cat_name', size=(80, 1))],
]


# Create the window
window = sg.Window('Make CAT CSV', layout, size=(900, 400))

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Save current paths':
        # Update the settings in the INI file
        config.set('make_cat_csv', 'base_dir', values['base_dir'])
        config.set('make_cat_csv', 'csv_file_path', values['csv_file_path'])
        config.set('planning', 'root_dir', values['root_dir'])
        config.set('planning', 'assoc_file', values['assocs_file_path'])
        config.set('planning', 'output_file', values['planning_file_path'])
        config.set('catalog', 'script_filepath', values['script_filepath'])  # Update the script file path in the INI file
        config.set('catalog', 'cat_path', values['cat_path'])
        config.set('catalog', 'cat_name', values['cat_name'])  # Update the catalog output name in the INI file
        with open('catia_catalog_settings.ini', 'w') as configfile:
            config.write(configfile)
    elif event == 'Generate CSV for Catia batch Catalog':
        # Update the settings in the INI file
        config.set('make_cat_csv', 'base_dir', values['base_dir'])
        config.set('make_cat_csv', 'csv_file_path', values['csv_file_path'])
        #config.set('planning', 'root_dir', values['root_dir'])  # Update the root directory in the INI file
        with open('catia_catalog_settings.ini', 'w') as configfile:
            config.write(configfile)

        # Run the main script
        base_dir = values['base_dir']
        batch_catalog_file_path = values['csv_file_path']
        batch_catalog_data = []
        for folder in os.listdir(base_dir):
            folder_path = os.path.join(base_dir, folder)
            if os.path.isdir(folder_path):
                csv_file_path = os.path.join(folder_path, 'data.csv')
                if os.path.isfile(csv_file_path):
                    with open(csv_file_path, 'r') as csv_file:
                        csv_reader = csv.reader(csv_file)
                        csv_data = list(csv_reader)
                        batch_catalog_data.append({
                            'chapter': folder,
                            'keywords': csv_data[0],
                            'types': csv_data[1],
                            'units': csv_data[2],
                            'components': csv_data[4:]
                        })
        # Open the BatchCatalog.csv file
        with open(batch_catalog_file_path, 'w') as batch_catalog_file:
            # Write the top level chapter to the BatchCatalog.csv file
            batch_catalog_file.write('CHAPTER;Goodhand_Clamps\n')
            batch_catalog_file.write('Keywords;Name\n')
            batch_catalog_file.write('Types;String\n')
            for data in batch_catalog_data:
                batch_catalog_file.write(data['chapter'] + ';' + data['chapter'] + '\n')
            batch_catalog_file.write('END\n')

            # Loop over the data in the batch_catalog_data list
            for data in batch_catalog_data:
                # Write the data to the BatchCatalog.csv file
                batch_catalog_file.write('ENDCHAPTER;' + data['chapter'] + '\n')
                batch_catalog_file.write('Keywords;' + ';'.join([f"{keyword} ({unit})" if unit != 'None' else keyword for keyword, unit in zip(data['keywords'], data['units'])]) + '\n')
                batch_catalog_file.write('Types;' + ';'.join(data['types']) + '\n')
                
                # Loop over the components
                for component in data['components']:
                    # Initialize an empty list to store the validated values
                    validated_values = []
                    
                    # Loop over the values and their corresponding types
                    for value, type in zip(component, data['types']):
                        # Validate the value based on its type
                        if type == 'String':
                            validated_values.append(value)
                        elif type == 'Real':
                            try:
                                float(value)
                                validated_values.append(value)
                            except ValueError:
                                validated_values.append('')
                        else:
                            validated_values.append('')
                    catproduct_path = os.path.join(base_dir, data['chapter'], component[0], component[0] + '.CATProduct')
                    if not os.path.isfile(catproduct_path):
                        catproduct_path = os.path.join(base_dir, data['chapter'], component[0] + '.CATPart')
                    batch_catalog_file.write(component[0] + ';' + component[0] + ';' + ';'.join(validated_values) + ';' + catproduct_path + '\n')
                batch_catalog_file.write('END\n')
        sg.popup('CSV file has been generated successfully.')
    elif event == 'Copy Step Files to Root':  # Add a condition for the 'Copy Files to Root' button
        config.set('planning', 'root_dir', values['root_dir'])  # Update the root directory in the INI file
        with open('catia_catalog_settings.ini', 'w') as configfile:
            config.write(configfile)
        result_message = ccf2root.copy_files_to_root()  # Call the copy_files_to_root function from the ccf2root module
        sg.popup(result_message, auto_close=True, auto_close_duration=3)
    elif event == 'Create Planning File':
        result_message = ccplanning.plan_moves()  # Call the plan_moves function from the ccplanning module
        sg.popup(result_message, auto_close=True, auto_close_duration=3)
    elif event == 'Move Catia Files to Directories':
        result_message = ccmback.copy_planned_moves()  # Call the copy_planned_moves function from the ccmback module
        sg.popup(result_message, auto_close=True, auto_close_duration=3)
    elif event == 'Create Cat Script file':  # Add a condition for the 'Create Cat Script file' button
        # Get the paths from the values
        input_file = values['csv_file_path']
        output_file = os.path.join(values['cat_path'], values['cat_name'] + '.catalog')
        script_file_path = values['script_filepath']

        # Create the CATScript content
        cat_script_content = f"""Language="VBSCRIPT"

Sub CATMain()

InputFile="{input_file}"
OutputFile="{output_file}"

Dim Catalog As Document
set Catalog=CATIA.Documents.Add("CatalogDocument")

Catalog.CreateCatalogFromcsv InputFile, OutputFile

Catalog.Close

End Sub
"""

        # Write the CATScript content to the file
        with open(script_file_path, 'w') as f:
            f.write(cat_script_content)

        sg.popup('CATScript file has been created successfully.', auto_close=True, auto_close_duration=3)

window.close()



# this script reads the settings from the INI file, displays a GUI that allows
# the user to change the base directory and CSV file path, updates the settings
# in the INI file when the 'Generate' button is clicked, and generates the CSV
# file based on the data in the CSV files in the subdirectories of the base
# directory.

# The script also handles the two different folder structures. It checks if a
# CATProduct file exists for each component, and if not, it assumes that a
# CATPart file exists instead. The script also constructs the 'Keywords' line
# for each chapter based on the keywords and units of measure in the CSV file
# for the chapter, appending the unit of measure to the keyword if the unit of
# measure is not 'None'.

# Please note that this script assumes that the CSV files in the subdirectories
# of the base directory have a specific structure, with the keywords, types,
# and units of measure in the first three rows, a 'HEADER END' line in the
# fourth row, and the component data in the following rows. If the CSV files
# do not have this structure, the script may not work correctly.

