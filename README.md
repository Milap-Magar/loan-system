# Loan Eligibility Prediction System

A comprehensive machine learning-powered web application for predicting loan eligibility using advanced analytics and modern web technologies.

## 🚀 New Enhanced Features

### ✨ Core Features
- **Advanced Machine Learning Model**: Random Forest classifier trained on extensive loan data
- **Real-time Prediction**: Instant loan eligibility assessment
- **User Authentication**: Secure login and registration system
- **Responsive Design**: Modern, mobile-friendly interface

### 📊 Analytics & Dashboard
- **Comprehensive Dashboard**: Visual analytics with charts and statistics
- **Prediction History**: Complete history of all user predictions
- **Performance Metrics**: Success rates, income analysis, and trends
- **Interactive Charts**: Visual representation of prediction data

### 📱 Mobile & Export Features
- **QR Code Generation**: Scan QR codes to view results on mobile devices
- **PDF Reports**: Download detailed prediction reports in PDF format
- **Excel Export**: Export prediction data to Excel spreadsheets
- **Mobile Responsive**: Optimized for all device sizes

### 🔧 Technical Enhancements
- **API Endpoints**: RESTful API for programmatic access
- **Database Integration**: Persistent storage of prediction history
- **Form Validation**: Client-side and server-side validation
- **Modern UI/UX**: Tailwind CSS with beautiful gradients and animations

## 🛠️ Technology Stack

- **Backend**: Django 4.2, Python 3.8+
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Machine Learning**: Scikit-learn, Random Forest Classifier
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Additional Libraries**: 
  - qrcode (QR code generation)
  - reportlab (PDF generation)
  - openpyxl (Excel export)
  - Pillow (Image processing)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Loan-Eligibility-Prediction
```

### 2. Create Virtual Environment
```bash
python -m venv env
# On Windows
env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
cd mysite
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Run the Application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

```
Loan-Eligibility-Prediction/
├── mysite/
│   ├── base/
│   │   ├── models.py          # Database models
│   │   ├── views.py           # View logic and API endpoints
│   │   ├── urls.py            # URL routing
│   │   ├── admin.py           # Admin interface configuration
│   │   └── forms.py           # User forms
│   ├── templates/
│   │   ├── home.html          # Enhanced home page
│   │   ├── predict.html       # Modern prediction form
│   │   ├── result.html        # Results with QR codes
│   │   ├── dashboard.html     # Analytics dashboard
│   │   ├── prediction_history.html # Prediction history
│   │   ├── header.html        # Navigation header
│   │   └── master.html        # Base template
│   ├── static/                # Static files (CSS, JS, images)
│   ├── savedModels/           # Trained ML models
│   └── manage.py
├── Datasets/                  # Training and test datasets
├── requirements.txt           # Python dependencies
└── README.md
```

## 🎯 Key Features Explained

### 1. QR Code Generation
- Automatically generates QR codes for each prediction
- QR codes contain prediction result and metadata
- Scan with any QR code reader app to view results on mobile

### 2. PDF Report Generation
- Professional PDF reports with prediction details
- Includes all input parameters and results
- Styled with company branding and colors

### 3. Excel Export
- Export prediction data to Excel format
- Includes all fields and results
- Color-coded results for easy identification

### 4. Analytics Dashboard
- Real-time statistics and metrics
- Visual charts showing prediction trends
- Income analysis and success rates
- Recent predictions table

### 5. Prediction History
- Complete history of all user predictions
- Pagination for large datasets
- Search and filter capabilities
- Download options for each prediction

### 6. API Endpoints
- RESTful API for programmatic access
- JSON responses for easy integration
- Authentication required for API access

## 🔐 Security Features

- User authentication and authorization
- CSRF protection
- Input validation and sanitization
- Secure file uploads
- Database query protection

## 📊 Machine Learning Model

- **Algorithm**: Random Forest Classifier
- **Features**: 10 input parameters (marital status, income, age, etc.)
- **Training Data**: Comprehensive loan dataset
- **Accuracy**: High prediction accuracy with balanced dataset
- **Preprocessing**: Label encoding for categorical variables

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface
- **Responsive Layout**: Works on all device sizes
- **Interactive Elements**: Hover effects and animations
- **Color-coded Results**: Green for eligible, red for not eligible
- **Progress Indicators**: Loading states and feedback
- **Form Validation**: Real-time validation with helpful messages

## 📱 Mobile Features

- **QR Code Scanning**: View results on mobile devices
- **Touch-friendly Interface**: Optimized for touch interactions
- **Responsive Design**: Adapts to different screen sizes
- **Fast Loading**: Optimized for mobile networks

## 🔧 API Documentation

### Prediction Endpoint
```
POST /api/predict/
Content-Type: application/json

{
    "marital": "single",
    "house_O": "owned",
    "car_O": "yes",
    "profession": "Software_Developer",
    "city": "Mumbai",
    "state": "Maharashtra",
    "current_jy": 5,
    "current_hy": 3,
    "income": 800000,
    "age": 28
}
```

### Response
```json
{
    "success": true,
    "result": "eligible",
    "prediction_id": "uuid-string",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🚀 Deployment

### Local Development
```bash
python manage.py runserver
```

### Production Deployment
1. Set `DEBUG = False` in settings.py
2. Configure production database
3. Set up static file serving
4. Use production web server (Gunicorn, uWSGI)
5. Configure reverse proxy (Nginx)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django framework and community
- Scikit-learn for machine learning capabilities
- Tailwind CSS for modern styling
- All contributors and users

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Note**: This is an enhanced version of the original loan eligibility prediction system with additional features for better user experience and functionality.
