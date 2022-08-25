import xlsxwriter
from pars1 import all_products


def writer(parametr):
    book = xlsxwriter.Workbook("C:\\Users\\User\\Desktop\\all_products.xlsx")
    page = book.add_worksheet("весь товар")

    row = 0
    column = 0

    page.set_column("A:A", 20)
    page.set_column("B:B", 20)
    page.set_column("C:C", 60)
    page.set_column("D:D", 50)
    page.set_column("F:F", 40)

    for item in parametr():
        page.write(row, column, item[0])
        page.write(row, column + 1, item[1])
        page.write(row, column + 2, item[2])
        page.write(row, column + 3, item[3])
        page.write(row, column + 4, item[4])
        row += 1

    book.close()


writer(all_products)