# Data Engineering Challenge

The code in this repo was developed using [Python 3.6.5](https://www.python.org/downloads/release/python-365/).

[Usage](#usage)

## Description

This repo provides the `unbabel_cli` CLI application implementing the functionality described in https://github.com/Unbabel/data-engineering-challenge.

Besides the moving average functionality it also includes an additional use case providing a simple anomaly detector based on [three-sigma rule](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule) for detecting outliers.


## Setup

Clone repo:

`
git clone git@github.com:jdlourenco/data-engineering-challenge.git
`

Change to `data-engineering-challenge` dir:

`
cd data-engineering-challenge
`

Create virtual env:

`
python -m venv venv
`

Activate virtual env:

`
source venv/bin/activate
`

Install dependencies:

`
pip install -r requirements.txt
`

Run tests:

`
python -m pytest
`

## Usage

#usage


A sample file containing the example presented in the [original repo](https://github.com/Unbabel/data-engineering-challenge) is included in [events.json](events.json).

### Generating sample input data

The [generate_entries.py](generate_entries.py) script can be used for generating sample input data. It generates a file containing `N_ENTRIES` as specified by its first argument and can be used with the following command:

`python generate_entries.py <N_ENTRIES>`

Besides randomly generating a sample file it also generates approximatly 1% outliers in order to demo the extra outlier detection use case.


## System design

The system is built around 4 main modules with the following roles:

| Component | Role                                                                              |
| --------- | ----------------------------------------------------------------------------------|
| Reader    | Reads input data from a specific data source                                      |
| Adapter   | Filters and transforms data into a suitable format for handling by the processors |
| Processor | Implements specific use case logic                                                |
| Writer    | Outputs results data to specific output targets                                   |

### Reader
The **reader** module is used to read input data and can be extended for supporting differnt
data sources. The current implementation includes a **JsonFileReader** class for reading
input data from a file containing a JSON object per line into a pandas data frame.

Example:
```
  client_name  duration             event_name  nr_words source_language target_language                  timestamp         translation_id
0     easyjet        20  translation_requested        30              en              fr 2018-12-26 18:11:08.509654   5aa5b2f39f7254a75aa5
1     easyjet        31  translation_delivered        30              en              fr 2018-12-26 18:15:19.903159   5aa5b2f39f7254a75aa4
2     booking        54  translation_delivered       100              en              fr 2018-12-26 18:23:19.903159  5aa5b2f39f7254a75bb33
```

### Adapter
The **adapter** module is used to filter and transform data into a suitable format using python
built-in types for easier handling by the processor layer for each use case. The current
implementation includes a **MovingAverageAdapter** and a **OutlierAdapter** for filtering by
the `event_name` field and transforming a pandas data frame into a dict list.

#### MovingAverageAdapter
The **MovingAverageAdapter** class filters rows in the input file by the `event_name` field
and transforms the input data frame containing rows by resampling and aggregating them into
1 minute time windows resulting in a list of dicts with 3 keys: `timestamp`, `sum` and `count`
containg the window timestamp and the sum and count of the `duration` field.

Example:
```
[
	{'timestamp': Timestamp('2018-12-26 18:15:00'), 'sum': 31, 'count': 1},
	{'timestamp': Timestamp('2018-12-26 18:16:00'), 'sum': 0,  'count': 0},
	{'timestamp': Timestamp('2018-12-26 18:17:00'), 'sum': 0,  'count': 0},
	{'timestamp': Timestamp('2018-12-26 18:18:00'), 'sum': 0,  'count': 0},
	{'timestamp': Timestamp('2018-12-26 18:19:00'), 'sum': 0,  'count': 0},
	{'timestamp': Timestamp('2018-12-26 18:20:00'), 'sum': 0,  'count': 0},
	{'timestamp': Timestamp('2018-12-26 18:21:00'), 'sum': 0,  'count': 0},
	{'timestamp': Timestamp('2018-12-26 18:22:00'), 'sum': 0,  'count': 0},
	{'timestamp': Timestamp('2018-12-26 18:23:00'), 'sum': 54, 'count': 1}
]
```

#### OutlierAdapter
The **OutlierAdapter** class filters rows in the input file by the `event_name` field
and transforms the input data frame intot a list of dicts with the original data frame
columns as keys.

### Processor

### Writer
The **writer** module is used to write output data and can be extended for supporting differnt
data targets. The current implementation includes a **JsonStdoutWriter** class for writing
output to `stdout` in JSON format.

