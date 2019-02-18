# Data Engineering Challenge

The code in this repo was developed using [Python 3.6.5](https://www.python.org/downloads/release/python-365/).

This README is organized in the following sections:
* [Description](#description)
* [Setup](#setup)
* [Usage](#usage)
* [System Design](#system-design)

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

A sample file containing the example presented in the [original repo](https://github.com/Unbabel/data-engineering-challenge) is included in [events.json](events.json).


### Getting help
For a description of the CLI supported options run:

```
python unbabel_cli.py --help 
Usage: unbabel_cli.py [OPTIONS]

Options:
  --mode [moving_average|outliers]
                                  moving_average: computes the moving average
                                  over the past N minutes aggregated in 1
                                  minute time windows determined by the
                                  window_size option
                                  outliers: uses the three-
                                  sigma rule for detecting outliers
                                  [default=moving_average]
  --input_file PATH               Input file  [required]
  --window_size INTEGER           Window size in minutes [default=10]
  --event_name [translation_requested|translation_delivered]
                                  Filters input data considering only rows
                                  matching event name
                                  [default=translation_delivered]
  --help                          Show this message and exit.

```

### Moving Average

#### Running the moving average use case

In order to run the moving average use case on the sample input file run:

```
python unbabel_cli.py --input_file events.json 
{"date": "2018-12-26T18:16:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:17:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:18:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:19:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:20:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:21:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:22:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:23:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:24:00", "average_translation_delivered": 42.5}
{"date": "2018-12-26T18:25:00", "average_translation_delivered": 42.5}
{"date": "2018-12-26T18:26:00", "average_translation_delivered": 54.0}
{"date": "2018-12-26T18:27:00", "average_translation_delivered": 54.0}
{"date": "2018-12-26T18:28:00", "average_translation_delivered": 54.0}
{"date": "2018-12-26T18:29:00", "average_translation_delivered": 54.0}
{"date": "2018-12-26T18:30:00", "average_translation_delivered": 54.0}
{"date": "2018-12-26T18:31:00", "average_translation_delivered": 54.0}
{"date": "2018-12-26T18:32:00", "average_translation_delivered": 54.0}
{"date": "2018-12-26T18:33:00", "average_translation_delivered": 54.0}
```

#### Running the moving average use case with a different `window_size`

The `window_size` option can be used for setting a different moving average window, e.g. `1 minute`:

```
python unbabel_cli.py --input_file events.json --window_size 1
{"date": "2018-12-26T18:16:00", "average_translation_delivered": 31.0}
{"date": "2018-12-26T18:17:00", "average_translation_delivered": 0}
{"date": "2018-12-26T18:18:00", "average_translation_delivered": 0}
{"date": "2018-12-26T18:19:00", "average_translation_delivered": 0}
{"date": "2018-12-26T18:20:00", "average_translation_delivered": 0}
{"date": "2018-12-26T18:21:00", "average_translation_delivered": 0}
{"date": "2018-12-26T18:22:00", "average_translation_delivered": 0}
{"date": "2018-12-26T18:23:00", "average_translation_delivered": 0}
{"date": "2018-12-26T18:24:00", "average_translation_delivered": 54.0}
```

#### Running the moving average use case on a different `event_name`

The `event_name` option can be used for computing the moving average on a different event type, e.g. `translation_requested`:

```
python unbabel_cli.py --input_file events.json --event_name translation_requested
{"date": "2018-12-26T18:12:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:13:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:14:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:15:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:16:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:17:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:18:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:19:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:20:00", "average_translation_requested": 20.0}
{"date": "2018-12-26T18:21:00", "average_translation_requested": 20.0}
```

### Outliers

#### Generating sample input data

The [generate_entries.py](generate_entries.py) script can be used for generating sample input data. It generates a file containing `N_ENTRIES` as specified by its first argument and can be used with the following command:

`python generate_entries.py <N_ENTRIES>`

Besides randomly generating a sample file it also generates approximatly 1% outliers in order to demo the extra outlier detection use case. In order to demonstrate the outlier functionality one can use the `generate_entries.py` script for generating a random sample input file with outliers.

For generating a sample file containing 20 entries run:

`python generate_entries.py 20`

This will generate a random sample file named `random_20.json`:

```
cat random_20.json
{"timestamp": "2018-02-17 23:08:58.025150", "translation_id": "e02f0278-ac8b-4b06-88b3-61c18f991804", "source_language": "fr", "target_language": "pt", "client_name": "booking", "event_name": "translation_requested", "nr_words": 342, "duration": 2}
{"timestamp": "2018-02-17 23:09:01.782707", "translation_id": "a4fd6b09-f840-4dff-844a-855d4890df39", "source_language": "en", "target_language": "pt", "client_name": "booking", "event_name": "translation_delivered", "nr_words": 329, "duration": 52}
{"timestamp": "2018-02-17 23:09:03.809987", "translation_id": "cc96563d-f01d-42b9-a048-500a9e1691b0", "source_language": "pt", "target_language": "es", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 964, "duration": 2}
{"timestamp": "2018-02-17 23:09:05.857942", "translation_id": "681e27a9-0234-48f6-a533-a697c8a15e68", "source_language": "en", "target_language": "fr", "client_name": "booking", "event_name": "translation_delivered", "nr_words": 114, "duration": 44}
{"timestamp": "2018-02-17 23:09:12.255362", "translation_id": "48dce229-2046-48ec-9325-fac1c5585c70", "source_language": "fr", "target_language": "de", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 736, "duration": 1}
{"timestamp": "2018-02-17 23:09:22.888078", "translation_id": "9a786dba-15c9-4050-bca6-09e37898f089", "source_language": "es", "target_language": "en", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 909, "duration": 43}
{"timestamp": "2018-02-17 23:09:26.844940", "translation_id": "6011da16-b687-4c76-961a-7dcb6a674df7", "source_language": "de", "target_language": "es", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 50, "duration": 6}
{"timestamp": "2018-02-17 23:09:37.447776", "translation_id": "e44caa4a-43f4-4c43-8f31-84b19533aea3", "source_language": "en", "target_language": "fr", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 420, "duration": 19}
{"timestamp": "2018-02-17 23:09:39.742053", "translation_id": "8addc8b9-447f-45ef-830a-003c473f5a85", "source_language": "fr", "target_language": "es", "client_name": "easyjet", "event_name": "translation_requested", "nr_words": 624, "duration": 41}
{"timestamp": "2018-02-17 23:09:44.608391", "translation_id": "6bbdc2cf-49e9-4503-ae1a-30358d9e8e50", "source_language": "fr", "target_language": "en", "client_name": "booking", "event_name": "translation_requested", "nr_words": 836, "duration": 4}
{"timestamp": "2018-02-17 23:09:52.112765", "translation_id": "d8c2e6fc-064c-4783-9a2c-aca0e7c153f9", "source_language": "pt", "target_language": "en", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 994, "duration": 23}
{"timestamp": "2018-02-17 23:09:56.167307", "translation_id": "a4dbc1ca-a935-43c7-81e3-862fd49c2e14", "source_language": "de", "target_language": "en", "client_name": "booking", "event_name": "translation_delivered", "nr_words": 814, "duration": 8}
{"timestamp": "2018-02-17 23:09:59.692986", "translation_id": "4012f1b2-4016-4e99-9149-315ecc9ad910", "source_language": "fr", "target_language": "pt", "client_name": "booking", "event_name": "translation_delivered", "nr_words": 312, "duration": 36}
{"timestamp": "2018-02-17 23:10:05.105078", "translation_id": "705067b5-4f87-4677-9c0a-7be918685d02", "source_language": "es", "target_language": "pt", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 311, "duration": 47}
{"timestamp": "2018-02-17 23:10:13.141282", "translation_id": "b047f22e-9dc2-4dba-9081-d1f8586d038b", "source_language": "pt", "target_language": "es", "client_name": "booking", "event_name": "translation_requested", "nr_words": 88, "duration": 26}
{"timestamp": "2018-02-17 23:10:23.567902", "translation_id": "44f3f506-a09d-45a2-b111-d25ffcab9523", "source_language": "de", "target_language": "fr", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 971, "duration": 24}
{"timestamp": "2018-02-17 23:10:26.433657", "translation_id": "32542691-5130-4259-b539-09677c811c47", "source_language": "en", "target_language": "de", "client_name": "easyjet", "event_name": "translation_requested", "nr_words": 764, "duration": 57}
{"timestamp": "2018-02-17 23:10:32.846556", "translation_id": "2a94fed2-7897-485d-8f68-7e38189c0915", "source_language": "en", "target_language": "fr", "client_name": "booking", "event_name": "translation_delivered", "nr_words": 346, "duration": 59}
{"timestamp": "2018-02-17 23:10:33.949701", "translation_id": "77cf3c5d-0f2a-478d-a702-c28cf0c28177", "source_language": "de", "target_language": "en", "client_name": "easyjet", "event_name": "translation_requested", "nr_words": 763, "duration": 33}
{"timestamp": "2018-02-17 23:10:40.951563", "translation_id": "d3f46f3e-1c34-49da-a49b-495da79efc38", "source_language": "pt", "target_language": "en", "client_name": "easyjet", "event_name": "translation_delivered", "nr_words": 740, "duration": 4874}
```

By inspecting the file's content one can easily identify the last line as an outlier:

```
{
	"timestamp": "2018-02-17 23:10:40.951563",
	"translation_id": "d3f46f3e-1c34-49da-a49b-495da79efc38",
	"source_language": "pt",
	"target_language": "en",
	"client_name": "easyjet",
	"event_name": "translation_delivered",
	"nr_words": 740,
	"duration": 4874
}
```

The sample file described above is included in [random_20.json](random_20.json).

#### Running the outliers use case

The `mode` option can be used for selecting the `outliers` use case and apply it to the file just described:
```
python unbabel_cli.py --input_file random_20.json --mode outliers
3sigma outlier detector on event_name='translation_delivered': mean=374.143 stdev=1295.292
{"client_name": "easyjet", "duration": 4874, "event_name": "translation_delivered", "nr_words": 740, "source_language": "pt", "target_language": "en", "timestamp": "2018-02-17T23:10:40.951563", "translation_id": "d3f46f3e-1c34-49da-a49b-495da79efc38"}
```

The output above shows the parameters used for the `three-sigma` rule followed by the detected outliers.

The first line shows the detector parameters `mean=374.143` and `stdev=1295.292`, resulting in detecting outliers with a value higher than `374.143 + 3*1295.292 = 4260.019`. As expected, the sample file last line is detected as an outlier because it's `duration` field value is `4874 > 4260.019`.


**Note:** the `outliers` mode is more effective on a large datasets because a sample's `mean` and `standard deviation` can be highly influenced by outliers on small datasets.


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
The **OutlierAdapter** class filters rows in the input file by the `event_name` field and transforms
the input data frame into a list of dicts with the original data frame columns as keys.

### Processor
The **processor** module is used to implement use cases logic. The current implementation includes
a **MovingAverageProcessor** and a **OutlierProcessor**.

#### MovingAverageProcessor
The **MovingAverageProcessor** class implements the computation of a per minute moving average on a
varying size time window. It leverages the transformation applied by the **MovingAverageAdapter** class
providing the aggregated `sum` and `count` on the `duration` field per minute. It's logic consists of:
1. building a `queue` with holding at most `window_size` items
2. iterating through the input rows
3. adding each row to the `queue`
4. computing the queue average by dividing the sum of sums and the sum of counts

Finally after iterating over all input rows an additional set of windows is generated while the last
set of rows still affect the moving average depending on the window size.

#### OutlierProcessor
The **OutlierProcessor** class implements the detection of outliers based on the `three-sigma` rule by
computing the `mean` and `standard_deviation` parameters on the input data. It then iterates through
all input rows outputing all rows having `duration` field value higher than `mean + 3*standard_deviation`.

### Writer
The **writer** module is used to write output data and can be extended for supporting differnt
data targets. The current implementation includes a **JsonStdoutWriter** class for writing
output to `stdout` in JSON format.

