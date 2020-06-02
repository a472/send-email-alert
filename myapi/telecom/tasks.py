from __future__ import absolute_import, unicode_literals
from celery import task
from django.conf import settings
from celery.registry import tasks
from data_analysis import report
from email.message import EmailMessage
import smtplib
from glob import glob

@task()
def test(arg):
    print(arg)

@task(bind=True)
def send_email_task(self):
    msg = EmailMessage()
    msg['Subject'] = "Customer-Churn Analysis Report"
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = settings.EMAIL_RECEIVER_LIST  #receiver email list
    msg.set_content('Here is the report')

    # generate report
    report()

    with open('template.html', 'rb')as f:
        file_data = f.read()
    file_string = file_data.decode(encoding='UTF-8')
    msg.add_alternative(file_string, subtype='html')

    allPdfFiles = glob("*.pdf")
    for file in allPdfFiles:
        with open(file, 'rb')as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(msg)


tasks.register(send_email_task)