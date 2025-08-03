# your imports go here
from car_retailer import CarRetailer
import random
import time
import string
from car import Car


def main_menu():
    print("Main Menu:")
    print("1. Look for the nearest car retailer")
    print("2. Get car purchase advice")
    print("3. Place a car order")
    print("4. Exit")


def generate_test_data():
    car_retailers = []

    for _ in range(3):  # Create 3 retailer objects
        retailer_id = str(random.randint(10000000, 99999999))
        characters = string.ascii_letters + " "
        retailer_name = ''.join(random.choice(characters) for _ in range(8))
        # Define lists of possible street names and suburbs
        street_names = ["Clayton Rd", "Main St", "Oak St", "Maple Ave", "Elm St"]
        suburbs = ["Clayton", "Mount Waverley", "Glen Waverley", "Mulgrave", "Notting Hill"]
        states = ["VIC", "NSW", "QLD"]

        # Randomly choose a street name, suburb, and state
        street_name = random.choice(street_names)
        suburb = random.choice(suburbs)
        address = street_name + " " + suburb
        state = random.choice(states)

        # Generate a random 4-digit postcode within the range 3000-3999 for VIC, 2000-2999 for NSW, or 4000-4999 for QLD
        if state == "VIC":
            postcode = random.randint(3000, 3999)
        elif state == "NSW":
            postcode = random.randint(2000, 2999)
        else:  # QLD
            postcode = random.randint(4000, 4999)
        carretailer_address = address + ", " + state + " " + str(postcode)
        carretailer_business_hours = (round(random.uniform(6.0, 9.0), 1), round(random.uniform(17.0, 23.0), 1))
        carretailer_stock = []
        retailer = CarRetailer(int(retailer_id), retailer_name, carretailer_address, carretailer_business_hours,
                               carretailer_stock)

        for _ in range(4):  # Create 4 car objects for each retailer
            # Generate random car data
            car_code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890", k=8))
            car_name = ''.join(random.choice(characters) for _ in range(17))
            car_capacity = random.randint(2, 10)
            car_horsepower = random.randint(100, 300)
            car_weight = random.randint(1000, 3000)
            car_type = random.choice(["AWD", "RWD", "FWD"])
            car = Car(car_code, car_name, car_capacity, car_horsepower, car_weight, car_type)
            car_data = (f"{car.car_code}, {car.car_name}, {car.car_capacity}, {car.car_horsepower},"
                        f" {car.car_weight}, {car.car_type}")
            retailer.carretailer_stock.append(car_data)

        car_retailers.append(retailer)

    # Shuffle the order of car retailers for randomness
    random.shuffle(car_retailers)

    # Clear the existing data in "stock.txt" by writing an empty string
    with open("data/stock.txt", "w") as file:
        file.write("")

    # Write the new data to "stock.txt"
    with open("data/stock.txt", "a") as file:
        for retailer in car_retailers:
            retailer_data = (f"{retailer.retailer_id}, {retailer.retailer_name}, {retailer.carretailer_address}, "
                             f"{retailer.carretailer_business_hours}, {retailer.carretailer_stock}")
            file.write(retailer_data + "\n")


