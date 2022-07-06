from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from .models import user_login

def index(request):
    return render(request,'./myapp/index.html')

def about(request):
    return render(request,'./myapp/about.html')

def contact(request):
    return render(request,'./myapp/contact.html')

def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, password=pwd, utype='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = ' Invalid Uname or Password !!!'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')

def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,password=opasswd,utype='admin')
            if ul is not None:
                ul.password=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)

from .models import file_store
from datetime import datetime
from django.core.files.storage import FileSystemStorage
def admin_file_store_add(request):
    if request.method == 'POST':
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        fname = fs.get_valid_name(u_file.name)

        fpath = fs.save(u_file.name, u_file)
        fsize = fs.size(fpath)
        user_id = int(request.session['user_id'])
        fsign = '1234567890'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'notshared'
        fs = file_store(user_id=user_id,fname=fname,fpath=fpath,fsize=fsize,fsign=fsign,dt=dt,tm=tm,status=status)
        fs.save()
        context = {'msg': 'Record Added'}
        return render(request, './myapp/admin_file_store_add.html', context)
    else:
        return render(request, './myapp/admin_file_store_add.html')


def admin_file_store_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    fs = file_store.objects.get(id=int(id))
    fs.delete()
    msg = 'Record Deleted'
    user_id = int(request.session['user_id'])
    fs_l = file_store.objects.filter(user_id=user_id)
    context = {'file_list': fs_l,'msg':msg}
    return render(request, './myapp/admin_file_store_view.html',context)

def admin_file_store_view(request):
    user_id = int(request.session['user_id'])
    fs_l = file_store.objects.filter(user_id=user_id)
    context = {'file_list': fs_l}
    return render(request, './myapp/admin_file_store_view.html', context)

def admin_user_details_view(request):
    cm_l = user_details.objects.all()
    context = {'user_list': cm_l}
    return render(request, './myapp/admin_user_details_view.html',context)

def admin_auditor_details_view(request):
    cm_l = auditor_details.objects.all()
    context = {'auditor_list': cm_l}
    return render(request, './myapp/admin_auditor_details_view.html',context)

def admin_auditor_reg_request_view(request):
    ad_l = user_login.objects.filter(utype='pending')
    ad = auditor_details.objects.all()
    context = {'auditor_list':ad_l, 'ad':ad}
    return render(request, './myapp/admin_auditor_reg_request_view.html',context)


def admin_approve_reject_auditor(request):
    id = request.GET.get('id')
    utype = request.GET.get('status')
    ad = user_login.objects.get(id=int(id))
    ad.utype = utype
    ad.save()
    ad = auditor_details.objects.all()
    ad_l = user_login.objects.filter(utype='')
    context = {'auditor_list': ad_l,'ad':ad}
    return render(request, './myapp/admin_auditor_reg_request_view.html', context)


######## USER ############################################################################################################
from .models import user_details

