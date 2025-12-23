import easyocr
import os
import pandas as pd
from dotenv import load_dotenv
from io import StringIO
from openai import OpenAI
from prompt import prompt

# Initialize environment variables and db path
load_dotenv()
API_KEY = os.getenv("OPENAI_APIKEY")
reader = easyocr.Reader(["en", "es"])


# Extract the text from the images through OCR technology
def extract_text(path):
    result = reader.readtext(path, detail=0)
    content = "\n".join(result)
    # print(content)
    return content


# Ask AI to structure the text
def structure_text(unstructured):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in invoice data extraction. Return only the CSV with no explanations or additional messages. If you cannot extract the data, return exactly the word 'error' without quotes",
            },
            {
                "role": "user",
                "content": prompt + "\n Here's the text to structure:\n" + unstructured,
            },
        ],
    )
    csv_invoice = response.choices[0].message.content.strip()

    if not csv_invoice or csv_invoice.lower() == "error":
        return None

    # print(csv_invoice)
    return csv_invoice


# Convert the csv to a pandas dataframe
def csv_to_df(structured):
    dtype_cols = {
        "invoice_date": str,
        "supplier": str,
        "description": str,
        "amount": str,
        "currency": str,
    }
    inv_df = pd.read_csv(StringIO(structured), delimiter=";", dtype=dtype_cols)
    inv_df["amount"] = pd.to_numeric(
        inv_df["amount"].str.replace(",", ".", regex=False), errors="coerce"
    )
    return inv_df
