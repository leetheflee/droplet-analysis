import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib

font = {'family' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)

plt.rcParams["figure.figsize"] = (10, 8)

fil = 'pfrpb1.txt'

if not os.path.isdir(fil.split('.')[0]):
    os.mkdir(fil.split('.')[0])

chars = 'CWYFMLIVAGPQNTSEDKHR'

lines = (open(fil).read().strip() + '\n').split('\n')

valids = []
headers = []

s = ""
in_s = False
for line in lines:
    if '>' in line:
        if '|' in line:
            headers.append(line.split('|')[2].strip().replace('/', '_').replace(':','_'))
        else:
            headers.append(line[1:])
        in_s = True
    elif line == '':
        in_s = False
        if len(s) > 0:
            valids.append(s)
        s = ''
    elif in_s:
        s += line

for k, line in enumerate(valids):
    print(headers[k], '%d / %d' % (k+1, len(valids)))

    arr = np.zeros((len(chars), len(line)))

    for i, c1 in enumerate(chars):
        a = arr[i]

        for j, c2 in enumerate(line):
            if c1 == c2:
                a[j] = 1.0

    plt.imshow(arr, aspect='auto', cmap='binary', interpolation='none')
    plt.yticks(np.arange(len(chars)), list(chars))

    plt.ylim((len(chars) - 0.5, -0.5))
    plt.xlim((-2.5, len(line) + 1.0))

    plt.savefig(fil.split('.')[0] + '/' + headers[k]+'.png')
    plt.show()
    plt.close()