from django.contrib import admin
from .models import User
from .models import Questions
from .models import Answers
from .models import SearchHistory
# Register your models here.
admin.site.register(User)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(SearchHistory)