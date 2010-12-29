from models import *
from django.contrib import admin
from django.conf import settings

class acceptMappingInline(admin.TabularInline):
    model = accept_mapping
    extra = 0

class redirectionAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'http://code.jquery.com/jquery-1.4.4.min.js',
            settings.MEDIA_URL + 'uriresolve/js/resourceTypeControl.js',
        )
        
    list_display = ('label', 'uri_link')
    list_filter = ('name_authority',)
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['label', 'description']
        }),
        ('URI Components', {
            'fields': ['name_authority', 'resource_type', 'resource_specific_string', 'representation_part']
        }),
        ('URI > URL Mapping', {
            'fields': [('url_string',)]# Does not seem important right now 'is_pattern')]
        }),
    ]
    
    inlines = [acceptMappingInline]
    
    def save_model(self, request, obj, form, change):
        uri_elements = []
        
        if obj.name_authority != None:
            uri_elements.append(obj.name_authority.name)
        
        if obj.resource_type != None:
            uri_elements.append(obj.resource_type.token)
            
        if obj.resource_specific_string != '':
            uri_elements.append(obj.resource_specific_string)
            
        if obj.representation_part != '':
            uri_elements.append(obj.representation_part)
        
        # Join the elements together, and append a / if there is no . in the string that means the URI points
        #  at an information resource (that is, at a file directly)
        s = '/uri-gin/' + '/'.join(uri_elements)
        if s.find('.') == -1 and len(uri_elements) > 0:
            s += '/'
            
        obj.uri_string = s
        obj.save()

class nameAuthorityAdmin(admin.ModelAdmin):
    fields = ('name',)
    
    def save_model(self, request, obj, form, change):
        obj.name = obj.name.lower()
        obj.save()
        
        # Need to create a redirection for this Name Authority
        r = redirection(
            label=obj.name.upper() + ' Name Authority', 
            description='Default representation for the ' + obj.name.upper() + ' name authority.',
            name_authority=obj,
            uri_string='/uri-gin/' + obj.name + '/',
            url_string='http://' + request.META['SERVER_NAME'] + '/uri-gin/' + obj.name + '/uridetail.html'
        )
        r.save()
        
        # Need to create a redirection for this Name Authority's resource types
        r = redirection(
            label=obj.name.upper() + ' Resource Types', 
            description='Default representation for the resource type registry defined by the ' + obj.name.upper() + ' name authority.',
            name_authority=obj,
            uri_string='/uri-gin/' + obj.name + '/type/',
            url_string='http://' + request.META['SERVER_NAME'] + '/uri-gin/' + obj.name + '/type/uridetail.html'
        )
        r.save()

class resourceTypeAdmin(admin.ModelAdmin):
    list_filter = ('name_authority',)
    
    fields = ('name_authority', 'label', 'description', 'token',)
    
    def save_model(self, request, obj, form, change):
        obj.save()
        
        # Need to create a redirection for this resource type
        r = redirection(
            label='Resource Type: ' + obj.label + ' (' + obj.name_authority.name.upper() + ')',
            description='Default representation for the ' + obj.label + ' resource type defined by the ' + obj.name_authority.name.upper() + ' name authority.',
            name_authority=obj.name_authority,
            uri_string='/uri-gin/' + obj.name_authority.name + '/type/' + obj.token + '/',
            url_string='http://' + request.META['SERVER_NAME'] + '/uri-gin/' + obj.name_authority.name + '/type/' + obj.token + '/uridetail.html'
        )
        r.save()
        
admin.site.register(redirection, redirectionAdmin)
admin.site.register(name_authority, nameAuthorityAdmin)
admin.site.register(resource_type, resourceTypeAdmin)
#admin.site.register(representation_type)