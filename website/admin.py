from django.contrib import admin
from .models import *
# Register your models here.
class _u_register(admin.ModelAdmin):
    list_display=['name','email','phone','address','password','gender','resume']

admin.site.register(u_register,_u_register)
                    
class _c_registers(admin.ModelAdmin):
    list_display=['cp_name','cp_email','cp_phone','cp_password','cp_gst_no']

admin.site.register(c_register,_c_registers)

class _adreg(admin.ModelAdmin):
    list_display=['admin_email','admin_password','id']
admin.site.register(ad_register,_adreg)


class _category(admin.ModelAdmin):
    list_display=['category_name','category_description','job_type','image']
admin.site.register(category,_category)

class _sub_job(admin.ModelAdmin):
    list_display=['job_title','job_description','job_type','job_salary','job_location','job_experience','job_qualification','job_vacancy','job_apply','job_skils']
admin.site.register(sub_job,_sub_job)

class JobApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'company', 'expected_salary', 'notice_period', 'status', 'applied_at','interview_date')
    list_filter = ('status', 'company', 'job', 'notice_period')
    search_fields = ('user__name', 'job__job_title', 'company__cp_name', 'expected_salary')

admin.site.register(JobApplicant, JobApplicantAdmin)

class cp_verifyAdmin(admin.ModelAdmin):
    list_display = ['company', 'verification_status','field_status_save']
    list_filter = ['verification_status']
    search_fields = ['company__cp_name']

admin.site.register(cp_verify, cp_verifyAdmin)

class _tender(admin.ModelAdmin):
    list_display=['title','description','budget','deadline']
admin.site.register(tender,_tender)