from app.data_cleaning import clean_sales_data, clean_inventory_data
from app.kpi_calculation import calculate_sales_kpis, calculate_inventory_kpis
from app.database import load_data_to_db
from app.report_generator import generate_excel_report

# File Paths
sales_file = 'data/sales_data.csv'
inventory_file = 'data/inventory_data.csv'
output_file = 'output/final_report.xlsx'

# Step 1: Clean Data
sales_df = clean_sales_data(sales_file)
inventory_df = clean_inventory_data(inventory_file)

# Step 2: Calculate KPIs
sales_kpis = calculate_sales_kpis(sales_df)
inventory_kpis = calculate_inventory_kpis(inventory_df)

# Step 3: Load Data to Database
load_data_to_db(sales_df, 'sales_data')
load_data_to_db(inventory_df, 'inventory_data')

# Step 4: Generate Excel Report
generate_excel_report(sales_df, sales_kpis, output_file)

# Step 5: Print KPIs
print('\nSales KPIs')
for key, value in sales_kpis.items():
    print(f'{key}: {value}')

print('\nLow Stock Products')
print(inventory_kpis['Low Stock Products'])

print('\nReport Generated Successfully!')