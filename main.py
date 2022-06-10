import openpyxl
import attRequest


def clean_address(address):
  addrLn = address.split(",")[0]
  zipcode = address[-5:]
  return addrLn, zipcode

def writeResults(res, addr, sheet):
  sheet.write(addr, 2, res['provider'])
  sheet.write(addr, 4, res['maxDownload'])
  sheet.write(addr, 6, res['packageName'])

loc = "./data.xls"

wb = openpyxl.load_workbook(loc)
sheet = wb.active
m_row = sheet.max_row

for addr in range(1, m_row + 1):
  print(sheet.cell_value(addr, 1))
  if sheet.cell_value(addr, 1)[-3].isnumeric() == True:
    addrLn, zipcode = clean_address(sheet.cell_value(addr, 1))
    print(addrLn, zipcode)
    res = attRequest.checkAddress(addrLn, zipcode)
    writeResults(res, addr, sheet)
  else:
    print("No zipcode")


