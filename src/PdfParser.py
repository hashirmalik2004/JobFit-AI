#this file handles PDF parsing and text extraction using PyMuPDF

import fitz  

def ExtractText(PdfPath):
    AllText = ""  

    try:
        Doc = fitz.open(PdfPath)

        TotalPages = len(Doc)
        print(f"opened PDF successfully  it has {TotalPages} pages")

        for PageNum in range(TotalPages):
            Page = Doc[PageNum] 
            PageText = Page.get_text("text", sort=True)

            AllText = AllText + PageText + "\n"

        Doc.close()
        print("PDF text extraction has been completed")

    except FileNotFoundError:
        print(f"ERROR: could not find the PDF file at: {PdfPath}")
        return ""

    except Exception as e:
        print(f"ERROR: something went wrong while reading the PDF: {e}")
        return ""

    return AllText


def ExtractTextFromBytes(PdfBytes):
    """
    same thing as ExtractText but takes raw bytes instead of a file path
    this is used when someone uploads a pdf through streamlit
    because streamlit gives us the file as bytes not a path
    """

    AllText = "" 

    try:
        Doc = fitz.open(stream=PdfBytes, filetype="pdf")

        TotalPages = len(Doc)
        print(f"opened uploaded PDF , it has {TotalPages} pages")

        for PageNum in range(TotalPages):
            Page = Doc[PageNum]
            
            PageText = Page.get_text("text", sort=True)
            AllText = AllText + PageText + "\n"

        Doc.close()
        print("uploaded PDF text extraction complete")

    except Exception as e:
        print(f"ERROR: couldnt read the uploaded pdf: {e}")
        return ""
    return AllText