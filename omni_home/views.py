from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import Inventory


@login_required
def dashboard(request):
    latest_items = Inventory.objects.select_related(
        'location', 'created_by'
    ).order_by('-created_at')[:10]
    
    return render(request, 'dashboard.html', {
        'latest_items': latest_items
    }) 