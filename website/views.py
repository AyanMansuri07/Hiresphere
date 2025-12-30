from django.shortcuts import render,redirect,HttpResponse
from .models import *
# .all the password related inbuild functions
from django.contrib.auth.hashers import check_password, make_password
# from django import request

# Create your views here.

def homepage(request):
    from django.db.models import Q
    query = request.GET.get('search', '')
    
    if query:
        cat = category.objects.filter(
            Q(category_name__icontains=query) | 
            Q(category_description__icontains=query)
        )
    else:
        cat = category.objects.all()

    # Check session data for logged-in or registered users
    loggedin_user = request.session.get('loggedin_user')
    u_registered = request.session.get('u_registered')
    loggedin_company = request.session.get('loggedin_company')

    applied_jobs = []
    user = None  # <- Make sure user is always defined

    if 'u_email' in request.session:
        user = u_register.objects.get(email=request.session['u_email'])
        applied_jobs = JobApplicant.objects.filter(user=user).values_list('job_id', flat=True)

    return render(request, 'home.html', {
        'cat': cat,
        'user_obj': user,  # Will be None if not logged in
        'loggedin_user': loggedin_user,
        'u_registered': u_registered,
        'loggedin_company': loggedin_company,
        'applied_jobs': applied_jobs
    })


def user_register(request):
    if request.method == 'POST':
        cat = category.objects.all()
        # craete a object name user to save further data form post method    
        user = u_register()
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.password =  make_password(request.POST['password'])
        user.phone = request.POST['phone']
        user.address = request.POST['address']  
        request.session['u_email'] = user.email 
        request.session['u_registered'] = user.name    
        user.save() 
        # passing the user as key for homepage data show according to the user or company
        return redirect('home')
    return render(request,'user_register.html')

def company_register(request):
    if request.method == 'POST':
        # craete a object name company to save further data form post method    
        cp = c_register() 
        cp.cp_name = request.POST['cname']
        cp.cp_email = request.POST['c_email']
        cp.cp_password =  make_password(request.POST['password'])
        cp.cp_phone = request.POST['phone']
        cp.cp_gst_no = request.POST['gstno']  
        request.session['cp_email'] = cp.cp_email    
        request.session['c_registered'] = cp.cp_name
        cp.save() 
        # passing the cp as key for homepage data show according to the cp or company
        return redirect('verification')
    return render(request,'cp_register.html')
   
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect, get_object_or_404
from .models import c_register, cp_verify

def verification(request):
    import json

    verify_email = request.session.get('cp_email')

    if not verify_email:
        return redirect('cp_register')

    company = c_register.objects.get(cp_email=verify_email)
    cp_verify_obj, created = cp_verify.objects.get_or_create(company=company)

    field_status = json.loads(cp_verify_obj.field_status_save) if cp_verify_obj.field_status_save else {}

    # 🔹 Ensure status is "Unverified" until admin approves
    if created and not cp_verify_obj.verification_status:
        cp_verify_obj.verification_status = "New Company"
        company.status = "Unverified"
        cp_verify_obj.save()
        company.save()
    elif cp_verify_obj.verification_status == "Updated":
            # cp_verify_obj.verification_status = "Verified" # ❌ Don't do this here!
            cp_verify_obj.save()
            company.status = "Verified"
            company.save()

    if request.method == 'POST':
        # Updating fields
        cp_verify_obj.registration_number = request.POST.get('registration_number', cp_verify_obj.registration_number)
        cp_verify_obj.business_type = request.POST.get('business_type', cp_verify_obj.business_type)
        cp_verify_obj.industry_type = request.POST.get('industry_type', cp_verify_obj.industry_type)
        cp_verify_obj.company_website = request.POST.get('company_website', cp_verify_obj.company_website)
        cp_verify_obj.company_address = request.POST.get('company_address', cp_verify_obj.company_address)
        cp_verify_obj.city = request.POST.get('city', cp_verify_obj.city)
        cp_verify_obj.state = request.POST.get('state', cp_verify_obj.state)
        cp_verify_obj.country = request.POST.get('country', cp_verify_obj.country)
        # cp_verify_obj.postal_code = request.POST.get('postal_code', cp_verify_obj.postal_code)
        cp_verify_obj.area_code = request.POST.get('area_code', cp_verify_obj.area_code)
        # cp_verify_obj.tax_id = request.POST.get('tax_id', cp_verify_obj.tax_id)
        # cp_verify_obj.company_pan = request.POST.get('company_pan', cp_verify_obj.company_pan)
        cp_verify_obj.rep_name = request.POST.get('rep_name', cp_verify_obj.rep_name)
        # cp_verify_obj.rep_designation = request.POST.get('rep_designation', cp_verify_obj.rep_designation)
        cp_verify_obj.rep_phone = request.POST.get('rep_phone', cp_verify_obj.rep_phone)
        cp_verify_obj.rep_email = request.POST.get('rep_email', cp_verify_obj.rep_email)
        cp_verify_obj.num_employees = request.POST.get('num_employees', cp_verify_obj.num_employees)
        cp_verify_obj.year_establishment = request.POST.get('year_establishment', cp_verify_obj.year_establishment)
        cp_verify_obj.company_description = request.POST.get('company_description', cp_verify_obj.company_description)
        cp_verify_obj.linkedin_profile = request.POST.get('linkedin_profile', cp_verify_obj.linkedin_profile)

        # Handling file uploads
        if 'registration_certificate' in request.FILES:
            cp_verify_obj.registration_certificate = request.FILES['registration_certificate']
        if 'company_logo' in request.FILES:
            cp_verify_obj.company_logo = request.FILES['company_logo']
        # if 'government_id' in request.FILES:
        #     cp_verify_obj.government_id = request.FILES['government_id']

        # 🔹 Keep status as "Unverified" until admin verifies all fields
        if cp_verify_obj.verification_status == "New Company":
            cp_verify_obj.verification_status = "Pending"
            company.status = "Unverified"
        elif cp_verify_obj.verification_status == "Pending":
            cp_verify_obj.verification_status = "Updated"
            company.status = "Unverified"
