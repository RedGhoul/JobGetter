from django.shortcuts import render
from django.http import HttpResponse
from jobber.tasks import GetJobs_Task
# Create your views here.
def startJobTest(request):
    GetJobs_Task()
    return HttpResponse("DONE")

def index(request):
    return HttpResponse("index")