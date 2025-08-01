from django.urls import path
from . import views


urlpatterns = [
    path('',views.LandingPage,name='landing'),
    path('signup/', views.signupPage, name='signup'),
    path('home/', views.Home, name='home'),
    path('logout/',views.LogoutPage,name='logout'),
    path('dataanalysis',views.DataAnalysis,name='data'),
    path('predict', views.Predict, name='predict'),
    path('result',views.Result,name='result'),
    
    # New enhanced features
    path('dashboard/', views.dashboard, name='dashboard'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('download/pdf/<str:prediction_id>/', views.download_pdf, name='download_pdf'),
    path('download/excel/<str:prediction_id>/', views.download_excel, name='download_excel'),
    path('api/predict/', views.api_prediction, name='api_prediction'),
]
 
 
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('home/',views.HomePage,name='home'),
    path('logout/',views.LogoutPage,name='logout'),

     path('result',views.Result,name='result'),
     path('dataanalysis',views.Data,name='dataanalysis'),
     path('team',views.About,name='team'),
     path('predict', views.Predict, name='predict'),
    
]
'''



