import uuid
import random
import json
import datetime
import sys

LANGUAGES   = ['en', 'pt', 'fr', 'es', 'de']
CLIENT_NAME = ['easyjet', 'booking']
TIME_FMT    = '%Y-%m-%d %H:%M:%S.%f'
NENTRIES    = 1_000_000

n_entries = int(sys.argv[1]) or NENTRIES

f = open(f'./random_{n_entries}.json', "w")

ts = datetime.datetime.now() - datetime.timedelta(days=365)

for i in range(n_entries):
	s_lan = random.choice(LANGUAGES)
	t_lan = random.choice([l for l in LANGUAGES if l != s_lan])

	entry = { 
		"timestamp":       ts.strftime(TIME_FMT),
		"translation_id":  str(uuid.uuid4()),
		"source_language": s_lan,
		"target_language": t_lan,
		"client_name":     random.choice(CLIENT_NAME),
		"event_name":      "translation_requested",
		"nr_words":        random.randint(1,1000),
		"duration":        random.randint(1,60)
	}

	f.write(f'{json.dumps(entry)}\n')

	ts += datetime.timedelta(seconds=random.randint(1,10), microseconds=random.randint(1,1000000))

f.close()