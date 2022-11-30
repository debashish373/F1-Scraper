from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import numpy as np

import datetime as dt
import warnings
warnings.filterwarnings('ignore')
import win32com.client as win32

option = webdriver.ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
url = 'https://www.formula1.com/en/results.html'
driver.get(url)
time.sleep(10)
try:
    driver.find_element_by_class_name('trustarc-agree-btn').click()
except:
    pass

#Fastest Laps
fl=pd.DataFrame()
for i,year in enumerate(range(2022,dt.datetime.today().year+1,1)):
    site=url+'/'+str(year)+'/fastest-laps.html'
    temp=pd.read_html(site)[0].dropna(how='all',axis=1)
    temp['DriverCode']=temp['Driver'].apply(lambda x:(str(x).split()[-1])).str.strip()
    temp['Driver']=temp['Driver'].str.strip()
    temp['Driver']=temp['Driver'].apply(lambda x:' '.join(str(x).split()[:-1])).str.strip()
    temp['Year']=year
    #print(year,temp.shape)
    if i==0:
        fl=temp.copy()
    else:
        fl=fl.append(temp).reset_index(drop=True)

#Races
races=pd.DataFrame()
for i,year in enumerate(range(2022,dt.datetime.today().year+1,1)):
    site=url+'/'+str(year)+'/races.html'
    temp=pd.read_html(site)[0].dropna(how='all',axis=1)
    temp['WinnerCode']=temp['Winner'].apply(lambda x:(str(x).split()[-1])).str.strip()
    temp['Winner']=temp['Winner'].str.strip()
    temp['Winner']=temp['Winner'].apply(lambda x:' '.join(str(x).split()[:-1])).str.strip()
    temp['Year']=year
    #print(year,temp.shape)
    if i==0:
        races=temp.copy()
    else:
        races=races.append(temp).reset_index(drop=True)    

#Driver Standings
ds=pd.DataFrame()
for i,year in enumerate(range(2022,dt.datetime.today().year+1,1)):
    site=url+'/'+str(year)+'/drivers.html'
    temp=pd.read_html(site)[0].dropna(how='all',axis=1)
    temp['DriverCode']=temp['Driver'].apply(lambda x:(str(x).split()[-1])).str.strip()
    temp['Driver']=temp['Driver'].str.strip()
    temp['Driver']=temp['Driver'].apply(lambda x:' '.join(str(x).split()[:-1])).str.strip()
    temp['Year']=year
    #print(year,temp.shape)
    if i==0:
        ds=temp.copy()
    else:
        ds=ds.append(temp).reset_index(drop=True)

#Constructor Standings
cs=pd.DataFrame()
for i,year in enumerate(range(2022,dt.datetime.today().year+1,1)):
    site=url+'/'+str(year)+'/team.html'
    temp=pd.read_html(site)[0].dropna(how='all',axis=1)
    temp['Year']=year
    #print(year,temp.shape)
    if i==0:
        cs=temp.copy()
    else:
        cs=cs.append(temp).reset_index(drop=True)    

pd.read_csv(r'Summaries\fastest_laps.csv').append(fl).drop_duplicates(subset=fl.columns.tolist()).to_csv(r'Summaries\fastest_laps.csv',index=False)
pd.read_csv(r'Summaries\race_summaries.csv').append(races).drop_duplicates(subset=races.columns.tolist()).to_csv(r'Summaries\race_summaries.csv',index=False)
pd.read_csv(r'Summaries\driver_standings.csv').append(ds).drop_duplicates(subset=['Driver','Year'],keep='last').to_csv(r'Summaries\driver_standings.csv',index=False)
pd.read_csv(r'Summaries\constructor_standings.csv').append(cs).drop_duplicates(subset=['Team','Year'],keep='last').to_csv(r'Summaries\constructor_standings.csv',index=False)
    
#Detailed extracts
##########################################################################################################################

#Driver details
driver_details=pd.DataFrame()
for i,year in enumerate(range(2022,dt.datetime.today().year+1,1)):
    site_=url+'/'+str(year)+'/drivers.html'
    driver.get(site_)
    drivers=([name.find('a')['data-value'] for name in BeautifulSoup(driver.page_source,'html').findAll("li", {"class": "resultsarchive-filter-item"})])[78:]
    for j,dv in enumerate(drivers):    
        site=url+'/'+str(year)+'/drivers/'+dv+'.html'
        temp=pd.read_html(site)[0].dropna(how='all',axis=1)
        temp['Year']=year
        temp['Driver']=dv.split('/')[1].replace('-',' ').title()
        print(year,dv)
        if len(driver_details)==0:
            driver_details=temp.copy()
        else:
            driver_details=driver_details.append(temp).reset_index(drop=True)
        
