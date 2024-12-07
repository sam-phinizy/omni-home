from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.db.models import Q
from .models import Inventory
from locations.models import Location
from .forms import InventoryForm


class InventoryDetailView(DetailView):
    model = Inventory
    template_name = "inventory/inventory_detail.html"
    context_object_name = "item"
    pk_url_kwarg = "item_number"


class InventoryListView(ListView):
    model = Inventory
    template_name = "inventory/inventory_list.html"
    context_object_name = "items"
    paginate_by = 10
    ordering = ["-created_at"]

    def get_location_and_children(self, location_id):
        """Get the selected location and all its descendants."""
        try:
            location = Location.objects.get(id=location_id)
            # Start with the current location
            locations = [location]
            # Get all children recursively
            to_process = list(location.children.all())
            while to_process:
                current = to_process.pop(0)
                locations.append(current)
                to_process.extend(list(current.children.all()))
            return locations
        except Location.DoesNotExist:
            return []

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by location (including children)
        location_id = self.request.GET.get("location")
        if location_id:
            locations = self.get_location_and_children(location_id)
            if locations:
                queryset = queryset.filter(location__in=locations)

        # Filter by type
        type_id = self.request.GET.get("type")
        if type_id:
            queryset = queryset.filter(types__id=type_id)

        # Search by name
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        return queryset.select_related("location", "created_by").prefetch_related(
            "types"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Inventory List"
        # Get all root locations (those without parents) first
        root_locations = Location.objects.filter(parent__isnull=True).order_by("name")

        # Function to build location hierarchy
        def build_location_tree(location, level=0):
            result = [
                {"id": location.id, "name": "—" * level + str(location), "level": level}
            ]
            for child in location.children.all().order_by("name"):
                result.extend(build_location_tree(child, level + 1))
            return result

        # Build the complete location tree
        locations = []
        for root in root_locations:
            locations.extend(build_location_tree(root))

        context["locations"] = locations
        context["selected_location"] = self.request.GET.get("location", "")
        context["search_query"] = self.request.GET.get("search", "")
        return context


@login_required
def inventory_edit(request, pk):
    item = get_object_or_404(Inventory, pk=pk)
    if request.method == "POST":
        form = InventoryForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.updated_by = request.user
            item.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect("inventory:detail", item_number=item.pk)
    else:
        form = InventoryForm(instance=item)
    return render(
        request, "inventory/inventory_edit.html", {"form": form, "item": item}
    )


@login_required
def inventory_create(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.updated_by = request.user
            item.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect("inventory:detail", item_number=item.pk)
    else:
        form = InventoryForm()
    return render(
        request, "inventory/inventory_edit.html", {"form": form, "is_create": True}
    )
