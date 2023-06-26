# if you have catproduct and cat part files
# all in the root of a folder mixed together
# and folders with the same file names somewhere
# within the same directory this script will
# use the 'assocs\output.txt' file to discover which
# cat parts are associated with which cat products
# and generate a planning JSON file detailing what files it thinks
# need moving in to which folders
# once json file exists you use the catia_catalogue_move_back.py
# script to actually do the move back
# the assocs\output.txt file is generated via a catia script that
# opens up each product and finds the associated parts and
# dumps the results in a text file - you wil want to change the
# location of this in the catia script to suit
# i would recommend doing all this part locally and then moving the
# whole lot on to the network once you have the catia parts / products
# etc all in the right structure, and have the "data.csv" files for each folder


import os
import json
import configparser

def plan_moves():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the INI file
    config.read('catia_catalog_settings.ini')

    # Get the paths from the INI file
    root_dir = config.get('planning', 'root_dir')
    assoc_file = config.get('planning', 'assoc_file')
    output_file = config.get('planning', 'output_file')

    # Check if the root directory exists
    if not os.path.isdir(root_dir):
        return f"The directory {root_dir} does not exist."

    # Check if the associations file exists
    if not os.path.isfile(assoc_file):
        return f"The associations file {assoc_file} does not exist."

    # Open the associations file
    with open(assoc_file, 'r') as f:
        lines = f.readlines()

    # Initialize an empty list to hold the parts for the current product
    parts = []

    # Initialize an empty list to hold the planned moves
    planned_moves = []

    # Loop through each line in the associations file
    for line in lines:
        # Strip the newline character from the end of the line
        line = line.strip()

        # If the line starts with 'Product', it's a product file
        if line.startswith('Product'):
            # If there are any parts in the list, find the matching folder or STEP file
            if parts:
                # Get the name of the product (without the file extension)
                product_name = os.path.splitext(os.path.basename(product))[0]

                # Initialize the move path as None
                move_path = None

                # Find a matching folder or STEP file in the root directory
                for dirpath, dirnames, filenames in os.walk(root_dir):
                    for dirname in dirnames:
                        if dirname.upper() == product_name.upper():
                            move_path = os.path.join(dirpath, dirname)
                            move_path = move_path.replace('/', '\\')
                    for filename in filenames:
                        if os.path.splitext(filename)[0].upper() == product_name.upper() and os.path.splitext(filename)[1].lower() in ['.step', '.stp']:
                            move_path = dirpath
                            move_path = move_path.replace('/', '\\')



                # Add the planned move to the list
                planned_moves.append({
                    'part_name': product_name,
                    'product_path': product,
                    'part_paths': parts,
                    'move_path': move_path
                })

            # Get the file path of the product
            product = line.split(': ')[1]

            # Clear the list of parts
            parts = []
        # If the line starts with 'Part', it's a part file
        elif line.startswith('Part'):
            # Get the file path of the part
            part = line.split(': ')[1]

            # Add the part to the list of parts
            parts.append(part)

    # Write the planned moves to the output file
    with open(output_file, 'w') as f:
        json.dump(planned_moves, f, indent=4)

    print("Planning completed.")
    return "Planning completed."

