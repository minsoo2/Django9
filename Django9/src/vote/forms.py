'''
Created on 2018. 9. 29.

@author: user
'''
#form : HTML 코드에서 사용할 입력양식 (<form>)을 모델클래스에 맞게 자동으로 만들어주는 기능 or 커스텀 입력양식을 만드는 기능을 제공
from django.forms.models import ModelForm
from .models import *   #Question 모델을 사용하기 위해
#class 폼이름  (ModelForm) 또는 (Form) 상속
#ModelForm : 모델클래스를 기반으로 입력양식을 생성할 때 상속받는 클래스
#Form : 커스텀 입력양식을 생성할 때 상속받는 클래스
class QuestionForm(ModelForm):
    class Meta: #Meta 클래스 정의를 통해 모델 클래스에 관한 정보를 입력
        #model : 어떤 모델클래스와 연동되는지 작성
        #fields : 모델클래스의 어떤 변수를 입력양식으로 만들 것인지 지정
        #exclude : 모델클래스의 어떤 변수를 입력양식에 제외할 것인지 지정, fields 와 둘 중 하나만 씀
        model = Question
        #fields, exclude 중 한 개만 사용해야함, 값을 넣을 땐 리스트 형태로, 리스트의 요소는 문자열의 형태로 입력
        fields = ['name']
        #exclude = ['pub_date']

#choice 모델클래스와 연동된 폼 클래스 정의        
class ChoiceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        #ModelForm 클래스의 생성자를 호출
        super().__init__(*args,**kwargs)
        self.fields['question'].label = '질문지'
    class Meta: #name, question을 작성할 수 있도록 설정
        model = Choice
        #fields = ['name','question']
        exclude = ['vote']
        