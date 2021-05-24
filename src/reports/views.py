from django.contrib import auth
from django.core.checks import messages
from django.forms.fields import JSONField
from django.shortcuts import render
from matplotlib.pyplot import autoscale
from profiles.models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import get_report_image
from .models import Report
from .forms import ReportForm
# Create your views here.

@login_required
def create_report_view(request):
    form = ReportForm(request.POST or None)
    if request.is_ajax():
        #name = request.POST.get('name')
        #remarks = request.POST.get('remarks')

        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()

        #Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({'msg':'send'})
    return JsonResponse({})