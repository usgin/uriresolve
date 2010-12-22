from models import *
from django.contrib import admin

class acceptMappingInline(admin.TabularInline):
    model = accept_mapping
    extra = 0

class redirectionAdmin(admin.ModelAdmin):
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

admin.site.register(redirection, redirectionAdmin)
admin.site.register(name_authority)
admin.site.register(resource_type)
#admin.site.register(representation_type)