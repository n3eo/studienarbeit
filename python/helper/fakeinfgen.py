from faker import Faker

class fakeInfos():
    def __init__(self):
        # Initialise faker
        self.fake = Faker()

    def get_person_info(self):
        return fake.first_name(), fake.last_name(), fake.email(), fake.date_of_birth()

    def get_ausleiher_info(self):
        return fake.street_address(), fake.postalcode(), fake.city(), fake.phone_number()

    def get_verlag_info(self):
        return fake.company(), fake.postalcode(), fake.street_address(), fake.email(), fake.catch_phrase()

    def get_isbn(self):
        return fake.isbn13().replace("-", "")

    def get_description(self):
        return fake.catch_phrase()

    def get_domain(self):
        return fake.tld()
