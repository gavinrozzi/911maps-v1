from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from calls.models import emergencycall, agency
from django.views.generic import ListView, TemplateView
from django.core import serializers
from django.core.serializers import serialize
from djgeojson.serializers import Serializer as GeoJSONSerializer
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from calls.serializers import EmergencycallSerializer
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    latest_calls_list = emergencycall.objects.order_by('-sent')[:6]
    total_call_count = emergencycall.objects.count()
    total_jurisdictions = emergencycall.objects.values('city').distinct().count()
    total_units = emergencycall.objects.values('units').distinct().count()
    total_code3 = emergencycall.objects.filter(priority="3").count()
    total_agencies = agency.objects.values('id').distinct().count()
    agency_list = agency.objects.all()
    template = loader.get_template('calls/index.html')
    context = {
        'latest_calls_list': latest_calls_list,
        'total_call_count' : total_call_count,
        'total_jurisdictions' : total_jurisdictions,
        'total_units' : total_units,
        'total_code3': total_code3,
        'total_agencies': total_agencies,
        'agency_list': agency_list,
    }
    return HttpResponse(template.render(context, request))

def all_calls_list(request):
    latest_calls_list = emergencycall.objects.all().order_by('-sent')
    calls_as_geojson = serialize('geojson', latest_calls_list, geometry_field='point')    
    context = {
        'latest_calls_list': latest_calls_list,
        'calls_as_geojson': calls_as_geojson
    }
    return render(request, 'calls/emergencycall_list.html', context)

class AboutPageView(TemplateView):
    template_name = 'calls/about.html'

def call_detail(request, id):
    try:
        call = emergencycall.objects.get(id=id)
    except call.DoesNotExist:
        raise Http404('911 call id {0} not found'.format(id))
    related_calls = emergencycall.objects.filter(description=call.description).filter(city=call.city).exclude(address=call.address).order_by('-sent')[:5]
    address_calls = emergencycall.objects.filter(address=call.address).filter(city=call.city).exclude(id=call.id).order_by('-sent')[:5]
    address_call_count = emergencycall.objects.filter(address=call.address).filter(city=call.city).exclude(id=call.id).order_by('-sent').count()
    related_call_count = emergencycall.objects.filter(description=call.description).filter(city=call.city).count() - 1
    first_related_call = emergencycall.objects.filter(description=call.description).filter(city=call.city).first()
    nearby_calls = emergencycall.objects.filter(point__distance_lte=(call.point, D(mi=1))).order_by('-sent')[:5]
    nearby_call_count = emergencycall.objects.filter(point__distance_lte=(call.point, D(mi=1))).order_by('-sent').count()
    return render(request, 'calls/call_detail.html', {'call': call, 'related_calls':related_calls, 'related_call_count':related_call_count, 'first_related_call': first_related_call, 'address_calls': address_calls, 'address_call_count': address_call_count, 'nearby_calls': nearby_calls, 'nearby_call_count': nearby_call_count})

def call_logs(request, id):

    try:
        call = emergencycall.objects.get(id=id)
    except call.DoesNotExist:
        raise Http404('911 call logs for call id {0} not found'.format(id))

    return render(request, 'calls/call_logs.html', {'call': call})

def priority(request):
    code1 = emergencycall.objects.filter(priority="1")
    code2 = emergencycall.objects.filter(priority="2")
    code3 = emergencycall.objects.filter(priority="3")
    total_code1 = emergencycall.objects.filter(priority="1").count()
    total_code2 = emergencycall.objects.filter(priority="2").count()
    total_code3 = emergencycall.objects.filter(priority="3").count()
    no_priority = emergencycall.objects.exclude(priority__isnull=False)
    total_no_priority = emergencycall.objects.exclude(priority__isnull=False).count()
    template = loader.get_template('calls/priority.html')
    context = {
        'code1': code1,
        'code2': code2,
        'code3': code3,
        'total_code1': total_code1,
        'total_code2': total_code2,
        'total_code3': total_code3,
        'no_priority' : no_priority,
        'total_no_priority' : total_no_priority,
    }
    return HttpResponse(template.render(context, request))

def priority_detail(request, id):
    try:
        call = emergencycall.objects.filter(priority=id)
    except call.DoesNotExist:
        raise Http404('911 call priority {0} not found'.format(id))

    return render(request, 'calls/call_priority.html', {'call': call})

def address_history(request, address, city, state):
    try:
        call = emergencycall.objects.filter(address__contains=address)
    except call.DoesNotExist:
        raise Http404('Address {0} not found'.format(id))

    return render(request, 'calls/address_history.html', {'address': address, 'city': city, 'state': state})

