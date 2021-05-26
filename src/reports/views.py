from products.models import Product
from typing import List
from django.contrib import auth
from django.core.checks import messages
from django.forms.fields import JSONField
from django.http.request import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from matplotlib.pyplot import autoscale
from profiles.models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils import get_report_image
from .models import Report
from .forms import ReportForm
from django.views.generic import ListView, DetailView

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from sales.models import Sale, Position, CSV
from products.models import Product
import csv
from django.utils.dateparse import parse_date
# Create your views here.

class ReportListView(ListView):
    model = Report
    template_name = 'reports/main.html'

class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'

class UploadTemplateView(TemplateView):
    template_name = 'reports/from_file.html'

def csv_upload_view(request):
    print('file is being send')

    if request.method == 'POST':
        csv_file = request.FILES.get('file')
        obj = CSV.objects.create(file_name=csv_file)

        with open(obj.file_name.path, 'r') as f:
            reader = csv.reader(f)
            reader.__next__()
            for row in reader:
                data = "".join(row)
                data = data.split(',')
                data.pop()

                transaction_id = data[1]
                product = data[2]
                quantity = int(data[3])
                customer = data[4]
                date = parse_date(data[5])

                try:
                    product_obj = Product.objects.get(name=product)
                except Product.DoesNotExist:
                    product_obj = None

                print(product_obj)


    return HttpResponse()

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

@login_required
def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {'obj': obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # If download 
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # If display
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response