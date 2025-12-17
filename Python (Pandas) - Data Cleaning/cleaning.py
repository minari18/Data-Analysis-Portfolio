import pandas as pd

# Get a general view of the dataset
df = pd.read_excel("raw_data/Customer Call List.xlsx")
# print(df.to_string())
# print(df.columns)

# Remove duplicates
df = df.drop_duplicates()

# Drop unnecessary columns
df = df.drop(columns="Not_Useful_Column")

# Clean "Last Name" data
df["Last_Name"] = df["Last_Name"].str.strip("123._/")

# Clean and estandarize the "Phone Number" data
str_numbers = []
for number in df["Phone_Number"]:
    string_num = str(number)  # Changes column data type to string
    str_numbers.append(string_num)
df["Phone_Number"] = str_numbers  # Changes column data type to string

df["Phone_Number"] = df["Phone_Number"].str.replace(
    "[^a-zA-Z0-9]", "", regex=True
)  # Removes all alphanumeric values

phone_numbers = []
for number in df["Phone_Number"]:
    formatted = number[0:3] + "-" + number[3:6] + "-" + number[6:]
    phone_numbers.append(formatted)
df["Phone_Number"] = phone_numbers  # Adds dashes to the phone numbers

# Replaces all "Nan" or "N/A" with NULL values
df["Phone_Number"] = df["Phone_Number"].str.replace("nan--", "")
df["Phone_Number"] = df["Phone_Number"].str.replace("Na--", "")

# Splits the "Adress" column into three separate ones
df[["Street_address", "State", "Zip Code"]] = df["Address"].str.split(
    ",", n=2, expand=True
)

# Change the format of the "Paying Customer" column
df["Paying Customer"] = df["Paying Customer"].str.replace("Yes", "Y")
df["Paying Customer"] = df["Paying Customer"].str.replace("No", "N")
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace("Yes", "Y")
df["Do_Not_Contact"] = df["Do_Not_Contact"].str.replace("No", "N")

# Handles all NULL values
df = df.fillna("")
df["Paying Customer"] = df["Paying Customer"].str.replace("N/a", "")
df["Address"] = df["Address"].str.replace("N/a", "")

# Filter out people who do not wanna get contacted
df = df[df["Do_Not_Contact"] == "N"]

# Filter out people who do not have a phone number
df = df[df["Phone_Number"] != ""]

# Drop the "Do_Not_Contact" column
df = df.drop(columns="Do_Not_Contact")

# Modify the indexes for the resulting table
df = df.reset_index(drop=True)
print(df.to_string())

# Create the new excel file with the clean data
df.to_excel("clean_data/Customer Call List.xlsx", index=False)
