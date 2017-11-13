#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 20:29:45 2017

@author: Xin
"""
import pandas as pd
import plotly.plotly as py

seleCol =  range(40,45)
seleCol.append(1)

laws = pd.read_csv('laws.csv', delimiter=' ', header=None, usecols=seleCol)

laws.columns = ['state', 'total score','curved score','grade','2010 gun death rate','2009 gun export rates']

laws.set_index('state', inplace = True)

#laws.to_csv('laws_filter.csv')

laws = pd.read_csv('laws_filter.csv', delimiter=',')

laws.sort_values(laws.columns[0], ascending = True, inplace = True)

laws.reset_index(drop=True, inplace = True)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

laws['code']=df['code']

laws = laws[['code','state', 'total score','curved score','grade',
             '2010 gun death rate','2009 gun export rates']]


for col in laws.columns:
    laws[col] = laws[col].astype(str)

##gun laws score
scl=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'],
        [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'],
        [0.6666666666666666, 'rgb(171,217,233)'],[0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'],
        [1.0, 'rgb(49,54,149)']]
laws['text'] = laws['state'] + '<br>' +\
    'score: '+laws['curved score']+'<br>'+'grade: '+laws['grade']+'<br>'+\
    'gun death rate: ' + laws['2010 gun death rate']

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = laws['code'],
        z = laws['curved score'].astype(float),
        locationmode = 'USA-states',
        text = laws['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "score")
        ) ]

layout = dict(
        title = 'gun laws score',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )
py.iplot( fig, filename='d3-cloropleth-map' )


##death rate
scl = [[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], 
              [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], 
              [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']]
laws['text'] = laws['state'] + '<br>' +\
    'score: '+laws['curved score']+'<br>'+'grade: '+laws['grade']+'<br>'+\
    'gun death rate: ' + laws['2010 gun death rate']

data = [ dict(
        type='choropleth',
        colorscale = scl,
        autocolorscale = False,
        locations = laws['code'],
        z = laws['2010 gun death rate'].astype(float)/100.0,
        locationmode = 'USA-states',
        text = laws['text'],
        marker = dict(
            line = dict (
                color = 'rgb(255,255,255)',
                width = 2
            ) ),
        colorbar = dict(
            title = "death rate")
        ) ]

layout = dict(
        title = '2010 gun death rate',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa' ),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
             )
    
fig = dict( data=data, layout=layout )
py.iplot( fig, filename='d3-cloropleth-map' )

