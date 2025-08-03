import random
import string
import time


class Order:
    def __init__(self, order_id=None, order_car=None, order_retailer=None, order_creation_time=None):
        self.order_id = order_id
        self.order_car = order_car
        self.order_retailer = order_retailer
        self.order_creation_time = order_creation_time if order_creation_time is not None else int(time.time())

    def __str__(self):
        return (f"{self.order_id}, {self.order_car.car_code}, {self.order_retailer.retailer_id}, "
                f"{self.order_creation_time}")

    def generate_order_id(car_code_input):
        # Ensure car_code is a string
        car_code = str(car_code_input)
        # Step 1: Generate a random string of 6 lowercase alphabetic characters
        random_chars = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))

        # Step 2: Convert every second character to uppercase
        random_chars = ''.join(c.upper() if i % 2 == 1 else c for i, c in enumerate(random_chars))

        # Step 3: Calculate ASCII codes and Step 4: Calculate the remainder
        str_1 = "~!@#$%^&*"
        processed_chars = [str_1[ord(c) ** 2 % len(str_1)] for c in random_chars]

        # Step 5 and Step 6: Append characters
        final_chars = ''
        for i, char in enumerate(processed_chars):
            final_chars += char * (i + 1)

        # Step 7: Append car_code and order creation time
        order_creation_time = str(int(time.time()))
        order_id = final_chars + car_code + order_creation_time

        return order_id
