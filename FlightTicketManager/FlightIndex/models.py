from django.db import models


# Create your models here.
class Flight(models.Model):
    """航班票务信息表"""
    flight_id = models.CharField(verbose_name="航班号", max_length=20, unique=True)
    departure_day = models.DateField(verbose_name="出发日期")
    departure_time = models.TimeField(verbose_name="出发时刻")
    arrival_time = models.TimeField(verbose_name="到达时刻")
    departure_airport = models.CharField(verbose_name="出发机场", max_length=20)
    arrival_airport = models.CharField(verbose_name="到达机场", max_length=20)
    stopover_airport = models.CharField(verbose_name="经停机场", max_length=20)
    first_class_num = models.IntegerField(verbose_name="头等舱数")
    first_class_price = models.IntegerField(verbose_name="头等舱价格")
    economy_class_num = models.IntegerField(verbose_name="经济舱数")
    economy_class_price = models.IntegerField(verbose_name="经济舱价格")
    aircraft_type = models.CharField(verbose_name="飞机型号", max_length=20, blank=True)
    voyage = models.IntegerField(verbose_name="航程", blank="True")
    company = models.CharField(verbose_name="航空公司", max_length=40, blank=True)

    # 联合主键
    class Meta:
        unique_together = (("flight_id", "departure_day"),)


class Airport(models.Model):
    """机场表"""
    airport_id = models.CharField(verbose_name="机场代码", max_length=20, primary_key=True, unique=True)
    airport_name = models.CharField(verbose_name="机场名称", max_length=20, unique=True)
    city = models.CharField(verbose_name="城市", max_length=20)

class User(models.Model):
    userid = models.CharField(verbose_name="账号",max_length=20,null=False,unique=True)
    password = models.CharField(verbose_name="密码",max_length=20,null=False)
    name=models.CharField(verbose_name="姓名",max_length=20)
    idnum=models.CharField(verbose_name="身份证号",max_length=40,null=False,unique=True)
    telnum=models.CharField(verbose_name="手机号",max_length=20,null=False)
    email = models.CharField(verbose_name="电子邮箱",max_length=40,null=True)

class Passenger(models.Model):
    name=models.CharField(verbose_name="乘机人姓名",max_length=20)
    idnum=models.CharField(verbose_name="乘机人身份证号",max_length=20)
    telnum=models.CharField(verbose_name="乘机人手机号",max_length=40)
    user = models.ManyToManyField(to='User')

class Order(models.Model):
    userid=models.CharField(verbose_name="账号",max_length=20,null=False)
    flightnum=models.CharField(verbose_name="航班号",max_length=20,null=False)
    departure_day=models.DateField(verbose_name="出发日期",null=False)
    passid=models.CharField(verbose_name="乘机人身份证号",max_length=20,null=False)
    classtype=models.CharField(verbose_name="舱位",max_length=20,null=False)
    ordertime=models.DateTimeField(verbose_name="订票时间")