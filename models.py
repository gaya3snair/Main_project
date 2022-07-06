from django.db import models
#user_login,user_details,file_store, file_share, auditor_details
# Create your models here.

class user_login(models.Model):
    uname = models.CharField(max_length=150)
    password = models.CharField(max_length=50)
    utype = models.CharField(max_length=50)

class user_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    profile_name = models.CharField(max_length=50)
    dob = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    addr = models.CharField(max_length=500)
    pin = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    email = models.CharField(max_length=150)
    status = models.CharField(max_length=50)

class file_store(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=150)
    fpath = models.CharField(max_length=150)
    fsize = models.CharField(max_length=50)
    fsign = models.CharField(max_length=150)
    file_extension = models.CharField(max_length=150)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

class file_share(models.Model):
    user_id = models.IntegerField()
    file_id = models.IntegerField()
    status = models.CharField(max_length=50)
    dt = models.CharField(max_length=50)
    tm = models.CharField(max_length=50)
    remark = models.CharField(max_length=500)

class auditor_details(models.Model):
    user_id = models.IntegerField()
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    profile_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=50)
    addr = models.CharField(max_length=500)
    pin = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    status = models.CharField(max_length=50)

class audit_request(models.Model):
    user_id = models.IntegerField()
    auditor_id = models.IntegerField()
    file_id = models.IntegerField()
    status = models.CharField(max_length=150)

class org_files(models.Model):
    user_id = models.IntegerField()
    auditor_id = models.IntegerField()
    file_path = models.CharField(max_length=150)
    dt = models.CharField(max_length=25)