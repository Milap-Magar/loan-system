from django.db import models
from django.contrib.auth.models import User

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction_id = models.CharField(max_length=36, unique=True)
    marital_status = models.CharField(max_length=20)
    house_ownership = models.CharField(max_length=20)
    car_ownership = models.CharField(max_length=10)
    profession = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    current_job_years = models.IntegerField()
    current_house_years = models.IntegerField()
    income = models.IntegerField()
    age = models.IntegerField()
    result = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = "Prediction Histories"
    
    def __str__(self):
        return f"{self.user.username} - {self.result} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    def get_income_category(self):
        """Get income category based on income value"""
        if self.income <= 375000:
            return "Low Income"
        elif self.income <= 750000:
            return "Medium Income"
        elif self.income <= 2250000:
            return "High Income"
        else:
            return "Very High Income"
    
    def get_age_category(self):
        """Get age category based on age value"""
        if self.age <= 32:
            return "Young Adult"
        elif self.age <= 44:
            return "Adult"
        elif self.age <= 56:
            return "Middle-aged"
        elif self.age <= 68:
            return "Senior"
        else:
            return "Elderly" 