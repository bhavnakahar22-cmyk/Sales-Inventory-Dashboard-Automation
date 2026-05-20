import pandas as pd


def clean_sales_data(file_path):
    df = pd.read_csv(file_path)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Handle missing values
    df.fillna(0, inplace=True)

    # Create Total Amount column
    df['Total_Amount'] = df['Quantity'] * df['Price']

    return df


def clean_inventory_data(file_path):
    df = pd.read_csv(file_path)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Fill null values
    df.fillna(0, inplace=True)

    return df