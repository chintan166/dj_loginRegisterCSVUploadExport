import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Democsv

@admin.register(Democsv)
class DemocsvAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2', 'field3')  # Display these fields in the list view
    search_fields = ('field1', 'field2', 'field3')  # Add search functionality
    list_filter = ('field1', 'field2')
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        """
        Export the selected data as a CSV file.
        """
        # Create an HttpResponse object with content type for CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=democsv_data.csv'

        writer = csv.writer(response)
        
        # Write the header row (field names)
        writer.writerow(['Field 1', 'Field 2', 'Field 3'])  # Adjust field names to your model

        # Write data rows
        for obj in queryset:
            writer.writerow([obj.field1, obj.field2, obj.field3])  # Adjust fields to your model
        
        return response

    export_as_csv.short_description = "Export selected as CSV" 

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Customize the display of fields in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')

    # Fields to search for in the admin interface
    search_fields = ('username', 'email')

    # Fields to filter by in the admin interface
    list_filter = ('is_staff', 'is_active', 'is_superuser')
