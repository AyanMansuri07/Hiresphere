from django.db import models

# Create your models here.
class u_register(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    phone=models.IntegerField()
    address=models.TextField()
    skills = models.TextField(blank=True, null=True)  
    social = models.TextField(blank=True, null=True)  
    gender=models.CharField(default='male',max_length=10) 
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True) 
    resume = models.FileField(null=True,blank=True)

    def __str__(self):
        return self.name
    
class c_register(models.Model):
    cp_name = models.CharField(max_length=255)
    cp_email = models.EmailField(unique=True)
    cp_phone = models.CharField(max_length=15)
    cp_gst_no = models.CharField(max_length=50)
    cp_password = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False) 
    STATUS_CHOICES = [
        ('Unverified', 'Unverified'),
        ('Verified', 'Verified'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Unverified'
    )
    

    def __str__(self):
        return self.cp_name
    
class ad_register(models.Model):
    admin_email = models.EmailField(default=" ")
    admin_password = models.CharField(max_length=8)
    
    def __str__(self):
        return self.admin_email
    
class category(models.Model):
    category_name=models.CharField(max_length=50)
    category_description=models.TextField()
    job_type = models.CharField(max_length=20, choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'),('Freelancer','Freelancer')], default='Full-Time')
    image = models.ImageField(upload_to='images/')
   

    def __str__(self):
        return self.category_name
    
    #this sub_job is called jobs page which is second page after click on the cat like docter in home page
    # job.html ref 
class sub_job(models.Model):
    id = models.AutoField(primary_key=True)
    # category_id=models.ForeignKey(category,on_delete=models.CASCADE)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    company = models.ForeignKey(c_register, on_delete=models.CASCADE)  

    job_title=models.CharField(max_length=50)
    job_description=models.TextField()
    job_type = models.CharField(max_length=20, choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'),('Freelancer','Freelancer')], default='Full-Time')
    # job_image = models.ImageField(upload_to='images/')
    job_salary = models.IntegerField()
    job_location = models.CharField(max_length=50)
    job_skils = models.CharField(max_length=50)
    job_experience = models.IntegerField()
    job_qualification = models.CharField(max_length=50)
    job_vacancy = models.IntegerField()
    # job_date = models.DateField()
    job_apply = models.CharField(max_length=50)
   
    def __str__(self):
        return self.job_title


class JobApplicant(models.Model):
    user = models.ForeignKey('u_register', on_delete=models.CASCADE)  # Candidate applying for the job
    job = models.ForeignKey('sub_job', on_delete=models.CASCADE)  # Job being applied for
    company = models.ForeignKey('c_register', on_delete=models.CASCADE)  # Company that posted the job

    resume = models.FileField(upload_to='resumes/', null=True, blank=True)  # Resume upload
    cover_letter = models.TextField(null=True, blank=True)  # Candidate's message
    linkedin = models.URLField(null=True, blank=True)  # LinkedIn Profile (optional)
    portfolio = models.URLField(null=True, blank=True)  # Portfolio or personal website (optional)
    
    expected_salary = models.IntegerField(null=True, blank=True)  # Candidate's expected salary
    notice_period = models.CharField(max_length=20, choices=[
        ('Immediate', 'Immediate'),
        ('15 Days', '15 Days'),
        ('1 Month', '1 Month'),
        ('2 Months', '2 Months')
    ], default='Immediate')  # Notice period selection
    
    interview_date = models.DateTimeField(null=True, blank=True) # Available interview date
    
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Reviewed', 'Reviewed'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected')
    ], default='Pending')  # Application status

    applied_at = models.DateTimeField(auto_now_add=True)  # Automatically store application date

    def __str__(self):
        return f"{self.user.name} applied for {self.job.job_title} at {self.company.cp_name}"

class cp_verify(models.Model):
    company = models.OneToOneField(c_register, on_delete=models.CASCADE)  # Link to registered company
    c_email = models.EmailField(blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    business_type = models.CharField(max_length=50, choices=[
        ('Private', 'Private'), ('Public', 'Public'), ('LLP', 'LLP'), ('Other', 'Other')
    ])
    industry_type = models.CharField(max_length=50, choices=[
        ('IT', 'IT'), ('Finance', 'Finance'), ('Healthcare', 'Healthcare'), 
        ('Manufacturing', 'Manufacturing'), ('Retail', 'Retail'), ('Other', 'Other')
    ])
    company_website = models.URLField(blank=True, null=True)
    company_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    # postal_code = models.CharField(max_length=20)
    area_code = models.CharField(max_length=10)

    registration_certificate = models.FileField(upload_to='documents/')
    # tax_id = models.CharField(max_length=50, blank=True, null=True)
    # company_pan = models.CharField(max_length=50, blank=True, null=True)
    company_logo = models.FileField(upload_to='logos/', blank=True, null=True)

    rep_name = models.CharField(max_length=255)
    # rep_designation = models.CharField(max_length=100)
    rep_phone = models.CharField(max_length=15)
    rep_email = models.EmailField()
    # government_id = models.FileField(upload_to='documents/')

    num_employees = models.IntegerField(blank=True, null=True)
    year_establishment = models.IntegerField(blank=True, null=True)
    company_description = models.TextField()
    linkedin_profile = models.URLField(blank=True, null=True)
    
    STATUS_CHOICES = [
        ('New Company', 'New Company'),
        ('Pending', 'Pending'),
        ('Updated', 'Updated'),
        ('Verified', 'Verified')
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='New Company')  # Default is New Company


    verification_status = models.CharField(max_length=20, choices=[
        ('New Company', 'New Company'),('Pending', 'Pending'), ('Updated', 'Updated'), ('Verified', 'Verified')
    ], default='New Company')
    field_status_save = models.JSONField(null=True, blank=True) 

    def save(self, *args, **kwargs):
        """ Auto-fill c_email from the related company's cp_email """
        if self.company:
            self.c_email = self.company.cp_email
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.company.cp_name} - {self.verification_status}"

class Notification(models.Model):
    company = models.ForeignKey(c_register, on_delete=models.CASCADE)
    job = models.ForeignKey(sub_job, null=True, blank=True, on_delete=models.SET_NULL)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ NEW FIELD: Determines if notification is for a User or CP
    TYPE_CHOICES = [
        ('user', 'User'),
        ('cp', 'Company'),
    ]
    recipient_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='user')

    def __str__(self):
        return f"Notification for {self.company.cp_name}: {self.message}"

class tender(models.Model):
    TENDER_TYPES = [
        ('Open', 'Open Tender'),
        ('Limited', 'Limited Tender'),
        ('Single', 'Single Tender'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    location = models.CharField(max_length=255,blank=True, null=True)
    industry_type = models.CharField(max_length=100,blank=True, null=True)
    eligibility = models.TextField(blank=True, null=True)
    contact_person = models.CharField(max_length=100,blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    contact_phone = models.CharField(max_length=15,blank=True, null=True)
    tender_type = models.CharField(max_length=20, choices=TENDER_TYPES, default='Open')
    terms_file = models.FileField(upload_to='tender_terms/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey('c_register', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    
class TenderApplication(models.Model):
    tender = models.ForeignKey(tender, on_delete=models.CASCADE, related_name='applications')
    applying_company = models.ForeignKey(c_register, on_delete=models.CASCADE, related_name='tender_applications')
    
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    proposal_summary = models.TextField()
    attached_file = models.FileField(upload_to='tender_proposals/', null=True, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applying_company.cp_name} → {self.tender.title}"
