from glob import glob
import os

target_date = '20050627'

path = '/home/rvalenzuela/download_trmm/*.data'
files = glob(path)
index = [i for i,s in enumerate(files) if target_date[:4] in s]

list_target = list()
with open(files[index[0]],'r') as file:
    for num,line in enumerate(file,1):
        if target_date in line:
            list_target.append(line[:-1])

outdir = '/home/rvalenzuela/Data/new_TRMM/'
auth = ' --user rvalenzuela --password earthData2017#'

# C21=[s for s in list_target if '1C21' in s]

for t in list_target:
    req = 'wget '+t+' '+auth+' -P '+outdir
    os.system(req)

