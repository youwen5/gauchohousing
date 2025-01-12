import csv
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import Apartment, Crime
import googlemaps
import os
from decouple import config
from django.core.exceptions import ObjectDoesNotExist

API_KEY = config("MAPS_API_KEY")

def get_lat_long(address):
    # Replace with your Google Maps API Key
    gmaps = googlemaps.Client(key=API_KEY)
    
    # Perform Geocoding
    try:
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
    except Exception as e:
        print(f"Error occurred during geocoding: {e}")
    
    return None, None  # Return None if no results or error

def get_general_coordinates(address):
    """
    Get general coordinates for a given address, even if the result is not precise.
    
    :param address: The address to geocode.
    :return: A tuple (latitude, longitude) or (None, None) if no result is found.
    """
    # Replace with your Google Maps API Key
    gmaps = googlemaps.Client(key=API_KEY)
    
    try:
        # Perform Geocoding
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            # Attempt to get the first result's location
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
    except Exception as e:
        print(f"Error occurred during general geocoding: {e}")
    
    # Fallback: Return a default location or None
    return None, None


def generate_street_view_image_url_for_apartments(request):
    # Replace with your Google Maps API Key
    gmaps = googlemaps.Client(key=API_KEY)
    
    try:
        # Fetch all apartments without a map_image_url
        apartments = Apartment.objects.filter(map_image_url__isnull=True)

        for apartment in apartments:
            # Search for the place using Google Maps API
            geocode_result = gmaps.geocode(apartment.address)

            if geocode_result:
                # Extract latitude and longitude from the geocode result
                location = geocode_result[0]['geometry']['location']
                apartment.latitude = location['lat']
                apartment.longitude = location['lng']

                # Generate a Google Street View Image API URL
                street_view_image_url = (
                    f"https://maps.googleapis.com/maps/api/streetview"
                    f"?size=600x300"  # Set the image dimensions
                    f"&location={location['lat']},{location['lng']}"  # Location coordinates
                    f"&fov=90"  # Field of view (10-120 degrees)
                    f"&heading=0"  # Heading (0 for North, 90 for East, etc.)
                    f"&pitch=0"  # Camera angle (0 for straight ahead, -90 for down, 90 for up)
                    f"&key={API_KEY}"  # Your API Key
                )

                # Update the database with the generated Street View URL
                apartment.map_image_url = street_view_image_url
                apartment.save()
            else:
                print(f"Could not fetch geocoding results for: {apartment.address}")

        # If successful, return a JSON success response
        return JsonResponse({'success': True})
    except Exception as e:
        # Handle any errors and return a failure response
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
def upload_csv_and_populate_from_file(request):
    # Path to the CSV file
    file_path = os.path.join(os.path.dirname(__file__), 'apartments.csv')

    # Check if the file exists
    if not os.path.exists(file_path):
        return JsonResponse({'error': 'CSV file not found'}, status=404)

    # Read and process the CSV file
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            apartment_name = row['apartment_name']
            phone_number = row['phone_number']
            price_range = row['price_range']
            bedroom_types = row['bedroom_types']
            address = row['address']

            # Get latitude and longitude from the address
            latitude, longitude = get_lat_long(address)

            # Only add the apartment if the geocoding returned valid coordinates
            if latitude is not None and longitude is not None:
                Apartment.objects.create(
                    apartment_name=apartment_name,
                    phone_number=phone_number,
                    price_range=price_range,
                    bedroom_types=bedroom_types,
                    address=address,
                    latitude=latitude,
                    longitude=longitude
                )
            else:
                print(f"Skipping apartment '{apartment_name}' due to invalid address: {address}")

    return JsonResponse({'message': 'Data imported successfully'})

def determine_relevance(crime_name):
    """
    Determine if the crime is relevant to a party map based on the crime name.

    :param crime_name: The name of the crime.
    :return: True if the crime is related to alcohol or noise ordinance, otherwise False.
    """
    relevant_keywords = ['alcohol', 'noise ordinance']
    return any(keyword in crime_name.lower() for keyword in relevant_keywords)

