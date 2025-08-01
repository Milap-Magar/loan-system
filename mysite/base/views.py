from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import models
from django.contrib import messages
import json
import io
import base64
import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import xlsxwriter
import uuid
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
from joblib import load
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import os

from .forms import CreateUserForm
from .models import PredictionHistory

def signupPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + user)
            return redirect('landing')
    context = {'form': form}
    return render(request, 'signup.html', context)

def LandingPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')
    return render(request, 'landing.html')

@login_required(login_url='landing')
def Home(request):
    user_predictions = PredictionHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
    total_predictions = PredictionHistory.objects.filter(user=request.user).count()
    eligible_count = PredictionHistory.objects.filter(user=request.user, result='eligible').count()
    not_eligible_count = PredictionHistory.objects.filter(user=request.user, result='not eligible').count()

    success_rate = round((eligible_count / total_predictions) * 100) if total_predictions > 0 else 0

    context = {
        'recent_predictions': user_predictions,
        'total_predictions': total_predictions,
        'eligible_count': eligible_count,
        'not_eligible_count': not_eligible_count,
        'success_rate': success_rate,
    }
    return render(request, 'home.html', context)

def LogoutPage(request):
    logout(request)
    return redirect('landing')

@login_required(login_url='landing')
def DataAnalysis(request):
    return render(request, 'dataanalysis.html')

@login_required(login_url='landing')
def Predict(request):
    return render(request, 'predict.html')

def getPredictions(marital, house_O, car_O, profession, city, state, current_jy, current_hy, income, age):
    model = load('savedModels/model.pkl')
    encoders = load('savedModels/encoders.sav')
    
    # Create a DataFrame with the input data
    data = pd.DataFrame({
        'Married/Single': [marital],
        'House_Ownership': [house_O],
        'Car_Ownership': [car_O],
        'Profession': [profession],
        'CITY': [city],
        'STATE': [state],
        'CURRENT_JOB_YRS': [current_jy],
        'CURRENT_HOUSE_YRS': [current_hy],
        'Cat_Income': [income],
        'Cat_Age': [age]
    })

    # Apply label encoding to categorical variables
    for column in data.columns:
        if column in encoders:
            data[column] = encoders[column].transform(data[column])

    # Make prediction
    prediction = model.predict(data)

    # Map numeric prediction to label
    return 'eligible' if prediction[0] == 1 else 'not eligible'

def generate_qr_code(data):
    """Generate QR code and return as base64 string"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return img_str

def generate_pdf_report(prediction_data, result):
    """Generate PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Title
    title = Paragraph("Loan Eligibility Prediction Report", title_style)
    elements.append(title)
    
    # Result section
    result_text = f"Prediction Result: {result.upper()}"
    result_style = ParagraphStyle(
        'Result',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        alignment=1
    )
    result_para = Paragraph(result_text, result_style)
    elements.append(result_para)
    
    # Data table
    data = [['Field', 'Value']]
    for key, value in prediction_data.items():
        data.append([key.replace('_', ' ').title(), str(value)])
    
    table = Table(data, colWidths=[2*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_excel_report(prediction_data, result):
    """Generate Excel report"""
    buffer = io.BytesIO()
    
    # Create workbook and worksheet
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet('Loan Prediction Report')
    
    # Formats
    title_format = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#4F81BD',
        'font_color': 'white'
    })
    
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'center',
        'bg_color': '#D9E1F2',
        'border': 1
    })
    _format = workbook.add_format({
        'font_size': 11,
        'align': 'left',
        'border': 1
    })
    
    result_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'bg_color': '#C6EFCE' if result == 'eligible' else '#FFC7CE',
        'font_color': '#006100' if result == 'eligible' else '#9C0006'
    })
    
    # Write title
    worksheet.merge_range('A1:B1', 'Loan Eligibility Prediction Report', title_format)
    
    # Write result
    worksheet.merge_range('A3:B3', f'Prediction Result: {result.upper()}', result_format)
    
    # Write data
    worksheet.write('A5', 'Field', header_format)
    worksheet.write('B5', 'Value', header_format)
    
    row = 6
    for key, value in prediction_data.items():
        worksheet.write(f'A{row}', key.replace('_', ' ').title(), data_format)
        worksheet.write(f'B{row}', str(value), data_format)
        row += 1
    
    # Set column widths
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 25)
    
    workbook.close()
    buffer.seek(0)
    return buffer

