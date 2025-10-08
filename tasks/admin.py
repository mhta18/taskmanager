from django.contrib import admin
from django.contrib.auth.models import User  
from .models import Task, BugReport, Note

class BaseItemAdminMixin:
    """Mixin with common admin configuration"""
    list_display = ('title', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        """Limit objects to those owned by the current user"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
    
    def save_model(self, request, obj, form, change):
        """Automatically set owner when creating new objects"""
        if not obj.pk:  # If creating new object
            obj.owner = request.user
        super().save_model(request, obj, form, change)

@admin.register(Task)
class TaskAdmin(BaseItemAdminMixin, admin.ModelAdmin):
    list_display = BaseItemAdminMixin.list_display + ('assigned_to', 'status', 'priority')
    list_filter = BaseItemAdminMixin.list_filter + ('status', 'priority', 'assigned_to')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status', 'priority')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    

@admin.register(BugReport)
class BugReportAdmin(admin.ModelAdmin, BaseItemAdminMixin):
    list_display = BaseItemAdminMixin.list_display + ('severity', 'status')
    list_filter = BaseItemAdminMixin.list_filter + ('severity', 'status')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner', 'expected_result')
        }),
        ('Bug Details', {
            'fields': ('severity', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_list_display(self, request):
        """Customize list display based on user permissions"""
        base_list = super().get_list_display(request)
        if request.user.is_superuser:
            return base_list
        return base_list

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin, BaseItemAdminMixin):
    list_display = BaseItemAdminMixin.list_display + ('note_type', 'is_pinned')
    list_filter = BaseItemAdminMixin.list_filter + ('note_type', 'is_pinned')
    search_fields = BaseItemAdminMixin.search_fields + ('tags',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'owner', 'tags')
        }),
        ('Note Details', {
            'fields': ('note_type', 'is_pinned')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        """For notes, show all if superuser, otherwise only user's notes"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

