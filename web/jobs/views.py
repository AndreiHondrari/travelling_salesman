from rest_framework import mixins as rest_mixins, status as rest_status, viewsets as rest_viewsets

from jobs import models, serializers, tasks


class JobsViewSet(
    rest_mixins.ListModelMixin,
    rest_mixins.CreateModelMixin,
    rest_mixins.RetrieveModelMixin,
    rest_viewsets.GenericViewSet
):
    lookup_field = 'uuid'
    serializer_class = serializers.JobSerializer

    def get_queryset(self):
        return models.Job.objects.filter(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = rest_status.HTTP_202_ACCEPTED
        return response

    def perform_create(self, serializer):
        instance = serializer.save()

        locations = serializer.validated_data['locations']
        num_vehicles = serializer.validated_data['num_vehicles']
        depot = serializer.validated_data['starting_location']

        tasks.calculate_shortest_path.apply_async((instance.id, locations, num_vehicles, depot))
