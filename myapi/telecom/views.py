from django.http import HttpResponse
import json


from .tasks import send_email_task


# Create your views here.
def index(request):
    send_email_task.delay()
    response = json.dumps([{"response": "Report successfully sent to the email"}])
    return HttpResponse(response, content_type='text/json')



