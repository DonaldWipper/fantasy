import FlaskApp.sport_fantasy as sport_fantasy
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')
    sport_fantasy.make_transfers()

sched.start()

