from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.core.paginator import Paginator


from .models import Qnaboard, Users


# Create your views here.

def qnacreate(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        nickName = request.POST['nickName']
        #admin_content = request.POST['admin_content']
        users = Users.objects.get(useremail=request.session['user'])
        qnadata = Qnaboard(title=title, content=content, qnawriter=users, nickName=nickName)
        #tmpuser = Users.objects.get(userEmail='syj0510@naver.com')
        #qnadata = Qnaboard(title=title, nickName=nickName, content=content, qnawriter=tmpuser)
        qnadata.save()
        return redirect("qnaread")
    else:
        return render(request, 'qnacreate.html', None)

def admin_answer(request, pk):
    admin = Qnaboard.objects.get(pk=pk)
    if request.method == 'POST':
       admin = Qnaboard.objects.get(pk=pk)
       admin_content = request.POST['admin_content']
       admin.admin_content = admin_content
       admin.save()
       return redirect('qnadetail', admin.pk)
    else:
       context = { 'admin': admin, "test":"test" }
    return render(request, 'qnadetail.html', context)


def qnaread(request):
    page = request.GET.get('page', 1)
    qnalist = Qnaboard.objects.all()
    paginator = Paginator(qnalist[::-1], 5)
    qnalistpage = paginator.get_page(page)
    context = {"qnalist": qnalistpage}
    return render(request, "qnaboard.html", context)

def qnadetail(request, pk):
    qnaboard = Qnaboard.objects.get(pk=pk)
    context = {"qnaboard": qnaboard,
               "useremail":request.session['user'],
                }
    return render(request, 'qnadetail.html', context)


def qnaregister(request):
    if request.method =='GET':
        return render(request, 'qnaregister.html')
    elif request.method == 'POST':
        useremail = request.POST.get('useremail', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password',None)
        res_data = {}
        if not (username and password and re_password and useremail):
            res_data['error']='아이디 또는 패스워드를 입력해주세요.'
        elif password != re_password:
            res_data['error']='비밀번호가 다릅니다.'
        else:
            users = Users(
                useremail=useremail,
                username=username,
                password=make_password(password)
            )
            users.save()

            return redirect('qnalogin')

        return render(request, 'qnaregister.html', res_data)

def qnalogin(request):
    context = None
    if request.method == "POST":
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        try :
            user = Users.objects.get(useremail=useremail)
        except Users.DoesNotExist :
            context = {'error': '계정을 확인하세요'}
        else :
            if check_password(password, user.password):
                request.session['user'] = user.useremail
                return redirect('qnaread')
            else :
                context = { 'error' : '패스워드를 확인하세요'}
    else :
        if 'user' in request.session:
            context = {'msg': '이미 %s 로그인 하셨습니다.' % request.session['user'] }
    return render(request, 'qnalogin.html', context)

def qnalogout(request):
    if 'user' in request.session :
        del request.session['user']
        context = {'msg' : '로그아웃 완료'}
    else :
        context = {'msg': '로그인 상태가 아닙니다!'}
    return render(request, 'qnalogout.html', context)

def qnamember(request) :
    if 'user' in request.session :
        context =  { 'useremail' : request.session.get('user')}
        return render(request, "member.html", context)
    else :
        context = {'error' : "회원만 볼 수 있는 페이지입니다. 로그인 해주세요!!"}
        return render(request, 'qnalogin.html', context)