# DO NOT change to Verified here!

        cp_verify_obj.save()
        company.save()

        return redirect('response')

    return render(request, 'verification.html', {'companies': company, 'field_status': field_status,'cp_verify_obj':cp_verify_obj})


# response-------------------------page
import json
def response(request):
    company_email = request.session.get("cp_email")
    if not company_email:
        return redirect('company_register')  # Redirect if no session data found

    # Get the verification details for the current company
    try:
        verification = cp_verify.objects.get(company__cp_email=company_email)
    except cp_verify.DoesNotExist:
        verification = None

    field_status = {}
    if verification and verification.field_status_save:
        field_status = json.loads(verification.field_status_save)  # Deserialize JSON

    return render(request, "response.html", {"field_status": field_status, "verification": verification})


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        cat = category.objects.all()

        # Candidate Login
        if u_register.objects.filter(email=email).exists():
            user = u_register.objects.get(email=email)
            if check_password(password, user.password): 
                request.session['u_email'] = user.email
                request.session['loggedin_user'] = user.name
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid password for candidate account.'})

        # Company Login
        elif c_register.objects.filter(cp_email=email).exists():
            company = c_register.objects.get(cp_email=email)

            if check_password(password, company.cp_password):
                # Check if company has a verification record
                cp_verify_obj = cp_verify.objects.filter(company=company).first()

                # if cp_verify_obj:
                #     if cp_verify_obj.verification_status == "Verified":
                #         # If verified, allow login
                #         request.session['cp_email'] = company.cp_email
                #         request.session['loggedin_company'] = company.cp_name 
                #         return redirect('home')
                #     else:
                #         # If in verification process, redirect to response page
                #         return redirect('response')
                if cp_verify_obj:
                    print("🚀 cp_verify_obj.verification_status =", cp_verify_obj.verification_status)

                    if cp_verify_obj.verification_status.strip().lower() == "verified":
                        request.session['cp_email'] = company.cp_email
                        request.session['loggedin_company'] = company.cp_name
                        return redirect('home')
                    else:
                        # Still under verification
                        request.session['cp_email'] = company.cp_email
                        return redirect('response')
                
                # If no verification record, show verification message
                return render(request, "login.html", {
                    "error": "Complete the verification first.",
                    "show_verify_button": True  # Show 'Verify Now' button
                })
            else:
                return render(request, 'login.html', {'error': 'Invalid password for company account.'})

        # Admin Login
        elif ad_register.objects.filter(admin_email=email).exists():
            admin = ad_register.objects.get(admin_email=email)
            if password == admin.admin_password:
                request.session['admin_email'] = admin.admin_email
                return render(request, 'admin_home.html', {'ad': admin.admin_email})
            else:
                return render(request, 'login.html', {'error': 'Invalid password for admin account.'})

        # Invalid Email
        return render(request, 'login.html', {'emailerror': 'Invalid email for account.'})

    return render(request, 'login.html')

