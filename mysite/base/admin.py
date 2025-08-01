from django.contrib import admin
from .models import PredictionHistory

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'result', 'profession', 'income', 'age', 'timestamp')
    list_filter = ('result', 'profession', 'timestamp')
    search_fields = ('user__username', 'profession', 'city', 'state')
    readonly_fields = ('prediction_id', 'timestamp')
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'prediction_id')
        }),
        ('Personal Details', {
            'fields': ('marital_status', 'age', 'profession')
        }),
        ('Financial Information', {
            'fields': ('income', 'house_ownership', 'car_ownership')
        }),
        ('Location & Experience', {
            'fields': ('city', 'state', 'current_job_years', 'current_house_years')
        }),
        ('Result', {
            'fields': ('result', 'timestamp')
        }),
    )
 