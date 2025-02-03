from django.contrib import admin
from .models import Venue, Event, EventDate,Enrollment
from .tasks import send_event_creation_email
# Inline model for EventDate
from import_export.admin import ExportMixin, ImportMixin  # Added ImportMixin for importing functionality
from import_export import resources

from django.http import HttpResponse
import csv
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


class EnrollmentResource(resources.ModelResource):
    class Meta:
        model = Enrollment
        fields = ('id', 'user', 'event', 'enrolled_on')
        export_order = ('id', 'user', 'event', 'enrolled_on')

    def dehydrate_user(self, enrollment):
        return f"{enrollment.user.first_name} {enrollment.user.last_name}"

    def dehydrate_event(self, enrollment):
        return enrollment.event.name

# Admin for Enrollment

class EnrollmentAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'event', 'enrolled_on', 'get_event_name')
    search_fields = ('user__username', 'event__name')
    list_filter = ('event', 'user')
    resource_class = EnrollmentResource

    def get_event_name(self, obj):
        return obj.event.name
    get_event_name.short_description = 'Event Name'

    def export_as_csv(self, request, queryset):
        # Custom export as CSV logic
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=exported_enrollments.csv'
        writer = csv.writer(response)
        writer.writerow(['User', 'Event', 'Enrolled On'])

        for enrollment in queryset:
            writer.writerow([enrollment.user.username, enrollment.event.name, enrollment.enrolled_on])
        
        return response

    export_as_csv.short_description = "Export selected enrollments as CSV"

    actions = ["export_as_csv"]  # Add custom export action
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventDate, EventDateAdmin)
admin.site.register(Enrollment,EnrollmentAdmin)