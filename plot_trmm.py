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


def product(prod, datef):

    print datef

    if prod == '1B01':
        lons, lats, dates, data = read_trmm.retrieve_1B01(datef)
    elif prod == '1C21':
        # read_trmm.print_dataset_1C21(base_dir,datef)
        lons, lats, dates, data = read_trmm.retrieve_1C21(datef)
    elif prod == '2A12':
        lons, lats, dates, data = read_trmm.retrieve_2A12(datef)
    elif prod == '2A25':
        print datef
        lons, lats, dates, data = read_trmm.retrieve_2A25(datef)

    ''' create figure and axes instances  '''
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    ''' create eq distance cylindrival Basemap instance '''
    m = Basemap(projection='cyl',
                llcrnrlat=-40, urcrnrlat=-20,
                llcrnrlon=-90, urcrnrlon=-60,
                # llcrnrlat=-50, urcrnrlat=-10,
                # llcrnrlon=-100, urcrnrlon=-50,
                # llcrnrlat=-90,urcrnrlat=90,\
                # llcrnrlon=-180,urcrnrlon=180,\
                resolution='l')

    ''' draw lines '''
    m.drawcoastlines()
    m.drawcountries()

    ''' draw parallels '''
    parallels = np.arange(-90., 90, 10.)
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    ''' draw meridians '''
    meridians = np.arange(0., 360., 10.)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

    ''' colormesh '''
    if prod == '1B01':
        # print lats
        cmap = get_IRcolors()
        m.pcolormesh(lons, lats, data - 273.15, vmin=-70, vmax=30, latlon=True, cmap=cmap)
    else:
        vmin = 0
        vmax = 50
        data[data < 10.] == np.nan
        # m.pcolormesh(lons, lats, data, latlon=True,cmap='gray_r',vmin=vmin, vmax=vmax)
        m.pcolormesh(lons, lats, data, latlon=True, cmap='nipy_spectral', vmin=vmin, vmax=vmax)

    m.colorbar()

    plt.suptitle('IR-channel date: ' + dates[0].strftime('%Y-%b-%d') \
                 + '\nTime: ' + dates[0].strftime('%H:%M') + '-' \
                 + dates[1].strftime('%H:%M') + ' UTC')


def fuse(product,datef,accum=False):

    from scipy.spatial import cKDTree

    data_list = list()
    lons_list = list()
    lats_list = list()

    for n,f in enumerate(datef):
        if product.keys()[0] == '1B01':
            out = read_trmm.retrieve_1B01(f)
        elif product.keys()[0] == '1C21':
            out = read_trmm.retrieve_1C21(f)
        elif product.keys()[0] == '2A25':
            out = read_trmm.retrieve_2A25(f, product['2A25'])
        lons, lats, dates, data = out

        if n == 0:
            beg = dates[0]
        if n == len(datef)-1:
            end = dates[1]

        data_list.extend(data.flatten())
        lons_list.extend(lons.flatten())
        lats_list.extend(lats.flatten())

    ''' interpolation using nearest neighbor '''
    coords = zip(lons_list, lats_list)
    tree = cKDTree(coords)
    cols = 700
    rows = 500
    lon_target = np.linspace(-90,-60,num=cols)
    lat_target = np.linspace(-20,-40,num=rows)
    long, latg = np.meshgrid(lon_target,lat_target)
    loni = long.flatten()
    lati = latg.flatten()
    coordsi = zip(loni,lati)
    dist, idx = tree.query(coordsi, k=8, eps=0, p=1,
                           distance_upper_bound=5)
    ig = np.empty((rows*cols,))
    data_np = np.array(data_list)
    for n in range(idx.shape[0]):
        if np.min(dist[n])>0.2:
            ig[n] = -9999
        else:
            if product.keys()[0] == '1B01':
                ig[n] = np.nanmin(data_np[idx[n]])
            elif product.keys()[0] == '1C21':
                ig[n] = np.nanmax(data_np[idx[n]])
            elif product.keys()[0] == '2A25':
                ig[n] = np.nanmax(data_np[idx[n]])
    mig = np.ma.masked_values(ig,-9999)
    mig = mig.reshape((rows,cols))


    if product.keys()[0] == '2A25' and accum is True:
        return mig, beg, end, latg, long

    plot_map(product, mig,
             datef, beg, end, latg, long)


def daily_accum2A25(datef):

    out = fuse({'2A25':'rainrate'}, datef, accum=True)
    grid, beg, end, latg, long = out
    delta = (end-beg).seconds/3600.  #hours
    gridAccum = grid * delta

    plot_map({'2A25':'accum'},gridAccum,
             datef, beg, end, latg, long)


def plot_map(product, mig, datef, beg, end, latg, long):

    ''' create eq distance cylindrival Basemap instance '''
    fig, ax = plt.subplots()

    m = Basemap(projection='cyl',
                llcrnrlat=-40, urcrnrlat=-20,
                llcrnrlon=-90, urcrnrlon=-60,
                # llcrnrlat=-90,urcrnrlat=90,\
                # llcrnrlon=-180,urcrnrlon=180,\
                resolution='l')

    ''' draw lines '''
    m.drawcoastlines()
    m.drawcountries()
    ''' draw parallels '''
    parallels = np.arange(-90., 90, 10.)
    m.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=10)
    ''' draw meridians '''
    meridians = np.arange(0., 360., 10.)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=10)

    if product.keys()[0] == '1B01':
        cmap = get_IRcolors()
        datagrid = mig - 273.15
        vmin = -70
        vmax = 30
        titletxt = 'IR composite'
    if product.keys()[0] == '1C21':
        cmap = 'nipy_spectral'
        datagrid = mig
        vmin = -20
        vmax = 50
        titletxt = 'Radar reflectivity'
    elif product.keys()[0] == '2A25':
        cmap = 'nipy_spectral'
        datagrid = mig
        if product['2A25'] == 'dBZnearSurf':
            vmin, vmax, titletxt = [-10, 50, 'Relfectivity near surface (dBZ) ']
        elif product['2A25'] == 'rainrate':
            vmin, vmax, titletxt = [0, 15, 'Rainfall rate (mm/hr) ']
        elif product['2A25'] == 'accum':
            vmin, vmax, titletxt = [0, 120, 'Rainfall accumulation ']

    ''' plot '''
    m.pcolormesh(long, latg, datagrid, vmin=vmin, vmax=vmax,
                 latlon=True, cmap=cmap)

    fmt = '%H:%M UTC %d-%b-%Y'
    plt.suptitle(titletxt + ' (n={})'.format(len(datef)) \
                 + '\nBeg: ' \
                 + beg.strftime(fmt) \
                 + '\nEnd: ' \
                 + end.strftime(fmt))

    m.colorbar()

def get_IRcolors():

    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    colors2 = plt.cm.binary(np.linspace(0.5, 1., 128))
    colors1 = plt.cm.rainbow_r(np.linspace(0, 1, 128))
    colors = np.vstack((colors1, colors2))
    mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)

    return mymap