def profile(request):
    user = u_register.objects.get(email=request.session['u_email'])

    if request.method == "POST":
        user.name = request.POST['name']
        user.phone = request.POST['phone']
        user.address = request.POST['address']
        user.skills = request.POST['skills']
        user.social = request.POST['social']

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        if 'resume' in request.FILES:
            user.resume = request.FILES['resume']
        
        user.save()
        return redirect('profile')

    return render(request, "profile.html", {"loggedin_user": user,"user_obj": user  })

   
def logout(request):
    # Clear all related session data
    keys_to_delete = ['u_email', 'cp_email', 'admin_email', 'loggedin_user', 'u_registered', 'loggedin_company']
    
    for key in keys_to_delete:
        if key in request.session:
            del request.session[key]

    return redirect('home')

import razorpay
from django.conf import settings


from googleapiclient.discovery import build
from django.conf import settings
from django.shortcuts import render
from .models import u_register

# ✅ Add your YouTube API Key here



from django.core.mail import send_mail
import random
def email(request):
    if request.method == 'POST':
        email = request.POST['email']
        if u_register.objects.filter(email=request.POST['email']).exists() or c_register.objects.filter(cp_email=email).exists():# Get the email from the form
            otp = random.randint(1111, 9999)
            send_mail(
                        'This is OTP verification mail',
                        f'Your OTP: {otp}',
                        'prajapatiyash168@gmail.com',  # Sender email
                        [email],  # Receiver email
                        fail_silently=False
                    )
            request.session['OTP'] = otp 
            print(otp)
            request.session['email'] = email 
           
            return redirect('otpverify')
        else:
            return render(request,'email.html',{'email':request.POST['email']})
    else:
        return render(request,'email.html')
from django.utils.timezone import now
from django.shortcuts import render, redirect
from .models import tender, c_register

def post_tender(request):
    tendercp = request.session.get('loggedin_company')

    if request.method == "POST":
        company = c_register.objects.get(cp_email=request.session['cp_email'])  # Get the logged-in company

        # Extract form data
        title = request.POST.get("title")
        description = request.POST.get("description")
        budget = request.POST.get("budget")
        deadline = request.POST.get("deadline")
        location = request.POST.get("location")
        industry_type = request.POST.get("industry_type")
        eligibility = request.POST.get("eligibility")
        tender_type = request.POST.get("tender_type")
        contact_person = request.POST.get("contact_person")
        contact_email = request.POST.get("contact_email")
        contact_phone = request.POST.get("contact_phone")
        terms_file = request.FILES.get("terms_file")

        # Basic validation
        if all([title, description, budget, deadline, location, industry_type, contact_person, contact_email, contact_phone]):
            tender.objects.create(
                title=title,
                description=description,
                budget=budget,
                deadline=deadline,
                location=location,
                industry_type=industry_type,
                eligibility=eligibility,
                
                contact_person=contact_person,
                contact_email=contact_email,
                contact_phone=contact_phone,
                terms_file=terms_file,
                company=company,
                created_at=now()
            )
            return redirect("tender_list")

        # Optional: add an error message if fields are missing
        return render(request, "post_tender.html", {
            'tendercp': tendercp,
            'error': 'Please fill all required fields.'
        })

    return render(request, "post_tender.html", {'tendercp': tendercp})

def tender_list(request):
    company_email = request.session.get('cp_email')
    your_tenders = request.GET.get("your") == "true"
    loggedin_company = request.session.get('loggedin_company')

    if your_tenders and company_email:
        company = c_register.objects.get(cp_email=company_email)
        tenders = tender.objects.filter(company=company).order_by('-created_at')
    else:
        tenders = tender.objects.all().order_by('-created_at')

    return render(request, 'tender_list.html', {
        'tenders': tenders,
        'your_tenders': your_tenders,
        'loggedin_company': loggedin_company,
    })
