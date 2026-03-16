from ninja import Router, Schema
from ninja.pagination import paginate, PageNumberPagination
from typing import Optional, List
from django.shortcuts import get_object_or_404

from .models import Property, PropertyType, Feature, PropertyImage, PropertyInquiry

router = Router(tags=['properties'])


class PropertyImageSchema(Schema):
    id: int
    image: str
    caption: str
    order: int


class PropertyListSchema(Schema):
    id: int
    title: str
    price: str
    listing_type: str
    property_type: Optional[str]
    bedrooms: int
    bathrooms: int
    area_sqm: Optional[str]
    lot_sqm: Optional[str]
    parking_spaces: int
    year_built: Optional[int]
    condition: Optional[str]
    pet_friendly: bool
    furnished: bool
    city: str
    region: str
    thumbnail_url: Optional[str]

    @staticmethod
    def resolve_lot_sqm(obj):
        return str(obj.lot_sqm) if obj.lot_sqm else None

    @staticmethod
    def resolve_thumbnail_url(obj):
        first = obj.images.first()
        if first and first.image:
            return first.image.url
        return None

    @staticmethod
    def resolve_property_type(obj):
        return obj.property_type.name if obj.property_type else None

    @staticmethod
    def resolve_price(obj):
        return str(obj.price)

    @staticmethod
    def resolve_area_sqm(obj):
        return str(obj.area_sqm) if obj.area_sqm else None


class PropertyDetailSchema(Schema):
    id: int
    title: str
    description: str
    price: str
    listing_type: str
    property_type: Optional[str]
    bedrooms: int
    bathrooms: int
    area_sqm: Optional[str]
    lot_sqm: Optional[str]
    parking_spaces: int
    year_built: Optional[int]
    condition: Optional[str]
    pet_friendly: bool
    furnished: bool
    address: str
    city: str
    region: str
    country: str
    features: List[str]
    images: List[PropertyImageSchema]
    created_at: str

    @staticmethod
    def resolve_lot_sqm(obj):
        return str(obj.lot_sqm) if obj.lot_sqm else None

    @staticmethod
    def resolve_property_type(obj):
        return obj.property_type.name if obj.property_type else None

    @staticmethod
    def resolve_price(obj):
        return str(obj.price)

    @staticmethod
    def resolve_area_sqm(obj):
        return str(obj.area_sqm) if obj.area_sqm else None

    @staticmethod
    def resolve_features(obj):
        return [f.name for f in obj.features.all()]

    @staticmethod
    def resolve_images(obj):
        return [
            {
                'id': img.id,
                'image': img.image.url if img.image else '',
                'caption': img.caption or '',
                'order': img.order,
            }
            for img in obj.images.all().order_by('order')
        ]

    @staticmethod
    def resolve_created_at(obj):
        return obj.created_at.isoformat()


class FilterOptionsSchema(Schema):
    property_types: List[dict]
    features: List[dict]
    cities: List[str]
    regions: List[str]
    conditions: List[dict]
    price_min: Optional[float]
    price_max: Optional[float]
    area_min: Optional[float]
    area_max: Optional[float]
    lot_min: Optional[float]
    lot_max: Optional[float]
    year_min: Optional[int]
    year_max: Optional[int]


