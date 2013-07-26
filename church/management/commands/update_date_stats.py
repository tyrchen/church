from django.core.management import BaseCommand

__author__ = 'tchen'

### Warning - do not use this script. I changed my mind when generating the stats. This is for real time stats,
### but for the problem we're solving it is not necessary.

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.gnats
stats = db['date_stats']
gnats = db['issues']

# consts
YEARS = range(2013, 2016)
TYPES = [('daily', 365), ('weekly', 53), ('monthly', 12)]
TYPE_FUNS = [
    ('daily', lambda x: x.timetuple().tm_yday),
    ('weekly', lambda x: x.date().isocalendar()[1]),
    ('monthly', lambda x: x.month)
]
STATS = ['created', 'resolved']


def pr_is_resolved(state):
    return state in ['feedback', 'monitored', 'suspended', 'closed']


class Command(BaseCommand):
    help = u'Initialize statistics data'
    need_stat = False

    def init_data(self, year, type,  length, state):
        doc = stats.find_one({'year': year, 'type': type, 'state': state})
        if not doc:
            self.need_stat = True
            data = [0] * length
            stats.insert({'year': year, 'type': type, 'state': state, 'data': data})
            print 'year %s, type %s, state %s, initialized with %d data' % (year, type, state, length)

    def update_one(self, state, dt, action='$inc'):
        year = dt.year

        for type, fun in TYPE_FUNS:
            query = {'year': year, 'type': type, 'state': state}
            stats.update(query, {action: {'data.%d' % (fun(dt) - 1): 1}})

    def update_stats(self):
        print 'Total %s PRs need to be processed.' % gnats.find({'need_stat': {'$gt': 0}}).count()
        for pr in gnats.find({'need_stat': {'$gt': 0}}):
            if pr['need_stat'] == 1:
                self.update_one('created', pr['arrived_at'])

            if pr_is_resolved(pr['state']) and pr['need_stat'] == 2:
                self.update_one('resolved', pr['modified_at'])
            elif not pr_is_resolved(pr['state']) and pr['need_stat'] == 3:
                self.update_one('resolved', pr['modified_at'], '$dec')
            pr['need_stat'] = 0
        print 'All PRs processed.'

    def init_stat(self):
        gnats.update({}, {'$set': {'need_stat': 1}}, multi=True)
        print 'All PRs are set to need re-statistics.'

    def handle(self, *args, **kwargs):
        for year in YEARS:
            for type, length in TYPES:
                for state in STATS:
                    self.init_data(year, type, length, state)

        if self.need_stat:
            self.init_stat()

        self.update_stats()
