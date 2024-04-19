import requests
import json

def fetch(url):
  headers = {
    "Content-Type": "application/json"
  }
  resp = requests.get(url=url, headers=headers)
  return resp.text


def main():
  fromDate = "2024-03-12"
  toDate = "2024-03-13"
  limit = "1"


  # In Java, String interpolation would work [better]
  jsonData = fetch("https://mobility.api.opendatahub.com/v2/tree%2Cnode/EChargingPlug/%2A/" + fromDate + "/" + toDate + "?limit=" + limit + "&offset=0&select=scode%2Csdatatypes.tmeasurements.mtransactiontime%2Csdatatypes.tmeasurements.mvalue%2Csparent.pcode&where=sorigin.eq.%22DRIWE%22&shownull=false&distinct=true&timezone=UTC")
  
  data = json.loads(jsonData)

  print(data['limit'])


if __name__ == "__main__":
  main()