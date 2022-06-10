import requests
import json

header = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"102\", \"Google Chrome\";v=\"102\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "x-dtpc": "16$86673792_303h54vHNHFGFACDGHAHVHFLNERWORQEKOMUFKQ-0e0",
    "Referer": "https://www.att.com/buy/broadband/availability.html",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

def buildSimplePayload(addressLn, zipcode): # returns payload for an apartment that doesn't require a unit number
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

def buildUnitPayload(addr): # returns payload for an apartment that requires a unit number
  # {"lobs":["broadband"],"addressLine1":"6801 Chesterbrook Ct","addressLine2":"UNIT LEASING 4","mode":"fullAddress","city":"","state":"","zip":"27615","unitType1":"UNIT","unitNumber1":"LEASING 4","unitNumber2":"","customerType":"consumer","relocation_flag":true}
  payload = {
    "lobs":["broadband"],
    "addressLine1": addr["addressLine1"],
    "addressLine2": addr["addressLine2"],
    "mode":"fullAddress",
    "city":"",
    "state":"",
    "zip":addr["zip"],
    "unitType1":"UNIT",
    "unitNumber1":addr["unitNumber1"],
    "unitNumber2":"",
    "customerType":"consumer",
    "relocation_flag":True
  }
  return payload

def newRequest(addr):
  payload = buildUnitPayload(addr)
  r = requests.post("https://www.att.com/msapi/onlinesalesorchestration/att-wireline-sales-eapi/v1/baseoffers", json=payload, headers=header)
  return parseResponse(r)

def parseResponse(res):
  result = {}
  # catching any incorrect responses
  if res.status_code != 200:
    result["status"] = "HTTP Error" + str(res.status_code)
    return result
  print(res)

  data = res.json()
  data = data['content'] # processing the content header out of the response

  if "error" in data['serviceAvailability']:
    result["status"] = "ERROR " + data['serviceAvailability']['error']["errorId"] 
    return result

  if "mduAddress" in data['serviceAvailability']:
    newaddr = data['serviceAvailability']['mduAddress'][0]
    print("multiple unit dwelling response detected. Selecting first option" + newaddr['addressLine2'])
    mduRes = newRequest(newaddr)
    if mduRes["status"] == "success":
      mduRes["status"] = "success - MDU"
      return mduRes
  
  if data['baseOffers'] == None:
    print("No base offers")
    result["status"] = "No Offers"
    return result
  # print(data)

  servicesAvail = data['serviceAvailability']['availableServices']
  print(servicesAvail['maxInternetDownloadSpeedAvailableMBPS'])
  print(servicesAvail['maxInternetDisplayText'])

  result["maxDownload"] = servicesAvail['maxInternetDownloadSpeedAvailableMBPS']
  result["packageName"] = servicesAvail['maxInternetDisplayText']
  result["provider"] = "ATT"
  result["status"] = "success"

  return result

def checkAddress(addressLn, zipcode):
  payload = buildSimplePayload(addressLn, zipcode)
  # r = requests.post("https://api.att.com/rest/1/services/address/validate", json=payload)
  r = requests.post("https://www.att.com/msapi/onlinesalesorchestration/att-wireline-sales-eapi/v1/baseoffers", json=payload, headers=header)
  # print(r.text)
  return parseResponse(r)


  