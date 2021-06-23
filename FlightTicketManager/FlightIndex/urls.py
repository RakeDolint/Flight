from django.urls import path
from FlightIndex import views

urlpatterns = [
    # 以下均如/flights/search/
    path('search/',views.flights_search),
    path('search_result/',views.search_result),
    path('booking/',views.book),
    path('booking_success/',views.booking_success),
    path('order_list/',views.order_list),
    path('refunding/',views.refund),
    path('no_order/',views.no_order),
]