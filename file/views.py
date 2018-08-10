import os
import time
from django.contrib import auth
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, QueryDict, JsonResponse, FileResponse
from django.shortcuts import render,reverse,redirect
from django.utils.encoding import escape_uri_path

from file import models
from django.contrib.auth.views import login_required
import re

# Create your views here.





#跳到上传文件页面
@login_required
def index(request):
    return render(request,'fileupload.html')


#文件上传
def fileload(request):
    print(request.method)
    myFile = request.FILES.get('file-7[]',None)#获取上传的文件，没有默认为None
    print(myFile)
    if re.match("^.+\\.(?i)(pdf)$",myFile.name):#判断一下文件是否为PDF文件，如果是PDF通过，不是拒绝上传
        classify = request.POST.getlist('classify')  # checkbox类型的取值
        classifyStr = "".join(classify)  # 将list转成字符串输出
        print('myValues', classify)
        print(classify)
        loadtime = time.strftime("%Y-%m-%d", time.localtime())  # 获取时间年-月-日
        print("时间", loadtime)
        if not myFile:
            return HttpResponse("no file for upload")
        destination = open(os.path.join("statics/filepath", myFile.name), "wb+")  # 创建了一个file对象
        try:
            file = models.Filename.objects.create(name=myFile.name, classify=classifyStr, time=loadtime)  # 将文件名存进数据库表中
        except:
            return redirect(reverse(index))
        print(file.name)
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()  # 关闭
        return redirect(reverse(index))
    else:
        return HttpResponse(u"Don't PDF file")

#展示页面
def fileview(request):
    fileinfo = models.Filename.objects.all()
    nametime = {}
    for i in fileinfo:
        print(i.name,i.time)
        nametime[i.name] = i.time #给字典赋值
    print(nametime)
    Fnametime = list(nametime.items())
    Fnametime.reverse()
    contacts = paging(request,Fnametime)#分页
    # paginator = Paginator(Fnametime,3)
    # page = request.GET.get('page')
    # try:
    #     contacts = paginator.page(page)
    # except PageNotAnInteger:
    #     contacts = paginator.page(1)
    # except EmptyPage:
    #     contacts = paginator.page(paginator.num_pages)

    return render(request,'file_list.html',{'data':contacts})
#下载
def filedown(request):
    filename = "".join( request.GET.getlist('name'))
    print(filename)
    print("你好我在filedown中")
    file = open('statics/filepath/'+filename,'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=''{}'.format(escape_uri_path(filename))#解决下载中文文件名的问题
    return response
#关键字搜索
def keyQuery(request):
    print("我在keyQuery中")
    keyname = request.POST.get('keyvalue')
    print(keyname)
    filename = models.Filename.objects.filter(name__contains=keyname).all()
    nametime = {}
    for i in filename:
        nametime[i.name] = i.time
    Fnametime = list(nametime.items())
    Fnametime.reverse()
    contacts = paging(request,Fnametime)
    print(nametime)
    return render(request,"file_list.html",{'data':contacts})
#按照条件查询
def queryfile(request):
    classify = request.GET.getlist('classify')#取到前端a标签里面传来的值
    classifyStr = "".join(classify)#将list转成字符串
    filename = models.Filename.objects.filter(classify__contains=classifyStr).all()
    nametime = {}
    for i in filename:
        nametime[i.name] = i.time
    Fnametime = list(nametime.items())#将字典转换成items()组成的列表
    Fnametime.reverse()#列表反转
    contacts = paging(request,Fnametime)#分页
    return render(request,'file_list.html',{'data':contacts})

#跳转到登录页面
def loginManager(request):
    return render(request,'login.html')

#用户登录验证
def loginVerify(request):
    print("我在loginVerify中")
    print(request)
    username = "".join(request.POST.getlist("username"))#取到ajax传过来的username值并转化成字符串
    password = "".join(request.POST.getlist("password"))#取到ajax传过来的password值并转化成字符串
    user = authenticate(username=username,password=password)
    if user:
        login(request,user)
        return JsonResponse({"success":"success"})
    else:
        return JsonResponse({"error":"fail"})


#分页函数
def paging(request,Fnametime):
    paginator = Paginator(Fnametime, 6)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return contacts

