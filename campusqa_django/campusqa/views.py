import hashlib
import json

from django.core import serializers
from django.db.models import Q
from campusqa.utils import message_helper, who_is_login, is_login, format_time, current_time, PaginationHelper

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
                        request.session['ISLOGIN'] = "true"
                        request.session['USERUNIQUEID'] = current_user.userID
                        return message_helper(success=True, dataToReturn=json.loads(
                            json.dumps({"userID": current_user.userID}, ensure_ascii=False)
                        ))
                    else:
                        return message_helper(error_message="密码错误")
                except models.User.DoesNotExist:
                    return message_helper(error_message="用户不存在")
            else:
                return message_helper(error_message="用户名或密码不能为空")
        else:
            return message_helper(error_message="请确认填写了必填字段")
    else:
        return message_helper(method_error=True)


def logout(request):
    if not is_login(request):
        return message_helper(error_message="请先登录")
    request.session.flush()
    return message_helper(success=True)


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
                if models.User.objects.filter(phoneNum=phoneNum).count() > 0:
                    return message_helper(error_message="该手机号已注册")
                else:
                    gender = 0 if (gender == '男') else 1
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
    if not is_login(request):
        return message_helper(error_message="请先登录")
    if user_id:
        if user_id == who_is_login(request):
            current_user = models.User.objects.filter(userID=user_id).values("name", "gender", "college",
                                                                             "enrollmentTime", 'phoneNum')
            data = json.loads(
                json.dumps(list(current_user), ensure_ascii=False)
            )
            data[0]['gender'] = '男' if (data[0]['gender'] == 0) else '女'
            if current_user.count() > 0:
                return message_helper(success=True,
                                      dataToReturn=data)
            else:
                return message_helper(error_message="用户不存在")
        else:
            return message_helper(error_message="权限不足，请使用对应账号登录")
    else:
        return message_helper(method_error=True)


def edit_user(request):
    if not is_login(request):
        return message_helper(error_message="请先登录")
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            name = request.POST.get('name')
            gender = request.POST.get('gender')
            college = request.POST.get('college')
            phoneNum = request.POST.get('phoneNum')
            enrollmentTime = request.POST.get('enrollmentTime')
            if name and gender and college and phoneNum and enrollmentTime:
                try:
                    user = models.User.objects.get(userID=who_is_login(request))
                    user.name = name
                    user.gender = 0 if (gender == '男') else 1
                    user.college = college
                    user.phoneNum = phoneNum
                    user.enrollmentTime = enrollmentTime
                    user.save()
                    return message_helper(success=True)
                except models.Questions.DoesNotExist:
                    return message_helper(error_message="用户不存在")
            else:
                return message_helper(error_message="请确认所有必填项已填写")
        else:
            return message_helper(error_message="请确认已修改个人信息")
    else:
        return message_helper(method_error=True)


def get_personal_question_list(request, user_id):
    page_size = request.GET.get('pageSize')
    page_num = request.GET.get('pageNum')
    if page_size and page_num:
        try:
            page_num = int(page_num)
            page_size = int(page_size)
        except ValueError:
            return message_helper(error_message="分页参数不正确")
    if user_id:
        if models.User.objects.filter(userID=user_id).count() > 0:
            pagination_helper = PaginationHelper(models.Questions.objects.filter(createUser=user_id).count(), page_size)
            if pagination_helper.total_page < page_num:
                return message_helper(error_message="页面不存在")
            return_message = {
                "totalPage": pagination_helper.total_page,
                "dataCount": pagination_helper.data_count,
                "currentPage": page_num,
            }
            question_list = models.Questions.objects.filter(createUser=user_id)[
                            pagination_helper.get_offset(page_num):page_size + pagination_helper.get_offset(page_num)]
            return_message['data'] = json.loads(serializers.serialize("json", question_list))
            return message_helper(success=True, dataToReturn=return_message)
        else:
            return message_helper(error_message="用户不存在")
    else:
        return message_helper(method_error=True)


