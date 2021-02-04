from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from jobs.models import Job,Resume
from jobs.models import cities,JobTypes
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect

def joblist(request):
    job_list = Job.objects.order_by('job_type') #django的models的内置方法
    context = {'job_list':job_list}

    for job in job_list:
        job.city_name = cities[job.job_city][1]
        job.job_type = JobTypes[job.job_type][1]
    return render(request,'joblist.html',context)
def detail(request,job_id): #jobid 通过变量传进来
    try:
        job = Job.objects.get(pk=job_id)
        job.city_name = cities[job.job_city][1]  #职位城市名

    except Job.DoesNotExist:
        raise Http404("Job does not exist")

    return render(request,"job.html",{'job':job})


from django.contrib.auth.mixins import LoginRequiredMixin

class ResumeCreateView(LoginRequiredMixin,CreateView):
    '''简历职位页面'''
    template_name = 'resume_form.html'
    success_url = '/joblist'
    model = Resume
    fields = ["username", "city", "phone",
              "email", "apply_position", "gender",
              "bachelor_school", "master_school", "major", "degree",
              "candidate_introduction", "work_experience", "project_experience"]
    #从url请求参数带入默认值
    def get_initial(self):
        initial = {}  #设置了初始值
        for  x in self.request.GET:
            initial[x] = self.request.GET[x]
        return initial

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.applicant = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())