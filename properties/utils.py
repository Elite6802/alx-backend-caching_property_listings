# properties/utils.py
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)


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


def get_redis_cache_metrics():
    """
    Retrieve Redis keyspace hit/miss metrics and calculate hit ratio.
    Metrics are logged and returned as a dictionary.
    """
    try:
        # Get raw Redis client
        client = cache.client.get_client()
        info = client.info('stats')  # Redis statistics

        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total_requests = hits + misses

        # Safe hit ratio calculation
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio,
        }

        # Log metrics
        logger.info(f"Redis Cache Metrics: Hits={hits}, Misses={misses}, Hit Ratio={hit_ratio:.2f}")

        return metrics

    except Exception as e:
        # Log error if something goes wrong
        logger.error(f"Error retrieving Redis cache metrics: {e}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0,
        }