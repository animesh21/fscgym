from django.shortcuts import get_object_or_404


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        field_filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                field_filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **field_filter)  # Lookup the object