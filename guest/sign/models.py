from django.db import models

# Create your models here.

# 发布会
class Event(models.Model):
    name = models.CharField(max_length=100)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=200)
    start_time = models.DateTimeField("events time")
    create_time = models.DateTimeField(auto_now=True)    # 创建时间（自动获取当前时间）

    def __str__(self):
        # , self.start_time
        return self.name

# 嘉宾表
class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)    # 关联发布会的id
    realname = models.CharField(max_length=64)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        # , self.phone
        return self.realname


class Meta:
    # Meta Django内部类，定义模型类的行为特性
    unique_together = ("event", "phone")