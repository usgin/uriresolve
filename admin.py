from models import *
from django.contrib import admin
from django.conf import settings

class acceptMappingInline(admin.TabularInline):
    model = accept_mapping
    extra = 2

class rewrite_ruleAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'http://code.jquery.com/jquery-1.4.4.min.js',
            settings.MEDIA_URL + 'uriresolve/js/resourceTypeControl.js',
        )
        
    list_display = ('label', 'uri_expression')
    list_filter = ('name_authority',)
    search_fields = ('label', 'uri_expression')
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['label', 'description']
        }),
        ('URI Components', {
            'fields': ['name_authority', 'resource_type', 'pattern']
        }),
    ]
    
    inlines = [acceptMappingInline]
    
    def save_model(self, request, obj, form, change):
        uri_elements = []
        
        if obj.name_authority != None:
            uri_elements.append(obj.name_authority.name)
        
        if obj.resource_type != None:
            uri_elements.append(obj.resource_type.token)
            
        if obj.pattern != '':
            uri_elements.append(obj.pattern)
        else:
            uri_elements.append('')
        
        # Join the elements together
        s = '^' + '/'.join(uri_elements) + '$'
            
        obj.uri_expression = s
        obj.save()

class nameAuthorityAdmin(admin.ModelAdmin):
    fields = ('name',)
    
    def save_model(self, request, obj, form, change):
        obj.name = obj.name.lower()
        obj.save()
        
        # Need to create a rewrite_rule for this Name Authority
        r = rewrite_rule(
            label=obj.name.upper() + ' Name Authority', 
            description='Default representation for the ' + obj.name.upper() + ' name authority.',
            name_authority=obj,
            uri_expression='^' + obj.name + '/?$'
        )
        # Check to see if it is already there...
        if len(rewrite_rule.objects.filter(uri_expression = r.uri_expression)) == 0:
            r.save()
            
            # Create the Accept-Mapping for this rewrite_rule
            am = accept_mapping(
                rewrite_rule=r,
                representation_type=representation_type.objects.get(pk=24), # This is the pk for text/html .html
                redirect_to='/uri-gin/' + obj.name + '/uri-description/'
            )
            am.save()
        
        # Need to create a rewrite_rule for this Name Authority's resource types
        r = rewrite_rule(
            label=obj.name.upper() + ' Resource Types', 
            description='Default representation for the resource type registry defined by the ' + obj.name.upper() + ' name authority.',
            name_authority=obj,
            uri_expression='^' + obj.name + '/type/?$'
        )
        # Check to see if it is already there...
        if len(rewrite_rule.objects.filter(uri_expression = r.uri_expression)) == 0:
            r.save()
            
            # Create the Accept-Mapping for this rewrite_rule
            am = accept_mapping(
                rewrite_rule=r,
                representation_type=representation_type.objects.get(pk=24), # This is the pk for text/html .html
                redirect_to='/uri-gin/' + obj.name + '/type/uri-description/'
            )
            am.save()
            
class resourceTypeAdmin(admin.ModelAdmin):
    list_filter = ('name_authority',)
    
    fields = ('name_authority', 'label', 'description', 'token',)
    
    def save_model(self, request, obj, form, change):
        obj.save()
        
        # Need to create a rewrite_rule for this resource type that catches the /uri-gin/authority/resource_type
        r = rewrite_rule(
            label='Resource Type Pointer: ' + obj.label + ' (' + obj.name_authority.name.upper() + ')',
            description = 'Default representation for the resource type: ' + obj.label + ', as defined by the ' + obj.name_authority.name.upper() + ' name authority.',
            name_authority=obj.name_authority,
            resource_type=obj,
            uri_expression='^' + obj.name_authority.name + '/' + obj.token + '/?$'
        )
        # Check to see if it is already there...
        if len(rewrite_rule.objects.filter(uri_expression = r.uri_expression)) == 0:
            r.save()
            
            # Create the Accept-Mapping for this rewrite_rule
            am = accept_mapping(
                rewrite_rule=r,
                representation_type=representation_type.objects.get(pk=24), # This is the pk for text/html .html
                redirect_to='/uri-gin/' + obj.name_authority.name + '/' + obj.token + '/uri-description/'
            )
            am.save()
            
admin.site.register(rewrite_rule, rewrite_ruleAdmin)
admin.site.register(name_authority, nameAuthorityAdmin)
admin.site.register(resource_type, resourceTypeAdmin)
admin.site.register(representation_type)