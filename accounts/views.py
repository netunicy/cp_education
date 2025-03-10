from django.contrib.auth import logout
import uuid
from django.contrib import messages,auth
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt, csrf_protect,requires_csrf_token
import mailtrap as mt
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import UserActivation,accept_t_c
from homepage.models import Mylogo


def logout_view(request):
    logout(request)
    return redirect('/')

@requires_csrf_token    
@csrf_protect  #you can refresh page when you auth
def login_user(request,*args, **kwargs):
    logo=Mylogo.objects.all()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            us_id = User.objects.get(username=username)
            id_user = us_id.id
            active_users = UserActivation.objects.filter(user_id=id_user,activated=True).exists()
            if active_users and user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse("homepage:homepage"))      
                #request.session['log_in']=log_in
                #request.session.modified = True
            #return HttpResponseRedirect(reverse("homepage:user_on"))       
            elif user is None:
                messages.error(request,"Έχετε καταχωρήσει λανθασμένα το Username ή το Password!")
                return render(request,'login.html')
            elif not active_users :
                messages.error(request,"Παρακαλώ επιβεβαιώστε το Email σας στον σύνδεσμο που σας έχει σταλεί")
                return render(request,'login.html')
        else:
            messages.error(request,"Έχετε καταχωρήσει λανθασμένα το Username ή το Password!")
            return render(request,'login.html')
    else:
        context = {'logo': logo,
        }
        return render(request,'login.html',context)

@requires_csrf_token
@csrf_protect
def user_register(request,):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        accept_terms=request.POST.get('t_c')
        
        if password1==password2:
            has_length_greater_than_8 = len(password1) >= 8
            has_uppercase = any(i.isupper() for i in password1)
            has_lowercase = any(i.islower() for i in password1)
            has_digit = any(i.isdigit() for i in password1)
            has_special_character = any(not i.isalnum() for i in password1)
            if has_length_greater_than_8 and has_uppercase and has_lowercase and has_digit and has_special_character:
                if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
                    messages.error(request,'Το Username και το Email ανήκουν σε άλλο χρήστη!')
                    return render(request,('register.html'))
        
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'Το Email χρησιμοποιείται από άλλο χρήστη!')
                    return render(request,('register.html'))
                     
                elif User.objects.filter(username=username).exists():
                    messages.error(request,'Το Username χρησιμοποιείται από άλλο χρήστη!')
                    return render(request,('register.html'))
                else:
                    #user2=accounts_details.objects.create(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                    user=User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                    t_c=accept_t_c.objects.create(accept_terms=accept_terms)
                    user.save()
                    #user2.save()
                    t_c.save()
                    #time.sleep(2)
                    user_id=User.objects.filter(username=username,email=email)
                    for i in user_id:
                        id_user=i.id
                    activation_key = str(uuid.uuid4())
                    user_activation = UserActivation(user_id=id_user, activation_key=activation_key)
                    user_activation.save()
                    activation_link = reverse('accounts:activate', kwargs={'activation_key': activation_key, 'user_id': id_user})
                    text=f'Πιέστε τον σύνδεσμο για ενεργοποίηση του λογαριασμού σας στο cpnetuni.com : {request.build_absolute_uri(activation_link)} '

                    mail = mt.Mail(
                        sender=mt.Address(email="no-reply@cpnetuni.com", name="Επιτυχία Εγγραφής"),
                        to=[mt.Address(email=email)],
                        subject="Ενεργοποίηση Λογαριασμού",
                        text=text,
                        category="Εγγραφές",
                    )

                    client = mt.MailtrapClient(token="388ed30f960c9bd511b4cbd740d05b7d")
                    client.send(mail)
                    
                    messages.add_message(request, messages.INFO,'Επιτυχία Εγγραφής. Σας έχει αποσταλεί σύνδεσμος ενεργοποίησης λογαριασμού 🚀. ')
                    return HttpResponseRedirect(reverse("homepage:homepage"))
            else:
                messages.error(request,'Ο Κωδικός σας δεν πληρεί τις προύποθέσεις (Τουλάχιστο 8 ψηφία και να περιέχει 1 αριθμό 1 κεφαλάιο και 1 ειδικό χαρακτήρα)')
                return render(request,('register.html'))
        
        else:
            messages.info(request,'Ο Κωδικός επαλήθευσης είναι λανθασμένος!',extra_tags="pswreg")
            return render(request,('register.html'))
    else:
        return render(request,('register.html'))
            
            

def activate_account(request, activation_key,user_id):
    try:
        #mylogo_home=logo.objects.filter(title='mylogo')
        user_activation = UserActivation.objects.filter(user_id=user_id,activation_key=activation_key)
        for i in user_activation:
            i.activated = True
            i.save()
        messages.error(request,'Έχετε επιβεβαιώσει με επιτυχία το Ηλεκτρονικό σας Ταχυδρομείο')
        #content={
            #'mylogo':mylogo_home,
        #}
        return render(request,('homepage.html'))   

    except UserActivation.DoesNotExist:
        messages.error(request,'Αποτυχία επιβεβαίωσης ηλεκτρονικού ταχυδρομίου')
        #content={
            #'mylogo':mylogo_home,
        #}
        return render(request, 'home.html')

