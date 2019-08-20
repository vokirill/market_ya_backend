import datetime
cur = '21.08.2019'
date_format = '%Y-%m-%d'
date = cur.split('.')
date = '{0}-{1}-{2}'.format(date[2], date[1], date[0])
date = datetime.datetime.strptime(date, date_format).date()
dt = datetime.datetime.now().date()
#dt = datetime.date(dt.year, dt.month, dt.day)
if date >= dt:
    print('a')
else:
    print('b')