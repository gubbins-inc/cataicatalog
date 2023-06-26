# this file uses the JSON file to copy parts from the root
# directory in to the folders that are in the same root directory
# and have the same name. You can manually delete the catia files
# in the root after - we do it this way because sometimes products
# share parts so only works to copy paste, not cut paste, otherwise
# the cut paste might fail when the shared file has already been cut


import os
import json
import shutil
import configparser

def copy_planned_moves():
    # Load the INI file
    config = configparser.ConfigParser()
    config.read('catia_catalog_settings.ini')

    # Get the planned moves file from the INI file
    planned_moves_file = config.get('planning', 'output_file')

    # Open the planned moves file
    with open(planned_moves_file, 'r') as f:
        planned_moves = json.load(f)

    # Loop through each planned move
    for planned_move in planned_moves:
        # Get the product path, part paths, and move path
        product_path = planned_move['product_path']
        part_paths = planned_move['part_paths']
        move_path = planned_move['move_path']

        # Check if product path, part paths, and move path exist
        if not os.path.isfile(product_path) or not all(os.path.isfile(part_path) for part_path in part_paths) or not os.path.isdir(move_path):
            print(f"Skipping move - Invalid file or path: {planned_move}")
            continue

        # Copy the product file
        shutil.copy(product_path, move_path)

        # Loop through each part path
        for part_path in part_paths:
            # Copy the part file
            shutil.copy(part_path, move_path)

    print("Moving completed.")

    return "Moving completed."


