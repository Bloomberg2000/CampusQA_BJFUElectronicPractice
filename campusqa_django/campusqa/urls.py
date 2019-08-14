"""campusqa_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('users/login', views.login),
    path('users/logout', views.logout),
    path('users/register', views.register),
    path('users/personalInfo/<int:user_id>/', views.get_personal_info),
    path('users/personalQuestionList/<int:user_id>/', views.get_personal_question_list),
    path('users/personalAnswerList/<int:user_id>/', views.get_personal_answer_list),

    path('search/', views.search_by_keywords),

    path('questions/', views.get_question_list),
    path('questions/create', views.create_question),
    path('questions/edit/<int:question_id>', views.edit_question),
    path('questions/delete/<int:question_id>', views.delete_question),

    path('answers/<int:question_id>', views.get_answer_list_by_question_id),
    path('answers/create/<int:question_id>', views.create_answer),
    path('answers/edit/<int:answer_id>', views.edit_answer),
    path('answers/delete/<int:answer_id>', views.delete_answer),

]
