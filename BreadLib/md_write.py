from .md_notif import *
import pandas as pd
import os
from openpyxl.styles import Alignment

def output_daily_tables(path, data, kw_number, data_total=None):
    try:
        if not data:
            msg_error("No data provided to output!")
            return
        # File path
        excel_file = os.path.join(path, "output.xlsx")
        column_names = ['LV-Position', 'Bezeichnung', 'Menge', 'Einheit']
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            days = list(dict.fromkeys(key[0] for key in data.keys()))
            # Must be in this way ( dict.fromkeys(...) ) 
            # Bad: days = list( { key[0] for key in data.keys() } )
            # {} creates set. Set always mixing arguments
            # from keys make dictionary and convert to list
            # code is ass, but it works

            sheets = {}
            rows_cursor = {}
            # First, make columns, where top one (row) is KW** Day
            # Second row is: 'LV-Position', 'Bezeichnung', 'Menge', 'Einheit'
            for index, day in enumerate(days):
                sheet = writer.book.create_sheet(title=str(day), index=index)
                sheets[day] = sheet
                rows_cursor[day] = 3
                # header
                sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=4)
                sheet.cell(row=1, column=1).value = f"KW{kw_number} - {day}"
                sheet.cell(row=1, column=1).alignment = Alignment(horizontal='center')
                for col_num, header in enumerate(column_names, 1):
                    sheet.cell(row=2, column=col_num).value = header
            
            # Real data
            for (d, lv, mat), val in data.items():
                if d in sheets:
                    sheet = sheets[d]
                    r = rows_cursor[d]
                    sheet.cell(row=r, column=1).value = lv
                    sheet.cell(row=r, column=2).value = mat
                    sheet.cell(row=r, column=3).value = val.get('Count', 0)
                    sheet.cell(row=r, column=4).value = val.get('Unit', 'm')
                    
                    rows_cursor[d] += 1

            if data_total is not None:
                sheet = writer.book.create_sheet(title="Summary")

                sheet.cell(row=1, column=1).value = f"KW{kw_number} Summary"
                sheet.merge_cells(start_row=1, start_column=1, end_row=1, end_column=4)

                for (lv, mat), val in data_total.items():
                    for col, text in enumerate(column_names, 1):
                        sheet.cell(row=2, column=col).value = text

                    current_row = 3
                    for (lv, mat), val in data_total.items():
                        sheet.cell(row=current_row, column=1).value = lv
                        sheet.cell(row=current_row, column=2).value = mat.strip()
                        sheet.cell(row=current_row, column=3).value = val.get('Count', 0)
                        sheet.cell(row=current_row, column=4).value = val.get('Unit', 'm')
                        current_row += 1

            if "Sheet1" in writer.book.sheetnames:
                writer.book.remove(writer.book["Sheet1"])
        msg_info(f"Data saved with path: {excel_file}")
    except PermissionError:
        msg_warning("Close output file before processing!")
    except Exception as e:
        msg_warning(e)