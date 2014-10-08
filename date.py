## pip install py-dateutil
# -*- coding: utf-8 -*-

from os import path, mkdir
from datetime import date as D
from dateutil.rrule import rrule, DAILY
from collections import OrderedDict as OD

'''
init should be a dict with a struct as:
   init['year'] a tuple of academic year: (datetime.date(start), datetime.date(finish)) 
   init['excludes'] a list of tuple pairs: [(datetime.date(exclude_start1), datetime.date(exclude_finish1))]
       where datetime.date(fmt) with format fmt=%Y, %m, %d
   init['classes'] a dict of dictionaries with a struct as:
        init['classes']['class_name1'] is a dict with struct as:
            {isoweekday1: numberOfLesson1, isoweekday_n: numberOfLesson_n}
                where isoweekday_n in [1..7]
'''
init = {
        'year': (D(2014, 9, 1), D(2015, 5, 31)),           

        'excludes': [
                    (D(2014, 11, 3), D(2014, 11, 9)),
                    (D(2014, 12, 29), D(2015, 1, 11)),
                    (D(2015, 2, 23), D(2015, 2, 23)),
                    (D(2015, 3, 9), D(2015, 3, 9)),
                    (D(2015, 3, 23), D(2015, 3, 29)),
                    (D(2015, 5, 1), D(2015, 5, 4)),
                    (D(2015, 5, 11), D(2015, 5, 11)),
                    (D(2015, 5, 25), D(2015, 5, 31))
                    ],

        'classes': {
                    '3А': {2: 1, 4: 2, 5: 2},
                    '3Б': {2: 3, 4: 6, 5: 4},
                    '3В': {3: 1, 5: 3},

                    '4А': {1: 4, 2: 5, 3: 6, 4: 5},
                    '4Б': {1: 1, 3: 3, 4: 1, 5: 5},

                    '6Б': {1: 3, 3: 5, 4: 3},
                    '6В': {1: 5, 2: 4, 5: 6},
                    }
        }

DAYS = {1: 'Mon',
        2: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat',
        7: 'Sun'}

def GetSchoolTimeTable(init):

    out = 'out'

    if 'year' in init and 'excludes' in init and 'classes' in init:
        
        for class_name in init['classes'].keys():
            d = dict()
            lessCounter = 0

            for dt in rrule(DAILY, dtstart=init['year'][0], until=init['year'][1]):
                dt = dt.date()
                _, _, weekday = dt.isocalendar()

                if weekday in init['classes'][class_name].keys():

                    if any(x[0] <= dt <= x[1] for x in init['excludes']):
                        lessCounter += 1

                    else:
                        d[dt.strftime('%Y.%m.%d')] = '{}-{}'.format(DAYS[weekday], init['classes'][class_name][weekday]) 

            if not path.exists(out):
                mkdir(out)

            with open(path.join(out, '{}.txt'.format(class_name)), 'w') as f:
                import datetime

                od = OD(sorted(d.items()))

                f.write(
                    'Class: {};\tTotal hours: {};\tLost hours: {}\nExcludes:\n\t{}\n\n{}'.format(
                        class_name,
                        len(d.keys()),
                        lessCounter,
                        str.join('\n\t', (str.format('{} -> {}', *x) for x in init['excludes'])),
                        str.join('\n', (
                            str.format('{}\t{}', v, datetime.datetime.strptime(k, '%Y.%m.%d').strftime('%d.%m.%Y')) for k, v in od.items()
                            ))
                    )
                )

if __name__ == '__main__':
    GetSchoolTimeTable(init)
