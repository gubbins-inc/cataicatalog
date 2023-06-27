Attribute VB_Name = "Catia_Catalog"
Sub ExtractCATProductMetadata()
    Dim CATIA As Object
    Set CATIA = GetObject(, "CATIA.Application")
    
    ' Specify the directory containing the CATProduct files
    Dim DirectoryPath As String
    ' Change this path
    DirectoryPath = "C:\Users\xx\Desktop\clamps"
    ' Change this path
    ' Get a reference to the file system object
    Dim FileSystem As Object
    Set FileSystem = CreateObject("Scripting.FileSystemObject")
    
    ' Get a reference to the directory
    Dim Directory As Object
    Set Directory = FileSystem.GetFolder(DirectoryPath)
    
    ' Create a text file for output
    Dim OutputFile As Object
    ' Change this path
    Set OutputFile = FileSystem.CreateTextFile("C:\Users\xxx\Desktop\clamps\assocs\output.txt", True)
    ' Change this path
    ' Loop through each file in the directory
    Dim File As Object
    For Each File In Directory.Files
        ' Check if the file is a CATProduct file
        If FileSystem.GetExtensionName(File.Name) = "CATProduct" Then
            ' Open the CATProduct file
            CATIA.Documents.Open (File.Path)
            
            ' Get a reference to the active document (the CATProduct file)
            Dim Document As Document
            Set Document = CATIA.ActiveDocument
            
            ' Write the file path of the CATProduct to the output file
            OutputFile.WriteLine "Product: " & File.Path
            
            ' Get a reference to the product
            Dim Product As Product
            Set Product = Document.Product
            
            ' Loop through each product in the product
            Dim Products As Products
            Set Products = Product.Products
            Dim i As Integer
            For i = 1 To Products.Count
                ' Get a reference to the product
                Set Product = Products.Item(i)
                
                ' Get a reference to the part document
                Dim PartDocument As Document
                Set PartDocument = Product.ReferenceProduct.Parent
                
                ' Write the file path of the CATPart to the output file
                OutputFile.WriteLine "Part: " & PartDocument.FullName
            Next i
            
            ' Close the CATProduct file
            Document.Close
        End If
    Next File
    
    ' Close the output file
    OutputFile.Close
End Sub