@requires_csrf_token
@csrf_protect
def forgot_username(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            for e in User.objects.filter(email=email):
                username=e.username
                text='Το Username σας είναι : {}'.format(username)
                mail = mt.Mail(
                    sender=mt.Address(email="no-reply@cpnetuni.com", name="Επαναφορά Ονόματος Χρήστη"),
                    to=[mt.Address(email=email)],
                    subject="Επαναφορά Username",
                    text=text,
                    category="Επαναφορά Username",
                )

                client = mt.MailtrapClient(token="388ed30f960c9bd511b4cbd740d05b7d")
                client.send(mail)
            return render(request,'send_username_done.html')
                
        else:
            messages.error(request, 'Το Email που καταχωρήσατε δεν είναι συνδεδεμένο με κάποιο λογαριασμο.\nΠαρακαλώ ελέγξτε το Email και ξανά προσπαθήστε!')
            return render(request,'send_username.html')      
    else:
        return render(request,('send_username.html'))
    
@requires_csrf_token
@csrf_protect
def changepassword(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = auth.authenticate(username=username, password=password1)
        if user is not None:
            user=User.objects.get(username=username)
            if password1!=password2:
                user.set_password(password2)
                user.save()
                messages.warning(request,"Επιτυχής αλλαγή Κωδικού Πρόσβασης")
                return redirect('homepage:homepage')
            else:
                messages.warning(request,"Ο Κωδικός σας είναι ο ίδιος με τον προηγούμενο! Παρακαλώ καταχωρήστε καινούργιο κωδικό πρόσβασης!")
                return render(request,'change_password.html')
        else:
            messages.warning(request,"Έχετε καταχωρήσει λανθασμένα το Username ή το Password!")
            return render(request,'change_password.html')
    else:
        return render(request,'change_password.html')

@requires_csrf_token
@csrf_protect
def change_username(request):
    user_email = request.user.email
    if request.method == 'POST':
        usernamenew = request.POST.get('username')
        useremail = request.POST.get('email')
        password = request.POST.get('password')

        exist_username = User.objects.filter(username=usernamenew).exists()
        exist_email = User.objects.filter(email=useremail).exists()
        user = User.objects.filter(email=user_email).first()

        if not usernamenew and not useremail:
            messages.error(request, 'Για ενημέρωση στοιχείων παρακαλώ καταχωρήστε Email ή Username!')
            return HttpResponseRedirect(reverse("accounts:change_username"))

        elif exist_username:
            messages.error(request, 'Τα Username που έχετε καταχωρήσει χρησιμοποιείται από άλλο χρήστη!')
            return HttpResponseRedirect(reverse("accounts:change_username"))

        elif exist_email:
            messages.error(request, 'Τα Email που έχετε καταχωρήσει χρησιμοποιείται από άλλο χρήστη!')
            return HttpResponseRedirect(reverse("accounts:change_username"))

        elif user is not None and check_password(password, user.password) and usernamenew:
            user.username = usernamenew
            user.save()
            messages.add_message(request, messages.INFO, 'Η ενημέρωση έχει πραγματοποιηθεί με επιτυχία. Απαιτείται Επανασύνδεση!')
            logout(request)
            return HttpResponseRedirect(reverse("homepage:homepage"))

        elif user is not None and check_password(password, user.password) and useremail:
            user.email = useremail
            user.save()
            user_id=request.user.id
            activation_key = str(uuid.uuid4())
            user_activation_exist = UserActivation.objects.filter(user_id=user_id).exists()
            if user_activation_exist:
                user_activations = UserActivation.objects.filter(user_id=user_id)
                for i in user_activations:
                    i.activation_key = activation_key
                    i.activated = False
                    i.save()
            user_email = useremail
            activation_link = reverse('accounts:activate', kwargs={'activation_key': activation_key, 'user_id': user_id})
            text = f'Πιέστε τον σύνδεσμο για επιβεβαίωση Ηλεκτρονικού Ταχυδρομίου : {request.build_absolute_uri(activation_link)} '

            mail = mt.Mail(
                sender=mt.Address(email="no-reply@cpnetuni.com", name="Επιβεβαίωση Ηλεκτρονικού Ταχυδρομίου"),
                to=[mt.Address(email=user_email)],
                subject="Επιβεβαίωση Ηλεκτρονικού Ταχυδρομίου",
                text=text,
                category="Αλλαγή Ηλεκτρονικής Διεύθυνσης",
            )

            client = mt.MailtrapClient(token="388ed30f960c9bd511b4cbd740d05b7d")
            client.send(mail)

            messages.add_message(request, messages.INFO, 'Η ενημέρωση έχει πραγματοποιηθεί με επιτυχία. Σας έχει αποσταλεί σύνδεσμος επιβεβαίωσης Ηλεκτρονικής Διεύθυνσης. ')
            logout(request)
            return HttpResponseRedirect(reverse("homepage:homepage"))

        else:
            messages.error(request, 'Έχετε καταχωρήσει λανθασμένο Κωδικό Ασφαλείας!')
            return HttpResponseRedirect(reverse("accounts:change_username"))
    else:
        return render(request, 'change_username.html')
@csrf_exempt
def Terms_and_Conditions(request):
    mylogo_home=Mylogo.objects.filter(title='mylogo')
    template = loader.get_template('t_c.html')
    context = {
        'mylogo':mylogo_home,
        }
    return HttpResponse(template.render(context, request))

