
from .models import Participants,Winner,Contest
from django import forms
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

class ParticipantForm(PopRequestMixin, CreateUpdateAjaxMixin,forms.ModelForm):
    photo = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-input-styled','accept': 'image/*', 'placeholder': 'Avtar'}))
    class Meta:
        model = Participants
        fields = ['photo']



#     #Validations on each field in form
#
#     def clean_phone1(self):
#         form_data = self.cleaned_data['phone1']
#         if form_data:
#             if len(str(form_data))  < 10 :
#                 raise ValidationError("Enter 10 digits")
#         return form_data
#
#     def clean_phone2(self):
#         form_data = self.cleaned_data['phone2']
#         if form_data:
#             if len(str(form_data))  < 10 :
#                 raise ValidationError("Phone 1 Enter atleast 10 digits")
#         return form_data
#
#
#     def clean_tower_no(self):
#         form_data = self.cleaned_data['tower_no']
#         if form_data:
#             if len(str(form_data))  > 2 :
#                 raise ValidationError("Tower Number cannot be greater than 2 digits")
#         return form_data
#
#     # def clean_v_model(self):
#     #     form_data = self.cleaned_data['v_model']
#     #     if form_data:
#     #         if len(str(form_data)) > 2:
#     #             raise ValidationError("V Model Error ")
#     #     return form_data
#
#
# # class VehicalInformationForm(forms.ModelForm):
# #     model = VehicalInformation
# #     fields = "__all__"
#
# class VehicalUserFormSet(BaseInlineFormSet):
#     # def get_form_kwargs(self, index):
#     #     kwargs = super(VehicalUserFormSet, self).get_form_kwargs(index)
#     #     kwargs.update({'parent': self.instance})
#     #     return kwargs
#
#     def clean(self):
#         super(VehicalUserFormSet, self).clean()
#         if any(self.errors):
#             return
#
#         phone_numbers = []
#         for form in self.form:
#             if len(form.cleaned_data.get('v_model')) > 2:
#                 raise forms.ValidationError(
#                     'V model Error ')
#
#
# VehicalUserFormSet = inlineformset_factory(VehicalUser, VehicalInformation,fields =('plate_no','v_model','v_color','v_type','v_description'),
# widgets={'plate_no': forms.TextInput(attrs={'pattern':'[a-zA-Z0-9]+','class': 'form-control','required':'true','placeholder':'MP23LA0101',"maxlength":"11", 'minlength':"7",'style':"text-transform:uppercase"}),
#          "v_model":forms.TextInput(attrs={'class': 'form-control','maxlength':'20','placeholder':'maruti'}),
#          "v_type":forms.Select(attrs={'class': 'form-control','required':'false','maxlength':'20'}),
#          "v_description":forms.TextInput(attrs={'class': 'form-control','maxlength':'50','placeholder':'This car was stolen'}),
#          "v_color":forms.TextInput(attrs={'class': 'form-control','maxlength':'20','placeholder':'Black'})},
#                                            can_delete=False,extra=1 )
#
#
#
#
#
# DELETED_TYPES = (
#         ('True', 'Inactive'),
#         ('False', 'Active'),
#
#     )
#
# from django.utils.translation import ugettext_lazy as _
#
# class VehicalInformationForm(PopRequestMixin, CreateUpdateAjaxMixin,forms.ModelForm):
#     # deleted = forms.ChoiceField(required=True, choices=DELETED_TYPES,
#     #                                 widget=forms.Select(attrs={'class': 'form-control'}))
#     class Meta:
#         model = VehicalInformation
#         fields = ['plate_no', 'v_model', 'v_color', 'v_type', 'v_description']
#         labels = {
#             'plate_no': _('Plate Number'),
#             'v_model': _('Vehicle Model'),
#             'v_color': _('Vehicle Color'),
#             'v_type': _('Vehicle Type'),
#             'v_description': _('Vehicle Description'),
#
#         }
#         widgets = {'plate_no': forms.TextInput(
#             attrs={'class': 'form-control', 'required': 'true', 'placeholder': 'MP23LA0101', "maxlength": "11"}),
#                    "v_model": forms.TextInput(
#                        attrs={'class': 'form-control', 'maxlength': '20', 'placeholder': 'maruti'}),
#                    "v_type": forms.Select(attrs={'class': 'form-control', 'required': 'false', 'maxlength': '20'}),
#                    "v_description": forms.TextInput(
#                        attrs={'class': 'form-control', 'maxlength': '50', 'placeholder': 'This car was stolen'}),
#                    "v_color": forms.TextInput(
#                        attrs={'class': 'form-control', 'maxlength': '20', 'placeholder': 'Black'})}
