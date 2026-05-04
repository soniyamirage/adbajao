import pandas as pd
import pymysql
import re

# ===============================
# DATABASE CONFIG
# ===============================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Nikhil_2617",
    "database": "adbajao",
    "port": 3306
}

# ===============================
# FILE PATH
# ===============================
excel_path = r"C:\Users\nikhi\Downloads\MASTER SCREEN LIST 9272 PAN INDIA WITH AGENCY RATES.xlsx"

table_name = "screenlisting_new"

# ===============================
# READ EXCEL
# ===============================
print("Reading Excel file...")

df = pd.read_excel(excel_path)

print(f"Total rows found: {len(df)}")
print(f"Total columns found: {len(df.columns)}")

# ===============================
# CLEAN COLUMN NAMES
# ===============================
def clean_column(col):
    col = col.strip().lower()
    col = re.sub(r'\W+', '_', col)
    return col

df.columns = [clean_column(col) for col in df.columns]

# Replace NaN with None
df = df.astype(object).where(pd.notnull(df), None)

# ===============================
# CONNECT DATABASE
# ===============================
print("Connecting to MySQL...")

conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

print("Connected successfully.")

# ===============================
# CREATE TABLE DYNAMICALLY
# ===============================
print("Creating table if not exists...")

columns_sql = ", ".join([f"`{col}` TEXT" for col in df.columns])

create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    {columns_sql}
)
"""

cursor.execute(create_table_query)
conn.commit()

print(f"Table `{table_name}` ready.")

# ===============================
# INSERT DATA
# ===============================
columns = ", ".join([f"`{col}`" for col in df.columns])
placeholders = ", ".join(["%s"] * len(df.columns))

insert_query = f"""
INSERT INTO {table_name} ({columns})
VALUES ({placeholders})
"""

print("Starting data insert...")

count = 0

for index, row in df.iterrows():
    cursor.execute(insert_query, tuple(row))
    count += 1

    if count % 500 == 0:
        conn.commit()
        print(f"{count} rows inserted...")

conn.commit()

print("===================================")
print(f"Finished! Total rows inserted: {count}")
print("===================================")

cursor.close()
conn.close()

print("Database connection closed.")