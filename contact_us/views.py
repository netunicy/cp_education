from django.shortcuts import redirect, render
import mailtrap as mt
from contact_us.forms import ContactForm
from homepage.models import Mylogo
from django.contrib import messages

def contact_us(request):
    form = ContactForm()  # Initialize the form
    logo = Mylogo.objects.all()  # Fetch logos

    if request.method == 'POST':
        form = ContactForm(request.POST)  # Populate form with POST data

        if form.is_valid():  # Validate the form before processing
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', 'N/A')  # Default value if phone is empty
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Setting up email
            mail = mt.Mail(
                sender=mt.Address(email="hello@cpnetuni.com", name="C.P Education Contact Us"),
                to=[mt.Address(email="cpnetunicontact@gmail.com")],
                bcc=[mt.Address(email="charalampospitris1983@gmail.com")],
                subject=subject,
                text=f"{name} {surname}\n{phone}\n{email}\n{message}",
                category="Contact Us"
            )

            # Sending email using Mailtrap
            client = mt.MailtrapClient(token="388ed30f960c9bd511b4cbd740d05b7d")
            client.send(mail)

            # Show success message
            messages.add_message(request, messages.INFO, 'Το μήνυμά σας στάλθηκε με επιτυχία. Θα επικοινωνήσουμε μαζί σας το αργότερο εντός δύο εργάσιμων ημερών.')
            return redirect('homepage:homepage')

    # Ensure `context` is always defined
    context = {'form': form, 'logo': logo}
    return render(request, "contact_us_form.html", context)
