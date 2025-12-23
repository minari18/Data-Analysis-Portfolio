# AInvoices
AInvoices is a comprehensive Data Analytics project. It addresses the following scenario:

*"Your manager has requested a summary of expenses for the current year based on receipts, which are scanned and stored as JPG images. You need to integrate this data into the company database and ultimately present a Power BI dashboard."*

The analyst quickly realizes that the volume of receipts is substantial, so they decide to automate the process using a Python script leveraging Optical Character Recognition (OCR) technology. However, another challenge arises: the receipts are in different formats, making it difficult to apply a standardized method for structuring the information. To overcome this, the analyst incorporates Artificial Intelligence into the workflow: using the OpenAI API and a carefully crafted prompt, they structure the text extracted via OCR.

This is the inspiration behind the project name AInvoices: a practical demonstration of how AI combined with process automation can significantly enhance business productivity.

Special thanks to Isaac González from the DataScience ForBusiness YouTube channel, whose project FacturIA inspired the creation of AInvoices.

## Step-by-Step Overview

1. Dataset acquisition

The dataset High-Quality Invoice Images for OCR by Osama Hosam Abdellatif and 2 collaborators was downloaded from Kaggle. Source: https://www.kaggle.com/datasets/osamahosamabdellatif/high-quality-invoice-images-for-ocr?resource=download 

2. Image selection

Three images from each of the three batches (Batch1, Batch2, Batch3) were selected, each batch containing receipts of a different style. These were stored in the invoices folder. Only three images per batch were used to reduce processing time for the initial tests.

3. Python pipeline development

The Python code was implemented with all core components:
- main.py contains the main pipeline: data extraction from images with easyocr, text structuring via OpenAI, data cleaning and error handling using pandas, and finally insertion into an SQLite database.
- Operational functions (extract_text, structure_text, csv_to_df) are located in helpers.py.
- The prompt used for AI structuring is stored in the prompt variable in prompt.py.
- Environment configuration (.env) and dependencies (requirements.txt) are also included.

4. Power BI integration

A new SQLite3 data source was created via ODBC, connecting to invoices.db. In Power BI, the source is set as an ODBC connection to AInvoices, and the invoices table is loaded into the Power BI model.

Before building the report, data was transformed to optimize reporting and improve accessibility. Column data types were adjusted for accuracy, and supplier names were standardized to capitalized format.

5. Visualization and dashboard design

Once cleaned, visualizations were chosen to provide analytical insights:
- Card visual for total expenses
- Table showing the top 5 most expensive purchases (DAX measure using RANKX)
- Pie chart showing the distribution of total expenses by supplier
- Full table displaying all fields for a complete perspective
