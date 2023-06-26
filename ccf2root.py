# this script walks a directory structure and moves and step files it finds
# down to to the root. This is the first step in getting them in to a catia
# catalogue. The next step is to use the Batch Utility within Catia to bulk
# convert them in to cat parts and cat products. If this generates products
# you are going to have a load of proceduraly generated cat part names and
# you will not know which product they belong to. There is a catia script
# ExtractCATProductMetadata which will open up each product and find the
# associations, then create a text file. we use that in the next python script
# (catia_catalog_planning.py) to figure out where to put everything back
# the catia VB script is duplicated at the end for ref

import os
import shutil
import configparser

def copy_files_to_root():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the INI file
    config.read('catia_catalog_settings.ini')

    # Get the root directory from the INI file
    root_dir = config.get('planning', 'root_dir')

    # Check if the directory exists
    if os.path.isdir(root_dir):
        filesfound = False
        # Walk through the root directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                # Check if the file is a .step, .stp, .STEP, or .STP file
                if filename.lower().endswith(('.step', '.stp')):
                    filesfound = True
                    # Construct the source file path
                    src_file_path = os.path.join(dirpath, filename)
                    # Construct the destination file path
                    dest_file_path = os.path.join(root_dir, filename)
                    # Copy the file to the root directory
                    shutil.copy2(src_file_path, dest_file_path)

        if filesfound:
            print("Copying completed. Step files in child directories have been copied into root.")
            return("Copying completed. Step files in child directories have been copied into root.")
        else:
            print("No Step files in child directories found.")
            return("No Step files in child directories found.")
    else:
        print(f"The directory {root_dir} does not exist.")
        return(f"The directory {root_dir} does not exist.")



#Sub ExtractCATProductMetadata()
#    Dim CATIA As Object
#    Set CATIA = GetObject(, "CATIA.Application")
#    
#    ' Specify the directory containing the CATProduct files
#    Dim DirectoryPath As String
########## change this directory #############################
#    DirectoryPath = "C:\Users\gcs\Desktop\clamps"
########## change this directory #############################
#    
#    ' Get a reference to the file system object
#    Dim FileSystem As Object
#    Set FileSystem = CreateObject("Scripting.FileSystemObject")
#    
#    ' Get a reference to the directory
#    Dim Directory As Object
#    Set Directory = FileSystem.GetFolder(DirectoryPath)
#    
#    ' Create a text file for output
#    Dim OutputFile As Object
########## change this directory #############################
#    Set OutputFile = FileSystem.CreateTextFile("C:\Users\gcs\Desktop\clamps\assocs\output.txt", True)
########## change this directory #############################

#   ' Loop through each file in the directory
#    Dim File As Object
#    For Each File In Directory.Files
#        ' Check if the file is a CATProduct file
#        If FileSystem.GetExtensionName(File.Name) = "CATProduct" Then
#            ' Open the CATProduct file
#            CATIA.Documents.Open (File.Path)
#            
#            ' Get a reference to the active document (the CATProduct file)
#            Dim Document As Document
#            Set Document = CATIA.ActiveDocument
#            
#            ' Write the file path of the CATProduct to the output file
#            OutputFile.WriteLine "Product: " & File.Path
#            
#            ' Get a reference to the product
#            Dim Product As Product
#            Set Product = Document.Product
#            
#            ' Loop through each product in the product
#            Dim Products As Products
#            Set Products = Product.Products
#            Dim i As Integer
#            For i = 1 To Products.Count
#                ' Get a reference to the product
#                Set Product = Products.Item(i)
#                
#                ' Get a reference to the part document
#                Dim PartDocument As Document
#                Set PartDocument = Product.ReferenceProduct.Parent
#                
#                ' Write the file path of the CATPart to the output file
#                OutputFile.WriteLine "Part: " & PartDocument.FullName
#            Next i
#            
#            ' Close the CATProduct file
#            Document.Close
#        End If
#    Next File
#    
#    ' Close the output file
#    OutputFile.Close
#End Sub
