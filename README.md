# send-email-alert
This app will send periodic email alert using CELERY and CELERY-BEAT After hitting soecific django API 

### In linux Install rabbitmq server..

*sudo apt-get install erlang*      

*sudo apt-get install rabbitmq-server*

*sudo systemctl enable rabbitmq-server*  

*sudo systemctl start rabbitmq-server*

*sudo systemctl status rabbitmq-server

### You can check queue dashboard on localhost:15672 after enabling plugins

*sudo rabbitmq-plugins enable rabbitmq_management*
default username: guest
default password: guest

### update settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = "example@gmail.com" [//]: <> (put your email here.)
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = 'PASSWORD' [//]: <> (put your email password here.)
EMAIL_RECEIVER_LIST = ['RECEIVER1','RECEIVER2']


CELERY_BROKER_URL = 'amqp://guest:guest@localhost'
worker_redirect_stdouts_level = 'ERROR'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BEAT_SCHEDULE = {
                'hourly_pullevents': {
                             'task': 'telecom.tasks.send_email_task',
                                      'schedule': crontab(minute='*/2', hour='*'),    [//]: <> (This will send email after every 2 min.)
                                      },

