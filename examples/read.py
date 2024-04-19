import requests
import json

def fetch(url):
  headers = {
    "Content-Type": "application/json"
  }
  resp = requests.get(url=url, headers=headers)
  #print(resp.json())
  return resp.json()


def main():
  fromDate = "2024-03-12"
  toDate = "2024-03-13"
  limit = "-1"


  # In Java, String interpolation would work [better]
  jsonData = fetch("https://mobility.api.opendatahub.com/v2/tree%2Cnode/EChargingPlug/%2A/" + fromDate + "/" + toDate + "?limit=" + limit + "&offset=0&select=scode%2Csdatatypes.tmeasurements.mtransactiontime%2Csdatatypes.tmeasurements.mvalue%2Csparent.pcode&where=sorigin.eq.%22DRIWE%22&shownull=false&distinct=true&timezone=UTC")
  
  data = jsonData

  restructured_dict = {}

  for station_key, station_value in data['data']["EChargingPlug"]["stations"].items():
    parent_code = station_value["sparent"]["pcode"]
    if parent_code not in restructured_dict:
        restructured_dict[parent_code] = {}
    if station_key not in restructured_dict[parent_code]:
        restructured_dict[parent_code][station_key] = []
    for measurement in station_value["sdatatypes"]["echarging-plug-status"]["tmeasurements"]:
        restructured_dict[parent_code][station_key].append((measurement["mtransactiontime"], measurement["mvalue"]))

  print(restructured_dict)

if __name__ == "__main__":
  main()