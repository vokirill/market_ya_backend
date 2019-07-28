def date_string(date_string):
    date = date_string.split('.')
    return '{0}-{1}-{2}'.format(date[2], date[1], date[0])


print(date_string('01.02.2019'))