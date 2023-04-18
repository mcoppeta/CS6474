import numpy as np
from datetime import date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Quarters starting at 2015 Q1 thru 2024 Q4
# each is tuple (eps, increase from previous?)
targets_apple = {
    2015: {
        1: (0.58, 0),
        2: (0.46, 0),
        3: (0.49, 1),
        4: (0.82, 1)
    },
    2016: {
        1: (0.48, 0),
        2: (0.36, 0),
        3: (0.42, 1),
        4: (0.84, 1)
    },
    2017: {
        1: (0.53, 0),
        2: (0.42, 0),
        3: (0.52, 1),
        4: (0.97, 1)
    },
    2018: {
        1: (0.68, 0),
        2: (0.59, 0),
        3: (0.73, 1),
        4: (1.05, 1)
    },
    2019: {
        1: (0.62, 0),
        2: (0.55, 0),
        3: (0.76, 1),
        4: (1.25, 1)
    },
    2020: {
        1: (0.64, 0),
        2: (0.65, 1),
        3: (0.73, 1),
        4: (1.68, 1)
    },
    2021: {
        1: (1.4, 0),
        2: (1.3, 0),
        3: (1.24, 0),
        4: (2.1, 1)
    },
    2022: {
        1: (1.52, 0),
        2: (1.2, 0),
        3: (1.29, 1),
        4: (1.88, 1)
    }
} 

def select_data():
    data = np.loadtxt('./youtube_data.txt', dtype=object, encoding='utf-8', delimiter="|", comments=None)
    headers = data[0]
    data = data[1:]
    newData = []
    for row in data:
        row[1] = int(row[1])
        row[2] = int(row[2])
        row[5] = int(row[5])
        row[6] = int(row[6])
        row[7] = int(row[7])
        row[8] = int(row[8])
        row[9] = int(row[9])

        yr = int(row[3].split('-')[0])
        if yr > 2022 or yr < 2015:
            continue
        else:
            newData.append(row)
    data = np.array(newData)
    return headers, data

# binary: 0 if eps, 1 if binary increase from previous
# target_apple 0 if samsung, 1 if apple
def get_y(data, binary, target_apple):
    if target_apple:
        targets = targets_apple
    y = []
    for row in data:
        t = row[3]
        year, month, d0 = t.split('-')
        year = int(year)
        month = int(month)

        if month in [1,2,3]:
            y.append(targets[year][1][binary])
        elif month in [4,5,6]:
            y.append(targets[year][2][binary])
        elif month in [7,8,9]:
            y.append(targets[year][3][binary])
        else:
            y.append(targets[year][4][binary])

    return np.array(y)

# transforms date field into the month (1-3) in quarter
def date_to_month_in_quarter(data, col):
    x = 0
    while x < len(data):
        year, month, d0 = data[x][col].split('-')
        month = int(month)
        q = ((month - 1) % 3) + 1
        data[x][col] = q
        x += 1
    return data

# transforms text field (presumably video title) to sentiment compound
def title_to_sentiment(data, col):
    analyzer = SentimentIntensityAnalyzer()
    for row in data:
        scores = analyzer.polarity_scores(row[col])
        row[col] = scores['compound']
    return data


def main(binary):
    headers, data = select_data()
    y = get_y(data, binary 1) # apple only rn
    return headers, data, y
    
    