'''
Need transform HDF4 to HDF5 using
h4toh5 tool

Raul Valenzuela
December 2015
'''

import matplotlib.pyplot as plt
import numpy as np
import read_trmm

from mpl_toolkits.basemap import Basemap, cm, shiftgrid
from datetime import datetime
from os.path import basename

# base_dir = '/home/raul/TRMM/'

# datef='19971231.00527.7.HDF'
# datef='19971231.00528.7.HDF'
# datef='19971223.00405.7.HDF'
# datef='19980621.03241.7.HDF'
# datef='19980925.04753.7.HDF'

def product(prod,datef):

	if prod == '1B01':
		lons,lats,dates,data = read_trmm.retrieve_1B01(datef)
	elif prod == '1C21':
		# read_trmm.print_dataset_1C21(base_dir,datef)
		lons,lats,dates,data = read_trmm.retrieve_1C21(datef)
	elif prod == '2A12':
		lons,lats,dates,data = read_trmm.retrieve_2A12(datef)
	elif prod == '2A25':
		lons,lats,dates,data = read_trmm.retrieve_2A25(datef)

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



	''' colormesh '''
	if prod == '1B01':

		cmap = get_IRcolors()
		m.pcolormesh(lons, lats, data-273.15, vmin=-70,vmax=30,latlon=True,cmap=cmap)
	else:
		vmin=0
		vmax=50
		data[data<10.]==np.nan
		# m.pcolormesh(lons, lats, data, latlon=True,cmap='gray_r',vmin=vmin, vmax=vmax)
		m.pcolormesh(lons, lats, data, latlon=True,cmap='nipy_spectral',vmin=vmin, vmax=vmax)
	
	cb = m.colorbar()

	plt.suptitle('Date: '+dates[0].strftime('%Y-%b-%d')\
				+'\nTime: '+dates[0].strftime('%H:%M')+'-'\
				+dates[1].strftime('%H:%M')+' UTC')


	# print data
	# fig,ax=plt.subplots()
	# im=ax.imshow(data,interpolation='none',aspect='auto')
	# plt.colorbar(im)
	# plt.draw()
	# plt.show()

	pngname=basename(datef)[:-3]+'png'
	plt.savefig(pngname, bbox_inches='tight')

def get_IRcolors():

	import matplotlib.pyplot as plt
	import matplotlib.colors as mcolors

	colors2 = plt.cm.binary(np.linspace(0.5, 1., 128))
	colors1 = plt.cm.rainbow_r(np.linspace(0, 1, 128))
	colors = np.vstack((colors1, colors2))
	mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

	return mymap