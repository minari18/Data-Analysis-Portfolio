import helpers
import pandas as pd
import os
import sqlite3

# Euros to USD exchange rate (as of 21/12/2025)
EUR_TO_USD = 1.17

# Initial empty dataframe
df = pd.DataFrame()
temp_df = []  # Temporaly contains invoice data
DB_PATH = "invoices.db"

# Iterate through all directories inside "invoices"
for directory in sorted(os.listdir("./invoices")):
    dir_path = os.path.join("./invoices", directory)

    if not os.path.isdir(dir_path):
        continue

    # Iterate through all files inside every directory
    for invoice in os.listdir(dir_path):
        invoice_path = os.path.join(dir_path, invoice)

        if not os.path.isfile(invoice_path):
            continue

        print(f"Processing invoice: {invoice_path}")

        # Extract the invoice's text content
        unstructured_txt = helpers.extract_text(invoice_path)
        structured_txt = helpers.structure_text(unstructured_txt)

        if structured_txt is None:
            print(
                f"[WARNING] OpenAI returned 'error' or empty CSV for {invoice_path}\nSkipping to next"
            )
            continue

        # Convert the csv to a dataframe
        inv_df = helpers.csv_to_df(structured_txt)

        # Append it to the temporal dataframe
        temp_df.append(inv_df)

# Validate if invoices were added to the temporary dataframe
if not temp_df:
    print("No invoices were processed.")
    exit()

# Combine all invoices
df = pd.concat(temp_df, ignore_index=True)
# print(df.to_string())

# Remove any extra spaces in the records and standarize to lowercase
df["currency"] = df["currency"].str.strip().str.lower()

# If necessary, convert currency from euros to usd
is_euros = df["currency"] == "euros"
df.loc[is_euros, "amount"] *= EUR_TO_USD
df.loc[is_euros, "currency"] = "dollars"

# Account for posible duplicates in openai's response
df = df.loc[:, ~df.columns.duplicated()]  # Removes duplicate columns
df = df[["invoice_date", "supplier", "description", "amount", "currency"]]

# Create SQLite connection
conn = sqlite3.connect(DB_PATH)

# Create the invoices table
TABLE_NAME = "invoices"
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_date TEXT,
    supplier TEXT,
    description TEXT,
    amount REAL,
    currency TEXT
);
"""
conn.execute(create_table_query)
conn.commit()

# Insert the dataframe into the database
df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

# Close connection
conn.close()
print("Process complete. Please check the database")
