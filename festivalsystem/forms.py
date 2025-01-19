# Φόρμες για εγγραφή χρηστών και υποβολή παραστάσεων


from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

from .models import User, Perfomance, Review

class RegistrationForm(UserCreationForm):
    # Φόρμα εγγραφής χρήστη με πεδία για email, όνομα, επώνυμο και τηλέφωνο
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "First name")
    last_name = forms.CharField(label = "Last name")
    phone = PhoneNumberField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user

class PerfomanceSubmissionForm(forms.ModelForm):
    # Φόρμα για την υποβολή παράστασης
    artists = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)
    class Meta:
        model = Perfomance
        fields = ['title', 'abstract', 'file', 'track', 'artists']
    
    def __init__(self, festival, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.festival = festival
        self.fields['track'].queryset = self.festival.track_set.all()

    def clean(self):
        cleaned_data = super().clean()
        track = cleaned_data.get('track')

        if track and track.festival != self.festival:
            self.add_error('track', "Invalid track selected.")

        return cleaned_data

class ReviewForm(forms.ModelForm):
    # Φόρμα για την υποβολή κριτικής
    class Meta:
        model = Review
        fields = ['score', 'comments']