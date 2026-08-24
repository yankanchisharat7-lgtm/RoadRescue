from django import forms
from .models import Mechanic


class MechanicProfileForm(forms.ModelForm):

    class Meta:
        model = Mechanic

        fields = [
            "name",
            "shop_name",
            "phone",
            "email",
            "location",
            "experience",
            "vehicle_type",
            "inspection_charge",
            "battery_charge",
            "tyre_change_charge",
            "engine_repair_charge",
            "oil_change_charge",
            "brake_repair_charge",
            "towing_charge_per_km",
            "photo",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mechanic Name",
                }
            ),

            "shop_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Garage / Shop Name",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Garage Location",
                }
            ),

            "experience": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Years of Experience",
                    "min": "0",
                }
            ),

            "vehicle_type": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "inspection_charge": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Inspection Charge",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "battery_charge": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Battery Service Charge",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "tyre_change_charge": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tyre Change Charge",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "engine_repair_charge": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Engine Repair Charge",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "oil_change_charge": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Oil Change Charge",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "brake_repair_charge": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Brake Repair Charge",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "towing_charge_per_km": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Towing Charge Per KM",
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
        }