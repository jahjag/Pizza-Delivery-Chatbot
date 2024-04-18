from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class Maps:
    def estimate_time(self, origin, destination):
        origin_coords = self.get_coordinates(origin)
        destination_coords = self.get_coordinates(destination)
        
        if origin_coords and destination_coords:
            distance = self.calculate_distance(origin_coords, destination_coords)
            
            if distance > 15:
                return "Warning: The distance is too long."
            else:
                average_speed = 20  # Average speed in km/h
                travel_time = self.calculate_time(distance, average_speed)
                i,d = self.extract_numbers_before_and_after_decimal(travel_time)
                # return f"We estimate delivery time of {travel_time:.2f} minutes."
                return f"We estimate delivery time of {i} minutes {d} seconds."
        else:
            return "Your location is not found. Specify the correct address."
        
    def extract_numbers_before_and_after_decimal(self,travel_time):
        # Convert the number to a string
        number_str = str(travel_time)

        # Split the string based on the decimal point
        parts = number_str.split('.')

        # Extract the number before the decimal point
        before_decimal = int(parts[0])

        # Extract the first two digits after the decimal point, if available
        after_decimal = int(parts[1][:2]) if len(parts) > 1 else 0

        return before_decimal, after_decimal

    def get_coordinates(self, address):
        geolocator = Nominatim(user_agent="your_app_name")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None

    def calculate_distance(self, origin_coords, destination_coords):
        return geodesic(origin_coords, destination_coords).kilometers

    def calculate_time(self, distance, average_speed):
        if distance > 0:
            time = (distance / average_speed) * 60  # Convert hours to minutes
            return time
        else:
            return 0
    
if __name__ == '__main__':
    o = Maps()
    ori = "Jntu, Hyderabad, India"
    dest = "Moosapet, Hyderabad, India"
    r = o.estimate_time(ori, dest)
    print(r)
