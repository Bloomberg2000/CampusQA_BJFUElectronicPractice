import datetime
import hashlib
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from . import models


# Create your views here.
def login(request):
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            phoneNum = request.POST.get('phoneNum')
            password = request.POST.get('password')
            if phoneNum and password:
                try:
                    current_user = models.User.objects.get(phoneNum=phoneNum)
                    password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()  # 对密码进行加密
                    if current_user.password == password:
                        return message_helper(success=True)
                    else:
                        return message_helper(error_message="密码错误")
                except models.User.DoesNotExist:
                    return message_helper(error_message="用户不存在")
            else:
                return message_helper(error_message="用户名或密码不能为空")
    else:
        return message_helper(method_error=True)


def register(request):
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            college = request.POST.get('college')
            phoneNum = request.POST.get('phoneNum')
            password = request.POST.get('password')
            enrollmentTime = request.POST.get('enrollmentTime')
            if name and gender and college and phoneNum and password and enrollmentTime:
                count = models.User.objects.filter(phoneNum=phoneNum).count()
                if models.User.objects.filter(phoneNum=phoneNum).count() > 0:
                    return message_helper(error_message="用户已存在")
                else:
                    gender = 0 if (gender is '男') else 1
                    password = hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()  # 对密码进行加密
                    new_user = models.User(name=name, gender=gender, college=college, phoneNum=phoneNum,
                                           password=password, enrollmentTime=enrollmentTime)
                    new_user.save()
                    return message_helper(success=True)

            else:
                return message_helper(error_message="请确认所有必填项已填写")
        else:
            return message_helper(error_message="用户信息不能为空")
    else:
        return message_helper(method_error=True)


def get_personal_info(request, user_id):
    if user_id:
        if user_id == who_is_login(request):
            current_user = models.User.objects.filter(userID=user_id)
            if current_user.count() > 0:
                return message_helper(success=True,
                                      dataToReturn=json.loads(serializers.serialize("json", current_user)))
            else:
                return message_helper(error_message="用户不存在")
        else:
            return message_helper(error_message="权限不足，请使用对应账号登录")
    else:
        return message_helper(method_error=True)


def get_personal_question_list(request, user_id):
    if user_id:
        if models.User.objects.filter(userID=user_id).count() > 0:
            question_list = models.Questions.objects.filter(createUser=user_id)
            return message_helper(success=True,
                                  dataToReturn=json.loads(serializers.serialize("json", question_list)))
        else:
            return message_helper(error_message="用户不存在")
    else:
        return message_helper(method_error=True)


def get_personal_answer_list(request, user_id):
    if user_id:
        if models.User.objects.filter(userID=user_id).count() > 0:
            question_list = models.Answers.objects.filter(createUser=user_id)
            return message_helper(success=True,
                                  dataToReturn=json.loads(serializers.serialize("json", question_list)))
        else:
            return message_helper(error_message="用户不存在")
    else:
        return message_helper(method_error=True)


def search_by_keywords(request, keyword):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_question_list(request):
    question_list = models.Answers.objects.all()
    return message_helper(success=True,
                          dataToReturn=json.loads(serializers.serialize("json", question_list)))


def create_question(request):
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title and content:
                createUser = models.User.objects.get(userID=who_is_login(request))
                createTime = datetime.datetime.now()
                editTime = datetime.datetime.now()
                if models.Questions.objects.filter(title=title).count() > 0:
                    return message_helper(error_message="题目已存在")
                else:
                    new_question = models.Questions(createUser=createUser, createTime=createTime, editTime=editTime,
                                                    title=title, content=content)
                    new_question.save()
                    return message_helper(success=True)
            else:
                return message_helper(error_message="请确认所有必填项已填写")
        else:
            return message_helper(error_message="请确认已输入问题标题和描述")
    else:
        return message_helper(method_error=True)


