from django.core.management.base import BaseCommand
from properties.models import Property, PropertyType, Feature


SAMPLE_PROPERTIES = [
    {
        'title': 'Modern Family Home with Pool',
        'description': 'A beautiful 4-bedroom family home with a private pool and spacious garden.',
        'price': 450000,
        'listing_type': 'sale',
        'type_slug': 'house',
        'bedrooms': 4,
        'bathrooms': 3,
        'area_sqm': 220,
        'lot_sqm': 500,
        'parking_spaces': 2,
        'year_built': 2015,
        'condition': 'good',
        'pet_friendly': True,
        'furnished': False,
        'address': '123 Oak Street',
        'city': 'Springfield',
        'region': 'Metro',
        'country': 'USA',
        'feature_slugs': ['pool', 'garage', 'garden'],
    },
    {
        'title': 'Downtown Apartment',
        'description': 'Stylish 2-bedroom apartment in the heart of the city.',
        'price': 1800,
        'listing_type': 'rent',
        'type_slug': 'apartment',
        'bedrooms': 2,
        'bathrooms': 2,
        'area_sqm': 95,
        'parking_spaces': 1,
        'year_built': 2020,
        'condition': 'new',
        'pet_friendly': False,
        'furnished': True,
        'address': '456 Main Ave',
        'city': 'Springfield',
        'region': 'Metro',
        'country': 'USA',
        'feature_slugs': ['elevator', 'parking', 'air-conditioning'],
    },
    {
        'title': 'Cozy Studio',
        'description': 'Compact studio perfect for students or young professionals.',
        'price': 950,
        'listing_type': 'rent',
        'type_slug': 'studio',
        'bedrooms': 1,
        'bathrooms': 1,
        'area_sqm': 45,
        'condition': 'renovated',
        'pet_friendly': True,
        'furnished': True,
        'address': '789 Elm St',
        'city': 'Springfield',
        'region': 'Metro',
        'country': 'USA',
        'feature_slugs': ['furnished', 'laundry'],
    },
]


class Command(BaseCommand):
    help = 'Create sample published properties for testing'

    def handle(self, *args, **options):
        created = 0
        for data in SAMPLE_PROPERTIES:
            feature_slugs = data.pop('feature_slugs', [])
            type_slug = data.pop('type_slug')
            pt, _ = PropertyType.objects.get_or_create(slug=type_slug, defaults={'name': type_slug.title()})
            data['property_type'] = pt
            data['status'] = 'published'

            prop, is_new = Property.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if is_new:
                for slug in feature_slugs:
                    f, _ = Feature.objects.get_or_create(slug=slug, defaults={'name': slug.title()})
                    prop.features.add(f)
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {prop.title}'))

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created {created} sample properties.'))
        else:
            self.stdout.write('Sample properties already exist.')
