import csv
from survey import Survey


def load_data(path):
    """
    Given a CSV of data, return a list of dictionaries
    """
    csv_data = csv.reader(open(path, 'rb'))
    header = csv_data.next()
    row = csv_data.next()
    d = dict(zip(header, [float(x) for x in row]))
    s0 = Survey(d['Depth'], d['Inc'], d['Azi'], d['TVD'], d['EW'], d['NS'], d['Dogleg'])
    survey_list = [s0]

    data = [row for row in csv_data]
    for row in data:
        d = dict(zip(header, [float(x) for x in row]))
        sn = survey_list[-1]
        sn1 = sn.next(d['Depth'], d['Inc'], d['Azi'])
        survey_list.append(sn1)

    return survey_list