def apply_tender(request, tender_id):
    if 'cp_email' not in request.session:
        return redirect('login')

    applying_company = get_object_or_404(c_register, cp_email=request.session['cp_email'])
    selected_tender = get_object_or_404(tender, id=tender_id)

    if selected_tender.company == applying_company:
        return render(request, 'error.html', {'message': 'You cannot apply to your own tender.'})

    cp_verify_obj = cp_verify.objects.filter(company=applying_company).first()

    if request.method == 'POST':
        contact_person = request.POST['contact_person']
        contact_email = request.POST['contact_email']
        proposal_summary = request.POST['proposal_summary']
        attached_file = request.FILES.get('attached_file')

        TenderApplication.objects.create(
            tender=selected_tender,
            applying_company=applying_company,
            contact_person=contact_person,
            contact_email=contact_email,
            proposal_summary=proposal_summary,
            attached_file=attached_file
        )

        Notification.objects.create(
            company=applying_company,
            message=f"You applied for the tender: '{selected_tender.title}'",
            recipient_type='cp'
        )

        Notification.objects.create(
            company=selected_tender.company,
            message=f"{applying_company.cp_name} applied for your tender: '{selected_tender.title}'",
            recipient_type='cp'
        )

        return redirect('tender_list')

    return render(request, 'tender_apply.html', {
        'tender': selected_tender,
        'poster': selected_tender.company,
        'cp': applying_company,
        'cp_verify': cp_verify_obj,
    })


def otpverify(request):
    if request.method == 'POST':  
        enterdotp=int(request.POST['otp1'])
        print(enterdotp)
        if int(request.session['OTP']) == enterdotp:
         
            return redirect('password')
        else:
            return render(request, 'otpverify.html')
    else:
        return render(request,'otp_verify.html')

def password(request):
    if request.method == 'POST':
        password = request.POST['password']
        email = request.session['email']
        if u_register.objects.filter(email=email).exists():
            user = u_register.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            del request.session['OTP']
            del request.session['email']
            return redirect('login')
        elif c_register.objects.filter(cp_email=email).exists():
            company = c_register.objects.get(cp_email=email)
            company.cp_password = make_password(password)
            company.save()
            del request.session['OTP']
            del request.session['email']
            return redirect('login')
    else:
            return render(request, 'password.html', {'error': 'Password and confirm password do not match!'})
def jobs(request, category_id ,category_name):
    if 'u_email' in request.session:
        user = u_register.objects.get(email=request.session['u_email']) 
        loggedin_user = request.session.get('loggedin_user')
        from django.db.models import Q
        query = request.GET.get('search', '')
        selected_sub_job = request.GET.get('sub_job', '')

        if query:
            jobs = sub_job.objects.filter(
                Q(category_id=category_id) &
                (
                    Q(job_title__icontains=query) |
                    Q(job_description__icontains=query) |
                    Q(job_qualification__icontains=query) |
                    Q(job_type__icontains=query)
                ) &
                Q(company__status='Verified')
            )
        elif selected_sub_job:
            jobs = sub_job.objects.filter(
                Q(category_id=category_id) &
                Q(job_title__icontains=selected_sub_job) &
                Q(company__status='Verified')
            )
        else:
            jobs = sub_job.objects.filter(
                category_id=category_id,
                company__status='Verified'
            )

        # ✅ Add company logo to each job from verification model
        for job in jobs:
            try:
                verification = cp_verify.objects.get(company=job.company)
                job.company_logo = verification.company_logo.url if verification.company_logo else None
            except cp_verify.DoesNotExist:
                job.company_logo = None

        sub_jobs = sub_job.objects.filter(category_id=category_id).values_list('job_title', flat=True)

        return render(request, 'jobs.html', {
            'JOBS': jobs,
            'sub_jobs': sub_jobs,
            'query': query,
            'category_name': category_name,
            'selected_sub_job': selected_sub_job,
            'loggedin_user': loggedin_user,
            'user_obj': user, 
            'u_registered': user.name,
        })

    else:
        return redirect('home')



