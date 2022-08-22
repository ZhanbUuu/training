import xlsxwriter
from pars3 import get_data

def writer(parametr):
    book = xlsxwriter.Workbook("C:\\Users\\User\\Desktop\\wears_pars3.xlsx")
    page = book.add_worksheet("одежда")

    row = 0
    column = 0

    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 60)
    page.set_column("D:D", 50)

    for item in parametr():
        page.write(row, column, item[0])
        page.write(row, column+1, item[1])
        page.write(row, column+2, item[2])
        page.write(row, column+3, item[3])
        row += 1

    book.close()

writer(get_data)