import json

import pytest
from faker import Faker

from jobs import models, serializers

pytestmark = pytest.mark.django_db

fake = Faker()


def test_job_deserialization_with_null_locations():
    """Check deserialization with null locations"""

    # prepare
    data = {
        'locations': None
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert not is_valid, serializer.validated_data
    assert 'locations' in serializer.errors, serializer.errors


def test_job_deserialization_with_empty_locations():
    """Check deserialization with empty locations"""

    # prepare
    data = {
        'locations': []
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert is_valid, serializer.errors


def test_job_deserialization_with_bad_locations_input():
    """Check inability to deserialize with non-list locations input"""

    # prepare
    data = {
        'locations': fake.pyint()
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert not is_valid, serializer.validated_data
    assert 'locations' in serializer.errors, serializer.errors


def test_job_deserialization_with_items_of_lesser_length():
    """Check inability to deserialize with locations items lengths of less than 2"""

    # prepare
    data = {
        'locations': [[55]]
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert not is_valid, serializer.validated_data
    assert 'locations' in serializer.errors, serializer.errors


def test_job_deserialization_with_items_of_bigger_length():
    """Check inability to deserialize with locations items lengths of more than 2"""

    # prepare
    data = {
        'locations': [[55, 22, 33]]
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert not is_valid, serializer.validated_data
    assert 'locations' in serializer.errors, serializer.errors


@pytest.mark.parametrize(
    "test_input",
    [
        [[11, True]],
        [[True, 22]],
        [[33, "af"]],
        [["fwafa", 44]],
    ]
)
def test_job_deserialization_with_elements_that_are_not_numbers(test_input):
    """Check inability to deserialize location items containing anything else than numbers"""

    # prepare
    data = {
        'locations': test_input
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert not is_valid, serializer.validated_data
    assert 'locations' in serializer.errors, serializer.errors


def test_job_deserialization_with_one_input():
    """Check deserialization with one location item"""

    # prepare
    data = {
        'locations': [
            [fake.pyint(), fake.pyint()]
        ]
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert is_valid, serializer.errors


def test_job_deserialization_with_multiple_inputs():
    """Check deserialization with multiple location items"""

    # prepare
    data = {
        'locations': [
            [fake.pyint(), fake.pyint()],
            [fake.pyint(), fake.pyint()],
            [fake.pyint(), fake.pyint()],
        ]
    }
    serializer = serializers.JobSerializer(data=data)

    # act
    is_valid = serializer.is_valid()

    # assert
    assert is_valid, serializer.errors


def test_serialization(django_user_model, rf):
    """Check successful serialization"""

    # prepare
    locations = [
        [fake.pyint(), fake.pyint()],
        [fake.pyint(), fake.pyint()],
        [fake.pyint(), fake.pyint()],
    ]
    user1 = django_user_model.objects.create(username=fake.pystr(), email=fake.email())
    job = models.Job.objects.create(
        locations=json.dumps(locations),
        created_by=user1
    )
    request = rf.get('something')
    serializer = serializers.JobSerializer(instance=job, context={'request': request})

    # act
    job_data = serializer.data

    # assert
    assert job_data['locations'] == locations
    assert job_data['status'] == job.status
    assert job_data['uuid'] == str(job.uuid)