def get_personal_answer_list(request, user_id):
    page_size = request.GET.get('pageSize')
    page_num = request.GET.get('pageNum')
    if page_size and page_num:
        try:
            page_num = int(page_num)
            page_size = int(page_size)
        except ValueError:
            return message_helper(error_message="分页参数不正确")
    if user_id:
        if models.User.objects.filter(userID=user_id).count() > 0:
            pagination_helper = PaginationHelper(models.Answers.objects.filter(createUser=user_id).count(), page_size)
            if pagination_helper.total_page < page_num:
                return message_helper(error_message="页面不存在")
            return_message = {
                "totalPage": pagination_helper.total_page,
                "dataCount": pagination_helper.data_count,
                "currentPage": page_num,
            }
            answer_list = models.Answers.objects.select_related().filter(createUser=user_id)[
                          pagination_helper.get_offset(page_num):page_size + pagination_helper.get_offset(page_num)]
            # return_message['data'] = json.loads(serializers.serialize("json", answer_list))
            format_answer_list = []
            for row in answer_list:
                format_answer_list.append(
                    {'answerID': row.answerID, 'createTime': row.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                     'editTime': row.editTime.strftime("%Y-%m-%d %H:%M:%S"), 'questionId': row.questionId.questionId,
                     'content': row.content, 'createUserID': row.createUser.userID,
                     'createUserName': row.createUser.name, 'questionName': row.questionId.title
                     })
            return message_helper(success=True,
                                  dataToReturn=format_answer_list)
        else:
            return message_helper(error_message="用户不存在")
    else:
        return message_helper(method_error=True)


def search_by_keywords(request):
    keyword = request.GET.get('keyword')
    if keyword:
        if is_login(request):
            models.SearchHistory(userID=models.User.objects.get(userID=who_is_login(request)),
                                 searchTime=current_time(),
                                 searchContent=keyword,
                                 isValid=True).save()
        question_list = models.Questions.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)).order_by('-editTime').select_related().all()
        quick_answer = models.QuickAnswer.objects.filter(question__icontains=keyword).all()
        format_question_list = []
        for row in question_list:
            format_question_list.append(
                {'questionID': row.questionId, 'createTime': row.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                 'editTime': row.editTime.strftime("%Y-%m-%d %H:%M:%S"), 'title': row.title,
                 'content': row.content, 'createUserID': row.createUser.userID, 'createUserName': row.createUser.name})
        message = {
            'askNow': json.loads(serializers.serialize("json", quick_answer)),
            'searchResult': format_question_list
        }
        return message_helper(success=True, dataToReturn=message)
    else:
        return message_helper(error_message="请输入搜索内容")


def get_question_list(request):
    page_size = request.GET.get('pageSize')
    page_num = request.GET.get('pageNum')
    if page_size and page_num:
        try:
            page_num = int(page_num)
            page_size = int(page_size)
        except ValueError:
            return message_helper(error_message="分页参数不正确")
    question_list = models.Questions.objects
    pagination_helper = PaginationHelper(question_list.count(), page_size)
    if pagination_helper.total_page < page_num:
        return message_helper(error_message="页面不存在")
    return_message = {
        "totalPage": pagination_helper.total_page,
        "dataCount": pagination_helper.data_count,
        "currentPage": page_num,
    }
    question_list = question_list.order_by('-editTime').select_related().all()[
                    pagination_helper.get_offset(page_num):page_size + pagination_helper.get_offset(page_num)]
    format_question_list = []
    for row in question_list:
        format_question_list.append(
            {'questionID': row.questionId, 'createTime': row.createTime.strftime("%Y-%m-%d %H:%M:%S"),
             'editTime': row.editTime.strftime("%Y-%m-%d %H:%M:%S"), 'title': row.title,
             'content': row.content, 'createUserID': row.createUser.userID, 'createUserName': row.createUser.name})
    return_message['data'] = format_question_list
    return message_helper(success=True, dataToReturn=return_message)


