from django import forms
from .models import PartnerProfile

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Όνομα",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε το όνομά σας'}),
        max_length=50,
        help_text="Το όνομα πρέπει να είναι ίδιο με αυτό στον τραπεζικό σας λογαριασμό."
    )

    last_name = forms.CharField(
        label="Επώνυμο",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε το επώνυμό σας'}),
        max_length=50,
        help_text="Το επώνυμο πρέπει να είναι ίδιο με αυτό στον τραπεζικό σας λογαριασμό."
    )

    country = forms.ChoiceField(
        label="Χώρα",
        choices=[('GR', 'Ελλάδα'), ('CY', 'Κύπρος')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    region = forms.CharField(
        label="Επαρχία",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε την επαρχία σας'}),
        max_length=100
    )

    address = forms.CharField(
        label="Διεύθυνση Κατοικίας",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε τη διεύθυνσή σας'}),
        max_length=255
    )

    postal_code = forms.CharField(
        label="Ταχυδρομικός Κώδικας",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε τον Ταχυδρομικό Κώδικα'}),
        max_length=10
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε το email σας'})
    )

    phone = forms.CharField(
        label="Τηλέφωνο",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε το τηλέφωνό σας'}),
        max_length=15
    )

    degree_title = forms.CharField(
        label="Τίτλος Σπουδών",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε τον τίτλο σπουδών σας'}),
        max_length=100
    )

    iban = forms.CharField(
        label="Αριθμός IBAN",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε το IBAN σας'}),
        max_length=34
    )

    bank_name = forms.CharField(
        label="Όνομα Τράπεζας",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Εισαγάγετε το όνομα της τράπεζας'}),
        max_length=100
    )

    id_card = forms.FileField(
        label="Αστυνομική Ταυτότητα (JPG)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text="Ανεβάστε την αστυνομική σας ταυτότητα σε μορφή JPG."
    )

    diploma = forms.FileField(
        label="Πτυχίο (PDF)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        help_text="Ανεβάστε το πτυχίο σας σε μορφή PDF."
    )

    class Meta:
        model = PartnerProfile
        fields = [
            'first_name', 'last_name', 'country', 'region', 'address',
            'postal_code', 'email', 'phone', 'degree_title', 'iban', 'bank_name',
            'id_card', 'diploma'
        ]

    def clean_diploma(self):
        diploma = self.cleaned_data.get('diploma')
        if diploma and not diploma.name.endswith('.pdf'):
            raise forms.ValidationError("Το πτυχίο πρέπει να είναι αρχείο PDF.")
        return diploma

    def clean_id_card(self):
        id_card = self.cleaned_data.get('id_card')
        if id_card and not id_card.name.endswith(('.jpg', '.jpeg')):
            raise forms.ValidationError("Η ταυτότητα πρέπει να είναι αρχείο JPG.")
        return id_card
