import requests
import json
import pandas as pd

def fetch(url):
  headers = {
    "Content-Type": "application/json"
  }
  resp = requests.get(url=url, headers=headers)
  #print(resp.json())
  return resp.json()

def dataframify(data):
  dfs = {} 

  # Iterate through the data to create one DataFrame per plug
  for station, plugs in data.items():
      for plug_name, time_series_data in plugs.items():
          # Create a DataFrame for each plug
          df = pd.DataFrame(time_series_data)
          # Convert 'timestamp' to datetime if necessary
          df['timestamp'] = pd.to_datetime(df['timestamp'])
          # Store DataFrame in dictionary
          dfs[plug_name] = df            

  # dfs['stationXY-1']
  return dfs


def calculate_charging_percentage(plug_frame):
    # Resample the data to hourly intervals and calculate the mean of 'isCharging'
    # 'isCharging' should be converted to int (True=1, False=0) for mean calculation to represent percentage
    plug_frame['isCharging'] = plug_frame['isCharging'].astype(int)
    hourly_charging = plug_frame.resample('h', on='timestamp')['isCharging'].mean()
    
    # Convert the mean to percentage
    hourly_percentage = hourly_charging * 100
    return hourly_percentage

def calculate_hourly_percentages(dfs):
  # Dictionary to store the hourly charging percentage DataFrames
  hourly_percentages = {}

  # Apply the function to each DataFrame
  for plug_name, df in dfs.items():
      hourly_percentages[plug_name] = calculate_charging_percentage(df)

  return hourly_percentages

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
        appending_dict = { "timestamp": measurement["mtransactiontime"], "isCharging": measurement["mvalue"] == 0 }
        # restructured_dict[parent_code][station_key].append((measurement["tmeasurements"], measurement["mvalue"]))
        restructured_dict[parent_code][station_key].append(appending_dict)

  # print(restructured_dict)

  dfs = dataframify(restructured_dict)
  hourly = calculate_hourly_percentages(dfs)
  print(hourly)





if __name__ == "__main__":
  main()