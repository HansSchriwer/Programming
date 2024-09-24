#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# 3 methods of converting PDFs to Excels


# In[ ]:


# Using tabula-py


# In[ ]:


# Import library
get_ipython().system(' pip install tabula-py')


# In[ ]:


import tabula

# Read PDF file
pdf_path = "input.pdf"
df = tabula.read_pdf(pdf_path, pages='all')

# Convert PDF to Excel
output_path = "output.xlsx"
tabula.convert_into(pdf_path, output_path, output_format="xlsx", pages='all')

print("PDF converted to Excel successfully!")


# In[ ]:


""" For the tabula-py method:
You need to install tabula-py using pip install tabula-py
Make sure you have Java installed on your system
This method works well for PDFs with tabular data """


# In[ ]:

""" For the pdftables_api method:
You need to install the library using pip install git+https://github.com/pdftables/python-pdftables-api.git
You need to sign up for an API key at PDFTables.com
This method can handle a wider variety of PDF layouts """


# In[ ]:


# Using PDFTables_api


# In[ ]:


import pdftables_api

# Replace 'my-api-key' with your actual PDFTables API key
c = pdftables_api.Client('my-api-key')

# Convert PDF to Excel
input_pdf = "input.pdf"
output_excel = "output.xlsx"
c.xlsx(input_pdf, output_excel)

print("PDF converted to Excel successfully!")


# In[ ]:


# Using PDFLumber


# In[ ]:


# Import library
get_ipython().system(' pip install pdfplumber pandas openpyxl')


# In[ ]:


import pdfplumber
import pandas as pd
from pathlib import Path

def pdf_to_excel(pdf_path, excel_path):
    with pdfplumber.open(pdf_path) as pdf:
        data = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                data.extend(table)
    
    if data:
        df = pd.DataFrame(data[1:], columns=data[0])
        df.to_excel(excel_path, index=False)
        print(f"PDF converted to Excel: {excel_path}")
    else:
        print("No tables found in the PDF.")

# Usage
pdf_file = "input.pdf"
excel_file = "output.xlsx"
pdf_to_excel(pdf_file, excel_file)


# In[ ]:


""" This script does the following:
It imports the necessary libraries: pdfplumber for PDF extraction and pandas for handling data and Excel output.
The pdf_to_excel function takes two parameters: the path to the input PDF file and the desired path for the output Excel file.
It opens the PDF using pdfplumber and iterates through all pages.
For each page, it attempts to extract tables using the extract_table() method.
If tables are found, the data is collected in the data list.
After processing all pages, if data was found, it creates a pandas DataFrame from the extracted data.
The DataFrame is then saved as an Excel file using the to_excel() method.
If no tables are found, it prints a message indicating so. """


# In[ ]:


# Final comments


# In[ ]:


""" This method using pdfplumber has some advantages:
It can handle multiple pages and multiple tables within a PDF.
It doesn't require Java installation, unlike the tabula-py method.
It's a pure Python solution, which can be easier to set up and maintain. """

