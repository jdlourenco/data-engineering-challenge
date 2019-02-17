import uuid
import random
import json
import datetime
import sys

NENTRIES    = 1_000_000

LANGUAGES   = ['en', 'pt', 'fr', 'es', 'de']
CLIENT_NAME = ['easyjet', 'booking']
TIME_FMT    = '%Y-%m-%d %H:%M:%S.%f'
EVENT_NAME  = ['translation_requested', 'translation_delivered']

n_entries = int(sys.argv[1]) if len(sys.argv) >= 2 else NENTRIES

f = open(f'./random_{n_entries}.json', "w")

ts = datetime.datetime.now() - datetime.timedelta(days=365)

has_outlier = False
outlier_ith = random.randint(0,99)

for i in range(n_entries):
	s_lan = random.choice(LANGUAGES)
	t_lan = random.choice([l for l in LANGUAGES if l != s_lan])

	is_outlier = i  % 100 == outlier_ith

	if not has_outlier and is_outlier:
		has_outlier = True

	if not has_outlier and i == n_entries - 1:
		is_outlier = True

	entry = { 
		"timestamp":       ts.strftime(TIME_FMT),
		"translation_id":  str(uuid.uuid4()),
		"source_language": s_lan,
		"target_language": t_lan,
		"client_name":     random.choice(CLIENT_NAME),
		"event_name":      random.choice(EVENT_NAME),
		"nr_words":        random.randint(1,1000),
		"duration":        random.randint(1,60) if not is_outlier else random.randint(1000,6000)
	}

	f.write(f'{json.dumps(entry)}\n')

	ts += datetime.timedelta(seconds=random.randint(1,10), microseconds=random.randint(1,1000000))

f.close()