def job_apply(request, job_id):
    if 'u_email' not in request.session:
        return redirect('login')

    try:
        job = sub_job.objects.get(id=job_id)
        company = job.company
        user_email = request.session.get('u_email')
        user = u_register.objects.get(email=user_email)
    except sub_job.DoesNotExist:
        return HttpResponse("Job not found", status=404)
    except u_register.DoesNotExist:
        return HttpResponse("User not found", status=404)

    # Prevent duplicate applications
    if JobApplicant.objects.filter(user=user, company=company, job=job).exists():
        return render(request, 'job_apply.html', {
            'job': job,
            'company': company,
            'user': user,
            'error': "You have already applied for this job."
        })

    if request.method == 'POST':
        # Get form data
        cover_letter = request.POST.get('cover_letter')
        linkedin = request.POST.get('linkedin')
        portfolio = request.POST.get('portfolio')
        expected_salary = request.POST.get('expected_salary')
        resume = user.resume  # using pre-uploaded resume from user model
        # resume can also be: request.FILES.get('resume') if allowing re-upload

        # Save application
        application = JobApplicant.objects.create(
            user=user,
            job=job,
            company=company,
            cover_letter=cover_letter,
            linkedin=linkedin,
            portfolio=portfolio,
            expected_salary=expected_salary,
            resume=resume  # You can switch to request.FILES.get('resume') if needed
        )

        # ✅ Notification for User
        Notification.objects.create(
            company=company,
            job=job,
            message=f"📢 You have successfully applied for '{job.job_title}' at '{company.cp_name}'.",
            recipient_type="user",
            created_at=now(),
        )

        # ✅ Notification for CP
        Notification.objects.create(
            company=company,
            job=job,
            message=f"🆕 New applicant '{user.name}' applied for '{job.job_title}'.",
            recipient_type="cp",
            created_at=now(),
        )

        return redirect('jobs', category_id=job.category.id, category_name=job.category.category_name)

    return render(request, 'job_apply.html', {
        'job': job,
        'company': company,
        'user': user
    })
def jobs_applied(request):
    
    if 'u_email' not in request.session:
        return redirect('login')  # Ensure only logged-in users can view

    user = u_register.objects.get(email=request.session['u_email'])  # Get logged-in user

    applied_jobs = JobApplicant.objects.filter(user=user).select_related('job')  # Fetch applied jobs

    return render(request, 'jobs_applied.html', {'applied_jobs': applied_jobs})


def post_job(request):
    cat = category.objects.all()

    if 'cp_email' in request.session:  # Ensure company is logged in
        company = c_register.objects.get(cp_email=request.session['cp_email'])  # Get logged-in company

        if request.method == "POST":
            category_id = request.POST.get('category')
            if category_id:
                job = sub_job()
                job.category_id = category_id
                job.company = company  # Assign the logged-in company
                job.job_title = request.POST['job_title']
                job.job_description = request.POST['job_description']
                
                job.job_salary = request.POST['job_salary']
                job.job_location = request.POST['job_location']
                job.job_experience = request.POST['job_experience']
                job.job_skils = request.POST['job_skils']
                job.job_qualification = request.POST['job_qualification']
                job.job_vacancy = request.POST['job_vacancy']

                job.save()
                return render(request, 'home.html', {'cat': cat, 'company': company, 'success': 'Job posted successfully!'})

            else:
                return render(request, 'post_job.html', {'cat': cat, 'company': company, 'error': 'Please select a category.'})

        return render(request, 'post_job.html', {'cat': cat, 'company': company})

    else:
        return redirect('login')  # Redirect to login if no company is logged in


def postedjobs(request):
    if 'cp_email' in request.session:
        company = c_register.objects.get(cp_email=request.session['cp_email'])
        jobs = sub_job.objects.filter(company=company)

        # Attach company logo to each job (if available)
        for job in jobs:
            try:
                job.company_logo = cp_verify.objects.get(company=job.company).company_logo.url
            except:
                job.company_logo = None  # fallback if logo not found

        return render(request, 'postedjobs.html', {'jobs': jobs, 'company': company,'loggedin_company': request.session.get('loggedin_company'),})
    else:
        return redirect('login')



