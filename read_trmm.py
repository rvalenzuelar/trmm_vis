'''
	Read TRMM hdf4 format

	Raul Valenzuela
	December, 2015
	raul.valenzuela@colorado.edu
'''

from pyhdf.SD import SD, SDC
from datetime import datetime
from brightness_temperature import BT
import numpy as np

def retrieve_1B01(*arg):
	
	hdf = SD(arg[0], SDC.READ)

	Lon, Lat, date_beg, date_end, st, en = retrieve_ancillary(hdf)

	' calculate brightness temperature from IR channel'
	'**************************************************'
	chIR=hdf.select('channels')[st:en,:,4] # [mW cm^-2 micrometer^-1 sr^-1]
	I = chIR * 1e-3 * (100**2) * 1e6 #[J s^-1 m^-3]
	wavelength=12e-6 #[m]
	T=BT(I, wavelength)

	return 	Lon[st:en,:], Lat[st:en,:],[date_beg,date_end], T


def retrieve_1C21(*arg):

	hdf = SD(arg[0], SDC.READ)

	Lon, Lat, date_beg, date_end, st, en = retrieve_ancillary(hdf)

	' osRain includes rays #20 to #30'
	# data=hdf.select('osRain')[st:en,:,0] # [dBZ]

	' normalSample correspond to dBZ in 140 levels'
	data=hdf.select('normalSample')[st:en,:,103] # [dBZ*100]
	data=data.astype(float)
	data[data<=-32700.]=np.nan
	data=data/100. #[dBZ]

	foo=hdf.select('normalSample')[:,:,:]
	print foo.shape
	# return 	Lon[:,20:31], Lat[:,20:31], [date_beg,date_end], osRain

	data = np.ma.masked_array(data, np.isnan(data))
	return 	Lon[st:en,:], Lat[st:en,:], [date_beg,date_end], data

def retrieve_2A12(*arg):

	hdf = SD(arg[0], SDC.READ)

	Lon, Lat, date_beg, date_end, st, en = retrieve_ancillary(hdf)

	# data=hdf.select('windSpeed')[st:en,:] # [m/s]
	# data[data==-9999.9]=np.nan

	# data=hdf.select('surfaceRain')[st:en,:] # [mm/hr]
	# data[data==-9999.9]=np.nan

	# data=hdf.select('surfacePrecipitation')[st:en,:] # [mm/hr]
	# data[data==-9999.9]=np.nan

	# data=hdf.select('freezingHeight')[st:en,:] # [m]
	# data[data==-9999.9]=np.nan

	# data=hdf.select('cloudWaterPath')[st:en,:] # [kg/m2]
	# data[data==-9999.9]=np.nan

	# data=hdf.select('rainWaterPath')[st:en,:] # [kg/m2]
	# data[data==-9999.9]=np.nan

	# data=hdf.select('iceWaterPath')[st:en,:] # [kg/m2]
	# data[data==-9999.9]=np.nan

	# data=hdf.select('totalPrecipitableWater')[st:en,:] # [mm]
	# data[data==-9999.9]=np.nan

	return 	Lon, Lat, [date_beg,date_end], data

def retrieve_2A25(*arg):

	hdf = SD(arg[0], SDC.READ)

	Lon, Lat, date_beg, date_end, st, en = retrieve_ancillary(hdf)

	# data=hdf.select('nearSurfZ')[:,:] # [dBZ]
	data=hdf.select('nearSurfZ')[st:en,:] # [dBZ]
	data[data==-99.99]=np.nan

	# data=hdf.select('nearSurfRain')[st:en,:] # [mm/hr]
	# data[data==-99.99]=np.nan

	# data=hdf.select('zeta')[st:en,:,1] # [mm/hr]
	# data[data==-99.99]=np.nan

	# data=hdf.select('correctZFactor')[st:en,:,10] # [dBZ]

	# data=hdf.select('rainFlag')[st:en] 

	# data=hdf.select('zmmax')[st:en,:] # [dBZ]

	data = np.ma.masked_array(data, np.isnan(data))
	return 	Lon[st:en,:], Lat[st:en,:], [date_beg,date_end], data
	# return 	Lon, Lat, [date_beg,date_end], data

def print_dataset_1B01(*arg):

	FILE_NAME=arg[0]+'1B01.'+arg[1]
	hdf = SD(arg[0], SDC.READ)

	'List available SDS datasets'
	for ds in hdf.datasets():
		print ds

def print_dataset_1C21(*arg):

	FILE_NAME=arg[0]+'1C21.'+arg[1]
	print FILE_NAME
	hdf = SD(FILE_NAME, SDC.READ)

	'List available SDS datasets'
	for ds in hdf.datasets():
		print ds

def print_dataset_2A12(*arg):

	FILE_NAME=arg[0]+'1B01.'+arg[1]
	hdf = SD(FILE_NAME, SDC.READ)

	'List available SDS datasets'
	for ds in hdf.datasets():
		print ds

def print_dataset_2A25(*arg):

	FILE_NAME=arg[0]+'1C21.'+arg[1]
	print FILE_NAME
	hdf = SD(FILE_NAME, SDC.READ)

	'List available SDS datasets'
	for ds in hdf.datasets():
		print ds

def retrieve_ancillary(hdf):

	Latitude = hdf.select('Latitude')[:]
	Longitude = hdf.select('Longitude')[:]

	' find indices of lon corresponding to Chile'
	lon1D = np.amax(Longitude,axis=1)
	idxsub = np.where((lon1D >= -90)&(lon1D <= -60))
	st=idxsub[0][0]
	en=idxsub[0][-1]

	' get datetime of swath'
	Yr=hdf.select('Year')[0]
	Mo=hdf.select('Month')[0]
	Dy=hdf.select('DayOfMonth')[0]
	Hr=hdf.select('Hour')[st:en]
	Mn=hdf.select('Minute')[st:en]
	date_beg=datetime(Yr,Mo,Dy,Hr[0],Mn[0],0)
	date_end=datetime(Yr,Mo,Dy,Hr[-1],Mn[-1],0)

	return Longitude, Latitude, date_beg, date_end, st, en
