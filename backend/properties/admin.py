from django.contrib import admin
from django.utils.html import format_html
from .models import PropertyType, Feature, Property, PropertyImage, PropertyInquiry


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    class Media:
        css = {'all': ('properties/css/admin_dragdrop.css',)}
        js = ('properties/js/admin_dragdrop.js',)
    list_display = [
        'title', 'listing_type', 'property_type', 'price', 'city',
        'status', 'created_at', 'thumbnail_preview'
    ]
    list_filter = ['listing_type', 'status', 'property_type', 'city', 'condition', 'pet_friendly', 'furnished']
    search_fields = ['title', 'description', 'address', 'city', 'region']
    prepopulated_fields = {}
    inlines = [PropertyImageInline]
    filter_horizontal = ['features']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'listing_type', 'property_type', 'status')
        }),
        ('Details', {
            'fields': (
                'bedrooms', 'bathrooms', 'area_sqm', 'lot_sqm',
                'parking_spaces', 'year_built', 'condition',
                'pet_friendly', 'furnished', 'features'
            )
        }),
        ('Location', {
            'fields': ('address', 'city', 'region', 'country')
        }),
    )

    def thumbnail_preview(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html(
                '<img src="{}" style="max-width: 60px; max-height: 60px; object-fit: cover;" />',
                first_image.image.url
            )
        return '-'

    thumbnail_preview.short_description = 'Preview'


@admin.register(PropertyInquiry)
class PropertyInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'property', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['property', 'name', 'email', 'phone', 'message', 'created_at']
