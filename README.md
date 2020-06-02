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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'<br />
EMAIL_HOST_USER = "example@gmail.com" &emsp; <!--- put your email here. ---> <br />
EMAIL_HOST = "smtp.gmail.com"<br />
EMAIL_PORT = 587<br />
EMAIL_USE_TLS = True<br />
EMAIL_HOST_PASSWORD = 'PASSWORD' &emsp;<!--- put your email password here.)---><br />
EMAIL_RECEIVER_LIST = ['RECEIVER1','RECEIVER2']<br />


CELERY_BROKER_URL = 'amqp://guest:guest@localhost'<br />
worker_redirect_stdouts_level = 'ERROR'<br />
CELERY_TIMEZONE = 'Asia/Kolkata'<br />
CELERY_BEAT_SCHEDULE = {<br />
                'hourly_pullevents': {<br />
                             'task': 'telecom.tasks.send_email_task',<br />
                                      'schedule': crontab(minute='*/2', hour='*'), &emsp; <!--- This will send email after every 2 min.---><br />
                                      },

### Run django server from myapi folder<br />
python3 manage.py runserver

### Run celery worker from myapi folder<br />
celery -A myapi worker -l info

### Run celery beat from myapi folder <br />
celery -A myapi beat -l info

### now hit api(http://127.0.0.1:8000/index) to get periodic email like this after every 2 minutes
![mail snapshot](customer_churn.PNG)


