from datetime import date
import datetime
import os

## pip install py-dateutil

DMY = '%d.%m.%Y'
YMD = '%Y.%m.%d'

DAYS = {1: 'Mon',
        2: 'Tue',
        3: 'Wed',
        4: 'Thu',
        5: 'Fri',
        6: 'Sat',
        7: 'Sun'}


class School():
    def __init__(self, name = None):
        self.name = name
        self.year = dict()
        self.excludes = []
        self.lessCounter = 0
        self.d = dict()

    def table(self, d):
        '''d should be a dict = {isoweekday: NumberOfLesson}'''
        self.workDays = d
        return self


    def range(self, year):
        '''The range of an academic year. Year is list'''
        self.year['start'] = year[0]
        self.year['finish'] = year[1]

        return self

    def append(self, items):
        '''The ranges of holidays etc. items is tuple or list'''
        if isinstance(items, list):
            for item in items:
                self.excludes.append(item)
        else:
            self.excludes.append(items)

        return self

    def check(self):
        '''Perform manipulations to produce schedule for academic year.'''
        from dateutil.rrule import rrule, DAILY

        for dt in rrule(DAILY, dtstart=self.year['start'], until=self.year['finish']):
            dt = dt.date()
            _, _, weekday = dt.isocalendar()

            if weekday in self.workDays.keys():

                if any(x[0] <= dt <= x[1] for x in self.excludes):
                    self.lessCounter += 1

                else:
                    self.d[dt.strftime(YMD)] = '{}-{}'.format(DAYS[weekday], self.workDays[weekday]) 

        return self


    def text(self):
        '''Return formatted string'''
        from collections import OrderedDict
        od = OrderedDict(sorted(self.d.items()))

        return 'Class: {};\t{}\nTotal hours: {}\nLost hours: {}\nExcludes:\n\t{}\n\n{}'.format(
                self.name, 
                str.join(', ', [DAYS[weekday] for weekday in self.workDays.keys()]),
                len(self.d.keys()),
                self.lessCounter,
                str.join('\n\t', (str.format('{} -> {}', *x) for x in self.excludes)) ,
                str.join('\n', (str.format('{}\t{}', v, datetime.datetime.strptime(k, YMD).strftime(DMY)) for k, v in od.items()))
                )



if __name__ == '__main__':
    '''
    init should be a dict with a struct as:
       init['year'] a tuple of academic year: (datetime.date(start), datetime.date(finish)) 
       init['excludes'] a list of tuple pairs: [(datetime.date(exclude_start1), datetime.date(exclude_finish1))]
       init['classes'] a dict of dictionaries with a struct as:
            init['classes']['class_name1'] is a dict with struct as:
                {isoweekday1: numberOfLesson1, isoweekday_n: numberOfLesson_n}
    '''

    init = {
            'year': (date(2014, 9, 1), date(2015, 5, 31)),           

            'excludes': [
                        (date(2014, 11, 3), date(2014, 11, 9)),
                        (date(2014, 12, 29), date(2015, 1, 11)),
                        (date(2015, 2, 23), date(2015, 2, 23)),
                        (date(2015, 3, 9), date(2015, 3, 9)),
                        (date(2015, 3, 23), date(2015, 3, 29)),
                        (date(2015, 5, 1), date(2015, 5, 4)),
                        (date(2015, 5, 11), date(2015, 5, 11)),
                        (date(2015, 5, 25), date(2015, 5, 31))
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

    for class_name in init['classes'].keys():
        if not os.path.exists('out'): os.mkdir('out')
        with open(os.path.join('out', '{}.txt'.format(class_name)), 'w') as f:
            print(
                    School(class_name).range(init['year']).append(init['excludes']).table(init['classes'][class_name]).check().text(),
                    file = f
                 )

