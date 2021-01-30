from django.contrib import admin
from jobs.models import Job

# Register your models here.

class JobAdmin(admin.ModelAdmin): #模型的管理类
    exclude = ('creator','create_date','modified_date') #设置页隐藏部分属性
    list_display = ('job_name','job_type','job_city','creator','create_date','modified_date') #添加展示页内容



    def save_model(self, request, obj, form, change):
        obj.creator = request.user  #当前登录用户设置成职位的创建人
        super().save_model(request,obj,form,change)

admin.site.register(Job,JobAdmin)


