
import sqlite3
import pandas as pd

# name of the xlsx. 
filename = 'workbook'
con = sqlite3.ocnnect(filename+'.db')
wb = pd.read_excel(filename+'.xlsx', sheetname=None)

for sheet in wb:
    wb[sheet].to_sql(sheet, con, index=False)
  
con.commit()
con.close()