def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        profile_name = request.POST.get('profile_name')

        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        print(gender)
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        uname=email
        status = "new"

        ul = user_login(uname=uname, password=password, utype='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender, dob=dob,addr=addr, pin=pin, contact=contact,
                               status=status,email=email,profile_name=profile_name )
        ud.save()

        print(user_id)
        context={'msg':'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')

        ul = user_login.objects.filter(uname=uname, password=password,utype='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}

            return render(request, 'myapp/user_home.html',context)
        else:
            context={'msg':'Invalid username or password'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)

def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('npasswd')
        current_password = request.POST.get('opasswd')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context={'msg':'Password changed'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password not changed'}
                return render(request, './myapp/user_changepassword.html',context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password not changed'}
            return render(request, './myapp/user_changepassword.html',context)
    else:
        return render(request, './myapp/user_changepassword.html')

import pyAesCrypt
def user_file_store_add(request):
    if request.method == 'POST':
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        fname = fs.get_valid_name(u_file.name)

        fpath = fs.save(u_file.name, u_file)

        #################
        file_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{fpath}')
        file_name, file_extension = os.path.splitext(file_path)
        ##################
        password = "please-use-a-long-and-random-password"
        pyAesCrypt.encryptFile(file_path,file_path+".aes",password)


        #################
        fsize = fs.size(fpath)
        user_id = int(request.session['user_id'])
        fsign = '1234567890'
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'notshared'
        fs = file_store(user_id=user_id,fname=fname,fpath=fpath,fsize=fsize,fsign=fsign,file_extension=file_extension,dt=dt,tm=tm,status=status)
        fs.save()
        #os.remove(file_path)
        context = {'msg': 'Record Added'}
        return render(request, './myapp/user_file_store_add.html', context)
    else:
        return render(request, './myapp/user_file_store_add.html')


def user_file_store_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    fs = file_store.objects.get(id=int(id))
    fs.delete()
    msg = 'Record Deleted'
    user_id = int(request.session['user_id'])
    fs_l = file_store.objects.filter(user_id=user_id)
    context = {'file_list': fs_l,'msg':msg}
    return render(request, './myapp/user_file_store_view.html',context)

def user_file_store_download(request):

    id = request.GET.get('id')
    print('id = '+id)
    fs = file_store.objects.get(id=int(id))
    file_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{fs.fpath}')
    password = "please-use-a-long-and-random-password"
    pyAesCrypt.decryptFile(file_path+ ".aes", file_path , password)

    context = {'fileurl': fs.fpath}
    return render(request, './myapp/user_file_store_download.html',context)

def user_file_store_view(request):
    user_id = int(request.session['user_id'])
    fs_l = file_store.objects.filter(user_id=user_id)
    context = {'file_list': fs_l}
    return render(request, './myapp/user_file_store_view.html', context)

def user_auditor_details_view(request):
    user_id = int(request.session['user_id'])
    ad_l = auditor_details.objects.all()
    context = {'auditor_list': ad_l}
    return render(request, './myapp/user_auditor_details_view.html', context)

def user_file_share_update(request):

    user_id = int(request.session['user_id'])
    file_id = request.GET.get('file_id')
    status = request.GET.get('status')
    fs = file_share.objects.get(id=int(file_id))
    fs.status=status
    fs.save()
    return user_file_share_view(request)

def user_file_share_view(request):
    user_id = int(request.session['user_id'])
    fs_l = file_store.objects.filter(user_id=user_id)
    tfshare_l = []
    for fs in fs_l:
        fshare_l =file_share.objects.filter(file_id = fs.id)
        for fshare in fshare_l:
            tfshare_l.append(fshare)
    context = {'share_list': tfshare_l,'file_list': fs_l}
    return render(request, './myapp/user_file_share_view.html', context)



######## AUDITOR ##############
from .models import auditor_details

def auditor_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        profile_name = request.POST.get('profile_name')

        gender = request.POST.get('gender')

        print(gender)
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        uname=email
        status = "new"

        ul = user_login(uname=uname, password=password, utype='pending')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ad = auditor_details(user_id=user_id,fname=fname, lname=lname, gender=gender, addr=addr, pin=pin, contact=contact,
                               status=status,email=email,profile_name=profile_name )
        ad.save()

        print(user_id)
        context={'msg':'Auditor Registered'}
        return render(request, 'myapp/auditor_login.html',context)

    else:
        return render(request, 'myapp/auditor_details_add.html')

def auditor_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('password')

        ul = user_login.objects.filter(uname=uname, password=password,utype='auditor')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}

            return render(request, 'myapp/auditor_home.html',context)
        else:
            context={'msg':'Invalid username or password'}
            return render(request, 'myapp/auditor_login.html',context)
    else:
        return render(request, 'myapp/auditor_login.html')

def auditor_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/auditor_home.html',context)

def auditor_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return auditor_login_check(request)
    else:
        return auditor_login_check(request)

def auditor_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('npasswd')
        current_password = request.POST.get('opasswd')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                context={'msg':'Password changed'}
                return render(request, './myapp/auditor_changepassword.html',context)
            else:
                context = {'msg': 'Password not changed'}
                return render(request, './myapp/auditor_changepassword.html',context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password not changed'}
            return render(request, './myapp/auditor_changepassword.html',context)
    else:
        return render(request, './myapp/auditor_changepassword.html')

def auditor_user_details_view(request):
    user_id = int(request.session['user_id'])
    ud_l = user_details.objects.all()
    context = {'user_list': ud_l}
    return render(request, './myapp/auditor_user_details_view.html', context)

def auditor_user_file_store_view(request):
    user_id = request.GET.get('user_id')
    ud = user_details.objects.get(id=int(user_id))
    fs_l = file_store.objects.filter(user_id=ud.user_id)
    context = {'file_list': fs_l}
    return render(request, './myapp/auditor_user_file_store_view.html', context)

from .models import file_share
def auditor_file_share_add(request):

    user_id = int(request.session['user_id'])
    file_id = request.GET.get('file_id')
    dt = datetime.today().strftime('%Y-%m-%d')
    tm = datetime.today().strftime('%H:%M:%S')
    status = 'notshared'
    remark= 'none'
    fs = file_share(user_id=user_id,file_id=file_id,dt=dt,tm=tm,status=status,remark=remark)
    fs.save()
    context = {'msg': 'Request send successfully'}
    return render(request, './myapp/auditor_file_share_add.html', context)

def auditor_file_share_view(request):
    user_id = int(request.session['user_id'])
    fshare_l =file_share.objects.filter(user_id=int(user_id))
    fs_l = file_store.objects.all()
    context = {'share_list': fshare_l,'file_list': fs_l}
    return render(request, './myapp/auditor_file_share_view.html', context)


def auditor_file_share_update(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        file_id = request.POST.get('file_id')
        remark = request.POST.get('remark')
        fs = file_share.objects.get(id=int(file_id))
        fs.remark = remark
        fs.save()
        context = {'file_id': file_id, 'msg': 'Remark posted'}
        return render(request, './myapp/auditor_file_share_update.html', context)
    else:
        file_id = request.GET.get('file_id')

        context = {'file_id': file_id}
        return render(request, './myapp/auditor_file_share_update.html', context)
from . send_mail import send_mail
from .algo import get_digest
import os
from project.settings import BASE_DIR
def auditor_file_store_compare(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        fpath = fs.save(u_file.name, u_file)

        upload_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{fpath}')
        fsign = get_digest(upload_path)
        print(fsign)
        f_share = file_share.objects.get(id=int(file_id))
        fs = file_store.objects.get(id=f_share.file_id)
        ofpath= fs.fpath
        original_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{ofpath}')
        ##################################
        password = "please-use-a-long-and-random-password"
        pyAesCrypt.decryptFile(original_path+ ".aes", original_path , password)
        ##################################
        osign = get_digest(original_path)
        print(osign)
        msg=''
        fsd = file_store.objects.get(id=int(file_id))
        ud = user_details.objects.get(user_id=int(fsd.user_id))
        if osign == fsign:
            msg = 'File is safe and sound'
            send_mail("Secure Cloud", msg, ud.email)
        else:
            msg = 'File has been tampered'
            send_mail("Secure Cloud", msg, ud.email)
        context = {'msg': msg,'file_id': file_id}
        return render(request, './myapp/auditor_file_store_compare.html', context)
    else:
        file_id = request.GET.get('file_id')
        context = {'file_id': file_id}
        return render(request, './myapp/auditor_file_store_compare.html',context)


def auditor_file_store_update(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        u_file = request.FILES['document']
        fs = FileSystemStorage()
        fname = fs.get_valid_name(u_file.name)

        fpath = fs.save(u_file.name, u_file)
        ##################################
        file_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{fpath}')
        password = "please-use-a-long-and-random-password"
        pyAesCrypt.encryptFile(file_path, file_path + ".aes", password)
        ##################################
        upload_path = file_path + ".aes"#os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{fpath}')

        fsize = fs.size(fpath)
        user_id = int(request.session['user_id'])
        fsign = get_digest(upload_path)
        print(fsign)
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        status = 'replaced'
        f_share = file_share.objects.get(id=int(file_id))
        f_share.status=status
        f_share.save()
        fs = file_store.objects.get(id=f_share.file_id)
        fs.fname=fname
        fs.fpath=fpath
        fs.fsize=fsize
        fs.fsign=fsign
        fs.dt=dt
        fs.tm=tm
        fs.status=status
        fs.save()
        context = {'msg': 'Record replaced','file_id': file_id}
        return render(request, './myapp/auditor_file_store_update.html', context)
    else:
        file_id = request.GET.get('file_id')
        context = {'file_id': file_id}
        return render(request, './myapp/auditor_file_store_update.html',context)

def auditor_file_store_download(request):

    id = request.GET.get('file_id')
    print('id = '+id)
    f_share = file_share.objects.get(id=int(id))
    fs = file_store.objects.get(id=f_share.id)
    file_path = os.path.join(BASE_DIR, f'myapp\\static\\myapp\\media\\{fs.fpath}')
    password = "please-use-a-long-and-random-password"
    pyAesCrypt.decryptFile(file_path+ ".aes", file_path , password)

    context = {'fileurl': fs.fpath}
    return render(request, './myapp/auditor_file_store_download.html',context)



from . models import audit_request
def user_audit_request_add(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        auditor_id = int(request.POST.get('auditor_id'))
        file_id = int(request.POST.get('file_id'))
        ar = audit_request(user_id=user_id, auditor_id=auditor_id, file_id=file_id,status='Pending')
        ar.save()
        context = {'msg' : 'Request Send'}
        return render(request, './myapp/user_audit_request_add.html', context)
    else:
        file_id = int(request.GET.get('id'))
        cm_l = auditor_details.objects.all()
        context = {'auditor_list': cm_l,'file_id':file_id}
        return render(request, './myapp/user_audit_request_add.html', context)


def auditor_audit_request_view(request):
    user_id = request.session['user_id']
    fd = audit_request.objects.filter(auditor_id=int(user_id))
    fs_l = file_store.objects.all()
    context = {'r_list': fd, 'file_list':fs_l}
    return render(request, './myapp/auditor_audit_request_view.html', context)


from . models import org_files
def user_send_file(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        auditor_id = int(request.POST.get('auditor_id'))
        dt = datetime.today().strftime('%Y-%m-%d')
        u_file = request.FILES['file_path']
        fs = FileSystemStorage()
        file_path = fs.save(u_file.name, u_file)
        org_f = org_files(user_id=user_id, auditor_id=auditor_id, file_path=file_path, dt=dt)
        org_f.save()
        context = {'msg':'File Send..'}
        return render(request, './myapp/user_send_file.html', context)
    else:
        ad = auditor_details.objects.all()
        context = {'auditor_list':ad}
        return render(request, './myapp/user_send_file.html', context)

def user_org_file_view(request):
    user_id = request.session['user_id']
    og_l = org_files.objects.filter(user_id = int(user_id))
    ad = auditor_details.objects.all()
    context = {'file_list':og_l, 'ad':ad}
    return render(request, './myapp/user_org_file_view.html', context)

def user_org_file_delete(request):
    user_id = request.session['user_id']
    id = request.GET.get('id')
    ogl = org_files.objects.get(id=int(id))
    ogl.delete()
    og_l = org_files.objects.filter(user_id=int(user_id))
    ad = auditor_details.objects.all()
    context = {'file_list': og_l, 'ad': ad}
    return render(request, './myapp/user_org_file_view.html', context)

def auditor_user_org_file_view(request):
    user_id = request.session['user_id']
    og_l = org_files.objects.filter(auditor_id = int(user_id))
    ad = user_details.objects.all()
    context = {'file_list':og_l, 'ad':ad}
    return render(request, './myapp/auditor_user_org_file_view.html', context)