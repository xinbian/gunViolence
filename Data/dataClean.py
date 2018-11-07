#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 20:29:45 2017

@author: Xin
"""
#%%
import pandas as pd
import plotly.plotly as py
import ast
import geopandas as gpd
import urllib2
from sklearn import preprocessing
import numpy as np
from sklearn.preprocessing import Imputer

min_max_scaler = preprocessing.MinMaxScaler()

seleCol =  range(40,45)
seleCol.append(1)

####  read law scores
laws = pd.read_csv('laws.csv', delimiter=' ', header=None, usecols=seleCol)
laws.columns = ['state', 'total_score','curved_score','grade','2010_gun_death_rate','2009_gun_export_rates']
laws.set_index('state', inplace = True)
#laws.to_csv('laws_filter.csv')
laws = pd.read_csv('laws_filter.csv', delimiter=',')
laws.sort_values(laws.columns[0], ascending = True, inplace = True)
laws.reset_index(drop=True, inplace = True)
#read state code
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
laws['code']=df['code']
laws = laws[['code','state','curved_score']]

#sklearn.preprocessing.robust_scale(X, axis=0, with_centering=True, \
#with_scaling=True, quantile_range=(25.0, 75.0), copy=True)[source]¶

######

#### read crime rate
crime = pd.read_csv('crime_data_w_population_and_crime_rate.csv', 
                   usecols=[0, 1, 2, 21, 22, 23])
#create FIPS code by combining FIPSstate and FIPScity
crime['FIPStxt'] = pd.to_numeric(crime.FIPS_ST.apply(str)+
     crime.FIPS_CTY.apply(str).str.zfill(3))
######

#### read 2015 unemployment rate and household income
#### No income data from PR
eco = pd.read_csv('Unemployment.csv',usecols=[0, 1, 2, 41, 46])
eco['Median_Household_Income_2015'] = eco['Median_Household_Income_2015'].str.replace(',','')
eco['Median_Household_Income_2015'] = pd.to_numeric(eco['Median_Household_Income_2015'])
eco['Median_Household_Income_2015'].fillna((eco['Median_Household_Income_2015'].mean()), inplace=True)
eco['Unemployment_rate_2015'].fillna((eco['Unemployment_rate_2015'].mean()), inplace=True)

######


####containing 2015 Estimated percent of people of all ages
poverty = pd.read_csv('PovertyEstimates.csv',usecols=[0, 11])
#missing value'
poverty.rename(index=str, columns={'CI90LBALLP_2015':'poverty_rate'}, inplace=True)
poverty.ix[561,['poverty_rate']]=  0 
poverty['poverty_rate'] = pd.to_numeric(poverty['poverty_rate'])
#set missing value by median
poverty['poverty_rate'].fillna((poverty['poverty_rate'].mean()), inplace=True)
####

###Sources: Census Bureau,2011-2015 American Community Survey 5-yr average.
edu = pd.read_csv('Education.csv',usecols=[0, 45])
edu.rename(index=str, columns={'Percent of adults completing some college or associate\'s degree, 2011-2015':'college_rate'}, inplace=True)
edu['college_rate'].fillna((edu['college_rate'].mean()), inplace=True)
####

####cdc firearm death 1999-2015
fire = pd.read_csv('Underlying Cause of Death, 1999-2015.txt', 
                    delimiter='\t') 
fire['Deaths'] = pd.to_numeric(fire['Deaths'], errors='coerce')
fire['Population'] = pd.to_numeric(fire['Population'])
fire['fire_rate'] = 100000.0*fire['Deaths']/fire['Population']
#fill nan with 0
fire['fire_rate'] = fire['fire_rate'].fillna(value=0.0)
#round
fire['fire_rate'] = fire['fire_rate'].round(2)
####

#merge to one dataframe
allData = pd.merge(eco, poverty, on='FIPStxt')
allData = pd.merge(allData, edu, left_on='FIPStxt', right_on='FIPS Code')
#allData = pd.merge(allData, crime, on='FIPStxt')
allData = pd.merge(allData, fire, left_on='FIPStxt', right_on='County Code')
allData = pd.merge(allData, laws, left_on='State', right_on='code')
allData = pd.merge(allData, crime, on='FIPStxt')
#allData FIPStxt code padding (add zero)
allData['FIPStxt'] = allData.FIPStxt.apply(str).str.zfill(5)
             
#%%
'''not used
def norm(data_frame):
    return (data_frame-data_frame.min())/(data_frame.max()-data_frame.min())
#min-max normalize data
allData['curved_score']  = norm(allData['curved_score'])
allData['Unemployment_rate_2015']=norm(allData['Unemployment_rate_2015'])
allData['Median_Household_Income_2015']=norm(allData['Median_Household_Income_2015'])
allData['poverty_rate']=norm(allData['poverty_rate'])
#allData['crime_rate_per_100000']=norm(allData['crime_rate_per_100000'])
allData['college_rate']=norm(allData['college_rate'])
allData['fire_rate']=norm(allData['fire_rate'])
allData['crime_rate_per_100000']=norm(allData['crime_rate_per_100000'])
'''


#normalize data
laws['curved_score'] = preprocessing.minmax_scale(laws['curved_score'])
eco['Unemployment_rate_2015'] = preprocessing.minmax_scale(eco['Unemployment_rate_2015'])
eco['Median_Household_Income_2015'] = preprocessing.minmax_scale(eco['Median_Household_Income_2015'])
crime['crime_rate_per_100000'] = preprocessing.minmax_scale(crime['crime_rate_per_100000'])
poverty['poverty_rate'] = preprocessing.minmax_scale(poverty['poverty_rate'])
edu['college_rate'] = preprocessing.minmax_scale(edu['college_rate'])
fire['fire_rate']  = preprocessing.minmax_scale(fire['fire_rate'] )


#write to file
allData.to_csv('allData.csv')

#%%
url = 'http://catalog.civicdashboards.com/dataset/ff54801b-6683-4566-b267-d873b7fa6369/resource/c6540266-7bea-4c88-8deb-0ec6870c50b9/download/5766c073476c40b1aa888aa245423989temp.geojson'


req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
page = urllib2.urlopen(req);response=page.read();page.close()
cookie=page.info()['Set-Cookie']
# top is for obtaining the cookie via the info get.
req = urllib2.Request(url)#send the new url with the cookie.
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
req.add_header('Cookie',cookie)
page = urllib2.urlopen(req)
response=page.read();page.close()
new_york_data = ast.literal_eval(response)


county_names = []
county_names_dict = {}

for county in new_york_data['features']:
    for m in range(len(county['properties']['name'])):
        if county['properties']['name'][m:m+6] == 'County':
            county_names.append(county['properties']['name'][0:m-1])
            county_names_dict[county['properties']['name'][0:m-1]] = county['properties']['name']
            
print county_names




url = 'https://bubinga.co/wp-content/uploads/jsoncounties.min_.js'

req = urllib2.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
page = urllib2.urlopen(req);response=page.read();page.close()

# top is for obtaining the cookie via the info get.
req = urllib2.Request(url)#send the new url with the cookie.
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
req.add_header('Cookie',cookie)
page = urllib2.urlopen(req)
response=page.read();page.close()
new_york_data = ast.literal_eval(response)


county_names = []
county_names_dict = {}

for county in new_york_data['features']:
    for m in range(len(county['properties']['name'])):
        if county['properties']['name'][m:m+6] == 'County':
            county_names.append(county['properties']['name'][0:m-1])
            county_names_dict[county['properties']['name'][0:m-1]] = county['properties']['name']
            
print county_names






# =============================================================================
# #visualization
# for col in laws.columns:
#     laws[col] = laws[col].astype(str)
# 
# ##gun laws score
# scl=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'],
#         [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'],
#         [0.6666666666666666, 'rgb(171,217,233)'],[0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'],
#         [1.0, 'rgb(49,54,149)']]
# laws['text'] = laws['state'] + '<br>' +\
#     'score: '+laws['curved score']+'<br>'+'grade: '+laws['grade']+'<br>'+\
#     'gun death rate: ' + laws['2010 gun death rate']
# 
# data = [ dict(
#         type='choropleth',
#         colorscale = scl,
#         autocolorscale = False,
#         locations = laws['code'],
#         z = laws['curved score'].astype(float),
#         locationmode = 'USA-states',
#         text = laws['text'],
#         marker = dict(
#             line = dict (
#                 color = 'rgb(255,255,255)',
#                 width = 2
#             ) ),
#         colorbar = dict(
#             title = "score")
#         ) ]
# 
# layout = dict(
#         title = 'gun laws score',
#         geo = dict(
#             scope='usa',
#             projection=dict( type='albers usa' ),
#             showlakes = True,
#             lakecolor = 'rgb(255, 255, 255)'),
#              )
#     
# fig = dict( data=data, layout=layout )
# py.iplot( fig, filename='d3-cloropleth-map' )
# 
# 
# ##death rate
# scl = [[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], 
#               [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], 
#               [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
# laws['text'] = laws['state'] + '<br>' +\
#     'score: '+laws['curved score']+'<br>'+'grade: '+laws['grade']+'<br>'+\
#     'gun death rate: ' + laws['2010 gun death rate']
# 
# data = [ dict(
#         type='choropleth',
#         colorscale = scl,
#         autocolorscale = False,
#         locations = laws['code'],
#         z = laws['2010 gun death rate'].astype(float)/100.0,
#         locationmode = 'USA-states',
#         text = laws['text'],
#         marker = dict(
#             line = dict (
#                 color = 'rgb(255,255,255)',
#                 width = 2
#             ) ),
#         colorbar = dict(
#             title = "death rate")
#         ) ]
# 
# layout = dict(
#         title = '2010 gun death rate',
#         geo = dict(
#             scope='usa',
#             projection=dict( type='albers usa' ),
#             showlakes = True,
#             lakecolor = 'rgb(255, 255, 255)'),
#              )
#     
# fig = dict( data=data, layout=layout )
# py.iplot( fig, filename='d3-cloropleth-map' )
# 
# =============================================================================
