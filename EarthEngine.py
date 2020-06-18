# -*- coding: utf-8 -*-
#%%
import pandas as pd
import ee
ee.Initialize()
#%%
def fips2landuse(fips):
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
    
    land.columns = [fips]
    land = land[land.index.isin(['Soybeans','Corn','Winter Wheat'])]
    land = land[~land.index.isna()]
    land = land/land.sum()
    return(land)
    #land.to_csv('Data/land.csv')
#%%
out = []
lst = ['17055', '26161', '47147', '26151', '21211', '26147', '26145', '31095', '39011', '21219', '47099', '21221', '21225', '47079', '47075', '31067', '39031', '39033', '39037', '51165', '47051', '39045', '47033', '51193', '39097', '18113', '39137', '29183', '39149', '26157', '18183', '39171', '51057', '18001', '17189', '18003', '37035', '37057', '37059', '21033', '20139', '18031', '17177', '20115', '20113', '18037', '37107', '17163', '20079', '18059', '51001', '21093', '21105', '37151', '37159', '31151', '51033', '37179', '21141', '47183', '26115', '47053', '17037', '18145', '29057', '17133', '26087', '24021', '26075', '26091', '26073', '29073', '26025', '26059', '26067', '26063', '26065', '26099', '31059', '39175', '18177', '17075', '31099', '31097', '18027', '37053', '17121', '39039', '51133', '17119', '26093', '39029', '21227', '20013', '21213', '18127', '18047', '37135', '17027', '21059', '37147', '37157', '20045', '55117', '20121', '37191', '37195', '37081', '21047', '18129', '31133', '55101', '39065', '31127', '55071', '39119', '55039', '24011', '18175', '46015', '39159', '46023', '39091', '39161', '17201', '39165', '29141', '47017', '17059', '39147', '18095', '39143', '39071', '17193', '29133', '55025', '55027', '47031', '17141', '37029', '18181', '28053', '21199', '37083', '5095', '46059', '31169', '55111', '24013', '5107', '39155', '17089', '24029', '18061', '39169', '5147', '55131', '55021', '18057', '37131', '55135', '47149', '5031', '46125', '5067', '39023', '31081', '28151', '39083', '31065', '28011', '21231', '39101', '39075', '18135', '31041', '37025', '31035', '39051', '39021', '37117', '39107', '51097', '18091', '26015', '37073', '39103', '17061', '39109', '26081', '31109', '18085', '17033', '17049', '37001', '21027', '37015', '37077', '26045', '37061', '20191', '26057', '17169', '37101', '17179', '26049', '42027', '17173', '37079', '39173', '37133', '39077', '36065', '45075', '47047', '39057', '39063', '45085', '39069', '39113', '45051', '39125', '39129', '39133', '39135', '17135', '39157', '17137', '17125', '39027', '37143', '26027', '17095', '42071', '37163', '37167', '42077', '17157', '37197', '47167', '45033', '26155', '17105', '39003', '39007', '42133', '47097', '45027', '17203', '18139', '31147', '51061', '18157', '20125', '18087', '51113', '18159', '18099', '18075', '31137', '36011', '18163', '18169', '55087', '31019', '18107', '18051', '20149', '31083', '31155', '31131', '29186', '31129', '29207', '20127', '31061', '31159', '24019', '24025', '42119', '18063', '37145', '51007', '17113', '18173', '20085', '39041', '29099', '17111', '20003', '17159', '55115', '31135', '55127', '21185', '26111', '47131', '39001', '47119', '51101', '47113', '21163', '51047', '55049', '47103', '21149', '51171', '51119', '42075', '21075', '21067', '29051', '46115', '18103', '31001', '37013', '28163', '42099', '37065', '42001', '45061', '48277', '36067', '39095', '18011', '17117', '17123', '39099', '24039', '29107', '45049', '18033', '28133', '45041', '29159', '55105', '28083', '39123', '28027', '51550', '20117', '45031', '39141', '36117', '17103', '42067', '31101', '26117', '26017', '26005', '18071', '17007', '39047', '29151', '31023', '5055', '18069', '51159', '17017', '20005', '5021', '17143', '45005', '51137', '47009', '17021', '39015', '31111', '17149', '18015', '21039', '26011', '21017', '45069', '42029', '21101', '18039', '55055', '18137', '17083', '55083', '42005', '29011', '55139', '17079', '18035', '37017', '17035', '37097', '20177', '55043', '28135', '24047', '48147', '42055', '24035', '37069', '29173', '29007', '47015', '17053', '46135', '40035', '17183', '47003', '13033', '46067', '46123', '20157', '21009', '18005', '20205', '20173', '28137', '20181', '36069', '20111', '55073', '29111', '40071', '29163', '26037', '29019', '17145', '17153', '55137', '5077', '17011', '55047', '55045', '39167', '17025', '47165', '45009', '26149', '39017', '37187', '17073', '17167', '18067', '37177', '51131', '31029', '37155', '17067', '18049', '21137', '17099', '39139', '29131', '39151', '55015', '24045', '46003', '46005', '46043', '17009', '55065', '18147', '18079', '29195', '48139', '26023', '21155', '31141', '51037', '28107', '18065', '31181', '21103', '37137', '20061', '21083', '20123', '42061', '20133', '20143', '18023', '18019', '18017', '37049', '17185', '20169', '18141', '17195', '17045', '20031', '42041', '20021', '31063', '26139', '31025', '26123', '39089', '42085', '18081', '18083', '40103', '29069', '40115', '31073', '42073', '20015', '29033', '51800', '29101', '17015', '17041', '42095', '42109', '17057', '42087', '28125', '17091', '28087', '26077', '29071', '42019', '28095', '45003', '17001', '29037', '29025', '17019', '36063', '20095', '31145', '5117', '5093', '31085', '13163', '51081', '46085', '31089', '28055', '46077', '17165', '46119', '31047', '46051', '55005', '29147', '37095', '20131', '51181', '18021', '29117', '26107', '37045', '36037', '13251', '31093', '47125', '55057', '55059', '31037', '51036', '24041', '21183', '38071', '17023', '31125', '29031', '37139', '38035', '20035', '13193', '17029', '17081', '17077', '20087', '21035', '36051', '36101', '36099', '36055', '40125', '28103', '31121', '42107', '17127', '45089', '46009', '46011', '29083', '29137', '29143', '29157', '29175', '39145', '17101', '38093', '29219', '37109', '17139', '31057', '29109', '46107', '39019', '5041', '5069', '39117', '26105', '17197', '36053', '37007', '29047', '39043', '29127', '38029', '18151', '18179', '18041', '38003', '18089', '39127', '40101', '17171', '17051', '21055', '55077', '47123', '55061', '47115', '55019', '45007', '21007', '47055', '24043', '17047', '10005', '51175', '51143', '20011', '46057', '55095', '21233', '42037', '22009', '21161', '5035', '26129', '46013', '22025', '19177', '5017', '37171', '22035', '36121', '1083', '36123', '42043', '54037', '22029', '17199', '55141', '29001', '48357', '38017', '31107', '22065', '24015', '46049', '19101', '46061', '20147', '47177', '22077', '34033', '20059', '39049', '34019', '39005', '17107', '29095', '55081', '42063', '42097', '13069', '19111', '21029', '37051', '13253', '37041', '37033', '55109', '55123', '38081', '47077', '55009', '18119', '45025', '20201', '42049', '18131', '20145', '46129', '37091', '48481', '18053', '17147', '18009', '22067', '17191', '21217', '19057', '47117', '22041', '10001', '21239', '38005', '10003', '21069', '47069', '21085', '31185', '47045', '21207', '38021', '29041', '40097', '29049', '45035', '29189', '45029', '18153', '31087', '20009', '29155', '51085', '1089', '55029', '42011', '17071', '22123', '29103', '42093', '26021', '22107', '1077', '55075', '18121', '55033', '17115', '42129', '17181', '42039', '47111', '29135', '37047', '45067', '38101', '17093', '22097', '20069', '31143', '31139', '51067', '5085', '51083', '17065', '29021', '31163', '26121', '19103', '34005', '31113', '48341', '46027', '5063', '42017', '17131', '31027', '13273', '5111', '48181', '48065', '21049', '29061', '55103', '37103', '29017', '31175', '18117', '21031', '19183', '5121', '20047', '20063', '20141', '36029', '31079', '31011', '37037', '28033', '29201', '29165', '21001', '55001', '29139', '51073', '17063', '42079', '38063', '46079', '38091', '17129', '21215', '40135', '17109', '46021', '22083', '46087', '26007', '38097', '17013', '38099', '38103', '39009', '39093', '38073', '17005', '46025', '24031', '46097', '28089', '18133', '5123', '20073', '48117', '13107', '34011', '51149', '29113', '19107', '21209', '48145', '31177', '22079', '29097', '22069', '20151', '29053', '19115', '20163', '39025', '17085', '29087', '26141', '42057', '1049', '38039', '51109', '46039', '55023', '20001', '17003', '29177', '46073', '31119', '46053', '29015', '19139', '21045', '46037', '28051', '13243', '37165', '20159', '24005', '48421', '45063', '18161', '36045', '13027', '42081', '21179', '47071', '55133', '55121', '48309', '20207', '20203', '31003', '21087', '18029', '29167', '51177', '21145', '20049', '29115', '13131', '18171', '45011', '46083', '13165', '20197', '46109', '46111', '20081', '20099', '31015', '51053', '51031', '28119', '21157', '29003', '13197', '37169', '42051', '18093', '18167', '19051', '31069', '31167', '34015', '20165', '26051', '28013', '39079', '20185', '31077', '51135', '18045', '46035', '17097', '46045', '29125', '37003', '40053', '13267', '38067', '55063', '55053', '38015', '1079', '13087', '17175', '29023', '37093', '28081', '42009', '37125', '19135', '21099', '29027', '18165', '42013', '19145', '21229', '17187', '38045', '40087', '19087', '38043', '31053', '20043', '48153', '42007', '29211', '29205', '38077', '37183', '28049', '34041', '20193', '27145', '46101', '46091', '48085', '31179', '27143', '28143', '19095', '1043', '18007', '48349', '19185', '28093', '55017', '20179', '20175', '5003', '20171', '54003', '20029', '27173', '51107', '27019', '18109', '27085', '31055', '31153', '20037', '51011', '29079', '20023', '31103', '29075', '55013']
for i in range(1000):
    print(i/100)
    if(i==0):
        out=fips2landuse(lst[i])
    else:
        out = out.join(fips2landuse(lst[i].rjust(5,'0')))
out = out.T
out.columns = ['soyb','corn','weat']
out.reset_index().to_csv('Data/land.csv',index=None)