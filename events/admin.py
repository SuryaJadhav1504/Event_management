from django.contrib import admin
from .models import Venue, Event, EventDate,Enrollment
from .tasks import send_event_creation_email
# Inline model for EventDate

class EventDateInline(admin.TabularInline):
    model = EventDate
    extra = 1

# Admin for Venue
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')
    list_filter = ('name',)

# Admin for Event
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'get_event_dates')  
    search_fields = ('name', 'description')
    list_filter = ('venue',)
    inlines = [EventDateInline]

    def get_event_dates(self, obj):
        return ", ".join([f"{event.date} at {event.time}" for event in obj.event_dates.all()])
    get_event_dates.short_description = 'Event Dates'

    def get_registered_users(self, obj):
        # Display enrolled users for each event
        return ", ".join([enrollment.user.username for enrollment in obj.enrollment_set.all()])
    get_registered_users.short_description = 'Registered Users'

    

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Only trigger if it's a new event, not an update
            print(f"Triggering email task for event: {obj.name}")
            send_event_creation_email(obj.name)  # Trigger task
# Admin for EventDate
class EventDateAdmin(admin.ModelAdmin):
    list_display = ('event', 'date', 'time')
    search_fields = ('event__name',)
    list_filter = ('date',)

# Register models with admin
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventDate, EventDateAdmin)
admin.site.register(Enrollment)