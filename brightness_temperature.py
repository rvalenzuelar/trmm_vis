'''
	Compute brighness temperature
	given a radiance I and 
	wavelength wl 

	Raul Valenzuela
	December, 2015
'''

import numpy as np 


def BT(*arg):


	I=arg[0] 	#[J s^-1 m^-3]
	wl=arg[1]	#[m]

	' set some constants '
	h =  6.626e-34     # /* Plank's const in Js */
	k =  1.38e-23      # /* Boltzmanns const in J/K */
	c =  2.992e8     # /* speed of light in m/s */


	f = (2 * h * c**2) / (I * wl**5)
	BT = (h*c)/(np.log(f+1)*k*wl)

	return BT