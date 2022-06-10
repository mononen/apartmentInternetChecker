import xlrd
import attRequest


def clean_address(address):
  addrLn = address.split(",")[0]
  zipcode = address[-5:]
  return addrLn, zipcode


loc = ("./data.xls")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

for addr in range(sheet.nrows):
  print(sheet.cell_value(addr, 1))
  if sheet.cell_value(addr, 1)[-3].isnumeric() == True:
    addrLn, zipcode = clean_address(sheet.cell_value(addr, 1))
    print(addrLn, zipcode)
    attRequest.checkAddress(addrLn, zipcode)
  else:
    print("No zipcode")


