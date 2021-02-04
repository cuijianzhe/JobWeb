from django.contrib import admin
from jobs.models import Job
from jobs.models import Resume

from django.contrib import messages
from interview.models import Candidate
from datetime import datetime

# Register your models here.

class JobAdmin(admin.ModelAdmin): #模型的管理类
    exclude = ('creator','create_date','modified_date') #设置页隐藏部分属性
    list_display = ('job_name','job_type','job_city','creator','create_date','modified_date') #添加展示页内容



    def save_model(self, request, obj, form, change):
        obj.creator = request.user  #当前登录用户设置成职位的创建人
        super().save_model(request,obj,form,change)


def enter_interview_process(modeladmin,request,queryset):
    candidate_names = ""
    for resume in queryset:
        candidate = Candidate()
        candidate.__dict__.update(resume.__dict__) #简历对象里面的所有属性赋值到候选人应聘者里面的所有属性
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + "," + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人: %s 已成功进入面试流程' % (candidate_names))

enter_interview_process.short_description = u"进入面试流程"

class ResumeAdmin(admin.ModelAdmin):

    actions = [enter_interview_process,]
    list_display = ('username', 'applicant', 'city', 'apply_position', 'bachelor_school', 'master_school',  'major','created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender", ), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience","project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Job,JobAdmin)
admin.site.register(Resume,ResumeAdmin)


