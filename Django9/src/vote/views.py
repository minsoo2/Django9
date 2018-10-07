from django.shortcuts import render, get_object_or_404
from .models import Question, Choice, Comment

from django.http.response import HttpResponseRedirect
#HttpResponseRedirect : HTML 파일을 클라이언트에게 보내는것이 아닌,
#300번대 코드와 함께 URL주소를 클라이언트에게 전송함
from django.urls import reverse
from _datetime import datetime

#데코레이터 : 뷰함수 호출전 특정 조건을 만족하는지 검사하는 함수를 붙임
#login_required 함수 : 뷰 함수 호출 전 요청자가 로그인이 되어있는지 확인
#요청자가 비로그인 상태일 때, 로그인 페이지로 리다이렉트함
from django.contrib.auth.decorators import login_required

from test.dtracedata import instance
#reverse(문자열) : 문자열에 해당하는 별칭을 가진 url 주소를 반환
#매개변수가 추가로 사용되는 뷰함수 인경우 args 변수에 튜플형식으로 인자값을 저장
#reverse('vote:index')
#reverse('vote:detail', args=(question.id ,) )
#질문 목록 보여주기
def index(request):
    if request.method=="GET":
        b = Comment.objects.all()
        a = Question.objects.all()
        return render(request, 'vote/index.html', {'question_list' : a , 'comment_list' : b})
    elif request.method=="POST":
        comment1 = request.POST.get('comment') # 'comment' 라는 이름으로 댓글 내용을 보내줄 때
        #객체를 처음부터 생성해주기
        obj = Comment() #Comment 모델 클래스의 객체 생성. 데이터베이스에 반영 X 상태
        obj.comment = comment1
        #     ↑ 모델 Comment 안에 있는 변수 comment 임
        #request.user : 해당 요청을 한 클라이언트의 유저 정보 
        obj.user = request.user
        obj.save()
        return HttpResponseRedirect(reverse('vote:index'))
#질문에 대한 설문지 제공
def detail(request, question_id):
    #get_object_or_404 : 모델클래스의 객체 한개를 추출, 조건에 맞는
    #객체가 없는경우 클라이언트에게 404 에러메시지를 전달
    question = get_object_or_404(Question, id = question_id)
    return render(request,'vote/detail.html',
                  {'question' : question})
from django.db.models import F
#F : race condition 문제 방지를 위한 클래스
#모델클래스의 객체에 저장된 변수값을 가져올 때 F 객체를 생성해 사용하면 동시에 같은 요청을 하는 클라이언트에게 순차적으로 값을 전달
#투표처리
def vote(request):
    #사용자가 POST 방식으로 요청했는지 확인
    if request.method == "POST":
        #POST방식으로 보낸 데이터 중 'select' 키로 보낸 데이터를 추출
        id1 = request.POST.get('select')
        #사용자가 보낸 select 값으로 Choice 객체를 찾음
        obj = get_object_or_404(Choice,id=id1)
        #obj.vote += 1 #객체 안에있는 vote 변수에 1증가
        obj.vote = F('vote')+1 
        obj.save() #데이터베이스에 변경사항을 저장
        # obj.question : question변수가 외래키로 지정되있으므로,
        # 연결된 객체를 저장함
        #print(obj.question)
        #print(reverse('vote:result' , args=(obj.question.id ,) ) )
        #메인페이지 주소를 클라이언트에게 전달
        return HttpResponseRedirect( reverse('vote:result' , args=(obj.question.id, ) ) )
#결과화면 보여주기
def result(request, question_id):
    obj = get_object_or_404(Question, id = question_id)
    
    return render(request,'vote/result.html',
                  {'question':obj})

from .forms import QuestionForm,ChoiceForm
#질문글 추가
@login_required
def questionRegister(request):
    #새 입력양식을 전달
    if request.method == "GET":
        form1 = QuestionForm() #QuestionForm 객체 생성
        #as_table(), as_p() : HTML 문서의 형태로 입력양식을 제공할 때 사용하는 함수
        #as_table() : <table> </table> 사이에 넣을 때 사용 
        #as_p : <p> </p> 사이에 넣을 때 사용 
        print(form1.as_table())
        return render(request,'vote/questionRegister.html',{'form':form1})
    #사용자 입력을 기반으로 Question 객체 생성 후 데이터베이스에 저장
    elif request.method == "POST":
        #사용자 입력을 해당 폼 객체 생성시 넣을 수 있음
        #request.POST : POST 방식으로 날아온 모든 데이터 
        form1 = QuestionForm(request.POST)
        #form1.save() #사용자가 입력한 데이터를 기반으로 데이터베이스에 저장 및 객체 반환
        #form1.save(commit=False) : 사용자가 입력한 데이터를 기반으로 객체 반환(DB에 저장 x)
        #사용자가 입력한 데이터로 연동된 모델클래스의 객체로 변환
        #obj : Question 객체를 가지고 있음
        obj = form1.save(commit=False) #사용자가 입력한 양식에는 pub_date 가 비어있으니까 값을 채워주기 위해서 DB에 저장하기 전 pub_date를 작업해줌 
        obj.pub_date = datetime.now()#pub_date 변수에 값 대입
        obj.save() # 객체를 데이터베이스에 저장
                                    #reverse 첫번째 매개변수 : url
        return HttpResponseRedirect(reverse('vote:index'))

