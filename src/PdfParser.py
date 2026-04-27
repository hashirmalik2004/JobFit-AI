# PdfParser.py
# this file handles PDF parsing and text extraction using PyMuPDF (fitz)

import fitz  # PyMuPDF library used to read and extract text from PDF files

def ExtractText(PdfPath):
    AllText = ""  # this will store all text from the entire PDF

    try:
        # open the PDF file using its file path
        Doc = fitz.open(PdfPath)

        # get total number of pages in the PDF
        TotalPages = len(Doc)
        print(f"opened PDF successfully , it has {TotalPages} pages")

        # loop through each page one by one
        for PageNum in range(TotalPages):
            Page = Doc[PageNum]  # access current page

            # extract text from the page
            # "text" → plain text extraction
            # sort=True → ensures text is read in a logical order (important for multi-column PDFs)
            PageText = Page.get_text("text", sort=True)

            # append page text to the full document text
            AllText = AllText + PageText + "\n"

        # close the PDF file to free memory
        Doc.close()
        print("PDF text extraction has been completed")

    # handle case where file path is wrong or file doesn't exist
    except FileNotFoundError:
        print(f"ERROR: could not find the PDF file at: {PdfPath}")
        return ""

    # handle any other unexpected errors
    except Exception as e:
        print(f"ERROR: something went wrong while reading the PDF: {e}")
        return ""

    # return the full extracted text
    return AllText


def ExtractTextFromBytes(PdfBytes):
    """
    same thing as ExtractText but takes raw bytes instead of a file path
    this is used when someone uploads a PDF through streamlit
    because streamlit gives us the file as bytes not a path
    """

    AllText = ""  # stores all extracted text

    try:
        # open PDF using raw bytes instead of file path
        # stream=PdfBytes → tells fitz we are passing file data directly
        # filetype="pdf" → explicitly specify file type
        Doc = fitz.open(stream=PdfBytes, filetype="pdf")

        # get number of pages
        TotalPages = len(Doc)
        print(f"opened uploaded PDF , it has {TotalPages} pages")

        # loop through all pages
        for PageNum in range(TotalPages):
            Page = Doc[PageNum]  # access current page
            
            # extract text in readable order
            PageText = Page.get_text("text", sort=True)

            # append to full text
            AllText = AllText + PageText + "\n"

        # close document
        Doc.close()
        print("uploaded PDF text extraction complete")

    # handle errors (corrupt file, wrong format, etc.)
    except Exception as e:
        print(f"ERROR: couldnt read the uploaded PDF: {e}")
        return ""

    # return extracted text
    return AllText