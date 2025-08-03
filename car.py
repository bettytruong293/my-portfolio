class Car:
    def __init__(self, car_code, car_name, car_capacity, car_horsepower, car_weight, car_type):
        self.car_code = car_code
        self.car_name = car_name
        self.car_capacity = car_capacity
        self.car_horsepower = car_horsepower
        self.car_weight = car_weight
        self.car_type = car_type

    def __str__(self):
        formatted_str = (f"{self.car_code},{self.car_name},{self.car_capacity},{self.car_horsepower},"
                         f"{self.car_weight},{self.car_type}")
        return formatted_str

    def probationary_licence_prohibited_vehicle(self):
        power_to_mass_ratio = round((self.car_horsepower/self.car_weight)*1000, 3)
        if power_to_mass_ratio > 130:
            return True
        else:
            return False

    def found_matching_car(self, search_car_code):
        return search_car_code == self.car_code

    def get_car_type(self):
        return self.car_type
