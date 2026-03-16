"""
Management command to seed 50+ mock properties with varied characteristics
for testing filters. Uses reproducible random data (seed=42).
"""
import random
from decimal import Decimal

from django.core.management.base import BaseCommand

from properties.models import Feature, Property, PropertyType

CITIES = [
    'Springfield',
    'Riverside',
    'Lakeside',
    'Harbor City',
    'Mountain View',
    'Coastal Bay',
    'Downtown',
    'Westside',
]

REGIONS = ['Metro', 'Coastal', 'Suburban', 'Rural']

PROPERTY_TYPES = [
    ('House', 'house'),
    ('Apartment', 'apartment'),
    ('Land', 'land'),
    ('Condo', 'condo'),
    ('Villa', 'villa'),
    ('Studio', 'studio'),
]

CONDITIONS = ['new', 'renovated', 'good', 'needs_work']

FEATURE_SLUGS = [
    'pool',
    'garage',
    'garden',
    'balcony',
    'parking',
    'elevator',
    'security',
    'furnished',
    'air-conditioning',
    'heating',
    'laundry',
    'gym',
    'storage',
    'terrace',
    'view',
    'waterfront',
    'gated-community',
    'smart-home',
    'solar-panels',
]

TITLE_TEMPLATES = [
    'Spacious {type} in {city}',
    'Modern {bedrooms}-Bed {type} in {city}',
    'Luxury {type} #{idx} in {city}',
    'Charming {type} in {city}',
    'Contemporary {type} in {city}',
    'Cozy {type} in {city}',
    'Stunning {type} in {city}',
    'Elegant {type} in {city}',
    'Family {type} in {city}',
    'Renovated {type} in {city}',
]

ADDRESS_TEMPLATES = [
    '{num} Oak Street',
    '{num} Main Avenue',
    '{num} Elm Street',
    '{num} Maple Drive',
    '{num} Pine Lane',
    '{num} Cedar Road',
    '{num} Birch Boulevard',
    '{num} Willow Way',
]

DESCRIPTION_SNIPPETS = [
    'Beautiful property with plenty of natural light.',
    'Well-maintained and ready for move-in.',
    'Great location with easy access to amenities.',
    'Perfect for families or professionals.',
    'Recently updated with modern finishes.',
    'Spacious layout with open floor plan.',
    'Quiet neighborhood with excellent schools nearby.',
    'Close to shopping, dining, and entertainment.',
]


def ensure_property_types_and_features():
    """Ensure PropertyType and Feature records exist (from seed_data)."""
    for name, slug in PROPERTY_TYPES:
        PropertyType.objects.get_or_create(slug=slug, defaults={'name': name})

    feature_data = [
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
    for name, slug in feature_data:
        Feature.objects.get_or_create(slug=slug, defaults={'name': name})


def get_bedrooms_for_type(prop_type_slug: str, rng: random.Random) -> int:
    """Return bedrooms based on property type constraints."""
    if prop_type_slug == 'land':
        return 0
    if prop_type_slug == 'studio':
        return 1
    if prop_type_slug in ('apartment', 'condo'):
        return rng.randint(1, 4)
    if prop_type_slug in ('house', 'villa'):
        return rng.randint(2, 6)
    return rng.randint(1, 4)


def get_bathrooms(bedrooms: int, rng: random.Random) -> int:
    """Return bathrooms correlated with bedrooms."""
    if bedrooms == 0:
        return rng.choice([0, 1])
    return rng.randint(max(1, bedrooms - 1), min(5, bedrooms + 1))


def get_area_for_type(prop_type_slug: str, rng: random.Random) -> Decimal | None:
    """Return area_sqm based on property type."""
    if prop_type_slug == 'land':
        return rng.choice([None, Decimal(str(rng.randint(500, 2000)))])
    if prop_type_slug == 'studio':
        return Decimal(str(rng.randint(25, 55)))
    if prop_type_slug in ('apartment', 'condo'):
        return Decimal(str(rng.randint(55, 180)))
    if prop_type_slug in ('house', 'villa'):
        return Decimal(str(rng.randint(120, 600)))
    return Decimal(str(rng.randint(50, 300)))


def get_lot_for_type(prop_type_slug: str, rng: random.Random) -> Decimal | None:
    """Return lot_sqm for types that typically have lots."""
    if prop_type_slug in ('house', 'villa', 'land'):
        return Decimal(str(rng.randint(200, 1500)))
    return None


def generate_property(idx: int, rng: random.Random) -> Property:
    """Generate a single property with varied characteristics."""
    listing_type = rng.choice(['sale', 'rent'])
    type_name, type_slug = rng.choice(PROPERTY_TYPES)
    property_type = PropertyType.objects.get(slug=type_slug)

    bedrooms = get_bedrooms_for_type(type_slug, rng)
    bathrooms = get_bathrooms(bedrooms, rng)
    area_sqm = get_area_for_type(type_slug, rng)
    lot_sqm = get_lot_for_type(type_slug, rng)

    if listing_type == 'sale':
        price = Decimal(str(rng.randint(80000, 2500000)))
    else:
        price = Decimal(str(rng.randint(600, 8000)))

    city = rng.choice(CITIES)
    region = rng.choice(REGIONS)

    templates = [t for t in TITLE_TEMPLATES if '{bedrooms}' not in t or bedrooms > 0]
    title_template = rng.choice(templates or TITLE_TEMPLATES)
    title = title_template.format(
        type=type_name,
        city=city,
        bedrooms=bedrooms,
        idx=idx,
    )

    address = rng.choice(ADDRESS_TEMPLATES).format(num=rng.randint(1, 9999))
    description = rng.choice(DESCRIPTION_SNIPPETS)

    pet_friendly = rng.random() < 0.4
    furnished = rng.random() < (0.4 if listing_type == 'rent' else 0.2)
    condition = rng.choice(CONDITIONS)
    parking_spaces = rng.randint(0, 4)
    year_built = rng.randint(1950, 2024) if rng.random() > 0.1 else None

    prop = Property.objects.create(
        title=title,
        description=description,
        price=price,
        listing_type=listing_type,
        property_type=property_type,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        area_sqm=area_sqm,
        lot_sqm=lot_sqm,
        parking_spaces=parking_spaces,
        year_built=year_built,
        condition=condition,
        pet_friendly=pet_friendly,
        furnished=furnished,
        address=address,
        city=city,
        region=region,
        country='USA',
        status='published',
    )

    num_features = rng.randint(0, 5)
    if num_features > 0:
        feature_slugs = rng.sample(FEATURE_SLUGS, min(num_features, len(FEATURE_SLUGS)))
        for slug in feature_slugs:
            f = Feature.objects.get(slug=slug)
            prop.features.add(f)

    return prop


class Command(BaseCommand):
    help = 'Seed 50+ mock properties with varied characteristics for filter testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=55,
            help='Number of properties to create (default: 55)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing properties before seeding',
        )

    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']

        if clear:
            deleted, _ = Property.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing properties.'))

        ensure_property_types_and_features()

        rng = random.Random(42)

        created = 0
        for i in range(count):
            prop = generate_property(i + 1, rng)
            created += 1
            self.stdout.write(self.style.SUCCESS(f'Created: {prop.title}'))

        self.stdout.write(self.style.SUCCESS(f'Created {created} mock properties.'))
