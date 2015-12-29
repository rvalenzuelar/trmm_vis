'''
	Plot TRMM product automagically

	Raul Valenzuela
	December 2015
	raul.valenzuela@colorado.edu
'''

import plot_trmm

from glob import glob

base_dir = '/home/raul/TRMM/'

# date='19980926'
# date='19980603'
date='19990628'
# date='19990629'

product='2A25'
# product='1B01'

def main():

	datef = get_filenames(base_dir,product,date)

	for f in datef:
		plot_trmm.product(product,f)


def get_filenames(base_dir,product,date):

	
	out=glob(base_dir+'/'+product+'.'+date+'*')
	out.sort()
	return out

main()