def jurisdiction(request, jurisdiction_name):
    jursdiction_call_list = emergencycall.objects.order_by('-sent').filter(city=jurisdiction_name)
    paginator = Paginator(jursdiction_call_list, 25)
    page = request.GET.get('page') 
    jurisdiction_calls = paginator.get_page(page)
    oldest_call = emergencycall.objects.filter(city=jurisdiction_name).first()
    total_calls = emergencycall.objects.filter(city=jurisdiction_name).count()
    total_overdoses = emergencycall.objects.filter(city=jurisdiction_name).filter(description='OVERDOSE')
    calls_as_geojson = serialize('geojson', jursdiction_call_list, geometry_field='point')
    context = {
        'jurisdiction_name': jurisdiction_name, 
        'jursdiction_call_list': jursdiction_call_list, 
        'total_calls': total_calls, 
        'jurisdiction_calls': jurisdiction_calls,
        'jursdiction_call_list': jursdiction_call_list,
        'oldest_call': oldest_call,
        'calls_as_geojson': calls_as_geojson,
    }
    try:
        call = emergencycall.objects.filter(city=jurisdiction_name)
    except call.city.DoesNotExist:
        raise Http404('Jurisdiction {0} not found'.format(jurisdiction_name))

    return render(request, 'calls/jurisdiction.html', context)

def jurisdiction_geojson(request, jurisdiction_name):
    calls_as_geojson = serialize('geojson', emergencycall.objects.order_by('-sent').filter(city=jurisdiction_name), geometry_field='point')
    return HttpResponse(calls_as_geojson, content_type="application/json")

def jurisdiction_list(request):
    total_jurisdictions = emergencycall.objects.values('city').distinct().count()
    jurisdictions = emergencycall.objects.values('city').distinct()
    city_calls = emergencycall.objects.filter(city='city').count()
    template = loader.get_template('calls/jurisdictions.html')
    context = {
        'total_jurisdictions': total_jurisdictions,
        'jurisdictions': jurisdictions,
    }
    return render(request, 'calls/jurisdictions.html', {'jurisdictions': jurisdictions, 'total_jurisdictions': total_jurisdictions, 'city_calls': city_calls})

def agency_list(request):
    total_agencies = agency.objects.values('id').distinct().count()
    jurisdictions = emergencycall.objects.values('city').distinct().count()
    agency_list = agency.objects.all()
    template = loader.get_template('calls/agency_list.html')
    context = {
        'total_agencies': total_agencies,
        'jurisdictions': jurisdictions,
        'agency_list': agency_list,
    }
    return HttpResponse(template.render(context, request))

def agency_detail(request, slug):
    total_agencies = agency.objects.values('id').distinct().count()
    total_calls = emergencycall.objects.filter(agency=slug).count()
    oldest_call = emergencycall.objects.filter(agency_id=slug).first()
    newest_call = emergencycall.objects.filter(agency_id=slug).last()
    agency_calls = emergencycall.objects.filter(agency=slug).order_by('-sent')
    agency_details = agency.objects.get(id=slug)
    mva = emergencycall.objects.filter(agency_id=slug).filter(description__contains='MVA')
    total_mva = emergencycall.objects.filter(agency_id=slug).filter(description__contains='MVA').count()
    overdose = emergencycall.objects.filter(agency_id=slug).filter(description__contains='OVERDOSE')
    total_overdose = emergencycall.objects.filter(agency_id=slug).filter(description__contains='OVERDOSE').count()
    fire = emergencycall.objects.filter(agency_id=slug).filter(description__contains='FIRE')
    total_fire = emergencycall.objects.filter(agency_id=slug).filter(description__contains='FIRE').count()
    water = emergencycall.objects.filter(agency_id=2).filter(description__contains='WATER')
    total_water = emergencycall.objects.filter(agency_id=2).filter(description__contains='WATER').count()
    jurisdictions = emergencycall.objects.values('city').distinct().count()
    agency_list = agency.objects.all()
    template = loader.get_template('calls/agency_detail.html')
    context = {
        'total_agencies': total_agencies,
        'agency_calls': agency_calls,
        'agency_details': agency_details,
        'total_calls': total_calls,
        'oldest_call': oldest_call,
        'newest_call': newest_call,
        'mva': mva,
        'total_mva': total_mva,
        'overdose': overdose,
        'total_overdose': total_overdose,
        'fire': fire,
        'total_fire': total_fire,
        'water': water,
        'total_water': total_water,
    }
    return HttpResponse(template.render(context, request))

