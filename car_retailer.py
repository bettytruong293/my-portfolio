from retailer import Retailer
from car import Car
from order import Order
import random
import re
import time


class CarRetailer(Retailer):
    def __init__(self, retailer_id=None, retailer_name=None, carretailer_address=None,
                 carretailer_business_hours=(6.0, 23.0), carretailer_stock=None):
        super().__init__(retailer_id, retailer_name)
        if carretailer_stock is None:
            self.carretailer_stock = []
        self.carretailer_address = carretailer_address
        self.carretailer_stock = carretailer_stock
        self.carretailer_business_hours = carretailer_business_hours

        # Validate retailer_id
        if retailer_id is not None:
            if not isinstance(retailer_id, int) or not (10000000 <= retailer_id <= 99999999):
                raise ValueError("Retailer ID must be an 8-digit integer.")

        # Validate retailer_name
        if retailer_name is not None:
            if not all(char.isalpha() or char.isspace() for char in retailer_name):
                raise ValueError("Retailer name can only consist of letters and whitespace.")

        # Validate carretailer_address
        if carretailer_address is not None:
            address_parts = carretailer_address.split(', ')
            if len(address_parts) != 2:
                raise ValueError(
                    "Invalid address format. The address should be in the format 'Street Address, State Postcode'.")

        # Validate carretailer_business_hours
        if carretailer_business_hours is not None:
            (start_hour, end_hour) = carretailer_business_hours
            if not (6.0 <= start_hour <= 23.0) or not (6.0 <= end_hour <= 23.0) or start_hour > end_hour:
                raise ValueError(
                    "Invalid business hours format. Business hours should be within the range of 6:00AM to 11:00PM "
                    "(inclusive).")

    def extract_data_from_stock_file(path='data/stock.txt'):
        try:
            with open("data/stock.txt", "r") as file:
                lines = file.read()

            pattern = r"(\d+),\s(.*?),\s(.*?),\s\((.*?),\s(.*?)\),\s\[(.*?)\]"
            matches = re.findall(pattern, lines)
            return matches

        except FileNotFoundError:
            print(f"{path} file not found.")
        except Exception as e:
            print(f"Error reading {path}: {e}")

    def __str__(self):
        formatted_str = (f"{self.retailer_id}, {self.retailer_name}, {self.carretailer_address}, "
                         f"{self.carretailer_business_hours}, {self.carretailer_stock}']\n")
        return formatted_str

    def load_current_stock(self, path='data/stock.txt'):
        with open(path, "r") as file:
            lines = file.read()

        pattern = r"(\d+),\s(.*?),\s(.*?),\s\((.*?),\s(.*?)\),\s\[(.*?)\]"
        matches = re.findall(pattern, lines)
        for match in matches:
            retailer_id, retailer_name, carretailer_address, start_hour, end_hour, stock_data = match
            carretailer_stock = []
            car_details = re.findall(r"'(.*?)'", stock_data)
            for car_detail in car_details:
                car_data = car_detail.split(', ')
                #          # Check if there are enough elements in car_data
                if len(car_data) != 6:
                    continue  # Skip this car data if it doesn't have all expected values
                car_code, car_name, car_capacity, car_horsepower, car_weight, car_type = car_data
                # Create a Car object and store it in the dictionary
                car = Car(car_code, car_name, int(car_capacity), int(car_horsepower), int(car_weight), car_type)
                carretailer_stock.append(car.car_code)
                return carretailer_stock

    def is_operating(self, cur_hour):
        start_hour, end_hour = self.carretailer_business_hours
        return start_hour <= cur_hour <= end_hour

    def get_all_stock(self):
        try:
            # Extract stock data from the stock.txt file
            matches = self.extract_data_from_stock_file()

            # Initialize a list to store the Car objects
            car_objects = []

            # Process the stock data to create Car objects
            for match in matches:
                retailer_id, retailer_name, carretailer_address, start_hour, end_hour, stock_data = match
                if retailer_id != self.retailer_id:
                    car_details = re.findall(r"'(.*?)'", stock_data)
                    for car_detail in car_details:
                        car_data = car_detail.split(', ')
                    #          # Check if there are enough elements in car_data
                        if len(car_data) != 6:
                            continue  # Skip this car data if it doesn't have all expected values
                        car_code, car_name, car_capacity, car_horsepower, car_weight, car_type = car_data
                    # Create a Car object and store it in the dictionary
                        car = Car(car_code, car_name, int(car_capacity), int(car_horsepower), int(car_weight), car_type)
                        car_objects.append(car)

                return car_objects

        except FileNotFoundError:
            print("stock.txt file not found.")
            return []
        except Exception as e:
            print(f"Error reading stock.txt: {e}")
            return []

    def get_postcode_distance(self, postcode):
        matches = self.extract_data_from_stock_file()
        for match in matches:
            retailer_id, retailer_name, carretailer_address, start_hour, end_hour, carretailer_stock = match
            retailer = CarRetailer(int(retailer_id), retailer_name, carretailer_address,
                                   (float(start_hour), float(end_hour)), carretailer_stock)
        # Ensure carretailer_address is not None
            if not retailer.carretailer_address:
                raise ValueError("Car retailer address is not set.")

        # Extract the postcode from the carretailer_address
            address_parts = retailer.carretailer_address.split(', ')
            if len(address_parts) != 2:
                raise ValueError(
                    "Invalid carretailer_address format. The address should be in the format 'Street Address,"
                    " State Postcode'.")

            postcode_parts = address_parts[1].split(' ')
            if len(postcode_parts) != 2:
                raise ValueError("Invalid postcode format in carretailer_address.")

            carretailer_postcode = int(postcode_parts[1])

            # Calculate and return the absolute difference
            return abs(postcode - carretailer_postcode)

    def remove_from_stock(self, car_code):
        try:
            matches = self.extract_data_from_stock_file()

            # Initialize variables to track if the car was found and to store updated stock data
            car_removed = False
            updated_stock = []

            for match in matches:
                retailer_id, retailer_name, carretailer_address, start_hour, end_hour, stock_data = match

                # Create a CarRetailer object to parse the stock data
                retailer = CarRetailer(int(retailer_id), retailer_name, carretailer_address,
                                       (float(start_hour), float(end_hour)), stock_data)

                # Initialize carretailer_stock
                carretailer_stock = []

                # Initialize flag to indicate whether the car was removed for this retailer
                car_removed_for_retailer = False

                # Process car data for this retailer
                car_objects = re.findall(r"'(.*?)'", stock_data)
                for car_detail in car_objects:
                    car_data = car_detail.split(', ')

                    # Check if there are enough elements in car_data
                    if len(car_data) != 6:
                        continue  # Skip this car data if it doesn't have all expected values

                    car_code, car_name, car_capacity, car_horsepower, car_weight, car_type = car_data

                    # Check if this is the retailer's data
                    if retailer_id == retailer.retailer_id:
                        if car_data[0] == car_code:
                            car_removed_for_retailer = True
                    else:
                        # For other retailers, add their car data to carretailer_stock
                        carretailer_stock.append(car_detail)

                if car_removed_for_retailer:
                    car_removed = True
                else:
                    # If the car was not removed for this retailer, update the stock data for this retailer
                    updated_stock.append(
                        f"{retailer.retailer_id}, {retailer.retailer_name}, {retailer.carretailer_address}, "
                        f"({retailer.carretailer_business_hours[0]}, {retailer.carretailer_business_hours[1]}), "
                        f"'{', '.join(carretailer_stock)}'"
                    )

            if car_removed:
                # Update the stock.txt file with the modified stock data
                with open('data/stock.txt', 'w') as file:
                    for stock_entry in updated_stock:
                        file.write(f"{stock_entry}\n")

                print(f"Car with code '{car_code}' has been successfully removed from stock.")
                return True
            else:
                print(f"Car with code '{car_code}' was not found in stock or removal was unsuccessful.")
                return False

        except FileNotFoundError:
            print("stock.txt file not found.")
            return False
        except Exception as e:
            print(f"Error removing car from stock: {e}")
            return False

    def add_to_stock(self, car):
        if car.car_code in self.carretailer_stock:
            print('This car already exists in the current stock')
            return False
        else:
            # Add the car code to the carretailer_stock list
            self.carretailer_stock.append(car.car_code)
            car_data = Car.__str__(car)
            # Open the stock.txt file in append mode and write the car data
            with open('data/stock.txt', 'a') as file:
                file.write(car_data + '\n')
            return True  # Addition successful

    def get_stock_by_car_type(self, car_types):
        cars_match = []

        try:
            # Extract stock data from the stock.txt file
            matches = self.extract_data_from_stock_file()

            # Process the stock data and filter cars by car type
            for match in matches:
                retailer_id, retailer_name, carretailer_address, start_hour, end_hour, stock_data = match
                car_details = re.findall(r"'(.*?)'", stock_data)
                for car_detail in car_details:
                    car_data = car_detail.split(', ')
                    #          # Check if there are enough elements in car_data
                    if len(car_data) != 6:
                        continue  # Skip this car data if it doesn't have all expected values
                    car_code, car_name, car_capacity, car_horsepower, car_weight, car_type = car_data
                    # Create a Car object and store it in the dictionary
                    car = Car(car_code, car_name, int(car_capacity), int(car_horsepower), int(car_weight), car_type)
                    if car.car_type in car_types:
                        cars_match.append(car)

        except FileNotFoundError:
            print("stock.txt file not found.")

        return cars_match

    def get_stock_by_licence_type(self, licence_type):
        # Initialize an empty list to store matching Car objects
        matching_cars = []

        # Define the Power to Mass ratio threshold for prohibited vehicles
        power_to_mass_threshold = 130

        # Extract stock data from the stock.txt file
        matches = self.extract_data_from_stock_file()

        # Process the stock data and filter cars by licence type
        for match in matches:
            retailer_id, retailer_name, carretailer_address, start_hour, end_hour, stock_data = match
            car_details = re.findall(r"'(.*?)'", stock_data)
            for car_detail in car_details:
                car_data = car_detail.split(', ')
                #          # Check if there are enough elements in car_data
                if len(car_data) != 6:
                    continue  # Skip this car data if it doesn't have all expected values
                car_code, car_name, car_capacity, car_horsepower, car_weight, car_type = car_data
                # Create a Car object and store it in the dictionary
                car = Car(car_code, car_name, float(car_capacity), float(car_horsepower), int(car_weight), car_type)
                # Calculate the Power to Mass ratio
                try:
                    power_to_mass_ratio = round((car.car_horsepower / car.car_weight) * 1000, 3)

                    # Check if the car is not a prohibited vehicle based on licence type
                    if (licence_type == "L" and power_to_mass_ratio <= power_to_mass_threshold) or \
                            (licence_type == "P" and power_to_mass_ratio <= power_to_mass_threshold) or \
                            (licence_type == "Full"):
                        car = Car(car_code, car_name, None, car_horsepower, car_weight, car_type)
                        matching_cars.append(car)
                except ValueError:
                    # Handle invalid horsepower or weight values
                    pass

            return matching_cars

    def car_recommendation(self):
        # Create a dictionary to store car objects by car code
        matches = self.extract_data_from_stock_file()
        for match in matches:
            retailer_id, retailer_name, carretailer_address, start_hour, end_hour, stock_data = match
            car_dict = {}
            carretailer_stock = []
            car_details = re.findall(r"'(.*?)'", stock_data)
            for car_detail in car_details:
                car_data = car_detail.split(', ')
                #          # Check if there are enough elements in car_data
                if len(car_data) != 6:
                    continue  # Skip this car data if it doesn't have all expected values
                car_code, car_name, car_capacity, car_horsepower, car_weight, car_type = car_data
                # Create a Car object and store it in the dictionary
                car = Car(car_code, car_name, int(car_capacity), int(car_horsepower), int(car_weight), car_type)
                carretailer_stock.append(car_code)
                CarRetailer(int(retailer_id), retailer_name, carretailer_address, (float(start_hour), float(end_hour)),
                            carretailer_stock)
                car_dict[car_code] = car

            # Select a random car code
            random_car_code = random.choice(carretailer_stock)
            #     # Get the corresponding Car object from the dictionary
            selected_car = car_dict.get(random_car_code)
            return selected_car

    def create_order(self, car_code):
        current_time = int(time.time())  # Get the current UNIX timestamp
        car_to_order = None
        car_objects = self.get_all_stock()
        # Find the car in the retailer's stock based on car_code
        for car in car_objects:
            if car_code == car.car_code:
                self.remove_from_stock(car.car_code)
                car_to_order = car

        if car_to_order:
            # Generate a unique order_id as specified
            order_id = Order.generate_order_id(car_to_order.car_code)

            # Create an Order object
            order = Order(
                order_id,
                car_to_order,
                self,
                current_time
            )

            # Append the order to "order.txt"
            with open("order.txt", "a") as order_file:
                order_file.write(f"{order_id}, {car_to_order.car_code}, {self.retailer_id}, {current_time}")

            # Update the "stock.txt" file with the modified stock
            with open("stock.txt", "w") as stock_file:
                stock_file.write(f"{self.retailer_id}, {self.retailer_name}, {self.carretailer_address}, "
                                 f"{self.carretailer_business_hours}, {self.carretailer_stock}\n")

            return order
        else:
            return None
