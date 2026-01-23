import pandas as pd

#Reads a spreadsheet and return a specific column as a list.
def read_spreadsheet(file_path, column):
    df = pd.read_excel(file_path)

    unique_values = set()
    result = []

    for value in df[column]:
        if value not in unique_values:
            unique_values.add(value)
            result.append(value)

    return result