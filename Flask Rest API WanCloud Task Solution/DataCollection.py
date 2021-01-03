import requests
import json


# Data Collectection From First COVID-19 API Server
response_region = requests.get("https://covid-api.com/api/regions")
region_names=response_region.json()
#print('Region Names: ')
#print(region_names)

response_prov_iso = requests.get("https://covid-api.com/api/provinces/?iso=CHN")
prov_iso=response_prov_iso.json()
#print('Provinces BY ISO: ')
#print(prov_iso)

response_report=requests.get('https://covid-api.com/api/reports?date=2020-03-14&q=China%20Beijing&iso=CHN&region_name=China&region_province=Beijing')
reports=response_report.json()
#print('List Of Reports: ')
#print(reports)

response_totdata=requests.get('https://covid-api.com/api/reports/total?date=2020-04-15')
tot_data_ondate=response_totdata.json()
#print('Total data By Date: ')
#print(tot_data_ondate)


# Data Collectection From Second COVID-19 API Server
response_statsgeneral= requests.get('https://corona-virus-stats.herokuapp.com/api/v1/cases/general-stats')
statsgeneral=response_statsgeneral.json()
#print('General Stats: ')
#print(statsgeneral)

response_countriesstats= requests.get('https://corona-virus-stats.herokuapp.com/api/v1/cases/countries-search')
statscountries=response_countriesstats.json()
#print('Countries Stats: ')
#print(statscountries)

# Data Collectection From Third COVID-19 API Server
response_By_Country= requests.get('https://covid19-stats-api.herokuapp.com/api/v1/cases?country=China')
dataOneCountry=response_By_Country.json()
#print('Data One Country: ')
#print(dataOneCountry)
General=statsgeneral['data']
#print(General)
GeneralStats={}
GeneralStats['total']=General['total_cases']
GeneralStats['recovered']=General['recovery_cases']
GeneralStats['deaths']=General['death_cases']
GeneralStats['current_infects']=General['currently_infected']
TotalData_Date=tot_data_ondate['data']
#print(TotalData_Date)
Data_Date={}
Data_Date['date']=TotalData_Date['date']
Data_Date['confirmed']=TotalData_Date['confirmed']
Data_Date['deaths']=TotalData_Date['deaths']
Data_Date['recovered']=TotalData_Date['recovered']
Data_Date['active']=TotalData_Date['active']
BASE="http://127.0.0.1:5000/"
response=requests.put(BASE+"day/"+"China",dataOneCountry)
print(response.json())
input()
response=requests.get(BASE+"day/"+"China")
print(response.json())

response1=requests.put(BASE+"stats/"+"1",GeneralStats)
print(response1.json())
input()
response1=requests.get(BASE+"stats/"+"1")
print(response1.json())

response2=requests.put(BASE+"datedata/"+"2020-04-15",Data_Date)
print(response2.json())
input()
response=requests.get(BASE+"datedata/"+"2020-04-15")
print(response2.json())