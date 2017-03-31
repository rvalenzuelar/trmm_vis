'''
	Plot TRMM product automagically

	Raul Valenzuela
	December 2015
	raul.valenzuela@colorado.edu
'''

import plot_trmm
import matplotlib.pyplot as plt
from os.path import basename
from glob import glob

base_dir = '/home/rvalenzuela/Data/new_TRMM/'

# date = '20020602'
# date = '20020603'
# date = '20020604'
# date = '20020605'

# date = '20050625'
date = '20050626'
# date = '20050627'

# date = '20010718'
# date = '20020525'
# date = '20060711'
# date = '20000623'
# date = '20030520'

# date = '20040802'
# date = '20040801'

product = {'2A25':'rainrate'}  # [mm/hr]
# product = {'2A25':'dBZnearSurf'}
# product = {'1B01':''} # IR channel
# product = {'1C21':''} # radar reflectivity


def main():

    datef = get_filenames(base_dir, product, date)

    # for f in datef:
        # plot_trmm.product(product, f)

    # plot_trmm.fuse(product, datef)

    plot_trmm.daily_accum2A25(datef)

    # pngname = basename(datef[0])[:-3] + 'fuse.png'
    # plt.savefig('./figs/'+pngname,
    #             dpi=300, bbox_inches='tight')

def get_filenames(base_dir, product, date):

    # path = base_dir + date[:4] + '/' \
    #            + product + '.' + date + '*'

    path = base_dir + product.keys()[0] + '.' + date + '*'

    out = glob(path)
    out.sort()
    return out


main()
