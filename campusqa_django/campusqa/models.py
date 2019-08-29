from django.db import models


# Create your models here.
class User(models.Model):
    GENDER = (
        (0, '男'),
        (1, '女')
    )
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    gender = models.IntegerField(choices=GENDER)
    college = models.CharField(max_length=200)
    phoneNum = models.CharField(max_length=11, null=False)
    password = models.CharField(max_length=20)
    enrollmentTime = models.IntegerField()


class Questions(models.Model):
    questionId = models.AutoField(primary_key=True)
    createUser = models.ForeignKey(User, on_delete=models.CASCADE)
    createTime = models.DateTimeField()
    editTime = models.DateTimeField(null=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=2000)


class Answers(models.Model):
    answerID = models.AutoField(primary_key=True)
    createUser = models.ForeignKey(User, on_delete=models.CASCADE)
    createTime = models.DateTimeField()
    editTime = models.DateTimeField(null=True)
    questionId = models.ForeignKey(Questions, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)


class SearchHistory(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    searchTime = models.DateTimeField()
    searchContent = models.CharField(max_length=2000)
    isValid = models.BooleanField()


class QuickAnswer(models.Model):
    questionId = models.AutoField(primary_key=True)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=2000)
