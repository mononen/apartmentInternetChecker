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
  payload = buildPayload(addressLn, zipcode)
  # r = requests.post("https://api.att.com/rest/1/services/address/validate", json=payload)
  r = requests.post("https://www.att.com/msapi/onlinesalesorchestration/att-wireline-sales-eapi/v1/baseoffers", json=payload, headers=header)
  # print(r.text)
  return parseResponse(r)


  