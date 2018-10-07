'''
Created on 2018. 9. 30.

@author: user
'''
from django.urls import path
#views를 참고하기 위해 임포트
from .views import signup,signin,signout
app_name ='auth' #auth 라는 이름으로 해당 url을 만들겠다.

urlpatterns =[
    #127.0.0.1:8000/auth/signup
    path('signup/',signup,name='signup'),
    path('login/',signin,name='signin'),
    path('logout/',signout,name='signout'),
    ]