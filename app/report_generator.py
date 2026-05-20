import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font


def generate_excel_report(sales_df, kpis, output_path):
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        sales_df.to_excel(writer, sheet_name='Sales Data', index=False)

        kpi_df = pd.DataFrame(list(kpis.items()), columns=['KPI', 'Value'])
        kpi_df.to_excel(writer, sheet_name='KPI Summary', index=False)

    workbook = load_workbook(output_path)
    sheet = workbook['KPI Summary']

    # Apply bold font to headers
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    workbook.save(output_path)