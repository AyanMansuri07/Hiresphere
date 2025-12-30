from django.urls import path    
from .views import *

urlpatterns = [
    path('',homepage,name="home"),
    path('user_register',user_register,name="user_register"),
    path('company_register',company_register,name="company_register"),
    path('login',login,name="login"),
    path('jobs/<int:category_id>/<str:category_name>/', jobs, name="jobs"),
    path('job_apply/<int:job_id>/',job_apply, name="job_apply"),
    path('jobs_applied', jobs_applied, name="jobs_applied"), 
    path('verification/',verification,name="verification"),
 
    path("post-tender/", post_tender, name="post_tender"),
    path('tender_list', tender_list, name='tender_list'),
    path('apply_tender/<int:tender_id>/', apply_tender, name='apply_tender'),
    path('response',response,name="response"),
    path('post_job',post_job,name="post_job"),
    path('postedjob',postedjobs,name="postedjobs"),
    path('update_post_job/<int:job_id>/', update_post_job, name='update_post_job'),
    path('job_applicants/', job_applicants, name="job_applicants"),
    path('notifications/', notifications, name='notifications'),   
    path('user_notifications/', user_notifications, name="user_notifications"),
    path('selected/<int:notification_id>/', selected, name="selected"),
    path('verify_applicant/<int:applicant_id>/', user_verifybycp, name="user_verifybycp"), 
    path('profile',profile,name="profile"),
    path('email',email,name="email"),
    path('otpverify',otpverify,name="otpverify"),
    path('password',password,name="password"),
    path('logout/',logout,name='logout'),
    path('admin_home',admin_home,name="admin_home"),
    path('admin_userdetail',admin_userdetail,name="admin_userdetail"),
    path('admin_cpdetail',admin_cpdetail,name="admin_cpdetail"),
    path('admin_cp_auth/<str:company_email>/', admin_cp_auth, name='admin_cp_auth'),

    path('category_list',category_list,name="category_list"),
    path('add-category/', add_category, name='add_category'),
    path('delete-category/<int:category_id>/', delete_category, name='delete_category'),
    path('about/', about_us, name='about_us'),
    path('contact/', contact_us, name='contact_us'),
    path('terms/', terms, name='terms'),

  
]