def upload_csv_and_populate_from_file_crimes(request):
    # Path to the CSV file
    file_path = os.path.join(os.path.dirname(__file__), 'crimedata.csv')

    # Check if the file exists
    if not os.path.exists(file_path):
        return JsonResponse({'error': 'CSV file not found'}, status=404)

    # Read and process the CSV file
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            general_location = row.get('General Location', '').strip()
            name_crime = row.get('Nature (Classification)', '').strip()

            if not general_location or not name_crime:
                print(f"Skipping row due to missing data: {row}")
                continue

            # Get latitude and longitude from the location
            latitude, longitude = get_general_coordinates(general_location)

            # Only add the crime if the geocoding returned valid coordinates
            if latitude is not None and longitude is not None:
                relevant_to_party_map = determine_relevance(name_crime)  # Optional logic to determine relevance
                Crime.objects.create(
                    crime_name=name_crime,
                    latitude=latitude,
                    longitude=longitude,
                    relevant_to_party_map=relevant_to_party_map
                )
            else:
                print(f"Skipping crime '{name_crime}' due to invalid location: {general_location}")

    return JsonResponse({'message': 'Crime data imported successfully'})

def clear_apartment_data(request):
    try:
        # Delete all entries in the model
        Apartment.objects.all().delete()
        return JsonResponse({'message': 'All entries in the Apartment model have been deleted successfully.'})
    except Exception as e:
        # Handle any errors during deletion
        return JsonResponse({'error': f'An error occurred while clearing data: {str(e)}'}, status=500)

def get_all_apartments(request):
    try:
        # Query all apartments
        apartments = Apartment.objects.all()

        # Serialize the data into a list of dictionaries
        apartments_data = [
            {
                "id": apartment.id,
                "apartment_name": apartment.apartment_name,
                "phone_number": apartment.phone_number,
                "price_range": apartment.price_range,
                "bedroom_types": apartment.bedroom_types,
                "address": apartment.address,
                "latitude": apartment.latitude,
                "longitude": apartment.longitude,
                "image_link": apartment.map_image_url,
            }
            for apartment in apartments
        ]

        return JsonResponse({"apartments": apartments_data}, safe=False)
    except Exception as e:
        # Handle any errors
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

def get_all_crimes(request):
    """
    Retrieve all crimes from the database and return them as a JSON response.
    """
    try:
        # Fetch all crime records
        crimes = Crime.objects.all()

        # Serialize the data
        crime_data = [
            {
                "id": crime.id,
                "crime_name": crime.crime_name,
                "latitude": crime.latitude,
                "longitude": crime.longitude,
                "relevant_to_party_map": crime.relevant_to_party_map
            }
            for crime in crimes
        ]

        # Return as JSON response
        return JsonResponse({"crimes": crime_data}, safe=False)
    except Exception as e:
        # Handle errors and return an appropriate response
        return JsonResponse({"error": str(e)}, status=500)
    
def wipe_all_crimes(request):
    """
    Wipe all data from the Crime model.
    """
    try:
        # Delete all records in the Crime model
        Crime.objects.all().delete()
        return JsonResponse({'message': 'All crimes have been deleted successfully.'})
    except Exception as e:
        return JsonResponse({'error': f'Error occurred while deleting crimes: {str(e)}'}, status=500)
    
def parse_and_update_apartments(request):
    """
    Parses a CSV file to update the Apartment model with overall satisfaction
    and review summary fields based on apartment_name.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current file's directory
    file_path = os.path.join(base_dir, 'opinions.csv')   # Construct the file path

    # Check if the file exists
    if not os.path.exists(file_path):
        return JsonResponse({'error': 'CSV file not found'}, status=404)
    
    try:
        updated_count = 0
        skipped_count = 0

        with open(file_path, mode='r', encoding='utf-8') as csv_file:  # Corrected syntax
            reader = csv.DictReader(csv_file)
            for row in reader:
                apartment_name = row.get('apartment_name')
                overall_opinion = row.get('overal_opinion')  # Corrected spelling
                quick_summary = row.get('quick_summarized_description')

                if not apartment_name:
                    skipped_count += 1
                    continue  # Skip rows without an apartment name

                # Get the first matching apartment
                apartment = Apartment.objects.filter(apartment_name=apartment_name).first()
                if apartment:
                    if overall_opinion:
                        apartment.overall_satisfaction = float(overall_opinion)
                    if quick_summary:
                        apartment.review_summary = quick_summary
                    apartment.save()
                    updated_count += 1
                else:
                    skipped_count += 1

        return JsonResponse({
            'success': True,
            'message': 'CSV processed successfully.',
            'updated_count': updated_count,
            'skipped_count': skipped_count
        })
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)