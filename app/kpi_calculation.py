import pandas as pd


def calculate_sales_kpis(df):
    total_sales = df['Total_Amount'].sum()
    total_orders = df['Order_ID'].nunique()
    average_order_value = total_sales / total_orders

    top_product = (
        df.groupby('Product')['Total_Amount']
        .sum()
        .sort_values(ascending=False)
        .idxmax()
    )

    return {
        'Total Sales': total_sales,
        'Total Orders': total_orders,
        'Average Order Value': round(average_order_value, 2),
        'Top Product': top_product
    }


def calculate_inventory_kpis(df):
    low_stock = df[df['Stock_Quantity'] <= df['Reorder_Level']]

    return {
        'Low Stock Products': low_stock
    }