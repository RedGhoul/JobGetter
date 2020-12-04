from django.shortcuts import render
from django.http import HttpResponse
from jobber.tasks import Get_Jobs_Task
# Create your views here.

def index(request):
    return HttpResponse("Job Getter")