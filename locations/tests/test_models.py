import pytest
from django.db import IntegrityError
from locations.models import Location


@pytest.mark.django_db
class TestLocationModel:
    def test_create_location(self):
        """Test basic location creation"""
        location = Location.objects.create(name="Test Location")
        assert location.name == "Test Location"
        assert location.parent is None
        assert location.description is None

    def test_create_nested_location(self):
        """Test creating a location with a parent"""
        parent = Location.objects.create(name="Parent Location")
        child = Location.objects.create(
            name="Child Location",
            parent=parent,
            description="Test description"
        )

        assert child.parent == parent
        assert child.name == "Child Location"
        assert child.description == "Test description"
        assert parent.children.first() == child

    def test_str_representation(self):
        """Test the string representation of locations"""
        # Test location without parent
        location = Location.objects.create(name="Test Location")
        assert str(location) == "Test Location"

        # Test location with parent
        parent = Location.objects.create(name="Parent Location")
        child = Location.objects.create(name="Child Location", parent=parent)
        assert str(child) == "Child Location (in Parent Location)"

    def test_get_full_path(self):
        """Test the get_full_path method for nested locations"""
        # Create a three-level deep location structure
        grandparent = Location.objects.create(name="Building A")
        parent = Location.objects.create(name="Floor 1", parent=grandparent)
        child = Location.objects.create(name="Room 101", parent=parent)

        # Test paths at different levels
        assert grandparent.get_full_path() == ["Building A"]
        assert parent.get_full_path() == ["Building A", "Floor 1"]
        assert child.get_full_path() == ["Building A", "Floor 1", "Room 101"]

    def test_ordering(self):
        """Test that locations are ordered alphabetically by name"""
        Location.objects.create(name="Zoo")
        Location.objects.create(name="Airport")
        Location.objects.create(name="Building")

        locations = Location.objects.all()
        assert locations[0].name == "Airport"
        assert locations[1].name == "Building"
        assert locations[2].name == "Zoo" 