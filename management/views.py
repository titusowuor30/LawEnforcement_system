from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import *
import time

# Create your views here.
def home(request):
    recent_cases=Crime.objects.order_by('-time')[:3]
    featured_cases=Crime.objects.filter(featured=True)[:3]
    secret_cases=Crime.objects.filter(status='Secret')[:3]
    case_history=Crime.objects.order_by('-time')
    current_case=Crime.objects.order_by('-time').first()
    return render(request,'index.html',locals())


def logout_view(request):
  logout(request)
  return redirect('home') 


