from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon', hour=15)
def scheduled_job():
    print('This job is run every Monday at 3pm.')


sched.start()
