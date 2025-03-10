from django.shortcuts import redirect, render
import mailtrap as mt
import base64
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from homepage.models import Mylogo,Success_logo
from .models import T_C_Partnership
from .forms import UserProfileForm
@csrf_exempt
def T_C_Partner(request):
    logo=Mylogo.objects.all()
    t_c=T_C_Partnership.objects.all()
    context = {
        't_c':t_c,
        'mylogo':logo,
        }
    return render(request, "partnership_tc.html", context)

@csrf_exempt
def partner_register(request):
    logo = Mylogo.objects.all()
    
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Get all field values dynamically
            field_values = {field: cleaned_data.get(field, "") for field in cleaned_data}

            # Generate formatted text
            text = "\n".join(f"{key}={value}" for key, value in field_values.items())

            # Get uploaded files
            id_card = cleaned_data.get('id_card')  # InMemoryUploadedFile object
            diploma = cleaned_data.get('diploma')  # InMemoryUploadedFile object

            # Save form data to database
            form.save()

            id_card_base64 = base64.b64encode(id_card.read()) if id_card else None
            diploma_base64 = base64.b64encode(diploma.read()) if diploma else None

            # Create Mailtrap attachments correctly
            attachments = []
            
            if id_card_base64:
                attachments.append(mt.Attachment(
                    content=id_card_base64,
                    filename="id_card.jpg",
                    mimetype="application/jpg"
                ))

            if diploma_base64:
                attachments.append(mt.Attachment(
                    content=diploma_base64,
                    filename="diploma.pdf",
                    mimetype="application/pdf"
                ))

            # Create Mail object
            mail = mt.Mail(
                sender=mt.Address(email="mailtrap@cpnetuni.com", name="Αίτημα Συνεργασίας"),
                to=[mt.Address(email='charalampospitris1983@gmail.com')],
                bcc=[mt.Address(email='cpnetuni@gmail.com')],
                subject='Αίτημα Συνεργασίας',
                category="Συνεργασία",
                text=text
            )

            # Attach files to email
            mail.attachments = attachments

            # Send email via Mailtrap
            client = mt.MailtrapClient(token="388ed30f960c9bd511b4cbd740d05b7d")  # Replace with actual token
            client.send(mail)

            return redirect(reverse('partnership:partner_done'))
        else:
            # Αν η φόρμα δεν είναι έγκυρη, επιστρέφουμε τη σελίδα με μηνύματα σφάλματος
            context = {
                "form": form,
                "logo": logo,
            }
            return render(request, "partner_register.html", context)

    else:
        form = UserProfileForm()
        context = {
            "form": form,
            "logo": logo,
        }
        return render(request, "partner_register.html", context)


def partner_done(request):
    success_logo=Success_logo.objects.all()
    logo=Mylogo.objects.all()
    context = {
        "logo": logo,
        "success_logo":success_logo,
        }
    return render(request, "partnership_done.html", context)


    

    