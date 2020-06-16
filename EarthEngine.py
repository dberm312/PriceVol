# -*- coding: utf-8 -*-
#%%
import pandas as pd
import ee
ee.Initialize()
#%%
fips = '17037'
collection = ee.ImageCollection("USDA/NASS/CDL").select('cropland').filter(ee.Filter.date('2018-01-01', '2019-12-31')).first()
geo  = ee.FeatureCollection("TIGER/2018/Counties")
geo = geo.filter(ee.Filter.eq('STATEFP',fips[:2]))
geo = geo.filter(ee.Filter.eq('COUNTYFP',fips[2:]))
collection = collection.reduceRegion(
    reducer=ee.Reducer.autoHistogram(),
    geometry=geo,
    scale = 1000)
land = collection.getInfo()
land  = pd.DataFrame(land['cropland']).set_index(0)
temp = pd.read_html('https://developers.google.com/earth-engine/datasets/catalog/USDA_NASS_CDL#bands')[1].set_index('Value')
land = land.join(temp['Description']).set_index('Description').sort_values(1,ascending=False)
land.to_csv('Data/land.csv')