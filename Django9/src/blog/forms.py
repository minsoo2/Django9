'''
Created on 2018. 10. 6.

@author: user
'''
from django.forms.models import ModelForm
from django import forms
from .models import Post
class PostForm(ModelForm):
    #파일 데이터 저장, 사용자가 파일데이터를 주지않더라도 보낼 수 있도록 허용                                                    attribute 약자
    files = forms.FileField(required=False,widget=forms.ClearableFileInput(attrs={'multiple':True}))
    images = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = Post
        fields = ['type','headline','content']
        
    field_order = ['type','headline','files','images','content']
        