#질문글 수정
def questionUpdate(request, question_id):
    obj = get_object_or_404(Question, id=question_id)
    if request.method == "GET":
        #Question 객체에 저장된 값을 QuestionForm 객체를 생성할 때 입력
        #모델폼의 생성자에 instance 매개변수에 이미 생성된 객체를 넣어야 함 
        form = QuestionForm(instance = obj)
        return render(request,'vote/questionUpdate.html',{'form':form})
    elif request.method == "POST":
        #기존 객체를 사용자 입력 데이터로 변경
        form = QuestionForm(request.POST, instance = obj)
        form.save() #데이터베이스에 변경사항 저장
        
        return HttpResponseRedirect(reverse('vote:index'))

#질문글 삭제
def questionDelete(request, question_id):
    #삭제하고자 하는 객체를 찾아서 delete 함수 호출
    #모델 클래스의 객체.delete() : 데이터베이스에 해당 객체가 삭제됨
    question = get_object_or_404(Question, id =question_id)
    question.delete()
    return HttpResponseRedirect(reverse('vote:index'))

#답변 추가
#0)questionRegister 참고
def choiceRegister(request):
    #1)GET,POST 구분
    #1-1)GET
    #1-1-1)ChoiceForm 객체 생성
    #1-1-2)render함수 사용 html 문서를 클라이언트에 전달
    #    (생성한 폼객체를 템플릿엔진에게 전달)
    if request.method == "GET":
        obj = ChoiceForm()
        return render(request,'vote/choiceRegister.html',{'form':obj,'name':'답변 등록 페이지','submit':'답변 등록'})
    #1-2)POST
    #1-2-1)ChoiceForm 객체 생성(사용자의 데이터를 생성자의 인자값으로 넣기)
    #1-2-2)ChoiceForm 객체를 데이터베이스에 저장
    #1-2-3)어딘가로 보내주기(URL 전달) index,detail
    elif request.method == "POST":
        obj = ChoiceForm(request.POST)
        choice = obj.save() #내부적으로 수정해야할 데이터가 없기 떄문에 DB에 바로 저장, choice : Choice 객체를 가지고 있음
        #detail 로 보내기위해 choice 라는 변수로 받아준 것임
        #index로 보내기
        #return HttpResponseRedirect(reverse('vote:index'))
        #detail로 보내기
        return HttpResponseRedirect(reverse('vote:detail',args=(choice.question.id,)))
    #2)템플릿 제작
    #2-1)<form> 태그 생성
    #2-2)csrf_token 생성, submit 타입의 input태그 생성
    #2-3)view 함수에서 준 폼객체로 HTML 태그 생성
    #3)URL 등록 + 링크 생성
#답변 수정
#0)questionUpdate 참고
def choiceUpdate(request,choice_id):#1 매개변수 추가
    #2)Choice 객체 찾기
    obj = get_object_or_404(Choice,id=choice_id)
    #3)GET,POST 분리
    if request.method == "GET":
        form = ChoiceForm(instance = obj)
        return render(request,'vote/choiceRegister.html',{'form':form,'name':'답변 수정 페이지','submit':'답변 수정'})
    #3-1)GET : ChoiceForm 생성자의 인자로 Choice 객체를 입력
    #          HTML 파일 전달
    #3-2)POST : ChoiceForm 생성자의 인자로 입력데이터와 Choice 객체를 입력
    elif request.method == "POST":
        form = ChoiceForm(request.POST, instance = obj)
    #           수정사항을 데이터베이스에 저장
        form.save()
    #           index or detail URL을 클라이언트에게 전송
    #index
        #return HttpResponseRedirect(reverse('vote:index'))
    #detail
        return HttpResponseRedirect(reverse('vote:detail',args=(obj.question.id,)))
#답변 삭제
#0)questionDelete 참고하기
def choiceDelete(request,choice_id): #1) 매개변수 추가
    #2) 삭제하고자 하는 객체를 찾기(매개변수를 이용)
    #obj = Choice.objects.get(id=choice_id)
    obj = get_object_or_404(Choice, id = choice_id)
    i = obj.question.id #choice 객체와 연결된 question 객체의 id 값을 삭제하기 전에 미리 저장,detail 로 이동시 사용하기 위해
    #3) delete 함수 호출
    obj.delete()
    #4) 어딘가로 페이지 이동(index, detail)할 수 있도록 URL 지정
    #index 이동
    #return HttpResponseRedirect(reverse('vote:index'))
    #detail 이동
    return HttpResponseRedirect(reverse("vote:detail",args=(i,)))
    
    
    
    
    
    
    

