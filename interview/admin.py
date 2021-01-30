from django.contrib import admin
from django.http import HttpResponse
from django.db.models import Q
# from django.contrib import messages
# from django.utils.safestring import mark_safe
#
# from jobs.models import Resume
# from interview import candidate_field as cf
# from .tasks import send_dingtalk_message
# from .dingtalk import send

import logging
import csv
from datetime import datetime

from interview.models import Candidate
from interview import dingtalk

# Register your models here.

logger = logging.getLogger(__name__)

exportable_fields = ('username','city','phone','bachelor_school','master_school','degree','first_result',
                     'first_interviewer_user','second_result','second_interviewer_user','hr_result','hr_score','hr_remark','hr_interviewer_user')


# 通知一面面试官面试
def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers
    # 这里的消息发送到钉钉， 或者通过 Celery 异步发送到钉钉
    #send ("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )
    dingtalk.send("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )
    # messages.add_message(request, messages.INFO, '已经成功发送面试通知')


notify_interviewer.short_description = u'通知一面面试官'

def export_model_as_csv(modeladmin, request,queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )
    # 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list],
    )

    for obj in queryset:
        ## 单行 的记录（各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    # logger.error(" %s has exported %s candidate records" % (request.user.username, len(queryset)))
    logger.info("%s export %s candidate records"%(request.user,len(queryset)))
    return response
#定义函数名 描述
export_model_as_csv.short_description = u'导出为CSV文件'

# export_model_as_csv.allowed_permissions = ('export',)


#候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator','created_date','modified_date')
    actions = (export_model_as_csv,notify_interviewer,) #注册导出表函数

    ##当前用户是否有导出权限
    def has_export_permissions(self,request):
        opts = self.opts
        return request.user.has_perm('%s.%s'%(opts.app_label,"export"))

    list_display = (
        "username","city","bachelor_school","first_score","first_result","first_interviewer_user",
        "second_score","second_interviewer_user","hr_score","hr_result","last_editor"
    )

    ###筛选条件  右边增加一个筛选条件
    list_filter = ('city','first_result','second_result','hr_result','first_interviewer_user','second_interviewer_user','hr_interviewer_user')

    ### 查询字段
    search_fields = ('username','phone','email','bachelor_school')  #多一个搜索框
    ##只读文本字段
    # readonly_fields = ('first_interviewer_user','second_interviewer_user')

    ###自动排序
    ordering = ('first_score','second_score','hr_score')

    #添加可以直接批量编辑的字段
    default_list_editable = ('first_interviewer_user','second_interviewer_user',)

    def get_list_editable(self,request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request): #此方法改变替换父类方法
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin,self).get_changelist_instance(request)


    def get_group_names(self,user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names
    #对于非管理员，HR，获取自己是一面面试官或者二面面试官的候选人集合
    def get_queryset(self,request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )

    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)
        if 'interviewer' in group_names:
            logger.info('interviewer is in user group fo %s'%request.user.username)
            return ('first_interviewer_user','second_interviewer_user',)
        return ()


    #一面面试官仅填写一面反馈，二面面试官仅填写二面反馈
    def get_fieldsets(self,request,obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return default_fieldsets_second
        return default_fieldsets


    def save_model(self,request,obj,form,change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()

admin.site.register(Candidate,CandidateAdmin)
