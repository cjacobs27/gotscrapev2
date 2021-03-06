# This script works with the clock.py script: clock.py schedules the tasks below will be run. This script "queues jobs"
import os
import redis
from redis import Redis
from rq import Worker, Queue, Connection
import django
django.setup()
from gotsv2.update import Update
from gotsv2.infoscrape import Infoscrape

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()

# come back to below if other fix doesn't work
# h = Queue('high', connection=Redis())
# l = Queue('low', connection=Redis())
#
# u = Update()
# i = Infoscrape()
# result1 = h.enqueue(u.gender_foreign_key_init())
# result2 = l.enqueue(u.generate_links(), u.link_scrape(), u.character_model_update(),
#                    i.encode_gender_and_update(), i.scrape_titles_and_update_model(), i.populate_title_strings_model())

q = Queue('high', connection=Redis())

u = Update()
i = Infoscrape()

result = q.enqueue(u.gender_foreign_key_init(),u.generate_links(), u.link_scrape(), u.character_model_update(),
                   i.encode_gender_and_update(), i.scrape_titles_and_update_model(), i.populate_title_strings_model())