#Team details
team_details=pd.DataFrame()
for i,year in enumerate(range(2022,dt.datetime.today().year+1,1)):
    site_=url+'/'+str(year)+'/team.html'
    driver.get(site_)
    teams=([name.find('a')['data-value'] for name in BeautifulSoup(driver.page_source,'html').findAll("li", {"class": "resultsarchive-filter-item"})])[78:]
    for j,team in enumerate(teams):    
        site=url+'/'+str(year)+'/team/'+team+'.html'
        temp=pd.read_html(site)[0].dropna(how='all',axis=1)
        temp['Year']=year
        temp['Team']=team.replace('_',' ').title()
        print(year,team)
        if len(team_details)==0:
            team_details=temp.copy()
        else:
            team_details=team_details.append(temp).reset_index(drop=True)

pd.read_csv(r'Summaries\team_details.csv').append(team_details).drop_duplicates(subset=team_details.columns.tolist()).to_csv(r'Summaries\team_details.csv',index=False)
pd.read_csv(r'Summaries\driver_details.csv').append(driver_details).drop_duplicates(subset=driver_details.columns.tolist()).to_csv(r'Summaries\driver_details.csv',index=False)
            
#Race details
gp_details={}
details=['race-result.html','fastest-laps.html','pit-stop-summary.html','starting-grid.html','qualifying.html','practice-4.html','practice-3.html','practice-2.html','practice-1.html','practice-0.html','sprint-results.html','sprint-grid.html']
details_={'Race result':'race-result.html','Fastest laps':'fastest-laps.html','Pit stop summary':'pit-stop-summary.html','Starting grid':'starting-grid.html','Qualifying':'qualifying.html','Practice 4':'practice-4.html','Practice 3':'practice-3.html','Practice 2':'practice-2.html','Practice 1':'practice-1.html','Overall Qualifying':'qualifying.html','Qualifying 2':'qualifying-2.html','Qualifying 1':'qualifying-1.html','Warm Up':'practice-0.html','Starting grid':'starting-grid.html','Sprint':'sprint-results.html','Sprint grid':'sprint-grid.html','Warm Up':'practice-0.html'}
for i,year in enumerate(range(2022,dt.datetime.today().year+1,1)):
    site_=url+'/'+str(year)+'/races.html'
    driver.get(site_)
    races=([name.find('a')['data-value'] for name in BeautifulSoup(driver.page_source,'html').findAll("li", {"class": "resultsarchive-filter-item"})])[78:]
    races_=([name.text.strip() for name in BeautifulSoup(driver.page_source,'html').findAll("li", {"class": "resultsarchive-filter-item"})])[78:]
    for j,(race,race_) in enumerate(zip(races,races_)):
        for detail in details:
            site=url+'/'+str(year)+'/races/'+race+'/'+detail
            driver.get(site)
            t=([name.text.strip() for name in BeautifulSoup(driver.page_source,'html').findAll("li", {"class": "side-nav-item"})])[1:]
            if detail in [details_[_] for _ in t]:
                gp_details[year,race,detail]=pd.DataFrame()
                #site=url+'/'+str(year)+'/races/'+race+'/'+detail
                try:
                    temp=pd.read_html(site)[0].dropna(how='all',axis=1)
                    temp['Year']=year
                    #temp['Detail']=detail.split('.html')[0].replace('-',' ').title()
                    #temp['Grand Prix']=race.split('/')[1].replace('-',' ').title()
                    temp['Grand Prix']=race_
                    print(year,race,detail)
                    if len(gp_details[year,race,detail])==0:
                        gp_details[year,race,detail]=temp.copy()
                    else:
                        gp_details[year,race,detail]=gp_details[year,race,detail].append(temp).reset_index(drop=True)
                except Exception as e:
                    print(e)
               
race_details=pd.DataFrame()
qualifyings=pd.DataFrame()
practices=pd.DataFrame()
starting_grids=pd.DataFrame()
pitstops=pd.DataFrame()
fastestlaps_detailed=pd.DataFrame()
sprint_results=pd.DataFrame()
sprint_grid=pd.DataFrame()