def edit_question(request, question_id):
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            if question_id and title and content:
                editTime = datetime.datetime.now()
                try:
                    question = models.Questions.objects.get(questionId=question_id)
                    if question.createUser.userID == who_is_login(request):
                        question.editTime = editTime
                        question.title = title
                        question.content = content
                        question.save()
                        return message_helper(success=True)
                    else:
                        return message_helper(error_message="权限不足，请使用对应账号登录")
                except models.Questions.DoesNotExist:
                    return message_helper(error_message="问题不存在")
            else:
                return message_helper(error_message="请确认所有必填项已填写")
        else:
            return message_helper(error_message="请确认已修改问题标题和描述")
    else:
        return message_helper(method_error=True)


def delete_question(request, question_id):
    if question_id:
        try:
            question = models.Questions.objects.get(questionId=question_id)
            if question.createUser.userID == who_is_login(request):
                question.delete()
                return message_helper(success=True)
            else:
                return message_helper(error_message="权限不足，请使用对应账号登录")
        except models.Questions.DoesNotExist:
            return message_helper(error_message="问题不存在")
    else:
        return message_helper(method_error=True)


def get_answer_list_by_question_id(request, question_id):
    if question_id:
        if models.Questions.objects.filter(questionId=question_id).count() > 0:
            answer_list = models.Answers.objects.filter(questionId=question_id).all()
            return message_helper(success=True, dataToReturn=json.loads(serializers.serialize("json", answer_list)))
        else:
            return message_helper(error_message="问题不存在")
    else:
        return message_helper(method_error=True)


def create_answer(request, question_id):
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            content = request.POST.get('content')
            if question_id and content:
                createUser = models.User.objects.get(userID=who_is_login(request))
                createTime = datetime.datetime.now()
                editTime = datetime.datetime.now()
                try:
                    current_question = models.Questions.objects.get(questionId=question_id)
                    new_answer = models.Answers(createUser=createUser, createTime=createTime,
                                                editTime=editTime, questionId=current_question, content=content)
                    new_answer.save()
                    return message_helper(success=True)
                except models.Questions.DoesNotExist:
                    return message_helper(error_message="题目不存在")
            else:
                return message_helper(error_message="请确认所有必填项已填写")
        else:
            return message_helper(error_message="请确认已输入问题标题和描述")
    else:
        return message_helper(method_error=True)


def edit_answer(request, answer_id):
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            content = request.POST.get('content')
            if answer_id and content:
                editTime = datetime.datetime.now()
                try:
                    answer = models.Answers.objects.get(answerID=answer_id)
                    if answer.createUser.userID == who_is_login(request):
                        answer.editTime = editTime
                        answer.content = content
                        answer.save()
                        return message_helper(success=True)
                    else:
                        return message_helper(error_message="权限不足，请使用对应账号登录")
                except models.Answers.DoesNotExist:
                    return message_helper(error_message="问题不存在")
            else:
                return message_helper(error_message="请确认所有必填项已填写")
        else:
            return message_helper(error_message="请确认已修改答案")
    else:
        return message_helper(method_error=True)


def delete_answer(request, answer_id):
    if answer_id:
        try:
            answer = models.Answers.objects.get(answerID=answer_id)
            if answer.createUser.userID == who_is_login(request):
                answer.delete()
                return message_helper(success=True)
            else:
                return message_helper(error_message="权限不足，请使用对应账号登录")
        except models.Answers.DoesNotExist:
            return message_helper(error_message="问题不存在")
    else:
        return message_helper(method_error=True)


def who_is_login(request):
    return request.session.get('USERUNIQUEID')


def message_helper(success=False, method_error=False, error_message="", dataToReturn=None):
    MESSAGE = {
        "success": {"status": 200, "message": "Success!"},
        "error": {"status": 406},
        "method_error": {"status": 400, "message": "Bad Request, Please Contact Admin!"}
    }
    # 成功
    if success:
        message = MESSAGE["success"]
        if dataToReturn is None:
            return HttpResponse(json.dumps(message, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
        else:
            message['data'] = dataToReturn
            return HttpResponse(json.dumps(message, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")
    # 方法错误
    elif method_error:
        return HttpResponse(json.dumps(MESSAGE["method_error"], ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
    elif not success and not method_error:
        message = MESSAGE["error"]
        message["message"] = error_message
        return HttpResponse(json.dumps(message, ensure_ascii=False),
                            content_type="application/json,charset=utf-8")
