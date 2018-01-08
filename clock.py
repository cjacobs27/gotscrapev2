# This script works with the worker.py script: it schedules the tasks that are queued in worker.py via RQ/Redis

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=8)
def scheduled_job():
    print('This job is run every day at 8am.')


sched.start()
