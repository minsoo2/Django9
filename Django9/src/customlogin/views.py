from django.shortcuts import render
#forms.py 에 있는 클래스들을 이용할 꺼니까
from .forms import SignupForm,LoginForm
from django.http.response import HttpResponseRedirect
from django.urls import reverse
#django 에서 제공해주는 
from django.contrib.auth import authenticate,login
#User 안에 있는 createuser 함수를 이용해서 회원을 추가해야 함 
from django.contrib.auth.models import User
# Create your views here.

#회원가입
def signup(request):
    if request.method =="GET":
        form = SignupForm()
        return render(request,'customlogin/signup.html',{'form':form})
    elif request.method =="POST":
        form = SignupForm(request.POST)
        #사용자가 유효한 값을 넣었는지 확인하는 기능(아이디 중복, 비밀번호 형식 등)
        if form.is_valid():
            #is_valid() 함수 호출 후 cleaned_data 변수로 특정 입력을 추출할 수 있음, cleaned_data[키값]
            print(form.cleaned_data['username'])
            #form.save() #비밀번호를 암호화하는 과정이 생략되서 사용할 수 없음, 사용자가 입력한 텍스트 자체를 저장할 수 없음
            #비밀번호 값이 일치하는지 확인
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
                #유저 생성
                new_user = User.objects.create_user(form.cleaned_data['username'],
                                                    form.cleaned_data['email'],
                                                    form.cleaned_data['password'])
                new_user.first_name = form.cleaned_data['first_name']
                new_user.last_name = form.cleaned_data['last_name']
                new_user.save()
                
                return HttpResponseRedirect(reverse('index'))
            else:#비밀번호와 비밀번호 확인이 틀린경우
                return render(request,'customlogin/signup.html',{'form':form})
        else:#유효한 값을 입력하지 않은 경우,다시 사용자가 틀린 부분만 수정할 수 있게 form 을 넘겨줌
            return render(request,'customlogin/signup.html',{'form':form}) 
        
#로그인
def signin(request):
    if request.method=="GET":
        form = LoginForm()
        return render(request,'customlogin/signin.html',{'form':form})
    elif request.method=="POST":
        #form.is_valid() 호출 후 cleaned_data를 사용할 수 없음
        #is_valid() 호출 시 아이디 중복으로 False 값 반환됨
        form = LoginForm(request.POST) #사용자가 아이디, 비밀번호를 잘 못 입력한 경우 사용자 입력을 유지하기 위해 폼클래스 객체 생성
        username = request.POST.get('username') #username라는 변수로 날라온 데이터를 username 에 저장
        password = request.POST.get('password') #password라는 변수로 날라온 데이터를 password 에 저장
        #authenticate(username,password) 에는 username, password 라는 고정변수가 있음 , 암호화된 비밀번호와 일치하는지 확인하려고
        #User 모델 클래스에 해당 ID 와 Password 를 가진 객체를 반환, 객체가 없는 경우 None 값 반환
        user = authenticate(username= username,password= password)
        if user is not None:
            #해당 요청을 가진 클라이언트가 user 객체로 로그인하는 작업을 수행
            #                ↓ 53줄에서 찾아놓은 user,
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else :
            return render(request,'customlogin/signin.html',{'form':form, 'error':"아이디나 비밀번호가 맞지않습니다."})
            
#로그아웃
from django.contrib.auth import logout
def signout(request):
    #해당 요청을 한 클라이언트의 user 정보를 삭제
    logout(request)
    return HttpResponseRedirect(reverse('index'))











