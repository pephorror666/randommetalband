import pandas as pd

# Load the CSV file
df = pd.read_csv('metal_records.csv')

# Drop duplicates based on all columns
df.drop_duplicates(inplace=True)

# Save the cleaned data back to the same file
df.to_csv('metal_records_2.csv', index=False)