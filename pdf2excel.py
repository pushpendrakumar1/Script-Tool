import tabula
import pandas as pd
import re
import argparse
import subprocess
import os

# Create an argument parser
parser = argparse.ArgumentParser(description='Convert PDF to Excel with styling')

# Add arguments for input PDF and output Excel files
parser.add_argument('input_pdf', help='Input PDF file path')
parser.add_argument('output_excel', help='Output Excel file path')

# Parse the command-line arguments
args = parser.parse_args()

# Read the PDF file and extract tables
tables = tabula.read_pdf(args.input_pdf, pages='all', encoding='latin-1')

# Create a list to store the modified tables
modified_tables = []

# Iterate over the extracted tables and modify them
for table in tables:
    # Check if the table contains any rows
    if not table.empty:
        # Create a styler object for the table
        styler = table.style

        # Iterate over the rows
        for i in range(len(table)):
            row = table.loc[i, :]
            # Check if any cell in the row matches the "section + number" pattern
            if any(re.match(r"section \d+", str(cell).lower(), re.IGNORECASE) for cell in row):
                # Apply blue background to the cells in the row
                styler = styler.apply(lambda x: ['background-color: blue' if re.match(r"section \d+", str(cell).lower(), re.IGNORECASE) else '' for cell in x], axis=1)

        # Append the modified table to the list
        modified_tables.append(styler)

# Save the modified tables to an Excel file
with pd.ExcelWriter(args.output_excel, engine='xlsxwriter') as writer:
    # Iterate over the modified tables and write them to separate sheets
    for i, modified_table in enumerate(modified_tables):
        modified_table.to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)

print("PDF converted to Excel successfully!")

input_file = args.output_excel  # Use the output from the first script as input for the second one

try:
    # Run the final_tool.py script with the input_file argument
    subprocess.run(['python', 'final_tool.py', input_file], check=True)



    # Delete the Excel file if final_tool.py has finished executing
    print("Excel file Created successfully.")

except subprocess.CalledProcessError as e:
    print(f"Error running final_tool.py: {e}")
