from django.db import models

class Apartment(models.Model):
    apartment_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    price_range = models.CharField(max_length=255, null=True, blank=True)
    bedroom_types = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    map_image_url = models.URLField(max_length=500, null=True, blank=True)
    overall_satisfaction = models.FloatField(null=True, blank=True)  # Optional field for satisfaction (e.g., 1-5 scale)
    review_summary = models.TextField(null=True, blank=True)  # Optional field for review summaries
    
    def __str__(self):
        return self.apartment_name
    
class Crime(models.Model):
    crime_name = models.CharField(max_length=255)  # Name of the crime
    latitude = models.FloatField()  # Latitude of the crime location
    longitude = models.FloatField()  # Longitude of the crime location
    relevant_to_party_map = models.BooleanField(default=False)  # Relevance to party map

    def __str__(self):
        return self.crime_name