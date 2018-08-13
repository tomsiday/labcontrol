## Config files parser

import configparser
config = configparser.ConfigParser()

config['TWScan'] = {'start': '0',
                    'length': '100',
                    'step': '10',
                    'dwell': '1'}


config['XYScan'] = {'Xstart': '-50',
                    'Ystart': '-50',
                    'Xstep': '10',
                    'Ystep': '10',
                    'dwell': '1'}

with open('scan.conf','w') as configfile:
    config.write(configfile)
