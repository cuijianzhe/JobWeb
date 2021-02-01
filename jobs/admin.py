from django.contrib import admin
from jobs.models import Job
from jobs.models import Resume
# Register your models here.

class JobAdmin(admin.ModelAdmin): #模型的管理类
    exclude = ('creator','create_date','modified_date') #设置页隐藏部分属性
    list_display = ('job_name','job_type','job_city','creator','create_date','modified_date') #添加展示页内容



    def save_model(self, request, obj, form, change):
        obj.creator = request.user  #当前登录用户设置成职位的创建人
        super().save_model(request,obj,form,change)

class ResumeAdmin(admin.ModelAdmin):


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


