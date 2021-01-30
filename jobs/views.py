from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from jobs.models import Job
from jobs.models import cities,JobTypes

def joblist(request):
    job_list = Job.objects.order_by('job_type') #django的models的内置方法
    template = loader.get_template('joblist.html')  #使用加载器加载joblist到静态页面

    context = {'job_list':job_list}

    for job in job_list:
        job.city_name = cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]

    return HttpResponse(template.render(context)) #模板方法把上下文展现给

def detail(request,job_id): #jobid 通过变量传进来
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = cities[job.job_city][1]  #职位城市名

    except Job.DoesNotExist:
        raise Http404("Job does not exist")

    return render(request,"job.html",{'job':job})