def get_question_info(request, question_id):
    if question_id:
        question = models.Questions.objects.filter(questionId=question_id)
        if question.count() > 0:
            question_list = models.Questions.objects.select_related().filter(questionId=question_id).all()
            format_question_list = []
            for row in question_list:
                format_question_list.append(
                    {'questionID': row.questionId, 'createTime': row.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                     'editTime': row.editTime.strftime("%Y-%m-%d %H:%M:%S"), 'title': row.title,
                     'content': row.content, 'createUserID': row.createUser.userID,
                     'createUserName': row.createUser.name})
            return message_helper(success=True,
                                  dataToReturn=json.loads(json.dumps(format_question_list, ensure_ascii=False)))
        else:
            return message_helper(error_message="问题不存在")
    else:
        return message_helper(method_error=True)


def create_question(request):
    if not is_login(request):
        return message_helper(error_message="请先登录")
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            if title and content:
                createUser = models.User.objects.get(userID=who_is_login(request))
                createTime = current_time()
                editTime = current_time()
                if models.Questions.objects.filter(title=title).count() > 0:
                    return message_helper(error_message="题目已存在")
                else:
                    new_question = models.Questions(createUser=createUser, createTime=createTime, editTime=editTime,
                                                    title=title, content=content)
                    new_question.save()
                    return message_helper(success=True, dataToReturn=json.loads(
                        json.dumps({"questionID": new_question.questionId}, ensure_ascii=False)
                    ))
            else:
                return message_helper(error_message="请确认所有必填项已填写")
        else:
            return message_helper(error_message="请确认已输入问题标题和描述")
    else:
        return message_helper(method_error=True)


def edit_question(request, question_id):
    if not is_login(request):
        return message_helper(error_message="请先登录")
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            title = request.POST.get('title')
            content = request.POST.get('content')
            if question_id and title and content:
                editTime = current_time()
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
    if not is_login(request):
        return message_helper(error_message="请先登录")
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
    page_size = request.GET.get('pageSize')
    page_num = request.GET.get('pageNum')
    if page_size and page_num:
        try:
            page_num = int(page_num)
            page_size = int(page_size)
        except ValueError:
            return message_helper(error_message="分页参数不正确")
    if question_id:
        if models.Questions.objects.filter(questionId=question_id).count() > 0:
            answer_list = models.Answers.objects.filter(questionId=question_id)
            pagination_helper = PaginationHelper(answer_list.count(), page_size)
            if pagination_helper.total_page < page_num:
                return message_helper(error_message="页面不存在")
            return_message = {
                "totalPage": pagination_helper.total_page,
                "dataCount": pagination_helper.data_count,
                "currentPage": page_num,
            }
            answer_list = answer_list.order_by('-editTime').select_related().all()[
                          pagination_helper.get_offset(page_num):page_size + pagination_helper.get_offset(page_num)]
            format_answer_list = []
            for row in answer_list:
                format_answer_list.append(
                    {'answerID': row.answerID, 'createTime': row.createTime.strftime("%Y-%m-%d %H:%M:%S"),
                     'editTime': row.editTime.strftime("%Y-%m-%d %H:%M:%S"), 'questionId': row.questionId.questionId,
                     'content': row.content, 'createUserID': row.createUser.userID,
                     'createUserName': row.createUser.name
                     })
            return_message['data'] = format_answer_list
            return message_helper(success=True, dataToReturn=return_message)
        else:
            return message_helper(error_message="问题不存在")
    else:
        return message_helper(method_error=True)


def create_answer(request, question_id):
    if not is_login(request):
        return message_helper(error_message="请先登录")
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            content = request.POST.get('content')
            if question_id and content:
                createUser = models.User.objects.get(userID=who_is_login(request))
                createTime = current_time()
                editTime = current_time()
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
    if not is_login(request):
        return message_helper(error_message="请先登录")
    if request.method == 'POST':  # 当提交表单时
        # 判断是否传参
        if request.POST:
            content = request.POST.get('content')
            if answer_id and content:
                editTime = current_time()
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
    if not is_login(request):
        return message_helper(error_message="请先登录")
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
