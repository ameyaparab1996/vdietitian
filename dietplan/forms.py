from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from dietplan.models import UserDetails, feedback
from datetime import date
from django.utils import timezone

#Register user model
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                'placeholder':'password'}),
                               validators=[MinLengthValidator(8,'Password must be at least 8 charactres long')])
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control',
                                                            'placeholder':'username','autofocus':True}),
                               validators=[MinLengthValidator(6,'Your username must be at least 6 charactres long')])
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control',
                                                            'placeholder':'example@mail.com'}))
    def clean_username(self):
        name = self.cleaned_data['username']
        name_1 = name.lower()
        if name_1 == "admin" or name_1 == 'user':
            raise ValidationError('username can\'t be "user/admin"')
        return name
    def clean_email(self):
        return self.cleaned_data['email'].lower()
    class Meta:
        model = User
        fields = ('username','email','password')
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
        }


#necessary inputs' model
class UserInfoForm(forms.ModelForm):
    #Apply min criteria to height and weight
    weight = forms.FloatField(min_value=15.0, max_value=300.0)
    height = forms.FloatField(min_value=50.0, max_value=243.84)

    #validating date_of_birth
    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 12, dob.month, dob.day) > (today.year, today.month, today.day):
            raise ValidationError("You must be atleast 12 years old to proceed")
        return dob


    #adding common css
    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        # add common css classes to all widgets
        for field in iter(self.fields):
            #get current classes from Meta
            classes = self.fields[field].widget.attrs.get("class")
            if classes is not None:
                classes += " form-control"
            else:
                classes = "form-control"
            self.fields[field].widget.attrs.update({
                'class': classes
            })

    class Meta():
        model = UserDetails
        exclude = ('user','dietPlan','BMR','calorieintake')
        #fields = "__all__"
        labels={
            'weight':'Weight (in kg)',
            'height':'Height (in cms)'
        }
        widgets = {
            'date_of_birth':forms.TextInput(attrs={'type':'date','class':'form-control','autofocus':True})
        }

class feedbackForm(forms.ModelForm):
        weight = forms.FloatField(min_value=15.0, max_value=300.0)

        class Meta:
            model = feedback
            exclude = ('feedback_on','user','is_positive')
            widgets = {
                'weight':forms.TextInput(attrs={'class':'form-control'}),
            }
