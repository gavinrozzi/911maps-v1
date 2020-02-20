from django.urls import path, include
from django.conf.urls import url, include
from . import views
from djgeojson.views import GeoJSONLayerView
from calls.models import emergencycall
from calls.views import all_calls_list, AboutPageView, call_detail, priority, priority_detail, jurisdiction, call_list, address_history, agency_detail, call_nature, nature_list, jurisdiction_nature

urlpatterns = [
   path('', views.index, name='index'),
   path('calllist/', views.all_calls_list, name='all_calls_list'),
   path('about', AboutPageView.as_view()),
   path('call/<int:id>/', views.call_detail, name='call_detail'),
   path('natures/', views.nature_list, name='nature_list'),
   path('nature/<str:call_nature>/', views.call_nature, name='call_nature'),
   path('geojson/nature/<str:call_nature>/', views.call_nature_geojson, name='call_nature'),
   path('place/<str:place_name>/', views.place_detail, name='place_detail'),
   path('priority/', views.priority, name='priority'),
   path('priority/<int:id>', views.priority_detail, name='priority_detail'),
   path('call-logs/<int:id>/', views.call_logs, name='call_logs'),
   path('agencies/', views.agency_list, name='agency_list'),
   path('agency/<str:slug>/', views.agency_detail, name='agency_detail'),
   path('geojson/agency/<str:slug>/', views.agency_geojson, name='agency_detail'),
   path('jurisdictions/', views.jurisdiction_list, name='jurisdiction_list'),
   path('jurisdiction/<str:jurisdiction_name>/', views.jurisdiction, name='jurisdiction'),
   path('geojson/jurisdiction/<str:jurisdiction_name>/', views.jurisdiction_geojson, name='jurisdiction'),
   path('jurisdiction/<str:jurisdiction_name>/nature/<str:call_nature>/', views.jurisdiction_nature, name='jurisdiction_nature'),
   path('geojson/jurisdiction/<str:jurisdiction_name>/nature/<str:call_nature>/', views.jurisdiction_nature_geojson, name='data'),
   path('location/<str:state>/<str:city>/<str:address>/', views.address_history, name='address_history'),
   path('api_v1/', include('rest_framework.urls', namespace='rest_framework')),
   path('api_v1/calls', views.call_list, name='call_list')
]