@router.get('/properties', response=List[PropertyListSchema])
@paginate(PageNumberPagination, page_size=12)
def list_properties(
    request,
    search: Optional[str] = None,
    listing_type: Optional[str] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    min_area: Optional[float] = None,
    max_area: Optional[float] = None,
    min_lot: Optional[float] = None,
    max_lot: Optional[float] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    parking: Optional[int] = None,
    condition: Optional[str] = None,
    pet_friendly: Optional[bool] = None,
    furnished: Optional[bool] = None,
    listed_since: Optional[int] = None,
    city: Optional[str] = None,
    region: Optional[str] = None,
    features: Optional[str] = None,
    sort: Optional[str] = None,
):
    qs = Property.objects.filter(status='published').select_related('property_type').prefetch_related('images')

    if search and search.strip():
        from django.db.models import Q
        term = search.strip()
        qs = qs.filter(
            Q(title__icontains=term)
            | Q(description__icontains=term)
            | Q(address__icontains=term)
            | Q(city__icontains=term)
            | Q(region__icontains=term)
        )

    if listing_type:
        qs = qs.filter(listing_type=listing_type)
    if property_type:
        qs = qs.filter(property_type__slug=property_type)
    if min_price is not None:
        qs = qs.filter(price__gte=min_price)
    if max_price is not None:
        qs = qs.filter(price__lte=max_price)
    if bedrooms is not None:
        qs = qs.filter(bedrooms__gte=bedrooms)
    if bathrooms is not None:
        qs = qs.filter(bathrooms__gte=bathrooms)
    if min_area is not None:
        qs = qs.filter(area_sqm__gte=min_area)
    if max_area is not None:
        qs = qs.filter(area_sqm__lte=max_area)
    if min_lot is not None:
        qs = qs.filter(lot_sqm__gte=min_lot)
    if max_lot is not None:
        qs = qs.filter(lot_sqm__lte=max_lot)
    if min_year is not None:
        qs = qs.filter(year_built__gte=min_year)
    if max_year is not None:
        qs = qs.filter(year_built__lte=max_year)
    if parking is not None:
        qs = qs.filter(parking_spaces__gte=parking)
    if condition:
        qs = qs.filter(condition=condition)
    if pet_friendly is not None:
        qs = qs.filter(pet_friendly=pet_friendly)
    if furnished is not None:
        qs = qs.filter(furnished=furnished)
    if listed_since is not None:
        from django.utils import timezone
        from datetime import timedelta
        since = timezone.now() - timedelta(days=listed_since)
        qs = qs.filter(created_at__gte=since)
    if city:
        qs = qs.filter(city__iexact=city)
    if region:
        qs = qs.filter(region__iexact=region)
    if features:
        feature_slugs = [f.strip() for f in features.split(',') if f.strip()]
        for slug in feature_slugs:
            qs = qs.filter(features__slug=slug)

    if sort == 'price_asc':
        qs = qs.order_by('price')
    elif sort == 'price_desc':
        qs = qs.order_by('-price')
    else:
        qs = qs.order_by('-created_at')

    return qs


@router.get('/properties/{property_id}', response=PropertyDetailSchema)
def get_property(request, property_id: int):
    prop = get_object_or_404(
        Property.objects.filter(status='published')
        .select_related('property_type')
        .prefetch_related('images', 'features'),
        id=property_id
    )
    return prop


class InquirySchema(Schema):
    name: str
    email: str
    phone: str = ''
    message: str


@router.post('/properties/{property_id}/inquiry')
def submit_inquiry(request, property_id: int, payload: InquirySchema):
    prop = get_object_or_404(
        Property.objects.filter(status='published'),
        id=property_id
    )
    PropertyInquiry.objects.create(
        property=prop,
        name=payload.name,
        email=payload.email,
        phone=payload.phone or '',
        message=payload.message,
    )
    return {'success': True, 'message': 'Inquiry submitted successfully'}


@router.get('/filters', response=FilterOptionsSchema)
def get_filters(request):
    property_types = [
        {'id': pt.id, 'name': pt.name, 'slug': pt.slug}
        for pt in PropertyType.objects.all()
    ]
    features = [
        {'id': f.id, 'name': f.name, 'slug': f.slug}
        for f in Feature.objects.all()
    ]
    from django.db.models import Min, Max
    agg = Property.objects.filter(status='published').aggregate(
        price_min=Min('price'),
        price_max=Max('price'),
        area_min=Min('area_sqm'),
        area_max=Max('area_sqm'),
        lot_min=Min('lot_sqm'),
        lot_max=Max('lot_sqm'),
        year_min=Min('year_built'),
        year_max=Max('year_built'),
    )
    cities = list(
        Property.objects.filter(status='published')
        .values_list('city', flat=True)
        .distinct()
        .order_by('city')
    )
    regions = list(
        Property.objects.filter(status='published')
        .exclude(region='')
        .values_list('region', flat=True)
        .distinct()
        .order_by('region')
    )
    conditions = [
        {'value': 'new', 'label': 'New Construction'},
        {'value': 'renovated', 'label': 'Renovated'},
        {'value': 'good', 'label': 'Good Condition'},
        {'value': 'needs_work', 'label': 'Needs Work'},
    ]
    return {
        'property_types': property_types,
        'features': features,
        'cities': cities,
        'regions': regions,
        'conditions': conditions,
        'price_min': float(agg['price_min']) if agg['price_min'] else None,
        'price_max': float(agg['price_max']) if agg['price_max'] else None,
        'area_min': float(agg['area_min']) if agg['area_min'] else None,
        'area_max': float(agg['area_max']) if agg['area_max'] else None,
        'lot_min': float(agg['lot_min']) if agg['lot_min'] else None,
        'lot_max': float(agg['lot_max']) if agg['lot_max'] else None,
        'year_min': int(agg['year_min']) if agg['year_min'] else None,
        'year_max': int(agg['year_max']) if agg['year_max'] else None,
    }
