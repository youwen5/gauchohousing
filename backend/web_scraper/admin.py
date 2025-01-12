from django.contrib import admin
from .models import Apartment, Crime

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = (
        'apartment_name', 
        'phone_number', 
        'price_range', 
        'bedroom_types', 
        'address', 
        'overall_satisfaction', 
        'review_summary'
    )
    search_fields = ('apartment_name', 'address')
    list_filter = ('price_range', 'bedroom_types', 'overall_satisfaction')
    readonly_fields = ('review_summary',)  # Make review_summary read-only, if summaries are auto-generated

@admin.register(Crime)
class CrimeAdmin(admin.ModelAdmin):
    list_display = ('crime_name', 'latitude', 'longitude', 'relevant_to_party_map')
    list_filter = ('relevant_to_party_map',)
    search_fields = ('crime_name',)
    ordering = ('crime_name',)