#for x,y in new_dict.items():
#    temp=new_dict[x].copy()
    
for x,y in gp_details.items():
    temp=gp_details[x].copy()
    
    #temp['Year']=x[0]
    #temp['Grand Prix']=x[1].split('/')[1].replace('-',' ').title()
    print(x)
    temp['Detail']=x[2].split('.html')[0].title()
    
    if x[0]>=2022 and len(temp)!=0:
        
        temp['DriverCode']=temp['Driver'].apply(lambda x:(str(x).split()[-1])).str.strip()
        temp['Driver']=temp['Driver'].str.strip()
        temp['Driver']=temp['Driver'].apply(lambda x:' '.join(str(x).split()[:-1])).str.strip()

        if x[2] in ['race-result.html']:        
            race_details=race_details.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            race_details=race_details.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver']).reset_index(drop=True)
            
        elif x[2] in ['qualifying.html']:        
            qualifyings=qualifyings.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            qualifyings=qualifyings.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver']).reset_index(drop=True)
            
        elif x[2] in ['practice-1.html','practice-2.html','practice-3.html','practice-4.html']:        
            practices=practices.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            practices=practices.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver']).reset_index(drop=True)
                
        elif x[2] in ['starting-grid.html']:        
            starting_grids=starting_grids.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            starting_grids=starting_grids.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver']).reset_index(drop=True)
                
        elif x[2] in ['pit-stop-summary.html']:        
            pitstops=pitstops.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            pitstops=pitstops.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver','Time of day']).reset_index(drop=True)

        elif x[2] in ['fastest-laps.html']:
            fastestlaps_detailed=fastestlaps_detailed.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            fastestlaps_detailed=fastestlaps_detailed.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver']).reset_index(drop=True)

        elif x[2] in ['sprint-results.html']:
            sprint_results=sprint_results.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            sprint_results=sprint_results.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver']).reset_index(drop=True)

        elif x[2] in ['sprint-grid.html']:
            sprint_grid=sprint_grid.append(temp).reset_index(drop=True).dropna(how='all',axis=1)
            sprint_grid=sprint_grid.drop_duplicates(['Detail','Year','Grand Prix','Car','Driver']).reset_index(drop=True)

        else:
            print(x[2])
            
print(race_details.shape,
      qualifyings.shape,
      practices.shape,
      starting_grids.shape,
      pitstops.shape,
      fastestlaps_detailed.shape,
      sprint_results.shape,
      sprint_grid.shape
      )    


pd.read_csv(r'GPDetails\race_details.csv').append(race_details).drop_duplicates(subset=race_details.columns.tolist()).to_csv(r'GPDetails\race_details.csv',index=False)
pd.read_csv(r'GPDetails\qualifyings.csv').append(qualifyings).drop_duplicates(subset=qualifyings.columns.tolist()).to_csv(r'GPDetails\qualifyings.csv',index=False)
pd.read_csv(r'GPDetails\practices.csv').append(practices).drop_duplicates(subset=practices.columns.tolist()).to_csv(r'GPDetails\practices.csv',index=False)
pd.read_csv(r'GPDetails\starting_grids.csv').append(starting_grids).drop_duplicates(subset=starting_grids.columns.tolist()).to_csv(r'GPDetails\starting_grids.csv',index=False)
pd.read_csv(r'GPDetails\pitstops.csv').append(pitstops).drop_duplicates(subset=pitstops.columns.tolist()).to_csv(r'GPDetails\pitstops.csv',index=False)
pd.read_csv(r'GPDetails\fastestlaps_detailed.csv').append(fastestlaps_detailed).drop_duplicates(subset=fastestlaps_detailed.columns.tolist()).to_csv(r'GPDetails\fastestlaps_detailed.csv',index=False)
pd.read_csv(r'GPDetails\sprint_results.csv').append(sprint_results).drop_duplicates(subset=sprint_results.columns.tolist()).to_csv(r'GPDetails\sprint_results.csv',index=False)
pd.read_csv(r'GPDetails\sprint_grid.csv').append(sprint_grid).drop_duplicates(subset=sprint_grid.columns.tolist()).to_csv(r'GPDetails\sprint_grid.csv',index=False)
