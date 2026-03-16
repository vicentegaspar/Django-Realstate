from django.db import models


class PropertyType(models.Model):
    """Property type: house, apartment, land, etc."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Feature(models.Model):
    """Property features: pool, garage, garden, etc."""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Property(models.Model):
    LISTING_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.SET_NULL, null=True, related_name='properties'
    )
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lot_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    parking_spaces = models.PositiveIntegerField(default=0)
    year_built = models.PositiveIntegerField(null=True, blank=True)

    CONDITION_CHOICES = [
        ('new', 'New Construction'),
        ('renovated', 'Renovated'),
        ('good', 'Good Condition'),
        ('needs_work', 'Needs Work'),
    ]
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True)
    pet_friendly = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)

    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='')

    features = models.ManyToManyField(Feature, blank=True, related_name='properties')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class PropertyInquiry(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='inquiries'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Property inquiries'

    def __str__(self):
        return f"Inquiry from {self.name} for {self.property.title}"