def update_post_job(request, job_id):
    if 'cp_email' in request.session:  # Ensure company is logged in
        company = c_register.objects.get(cp_email=request.session['cp_email'])  # Get logged-in company

        # Fetch the job for editing
        try:
            job = sub_job.objects.get(id=job_id, company=company)
        except sub_job.DoesNotExist:
            return render(request, 'update_post_job.html', {'error': 'Job not found or unauthorized access.'})

        categories = category.objects.all()  # Load all categories for dropdown

        if request.method == "POST":
            # Update the existing job data
            job.category_id = request.POST.get('category')
            job.job_title = request.POST['job_title']
            job.job_description = request.POST['job_description']
            job.job_type = request.POST['job_type']
            job.job_salary = request.POST['job_salary']
            job.job_location = request.POST['job_location']
            job.job_experience = request.POST['job_experience']
            job.job_skils = request.POST['job_skils']
            job.job_qualification = request.POST['job_qualification']
            job.job_vacancy = request.POST['job_vacancy']

            job.save()
            return render(request, 'update_post_job.html', {
                'job': job,
                'categories': categories,
                'company': company,
                'success': 'Job updated successfully!'
            })

        return render(request, 'update_post_job.html', {
            'job': job,
            'categories': categories,
            'company': company
        })

    else:
        return redirect('login')  # Redirect if no company is logged in
    
from django.shortcuts import render, redirect
from .models import JobApplicant, c_register

def job_applicants(request):
    if 'cp_email' not in request.session:
        return redirect('login')  # Ensure only logged-in companies can view

    company = get_object_or_404(c_register, cp_email=request.session['cp_email'])
    applicants = JobApplicant.objects.filter(company=company).select_related('user', 'job')

    if request.method == "POST":
        applicant_id = request.POST.get("applicant_id")
        selected_date = request.POST.get("interview_date")
        

        if applicant_id and selected_date:
            applicant = get_object_or_404(JobApplicant, id=applicant_id)
            applicant.interview_date = selected_date  # Update interview date
            applicant.save()

    return render(request, 'job_applicant.html', {
        'company': company,
        'applicants': applicants
    })

def notifications(request):
    loggedin_company = request.session.get('loggedin_company')
    if 'cp_email' not in request.session:
        return redirect('login')

    company = c_register.objects.get(cp_email=request.session['cp_email'])

    # ✅ Show only CP notifications
    notifications = Notification.objects.filter(
        company=company, recipient_type="cp"
    ).order_by('-created_at')

    return render(request, 'notification.html', {'cp_notifications': notifications,'loggedin_company': loggedin_company})

def user_notifications(request):
    loggedin_user = request.session.get('loggedin_user')
    if 'u_email' not in request.session:
        return redirect('login')

    user = u_register.objects.get(email=request.session['u_email'])

    # ✅ Show only user notifications
    notifications = Notification.objects.filter(
        job__jobapplicant__user=user, recipient_type="user"
    ).distinct().order_by('-created_at')

    return render(request, 'user_notifications.html', {'notifications': notifications,'loggedin_user': loggedin_user})

