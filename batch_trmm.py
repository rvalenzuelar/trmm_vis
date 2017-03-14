'''
	Plot TRMM product automagically

	Raul Valenzuela
	December 2015
	raul.valenzuela@colorado.edu
'''

import plot_trmm

from glob import glob

base_dir = '/home/rvalenzuela/Data/TRMM/2002'

# date='19980926'
# date='19980603'
# date='19990628'
# date='19990629'
date = '20021231'

# product='2A25'
product = '1B01'


# 1B01.20021231.29239.7.HDF

def main():
    datef = get_filenames(base_dir, product, date)

    for f in datef:
        plot_trmm.product(product, f)


def get_filenames(base_dir, product, date):
    out = glob(base_dir + '/' + product + '.' + date + '*')
    out.sort()
    return out


main()
