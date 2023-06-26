# cataicatalog

take step files in organised folders, move them to root, use catia to convert to parts and products, return the catia file to directories, plan and execute move, create csv file for catia batch catalog generation

write your own script that organises files & folders in to one of 2 formats:

    root (folder)
  
  	  chapter 1 (folder)
   
  		  part 1 (folder)
    
  			  part 1 (product and parts)
     
  		  part 2 (folder)
    
  			  part 2 (product and parts)
     
  		  data.csv
    
  	  chapter 2 (folder)
   
  		  part 3 (folder)
    
  			  part 3 (product and parts)
     
  		  part 4 (folder)
    
  			  part 4 (product and parts)
     
  		  data.csv
  
   OR
  
    root (folder)
  
  	  chapter 1 (folder)
   
  		  part 1 (catia part)
    
  		  part 2 (catia part)
    
  		  part 3 (catia part)
    
  		  data.csv
    
  	  chapter 2 (folder)
   
  		  part 4 (catia part)
    
  		  part 5 (catia part)
    
  		  part 6 (catia part)
    
  		  data.csv

 none of the 'metadata' is hard coded in to the script, it is all read in from the data.csv file but must follow this format:

 row 1 - keyword names
 
 row 2 - data type
 
 row 3 - UOM to be appended to the keyword name in brackets
 
 row 4 - HEADER END
 
 rows 6 onwards - the data
 

      Clamp Name,	Holding Force,	Plunger Stroke,	Handle Opens,	Weight,	Spindle Supplied,	Flanged Washers Supplied,	Arm Opens
      string,	real,		real,		real,		real,	string,			string,				real
      None,		kg,		mm,		degrees,	Kg,	None,		        None,				degrees	
      HEADER END									
      GH-36202M,	91,		20.3,		,		0.113,	SA-064010,              N/A,                            
      SP-36202-MSS,	,		20.3,		,	        0.113,	SA-085010, 		N/A,

step 2: use the make_CAT-GUI_3 script (copy Step Files to Root) to make copies of all step files in the root

step 3: use catia batch utilities to turn step files in to products and or parts

step 4: use catia script (ExtractCATProductMetadata) to create an output file which documents which catparts belong to which catproducts (because the parts all get generic names)

step 5: use the make_CAT-GUI_3 script (Create PLanning File) to generate a planning file of where to copy-paste all the catia parts and products

step 6: check this looks right

step 7: use the make_CAT-GUI_3 script (Move Catia Files to Directories) to do the move

step 8: manually clean up the root of folder (delete stuff that has been moved or used)

step 9: move your work to where it is going to live (network)

step 10: point "Base Directory" in the make_CAT-GUI_3 script at this place

step 11: point "CSV File Path in the make_CAT-GUI_3 script ato where you want the catia batch CSV file to go

step 12: Geenrate the CSV file

step 13: Use Catia to batch generate a new cataloge by running the script (coming soon) that triggers to batch action.
