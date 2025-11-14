# properties/utils.py
from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Try to get queryset from Redis cache
    properties = cache.get('all_properties')
    if not properties:
        # Fetch from database if cache is empty
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    return properties
