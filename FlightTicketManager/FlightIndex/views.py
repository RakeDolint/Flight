from django.shortcuts import render,redirect
from django.template import loader
from FlightIndex import models
from time import strftime
# Create your views here.

# 获取今日时间，以便搜索航班时限定出发日期
today=strftime("%Y-%m-%d")

# 对搜索结果排序时的，参考字典
OrderBy_Dict={"ByTime":"departure_time","ByFirstPrice":"first_class_price","ByEconoPrice":"economy_class_price"}

# 查询航班的网页
def flights_search(request):
    if request.method=="POST":
        input_dep_city=request.POST.get("dep_city")
        input_arr_city=request.POST.get("arr_city")
        #根据输入的城市在Airport表里搜索(只选出第一个)
        find_dep_city=models.Airport.objects.filter(city__icontains=input_dep_city).first()
        find_arr_city=models.Airport.objects.filter(city__icontains=input_arr_city).first()
        # 确认找得到城市时才传参到session
        if find_arr_city and find_dep_city:
            request.session["dep_city"]=input_dep_city
            request.session["arr_city"]=input_arr_city
            request.session["dep_day"] = request.POST.get("dep_day")
            request.session["OrderBy"]=OrderBy_Dict[request.POST.get("InWhatOrder")]
            return redirect("/flights/search_result")
    return render(request,"flights_view.html",{"cur_time":strftime("%Y-%m-%d")})

# 查询结果的网页
def search_result(request):
    search_dep_day =request.session.get("dep_day")
    search_dep_city =request.session.get("dep_city")
    search_arr_city =request.session.get("arr_city")
    orderByWhat =request.session.get("OrderBy")
    # 根据城市搜索机场
    dep_airport_list = models.Airport.objects.filter(city=search_dep_city)
    arr_airport_list = models.Airport.objects.filter(city=search_arr_city)
    # 根据出发日期、出发机场、到达机场找到所有，并排序。
    # list里每一项都是数据库中的一行记录，在django中是一个实例化的class
    flight_list = models.Flight.objects.filter(departure_day=search_dep_day,
                                               departure_airport__in=[each.airport_name for each in dep_airport_list],
                                               arrival_airport__in = [each.airport_name for each in arr_airport_list]).order_by(orderByWhat)

    return render(request,"search_result.html",{"flight_list":flight_list})

# 订票的网页
def book(request):
    # url中获取传递的航班号
    flight_num=request.GET.get("flightid")
    # gyz写的登录系统中在session中确定了参数 用户账号
    user_id=request.session.get("userid")
    # 这里给出乘机人的列表返回给网站
    passenger_list = models.Passenger.objects.filter(user__userid=user_id)
    # 找到对应的航班号，按理来说只会找到一个，以防万一用了first
    flight_object=models.Flight.objects.filter(flight_id=flight_num).first()
    dep_day=flight_object.departure_day
    if request.method=="POST":
        # 获取时间，传递给订单系统中的“订票时间”
        cur_time=strftime("%Y-%m-%d %H:%M:%S")

        # 舱位
        class_type=request.POST.get("classtypes")


        # 这是乘机人复选框的返回结果，list中每一项都是选中的那一行的复选框value属性，这里我传递的value是作为主键的乘机人身份证号
        checkbox_list=request.POST.get("check_box_list")
        # 检查时间冲突
        for pass_idnum in checkbox_list:
            models.Order.objects.filter(passid=pass_idnum,departure_day=dep_day)



        # 订票成功保存到数据库
        for i,pass_idnum in enumerate(checkbox_list):

            models.Order.objects.create(
                userid=user_id,
                flightnum=flight_num,
                departure_day=flight_object.flight_id,
                passid=pass_idnum,
                classtype=class_type[i],
                ordertime=cur_time
            )

        # 订票成功后转到订单列表
        return redirect(request,"booking_success.html")
    return render(request,"booking.html",{"passenger_list":passenger_list})

# 订单列表网页
def order_list(request):
    user_id=request.session.get("userid")
    order_list=models.Order.objects.filter(userid=user_id)
    if not order_list:
        return render(request,"no_order.html")
    # 具体看order_list.html，为了在一个for循环里展示所有订单信息，
    # 我把订单，乘机人，航班合并(zip)到了一个combined_list
    passenger_list=[]
    flight_list=[]
    for order_object in order_list:
        passenger_list.append(models.Passenger.objects.filter(idnum=order_object.passid).first())
        flight_list.append(models.Flight.objects.filter(
            flight_id=order_object.flightnum,
            departure_day=order_object.departure_day).first())
    combined_list=zip(order_list,passenger_list,flight_list)

    return render(request,"order_list",{{"combined_list":combined_list}})

def booking_success(request):
    return render(request,"booking_success.html")
# 退票网页
def refund(request):
    order_id=request.GET.get("orderid")
    # 直接按订单号删除(?)数据库中用户订的票
    models.Order.objects.filter(id=order_id).delete()
    return render(request,"refunding.html")

def no_order(request):
    return render(request,"no_order.html")