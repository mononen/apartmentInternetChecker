import requests

def buildPayload(addressLn, zipcode):

  # {"lobs":["broadband"],"addressLine1":"4230 Garrett Rd","mode":"fullAddress","city":"","state":"","zip":"27707","unitType1":"","customerType":"consumer","relocation_flag":true}
  payload = {
    "lobs":["broadband"],
    "addressLine1": addressLn,
    "mode":"fullAddress",
    "city":"",
    "state":"",
    "zip":zipcode,
    "unitType1":"",
    "customerType":"consumer",
    "relocation_flag":True
  }
  return payload

def parseResponse(res):
  result = {}
  if res.status_code != 200:
    return False
  print(res)
  data = res.json()
  data = data['content']
  if data['baseOffers'] == None:
    return False
  # print(data)

  servicesAvail = data['serviceAvailability']['availableServices']
  print(servicesAvail['maxInternetDownloadSpeedAvailableMBPS'])
  print(servicesAvail['maxInternetDisplayText'])

  result["maxDownload"] = servicesAvail['maxInternetDownloadSpeedAvailableMBPS']
  result["packageName"] = servicesAvail['maxInternetDisplayText']
  result["provider"] = "ATT"

  return result

def checkAddress(addressLn, zipcode):
  payload = buildPayload(addressLn, zipcode)
  # r = requests.post("https://api.att.com/rest/1/services/address/validate", json=payload)
  r = requests.post("https://www.att.com/msapi/onlinesalesorchestration/att-wireline-sales-eapi/v1/baseoffers", json=payload)
  # print(r.text)
  return parseResponse(r)


  