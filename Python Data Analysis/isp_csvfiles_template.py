"""
Project for Week 3 of "Python Data Analysis".
Read and write CSV files using a dictionary of dictionaries.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv

def read_csv_fieldnames(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      A list of strings corresponding to the field names in
      the given CSV file.
    """
    with open(filename, 'r', newline='') as csvfile:
        # Initialize a CSV reader with custom separator and quote character
        csvreader = csv.reader(csvfile, delimiter=separator, quotechar=quote)
        
        # Read the first row which contains the field names
        fieldnames = next(csvreader)
        
    return fieldnames


def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file. The dictionaries in the
      list map the field names to the field values for that row.
    """
    data = []
    
    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=separator, quotechar=quote)
        
        # Read field names from the first row
        fieldnames = next(csvreader)
        
        for row in csvreader:
            # Create a dictionary mapping field names to row values
            row_dict = {fieldnames[i]: row[i] for i in range(len(fieldnames))}
            data.append(row_dict)
    
    return data


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file. The inner dictionaries map the field names to the
      field values for that row.
    """
    data_dict = {}
    header = []

    with open(filename, 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=separator, quotechar=quote)
        
        for i, row in enumerate(csvreader):
            if i == 0:
                header = row
            else:
                key_value = row[header.index(keyfield)]
                row_dict = {header[j]: row[j] for j in range(len(header))}
                data_dict[key_value] = row_dict

    return data_dict


def write_csv_from_list_dict(filename, table, fieldnames, separator, quote):
    """
    Inputs:
      filename   - name of CSV file
      table      - list of dictionaries containing the table to write
      fieldnames - list of strings corresponding to the field names in order
      separator  - character that separates fields
      quote      - character used to optionally quote fields
    Output:
      Writes the table to a CSV file with the name filename, using the
      given fieldnames. The CSV file should use the given separator and
      quote characters. All non-numeric fields will be quoted.
    """
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=separator, quotechar=quote, quoting=csv.QUOTE_NONNUMERIC)
        
        # Write header row
        csvwriter.writerow(fieldnames)
        
        # Write data rows
        for row in table:
            csvwriter.writerow([row[fieldname] if isinstance(row[fieldname], (int, float)) else quote + str(row[fieldname]) + quote for fieldname in fieldnames])
