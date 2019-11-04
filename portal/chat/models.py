import uuid

from django.db import models
# Create your models here.
class counsellor(models.Model):
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=100)
    user_status = models.BooleanField(default=False)
    user_information = models.TextField(max_length=1000)
    user_dp = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

class student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_status = models.BooleanField(default=False)

class Chatroom(models.Model):
    Chatroom_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Counsellor= models.ForeignKey(counsellor, on_delete=models.CASCADE)
    Student = models.ForeignKey(student, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    abort = models.BooleanField(default=False)

class messages(models.Model):
    message=models.TextField(max_length=1000)
    message_from = models.BooleanField()
    chat_session = models.ForeignKey(Chatroom, on_delete=models.CASCADE)
    message_time = models.DateTimeField()