def main():
    # Generate and load test data
    generate_test_data()
    # Create a list to store existing retailer objects
    retailer_objects = []

    # Load existing data from "stock.txt" and create retailer objects
    stock_data = CarRetailer.extract_data_from_stock_file()

    for retailer_id, retailer_name, carretailer_address, start_hour, end_hour, carretailer_stock in stock_data:
        # Create CarRetailer object with a default retailer ID
        retailer = CarRetailer(int(retailer_id), retailer_name, carretailer_address,
                               (float(start_hour), float(end_hour)),
                               carretailer_stock)

        # Generate a unique retailer ID for the retailer object
        retailer.generate_retailer_id(retailer_objects)

        # Append the retailer object to the list
        retailer_objects.append(retailer)
    while True:
        main_menu()  # Display the main menu
        choice = input("Enter your choice: ")

        if choice == "1":  # 1. Look for the nearest car retailer
            user_postcode = int(input("Enter your postcode: "))
            if user_postcode is not None:
                # Find the closest retailer
                closest_retailer = None
                min_distance = float('inf')

                for retailer in retailer_objects:
                    distance = retailer.get_postcode_distance(user_postcode)

                    if distance < min_distance:
                        min_distance = distance
                        closest_retailer = retailer

                if closest_retailer:
                    print(f"The nearest car retailer is {closest_retailer.retailer_name}.")
                else:
                    print("No car retailers found.")
            else:
                print("Invalid input. Please enter a valid integer for the postcode.")
        elif choice == "2":
            # Functionality for getting car purchase advice
            print("Available car retailers:")

            for retailer in retailer_objects:
                print(f"Retailer Name: {retailer.retailer_name}")
                print(f"Retailer ID: {retailer.retailer_id}")
                print(f"Address: {retailer.carretailer_address}")
                print(f"Business Hours: {retailer.carretailer_business_hours}")

            selected_retailer_id = input("Select a retailer by entering its ID: ")

            # Find the selected retailer directly by iterating through the list
            selected_retailer = None
            for retailer in retailer_objects:
                if retailer.retailer_id == selected_retailer_id:
                    selected_retailer = retailer
                    break

            if selected_retailer:
                print(f"Retailer Name: {selected_retailer.retailer_name}")
                print(f"Retailer ID: {selected_retailer.retailer_id}")

                print("----------------------------------------------------------------------------")
                print("Sub-menu Options:")
                print("i) Recommend a car")
                print("ii) Get all cars in stock")
                print("iii) Get cars in stock by car types")
                print("iv) Get probationary licence permitted cars in stock")

                sub_choice = input("Select a sub-menu option (i/ii/iii/iv): ")

                if sub_choice == 'i':
                    # Recommend a random car from the selected retailer's stock
                    recommended_car = selected_retailer.car_recommendation()
                    print(f"Recommended Car: {recommended_car}")

                elif sub_choice == 'ii':
                    # Get all cars in stock at the selected retailer
                    all_stock = selected_retailer.get_all_stock()
                    print("All Cars in Stock:")
                    for car in all_stock:
                        print(car)

                elif sub_choice == 'iii':
                    # Get cars in stock by car types
                    car_types = input("Enter car types separated by commas (e.g., AWD, RWD): ").split(', ')
                    matching_cars = selected_retailer.get_stock_by_car_type(car_types)
                    print(f"Cars in Stock by Car Types {car_types}:")
                    for car in matching_cars:
                        print(car)

                elif sub_choice == 'iv':
                    # Get user input for licence_type
                    licence_type = input("Enter licence type (L, P, or Full): ")
                    # Check if the input is valid before calling the function
                    if licence_type in ["L", "P", "Full"]:
                        probationary_cars = selected_retailer.get_stock_by_licence_type(licence_type)
                        print("Probationary Licence Permitted Cars in Stock:")
                        for car in probationary_cars:
                            print(car)
                    else:
                        print("Invalid licence type. Please enter L, P, or Full.")

                else:
                    print("Invalid sub-menu choice.")

        elif choice == "3":
            try:
                # Prompt the user to enter the retailer ID and car ID separated by a space
                retailer_id, car_id = input("Enter the retailer ID and car ID (e.g., 88727858 TOY123456): ").split()

                selected_retailer = None
                for retailer in retailer_objects:
                    if retailer.retailer_id == retailer_id:
                        selected_retailer = retailer
                        break

                if selected_retailer is None:
                    print("Invalid retailer ID. Please enter a valid retailer ID.")
                else:

                    # Get the current time in seconds since the epoch
                    current_time = time.localtime()

                    # Extract the current hour from the time struct
                    cur_hour = current_time.tm_hour
                    # Check if the retailer is currently operating
                    if selected_retailer.is_operating(cur_hour):
                        # Create an order and store it in "order.txt"
                        order = selected_retailer.create_order(car_id)
                        print("Order Placed Successfully!")
                        print(order)

                        # Append the order details to "order.txt"
                        with open("data/order.txt", "a") as order_file:
                            order_file.write(str(order) + "\n")
                    else:
                        print("The retailer is currently closed. Please place your order during business hours.")
            except ValueError:
                print("Invalid input format. Please enter the retailer ID and car ID separated by a space.")

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
