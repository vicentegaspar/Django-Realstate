from django.core.management.base import BaseCommand
from properties.models import PropertyType, Feature


class Command(BaseCommand):
    help = 'Seed PropertyType and Feature data'

    def handle(self, *args, **options):
        property_types = [
            ('House', 'house'),
            ('Apartment', 'apartment'),
            ('Land', 'land'),
            ('Condo', 'condo'),
            ('Villa', 'villa'),
            ('Studio', 'studio'),
        ]
        for name, slug in property_types:
            PropertyType.objects.get_or_create(slug=slug, defaults={'name': name})

        features = [
            ('Pool', 'pool'),
            ('Garage', 'garage'),
            ('Garden', 'garden'),
            ('Balcony', 'balcony'),
            ('Parking', 'parking'),
            ('Elevator', 'elevator'),
            ('Security', 'security'),
            ('Furnished', 'furnished'),
            ('Air Conditioning', 'air-conditioning'),
            ('Heating', 'heating'),
            ('Laundry', 'laundry'),
            ('Gym', 'gym'),
            ('Storage', 'storage'),
            ('Terrace', 'terrace'),
            ('View', 'view'),
            ('Waterfront', 'waterfront'),
            ('Gated Community', 'gated-community'),
            ('Smart Home', 'smart-home'),
            ('Solar Panels', 'solar-panels'),
        ]
        for name, slug in features:
            Feature.objects.get_or_create(slug=slug, defaults={'name': name})

        self.stdout.write(self.style.SUCCESS('Seeded PropertyType and Feature data'))