@login_required(login_url='landing')
def Result(request):
    if request.method == 'POST':
        marital = request.POST.get('marital')
        house_O = request.POST.get('house_O')
        car_O = request.POST.get('car_O')
        profession = request.POST.get('profession')
        city = request.POST.get('city')
        state = request.POST.get('state')
        current_jy = int(request.POST.get('current_jy'))
        current_hy = int(request.POST.get('current_hy'))
        income = int(request.POST.get('income'))
        age = int(request.POST.get('age'))
        
        result = getPredictions(marital, house_O, car_O, profession, city, state, current_jy, current_hy, income, age)
        
        prediction_data = {
            'marital': marital, 'house_O': house_O, 'car_O': car_O, 'profession': profession,
            'city': city, 'state': state, 'current_jy': current_jy, 'current_hy': current_hy,
            'income': income, 'age': age,
        }
        
        prediction_id = str(uuid.uuid4())
        PredictionHistory.objects.create(
            user=request.user, prediction_id=prediction_id, marital_status=marital,
            house_ownership=house_O, car_ownership=car_O, profession=profession,
            city=city, state=state, current_job_years=current_jy,
            current_house_years=current_hy, income=income, age=age,
            result=result, timestamp=timezone.now()
        )
        
        qr_data = f"Loan Eligibility Result: {result.upper()}\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\nPrediction ID: {prediction_id}"
        qr_code = generate_qr_code(qr_data)
        
        context = {
            'result': result, 'prediction_data': prediction_data,
            'prediction_id': prediction_id, 'qr_code': qr_code,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return render(request, 'result.html', context)
    return redirect('predict')

@login_required(login_url='landing')
def download_pdf(request, prediction_id):
    """Download PDF report for a specific prediction"""
    try:
        prediction = PredictionHistory.objects.get(prediction_id=prediction_id, user=request.user)
        
        prediction_data = {
            'marital': prediction.marital_status,
            'house_O': prediction.house_ownership,
            'car_O': prediction.car_ownership,
            'profession': prediction.profession,
            'city': prediction.city,
            'state': prediction.state,
            'current_jy': prediction.current_job_years,
            'current_hy': prediction.current_house_years,
            'income': prediction.income,
            'age': prediction.age,
        }
        
        buffer = generate_pdf_report(prediction_data, prediction.result)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="loan_prediction_{prediction_id}.pdf"'
        return response
    except PredictionHistory.DoesNotExist:
        messages.error(request, 'Prediction not found')
        return redirect('prediction_history')

@login_required(login_url='landing')
def download_excel(request, prediction_id):
    """Download Excel report for a specific prediction"""
    try:
        prediction = PredictionHistory.objects.get(prediction_id=prediction_id, user=request.user)
        
        prediction_data = {
            'marital': prediction.marital_status,
            'house_O': prediction.house_ownership,
            'car_O': prediction.car_ownership,
            'profession': prediction.profession,
            'city': prediction.city,
            'state': prediction.state,
            'current_jy': prediction.current_job_years,
            'current_hy': prediction.current_house_years,
            'income': prediction.income,
            'age': prediction.age,
        }
        
        buffer = generate_excel_report(prediction_data, prediction.result)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="loan_prediction_{prediction_id}.xlsx"'
        return response
    except PredictionHistory.DoesNotExist:
        messages.error(request, 'Prediction not found')
        return redirect('prediction_history')

@login_required(login_url='landing')
def prediction_history(request):
    """Display prediction history with pagination and filtering"""
    predictions_list = PredictionHistory.objects.filter(user=request.user).order_by('-timestamp')
    
    # Apply filters
    result_filter = request.GET.get('result')
    if result_filter:
        predictions_list = predictions_list.filter(result=result_filter)
    
    profession_filter = request.GET.get('profession')
    if profession_filter:
        predictions_list = predictions_list.filter(profession__icontains=profession_filter)
    
    city_filter = request.GET.get('city')
    if city_filter:
        predictions_list = predictions_list.filter(city__icontains=city_filter)
    
    # Pagination
    paginator = Paginator(predictions_list, 10)  # Show 10 predictions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique values for filter dropdowns
    all_predictions = PredictionHistory.objects.filter(user=request.user)
    professions = all_predictions.values_list('profession', flat=True).distinct().order_by('profession')
    cities = all_predictions.values_list('city', flat=True).distinct().order_by('city')
    
    context = {
        'page_obj': page_obj,
        'total_count': all_predictions.count(),
        'eligible_count': all_predictions.filter(result='eligible').count(),
        'not_eligible_count': all_predictions.filter(result='not eligible').count(),
        'filtered_count': predictions_list.count(),
        'professions': professions,
        'cities': cities,
        'current_filters': {
            'result': result_filter,
            'profession': profession_filter,
            'city': city_filter,
        }
    }
    print(f"Total Predictions: {all_predictions.count()}, Filtered: {predictions_list.count()}")
    return render(request, 'prediction_history.html', context)

@login_required(login_url='landing')
def dashboard(request):
    """Analytics dashboard"""
    user_predictions = PredictionHistory.objects.filter(user=request.user)
    
    # Basic statistics
    total_predictions = user_predictions.count()
    eligible_count = user_predictions.filter(result='eligible').count()
    not_eligible_count = user_predictions.filter(result='not eligible').count()
    
    # Income analysis
    if total_predictions > 0:
        avg_income = user_predictions.aggregate(avg_income=models.Avg('income'))['avg_income']
        max_income = user_predictions.aggregate(max_income=models.Max('income'))['max_income']
        min_income = user_predictions.aggregate(min_income=models.Min('income'))['min_income']
    else:
        avg_income = max_income = min_income = 0
    
    # Recent predictions
    recent_predictions = user_predictions[:5]
    
    context = {
        'total_predictions': total_predictions,
        'eligible_count': eligible_count,
        'not_eligible_count': not_eligible_count,
        'avg_income': round(avg_income) if avg_income else 0,
        'max_income': max_income,
        'min_income': min_income,
        'recent_predictions': recent_predictions,
    }
    return render(request, 'dashboard.html', context)

def api_prediction(request):
    """API endpoint for predictions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract data
            marital = data.get('marital')
            house_O = data.get('house_O')
            car_O = data.get('car_O')
            profession = data.get('profession')
            city = data.get('city')
            state = data.get('state')
            current_jy = int(data.get('current_jy'))
            current_hy = int(data.get('current_hy'))
            income = int(data.get('income'))
            age = int(data.get('age'))
            
            # Make prediction
            result = getPredictions(marital, house_O, car_O, profession, city, state, current_jy, current_hy, income, age)
            
            return JsonResponse({
                'success': True,
                'result': result,
                'prediction_data': {
                    'marital': marital, 'house_O': house_O, 'car_O': car_O, 'profession': profession,
                    'city': city, 'state': state, 'current_jy': current_jy, 'current_hy': current_hy,
                    'income': income, 'age': age,
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
