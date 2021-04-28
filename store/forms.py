#แบบฟอร์ม ลงทะเบียน
from django.contrib.auth.models import User
from django import forms
#ผูกข้อมูล User ที่ป้อนกับแบบฟอร์ม
from django.contrib.auth.forms import UserCreationForm

#สร้างแบบฟอร์ม Register
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required = True)
    last_name = forms.CharField(max_length=100, required = True)
    email = forms.EmailField(max_length=250 , help_text='example@gmail.com')

    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')

