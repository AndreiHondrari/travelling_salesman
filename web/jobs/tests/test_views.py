import json

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status as rest_status

from jobs import models

pytestmark = pytest.mark.django_db

fake = Faker()


def test_job_creation(django_user_model, client, mocker):
    """Check successful job creation"""

    # prepare
    mocked_tasks = mocker.patch('jobs.views.tasks')

    locations = [
        [fake.pyint(), fake.pyint()],
        [fake.pyint(), fake.pyint()],
        [fake.pyint(), fake.pyint()],
    ]

    data = {
        'locations': locations
    }

    user1 = django_user_model.objects.create(username=fake.pystr(), email=fake.email())
    client.force_login(user1)

    # act
    response = client.post(
        reverse('jobs:shortest-path-jobs-list'),
        data,
        content_type="application/json"
    )

    # assert
    assert response.status_code == rest_status.HTTP_202_ACCEPTED, response.data

    assert models.Job.objects.all().count() == 1

    job = models.Job.objects.first()
    assert job.num_vehicles == 1
    assert job.starting_location == 0

    response_json = response.json()
    assert response_json['uuid'] == str(job.uuid)
    assert response_json['status'] == job.status
    assert response_json['locations'] == locations

    assert mocked_tasks.calculate_shortest_path.apply_async.called_once_with(
        (job.id, locations, 1, 0,)
    )
