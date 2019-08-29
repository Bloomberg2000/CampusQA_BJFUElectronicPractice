import datetime
import json
import math

from django.http import HttpResponse


class PaginationHelper:
    def get_offset(self, pageNum):
        return (pageNum - 1) * self.page_size

    def __init__(self, dataCount, pageSize):
        self.data_count = dataCount
        self.page_size = pageSize
        self.total_page = math.ceil(dataCount / pageSize)
        if self.total_page == 0:
            self.total_page = 1


def is_login(request):
    return True if (request.session.get('ISLOGIN') == 'true') else False


def who_is_login(request):
    return request.session.get('USERUNIQUEID')


def format_time(time):
    return (time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")


def current_time():
    return format_time(datetime.datetime.now())


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
