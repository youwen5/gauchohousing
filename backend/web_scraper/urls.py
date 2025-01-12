from django.urls import path
from .views import upload_csv_and_populate_from_file, clear_apartment_data, get_all_apartments, generate_street_view_image_url_for_apartments, get_all_crimes, upload_csv_and_populate_from_file_crimes, wipe_all_crimes, parse_and_update_apartments

urlpatterns = [
    # Other URL patterns
    path('upload-csv/', upload_csv_and_populate_from_file, name='upload_csv'),
    path('clear/', clear_apartment_data, name='clear_apartment_data'), 
    path('get-all-apartments/', get_all_apartments, name='get_all_apartments'),
    path('generate-images-all-apartments/', generate_street_view_image_url_for_apartments, name='generate_all_apartments_images'),
    path('get-all-crime/', get_all_crimes, name='get_all_crimes'),
    path('generate-all-crimes/', upload_csv_and_populate_from_file_crimes, name='generate_all_crimes'),
    path('wipe-crimes/', wipe_all_crimes, name='wipe-crimes'),
    path('parse-and-update-apartments/', parse_and_update_apartments, name='parse_and_update_apartments'),
]
