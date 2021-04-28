from config.celery import app as celery_app


@celery_app.task
def ch_every_min():
    pass
