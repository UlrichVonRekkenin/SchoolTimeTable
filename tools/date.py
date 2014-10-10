# -*- coding: utf-8 -*-

from os import path, mkdir
from datetime import date, timedelta
import calendar

init = {
        'year': ((2014, 9, 1), (2015, 5, 31)),           

        'excludes': [
                    ((2014, 11, 3 ), (2014, 11, 9 )),
                    ((2014, 12, 29), (2015, 1 , 11)),
                    ((2015, 2 , 23), (2015, 2 , 23)),
                    ((2015, 3 , 9 ), (2015, 3 , 9 )),
                    ((2015, 3 , 23), (2015, 3 , 29)),
                    ((2015, 5 , 1 ), (2015, 5 , 4 )),
                    ((2015, 5 , 11), (2015, 5 , 11)),
                    ((2015, 5 , 25), (2015, 5 , 31))
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

def GetSchoolTimeTable(init):

    out = 'out'

    for class_name in init['classes'].keys():
        d = dict()
        lessCounter = 0

        if isinstance(init['year'], tuple):
            dt, finish = date(*init['year'][0]), date(*init['year'][1])

        elif isinstance(init['year'], datetime.date):
            dt, finish = init[0], init[1]        
        
        while dt != finish:

            if dt.isoweekday() in init['classes'][class_name].keys():

                if any(date(*x[0]) <= dt <= date(*x[1]) for x in init['excludes']):
                    lessCounter += 1

                else:
                    d[dt.strftime('%Y.%m.%d')] = '{}-{}'.format(
                            calendar.day_abbr[dt.isoweekday()],
                            init['classes'][class_name][dt.isoweekday()]
                        ) 

            dt += timedelta(days = 1)

        if not path.exists(out):
            mkdir(out)

        with open(path.join(out, '{}.txt'.format(class_name)), 'w') as f:
            import datetime

            f.write(
                'Class: {};\tTotal hours: {};\tLost hours: {}\nExcludes:\n\t{}\n\n{}'.format(
                    class_name,
                    len(d.keys()),
                    lessCounter,
                    str.join('\n\t', ('{} -> {}'.format(*x) for x in init['excludes'])),
                    str.join('\n', (
                        '{}\t{}'.format(
                                v,
                                datetime.datetime.strptime(k, '%Y.%m.%d').strftime('%d.%m.%Y')
                            ) for k, v in sorted(d.items())
                        ))
                )
            )

if __name__ == '__main__':
    GetSchoolTimeTable(init)