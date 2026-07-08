"""The ONE external-data layer: fetch + cache-on-first-use.

Add one module per external source (satellite, model, database...). Every fetcher
follows the cache pattern in ``example_source`` so raw sources are never read
ad-hoc across scripts (which is how one script re-downloads what another cached).
"""

from .example_source import example_source

__all__ = ["example_source"]
