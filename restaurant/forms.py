from datetime import timedelta, date

from django import forms

from .models import Booking, OPENING_HOUR, CLOSING_HOUR


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'phone_number', 'guest_number', 'booking_date', 'booking_time', 'comment']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['booking_date'].initial = date.today()
        self.fields['booking_time'].initial = OPENING_HOUR

        self.fields['booking_date'].widget.attrs['min'] = date.today()
        self.fields['booking_date'].widget.attrs['max'] = (date.today() + timedelta(days=7))

        self.fields['booking_time'].widget.attrs['min'] = OPENING_HOUR.strftime('%H:%M')
        self.fields['booking_time'].widget.attrs['max'] = CLOSING_HOUR.strftime('%H:%M')

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if not (date.today() <= booking_date <= (date.today() + timedelta(days=7))):
            raise forms.ValidationError("Booking date must be within the next 7 days.")
        return booking_date

    def clean_booking_time(self):
        booking_time = self.cleaned_data['booking_time']
        if not (OPENING_HOUR <= booking_time <= CLOSING_HOUR):
            raise forms.ValidationError(f"Booking time must be between {OPENING_HOUR.strftime('%I:%M %p')} and {CLOSING_HOUR.strftime('%I:%M %p')}.")
        return booking_time
