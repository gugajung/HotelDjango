from django.contrib.auth.models import User
from django import forms
from .models import Reservation, Profile, Telephone, Address
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.forms import BaseInlineFormSet
from functools import partial


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "password", "email"]


class ReservationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'date'}))
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'date'}))

    def __init__(self, *args, **kwargs):
        self.room_pk = kwargs.pop('room_pk', None)
        super(ReservationForm, self).__init__(*args, **kwargs)

    def clean(self, **kwargs):
        cleaned_data = super(ReservationForm, self).clean()
        start = cleaned_data.get('start_date')
        end = cleaned_data.get('end_date')
        if start >= end:
            self.add_error(None, ValidationError(
                "Start date must be earlier than end date of reservation"))
        reservation_query = Reservation.objects.filter(room__pk=self.room_pk)
        for reservation in reservation_query:
            if start <= reservation.end_date and reservation.start_date <= end:
                self.add_error(None, ValidationError(
                    'Room is already reserved from ' + str(
                        reservation.start_date) +
                    ' to ' + str(reservation.end_date)
                    + ', please change date'))
        return cleaned_data

    class Meta:
        model = Reservation
        fields = ["start_date", "end_date"]


class ProfileEditForm(forms.Form):
    # photo = forms.ImageField()
    name = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    street_nr = forms.IntegerField()
    telephone = forms.IntegerField()

    def clean(self, **kwargs):
        cleaned_data = super(ProfileEditForm, self).clean()
        telephone = cleaned_data.get('telephone')
        if 15 > len(str(telephone)) > 9:
            self.add_error(None, ValidationError(
                'Telephone number must be longer than 9 ' +
                'digits and up to 15 digits'))
        return cleaned_data








