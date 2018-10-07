'''
Created on 2018. 9. 30.

@author: user
'''
#ModelForm 을 사용하겠다고 알려주기
from django.forms import ModelForm
#django 에서 만들어준 폼을 참고(django에서 회원을 관리하는 모델클래스)
from django.contrib.auth.models import User
#입력양식을 사용할 떄 임포트(CharField 같은)
from django import forms
#회원가입에 사용할 폼
class SignupForm(ModelForm):
                        #리스트,사전형태
    def __init__(self,*args,**kwarg):
        super().__init__(*args,**kwarg)
        self.fields['password_check'].label = "비밀번호 확인"
    #패스워드 확인은 User 모델에 정의되어있지 않으니까 Meta 클래스 밖에서 내가 정의 해줌
    password_check = forms.CharField(max_length=200,widget=forms.PasswordInput())
    #forms.Input 다양한 input 이 있다는 것을 체크
    class Meta:
        model = User #import 한 User 를 넣어줌
        widgets={'password': forms.PasswordInput()}
        fields = ['username','password','first_name','last_name','email']
        #fields or exclude
    #field_order : 입력양식 순서 지정(리스트형태), 고정된 변수이름임
    field_order = ['username','password','password_check','first_name','last_name','email']
#로그인에 사용할 폼
class LoginForm(ModelForm):
    class Meta:
        model = User
        #password 입력 공간에 PasswordInput 위젯 적용하기
        widgets={'password':forms.PasswordInput()}
        fields = ['username','password']