def selected(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    # ✅ Get the job posting related to this notification
    job = notification.job  # Fetch job details
    company = job.company  # Fetch the company from job posting
    job_location = job.job_location  # ✅ Get the location from sub_job

    # ✅ Get the interview date for this user & job
    job_applicant = JobApplicant.objects.filter(job=job, user__email=request.session.get('u_email')).first()

    if not job_applicant:
        return render(request, 'error.html', {'message': "Job application not found!"})

    context = {
        'notification': notification,
        'company': company,
        'company_address': job_location,  # ✅ Now using job_location from sub_job
        'job': job,
        'interview_date': job_applicant.interview_date
    }

    return render(request, 'selected.html', context)


from datetime import datetime
from django.utils.timezone import now

def user_verifybycp(request, applicant_id):
    applicant = get_object_or_404(JobApplicant, id=applicant_id)

    if request.method == "POST":
        

        if request.method == "POST":
        # 🔽 Get the date and time from POST request
            interview_datetime_str = request.POST.get('interview_date')

        # 🔽 Convert string to datetime object
        if interview_datetime_str:
            final_date = datetime.strptime(interview_datetime_str, '%Y-%m-%dT%H:%M')
        else:
            final_date = None

        # ✅ Save interview date & update status
        applicant.status = "Reviewed"
        applicant.interview_date = final_date  # if you have a field for it
        applicant.save()

        # ✅ Create a Notification for the User (Correct Tagging)
        Notification.objects.create(
            company=applicant.company,
            job=applicant.job,
            message=f"🎉 You have been selected for '{applicant.job.job_title}' at '{applicant.company.cp_name}'. Your interview is scheduled on {final_date.strftime('%B %d, %Y at %I:%M %p')}.",
            recipient_type="user",
            created_at=now(),
        )

        # ✅ Create a Notification for the CP (Correct Tagging)
        Notification.objects.create(
            company=applicant.company,
            job=applicant.job,
            message=f"✅ You have successfully verified {applicant.user.name} for '{applicant.job.job_title}'. Interview scheduled for {final_date.strftime('%B %d, %Y at %I:%M %p')}.",
            recipient_type="cp",
            created_at=now(),
        )

        # ✅ Redirect back to job_applicants page
        return redirect('job_applicants')

    return render(request, 'user_verifybycp.html', {'applicant': applicant})


def admin_home(request):
    if 'admin_email' in request.session:
        return render(request,'admin_home.html')
    else:
        return redirect('login')

def admin_userdetail(request):
    user = u_register.objects.all()
   
    return render(request,'admin_userdetail.html',{'user':user})
 
from django.shortcuts import render
from .models import c_register


def admin_cpdetail(request):
    companies_data = []
    all_verifications = cp_verify.objects.select_related('company').all()

    for v in all_verifications:
        companies_data.append({
            'cp_name': v.company.cp_name,
            'cp_email': v.company.cp_email,
            'verification_status': v.verification_status,  # from cp_verify
            'status': v.company.status,  # from c_register
        })

    return render(request, 'admin_cpdetail.html', {'companies': companies_data})

from django.shortcuts import get_object_or_404, redirect, render
import json






# ------------this codd is complete ok ------------------------------------
from django.shortcuts import get_object_or_404, redirect, render
import json

def admin_cp_auth(request, company_email):
    verification = get_object_or_404(cp_verify, company__cp_email=company_email)
    company = verification.company

    if request.method == "POST":
        # ✅ Collect status of each field from form checkboxes
        field_status = {
            field: "✅" if request.POST.get(field) else "❌"
            for field in [
                "verify_name", "verify_email", "verify_phone", "verify_gst",
                "verify_registration", "verify_business_type", "verify_industry_type",
                "verify_website", "verify_address", "verify_city", "verify_state",
                "verify_country", "verify_area_code", 
                "verify_logo",
                "verify_certificate", "verify_government_id", "verify_rep_name", 
                "verify_rep_phone", "verify_rep_email",
                "verify_num_employees", "verify_year_establishment", 
                "verify_company_description", "linkedin_profile"
            ]
        }

        # ✅ Save field statuses in the database
        verification.field_status_save = json.dumps(field_status)

        # ✅ Auto-verify only if ALL fields are marked ✅
        if all(value == "✅" for value in field_status.values()):
            verification.verification_status = "Verified"
            company.status = "Verified"
        else:
            verification.verification_status = "Pending"
            company.status = "Unverified"

        # ✅ Save both models
        verification.save()
        company.save()

        # ✅ Reload from DB for template if needed later
        verification.refresh_from_db()
        company.refresh_from_db()

        return redirect('admin_cpdetail')  # 🔄 Back to list of companies

    return render(request, "admin_cp_auth.html", {
        "verification": verification,
    })
# ----------------------------------    this cod e is complete ok ------------------

# Display categories
def category_list(request):
    categories = category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

from django.core.files.storage import FileSystemStorage
# Add category
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        category_description = request.POST['category_description']
        image = request.FILES.get('image')
        job_type = request.POST['job_type']
        
        if image:
            fs = FileSystemStorage()
            image = fs.save(image.name, image)

        category.objects.create(category_name=category_name, image=image, category_description=category_description , job_type=job_type)
        return redirect('category_list')
    return render(request, 'add_category.html')


def delete_category(request, category_id):
    cat_obj = category.objects.get(id=category_id)
    cat_obj.delete()
    return redirect('category_list')

def about_us(request):
    loggedin_user = request.session.get('loggedin_user')

    return render(request, 'aboutus.html', {'loggedin_user': loggedin_user})

def contact_us(request):
    loggedin_user = request.session.get('loggedin_user')

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Here you can handle the message: store in DB, send email, etc.
        return render(request, 'contactus.html', {'success': True})
    return render(request, 'contactus.html',{'loggedin_user': loggedin_user,})

def terms(request): 
    return render(request, 'terms.html')