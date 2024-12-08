from re import L
import pytest
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventory.models import Inventory, InventoryType
from locations.models import Location

User = get_user_model()

@pytest.fixture
def test_location():
    return Location.objects.create(
        name='Test Location'
    )

@pytest.fixture
def test_user():
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def test_inventory_type():
    return InventoryType.objects.create(
        name='Test Type',
        key='test-type'
    )

@pytest.fixture
def test_inventory_item(test_user, test_inventory_type, test_location):
    item = Inventory.objects.create(
        name='Test Item',
        quantity=1,
        description='Test description',
        location=test_location,
        created_by=test_user,
        updated_by=test_user
    )
    item.types.add(test_inventory_type)
    return item

@pytest.fixture
def authenticated_client(client, test_user):
    client.force_login(test_user)
    return client

@pytest.mark.django_db
class TestInventoryModels:
    def test_inventory_type_str(self, test_inventory_type):
        assert str(test_inventory_type) == 'Test Type'

    def test_inventory_str(self, test_inventory_item):
        expected = f"{test_inventory_item.name} ({test_inventory_item.quantity}) at {test_inventory_item.location}"
        assert str(test_inventory_item) == expected

@pytest.mark.django_db
class TestInventoryViews:
    def test_inventory_list_view(self, authenticated_client):
        response = authenticated_client.get(reverse('inventory:list'))
        assert response.status_code == 200

    def test_inventory_detail_view(self, authenticated_client, test_inventory_item):
        response = authenticated_client.get(
            reverse('inventory:detail', kwargs={'item_number': test_inventory_item.pk})
        )
        assert response.status_code == 200
        assert test_inventory_item.name in str(response.content)

    def test_inventory_create_view(self, authenticated_client, test_location, test_inventory_type):
        response = authenticated_client.get(reverse('inventory:create'))
        assert response.status_code == 200

        # Test POST request
        data = {
            'name': 'New Test Item',
            'quantity': 1,
            'description': 'New test description',
            'location': test_location.id,
            'types': [test_inventory_type.id]
        }
        response = authenticated_client.post(reverse('inventory:create'), data)
        assert response.status_code == 302  # Redirect after successful creation
        assert Inventory.objects.filter(name='New Test Item').exists()

    def test_inventory_edit_view(self, authenticated_client, test_inventory_item, test_location):
        response = authenticated_client.get(
            reverse('inventory:inventory_edit', kwargs={'pk': test_inventory_item.pk})
        )
        assert response.status_code == 200

        # Test POST request
        data = {
            'name': 'Updated Test Item',
            'quantity': 2,
            'description': 'Updated description',
            'location': test_location.id,
            'types': [t.id for t in test_inventory_item.types.all()]
        }
        response = authenticated_client.post(
            reverse('inventory:inventory_edit', kwargs={'pk': test_inventory_item.pk}),
            data
        )
        assert response.status_code == 302
        test_inventory_item.refresh_from_db()
        assert test_inventory_item.name == 'Updated Test Item'
        assert test_inventory_item.quantity == 2

    def test_inventory_list_type_filter(self, authenticated_client, test_inventory_type, test_inventory_item):
        response = authenticated_client.get(
            f"{reverse('inventory:list')}?type={test_inventory_type.id}"
        )
        assert response.status_code == 200
        assert test_inventory_item.name in str(response.content)