def agency_geojson(request, slug):
    calls_as_geojson = serialize('geojson', emergencycall.objects.filter(agency=slug).order_by('-sent'), geometry_field='point')
    return HttpResponse(calls_as_geojson, content_type="application/json")

def call_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        calls = emergencycall.objects.all().order_by('-sent')
        serializer = EmergencycallSerializer(calls, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = EmergencycallSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def call_nature(request, call_nature):
    template = loader.get_template('calls/nature.html')
    calls = emergencycall.objects.filter(description__contains=call_nature).order_by('-sent')
    total_calls = emergencycall.objects.filter(description__contains=call_nature).count() 
    newest_call = emergencycall.objects.filter(description__contains=call_nature).last()
    oldest_call = emergencycall.objects.filter(description__contains=call_nature).first()
    calls_as_geojson = serialize('geojson', calls, geometry_field='point')
    context = {
        'call_nature': call_nature,
        'calls': calls,
        'total_calls': total_calls,
        'oldest_call': oldest_call,
        'newest_call': newest_call,
        'calls_as_geojson': calls_as_geojson,
       }
    return HttpResponse(template.render(context, request))

def call_nature_geojson(request, call_nature):
    calls_as_geojson = serialize('geojson', emergencycall.objects.filter(description__contains=call_nature).order_by('-sent'), geometry_field='point')
    return HttpResponse(calls_as_geojson, content_type="application/json")

def nature_list(request):
    template = loader.get_template('calls/natures.html')
    natures = emergencycall.objects.values('description').distinct()
    total_natures = emergencycall.objects.values('description').distinct().count() 
    context = {
        'natures': natures,
        'total_natures': total_natures,
       }
    return HttpResponse(template.render(context, request))

def jurisdiction_nature(request, call_nature, jurisdiction_name):
    template = loader.get_template('calls/jurisdiction_nature.html')
    calls = emergencycall.objects.filter(description__contains=call_nature).filter(city=jurisdiction_name).order_by('-sent')
    total_calls = emergencycall.objects.filter(description__contains=call_nature).filter(city=jurisdiction_name).count() 
    newest_call = emergencycall.objects.filter(description__contains=call_nature).filter(city=jurisdiction_name).last()
    oldest_call = emergencycall.objects.filter(description__contains=call_nature).filter(city=jurisdiction_name).first()
    jursdiction_call_list = emergencycall.objects.order_by('-sent').filter(city=jurisdiction_name).filter(description__contains=call_nature)
    total_calls = emergencycall.objects.filter(city=jurisdiction_name).filter(description__contains=call_nature).count()
    total_nature = emergencycall.objects.filter(city=jurisdiction_name).filter(description__contains=call_nature)
    call_points = list(emergencycall.objects.values_list('lat', 'lon'))
    calls_as_geojson = serialize('geojson', emergencycall.objects.filter(description__contains=call_nature).filter(city=jurisdiction_name).order_by('-sent'), geometry_field='point')
    context = {
        'call_nature': call_nature,
        'jurisdiction_name': jurisdiction_name,
        'calls': calls,
        'total_calls': total_calls,
        'oldest_call': oldest_call,
        'newest_call': newest_call,
        'call_points': call_points,
        'calls_as_geojson': calls_as_geojson,
       }
    return HttpResponse(template.render(context, request))

def jurisdiction_nature_geojson(request, jurisdiction_name, call_nature):
    calls_as_geojson = serialize('geojson', emergencycall.objects.filter(description__contains=call_nature).filter(city=jurisdiction_name).order_by('-sent'), geometry_field='point')
    return HttpResponse(calls_as_geojson, content_type="application/json")

def place_detail(request, place_name):
    place_call_list = emergencycall.objects.order_by('-sent').filter(place=place_name)
    paginator = Paginator(place_call_list, 25)
    page = request.GET.get('page') 
    place_calls = paginator.get_page(page)
    oldest_call = emergencycall.objects.filter(place=place_name).first()
    total_calls = emergencycall.objects.filter(place=place_name).count()
    total_overdoses = emergencycall.objects.filter(place=place_name).filter(description='OVERDOSE')
    calls_as_geojson = serialize('geojson', place_call_list, geometry_field='point')
    context = {
        'place_name': place_name, 
        'place_call_list': place_call_list, 
        'total_calls': total_calls, 
        'place_calls': place_calls,
        'oldest_call': oldest_call,
        'calls_as_geojson': calls_as_geojson,
    }
    try:
        call = emergencycall.objects.filter(place=place_name)
    except call.city.DoesNotExist:
        raise Http404('Jurisdiction {0} not found'.format(place_name))

    return render(request, 'calls/place_detail.html', context)