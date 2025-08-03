import random


class Retailer:
    def __init__(self, retailer_id=None, retailer_name=None):
        self.retailer_id = retailer_id
        self.retailer_name = retailer_name

    def __str__(self):
        formatted_str = self.retailer_id + ',' + self.retailer_name
        return formatted_str

    def generate_retailer_id(self, list_retailer=None):
        if list_retailer is None:
            list_retailer = []
        while True:
            new_retailer_id = str(random.randint(10000000, 99999999))
            if new_retailer_id not in [retailer.retailer_id for retailer in list_retailer]:
                self.retailer_id = new_retailer_id
                break


