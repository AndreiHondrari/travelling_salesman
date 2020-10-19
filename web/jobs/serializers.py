import json

from rest_framework import exceptions as rest_exceptions, serializers as rest_serializers

from jobs import models


class LocationsField(rest_serializers.Field):

    def to_internal_value(self, data):
        if data is None:
            return []

        if not isinstance(data, list):
            raise rest_exceptions.ValidationError("Locations must be a list")

        for elem in data:
            if len(elem) != 2:
                raise rest_exceptions.ValidationError("Location tuples must be consisting of exactly two coordinates")

            if type(elem[0]) not in (int, float,) or type(elem[1]) not in (int, float,):
                raise rest_exceptions.ValidationError("Locations coordinates must be numbers")

        return data

    def to_representation(self, value):
        return json.loads(value)


class JobSerializer(rest_serializers.ModelSerializer):
    result = rest_serializers.SerializerMethodField()
    locations = LocationsField()
    num_vehicles = rest_serializers.IntegerField(default=1, required=False)
    starting_location = rest_serializers.IntegerField(default=0, required=False)
    href = rest_serializers.HyperlinkedIdentityField(view_name='jobs:shortest-path-jobs-detail', lookup_field='uuid')

    class Meta:
        model = models.Job
        fields = ('uuid', 'status', 'result', 'locations', 'num_vehicles', 'starting_location', 'href',)
        read_only_fields = ('uuid', 'status', 'result', 'href',)

    def create(self, validated_data):
        validated_data['locations'] = json.dumps(validated_data['locations'])
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def get_result(self, obj):
        return obj.full_result
