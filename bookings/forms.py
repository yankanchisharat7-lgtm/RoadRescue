# `bookings/forms.py`
from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    VEHICLE_CHOICES = [
        ("Bike", "Bike"),
        ("Car", "Car"),
        ("Truck", "Truck"),
        ("EV", "Electric Vehicle"),
    ]

    vehicle_type = forms.ChoiceField(
        choices=VEHICLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        ),
        label="Vehicle Type"
    )

    class Meta:
        model = Booking

        fields = [
            "customer_name",
            "customer_phone",
            "customer_location",
            "vehicle_type",
            "problem",
        ]

        widgets = {
            "customer_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your name"
                }
            ),

            "customer_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your phone number"
                }
            ),

            "customer_location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your current location"
                }
            ),

            "problem": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe your vehicle problem"
                }
            ),
        }

    def clean_customer_name(self):
        name = self.cleaned_data["customer_name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Please enter a valid name."
            )

        if any(char.isdigit() for char in name):
            raise forms.ValidationError(
                "Name should not contain numbers."
            )

        return name

    def clean_customer_phone(self):
        phone = self.cleaned_data["customer_phone"].strip()

        digits = "".join(
            char for char in phone
            if char.isdigit()
        )

        if len(digits) != 10:
            raise forms.ValidationError(
                "Please enter a valid 10-digit phone number."
            )

        return digits

    def clean_customer_location(self):
        location = self.cleaned_data["customer_location"].strip()

        if len(location) < 3:
            raise forms.ValidationError(
                "Please enter a valid location."
            )

        return location

    def clean_problem(self):
        problem = self.cleaned_data["problem"].strip()

        if len(problem) < 5:
            raise forms.ValidationError(
                "Please describe your vehicle problem in more detail."
            )

        return problem

