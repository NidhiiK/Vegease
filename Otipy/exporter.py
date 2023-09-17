# exporter.py

import openpyxl

def export_to_excel(data, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Product Name", "Original Price", "Discounted Price", "Discount", "Timestamp"])

    for row in data:
        ws.append(row)

    wb.save(filename)
