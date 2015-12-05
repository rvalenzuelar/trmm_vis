'''
Need transform HDF4 to HDF5 using
h4toh5 tool

Raul Valenzuela
December 2015
'''

import h5py
import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.basemap import Basemap, cm, shiftgrid
from datetime import datetime


base_directory = '/home/raul/'

product='1B01'
# product='1C21'

# hfile=base_directory+product+'.19971231.00527.7.h5'
hfile=base_directory+product+'.19971231.00528.7.h5'
# hfile=base_directory+product+'.19971223.00405.7.h5'
# hfile=base_directory+product+'.19971223.00405.7.1.h5'

f = h5py.File(hfile, 'r')

swath=f['Swath']
lats=swath['Latitude'][()]
lons=swath['Longitude'][()]


lon1D = np.amax(lons,axis=1)
idxsub = np.where((lon1D>-90)&(lon1D<-60))
st=idxsub[0][0]
en=idxsub[0][-1]

channels=swath['channels']
data=channels[st:en,:,4]
print np.amin(data)
data[data<=-9999.]=np.nan
print np.amin(data)

scantime=swath['ScanTime']
Yr=scantime['Year'][0]
Mo=scantime['Month'][0]
Dy=scantime['DayOfMonth'][0]
Hr=scantime['Hour'][st:en]
Mn=scantime['Minute'][st:en]
date_beg=datetime(Yr,Mo,Dy,Hr[0],Mn[0],0)
date_end=datetime(Yr,Mo,Dy,Hr[-1],Mn[-1],0)


''' create figure and axes instances  '''
fig = plt.figure(figsize=(8,5))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

''' create eq distance cylindrival Basemap instance '''
m = Basemap(projection='cyl',\
			llcrnrlat=-40,urcrnrlat=-20,\
            llcrnrlon=-90,urcrnrlon=-60,\
            # llcrnrlat=-90,urcrnrlat=90,\
            # llcrnrlon=-180,urcrnrlon=180,\
            resolution='l')


''' draw lines '''
m.drawcoastlines()
m.drawcountries()

''' draw parallels '''
parallels = np.arange(-90.,90,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
''' draw meridians '''
meridians = np.arange(0.,360.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)



''' contours '''
# x, y = m(lons, lats) 
# clevs = np.arange(2,40,2)
# cs = m.contourf(x,y,data,clevs,cmap='nipy_spectral')
# cbar = m.colorbar(cs,location='bottom',pad="5%")

''' colormesh '''
m.pcolormesh(lons[st:en,:], lats[st:en,:], data, latlon=True,cmap='gray')
cb = m.colorbar()

plt.suptitle('Date: '+date_beg.strftime('%Y-%b-%d')\
			+'\nTime: '+date_beg.strftime('%H:%M')+'-'\
			+date_end.strftime('%H:%M')+' UTC')



plt.show()
