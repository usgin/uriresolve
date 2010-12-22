from django.db import models

RESOURCE_TYPE_CHOICES = (
    ('type', 'Resource Type'),
    ('register', 'Register'),
    ('collection', 'Collection'),
    ('vocabulary', 'Vocabulary'),
    ('dataset', 'Dataset'),
    ('registry', 'Registry'),
    ('catalog', 'Catalog'),
    ('organization', 'Organization'),
    ('person', 'Person'),
    ('concept', 'Concept'),
    ('authority', 'Naming authority'),
    ('document', 'Document'),
)

class redirection(models.Model):
    class Meta:
        ordering = ['label']

#---------------------------------------------------
# URI Metadata
#---------------------------------------------------
    label = models.CharField(
        max_length=100, 
        help_text='A label for this URI, for recognition in the admin interface'
    )
    
    description = models.TextField(
        blank=True, 
        help_text='(Optional) Free-text description of this URI',
    )
#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# URI components
#---------------------------------------------------    
    name_authority = models.ForeignKey('name_authority', blank=True, null=True)
    
    # resource_type = models.CharField(
        # max_length=100,
        # choices=RESOURCE_TYPE_CHOICES,
        # verbose_name='Resource Type',
        # help_text='A token that indicates the resource type, taken from the register at http://resources.usgin.org/uri-gin/usgin/resourceType/'
        # )
        
    resource_type = models.ForeignKey(
        'resource_type',
        verbose_name='Resource Type',
        help_text='A token that indicates the resource type, taken from the register at http://resources.usgin.org/uri-gin/usgin/resourceType/', 
        blank=True, 
        null=True
    )
        
    resource_specific_string = models.CharField(
        max_length=100, 
        verbose_name='Resource Specific String', 
        blank=True, 
        help_text='A string that may have syntax specially scoped for a particular resource type.'
    )
    
    representation_part = models.CharField(
        max_length=100, 
        verbose_name='Representation Part', 
        blank=True, 
        help_text='Intended to identify a representation of the preceding resource part.'
    )
#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# Pattern Matching vs. Straight Redirection
#---------------------------------------------------
    is_pattern = models.BooleanField(
        default=False,
        verbose_name='Use URI as a pattern',
        help_text='When a URI is used as a pattern, characters entered after the formal URI will be appended to the redirection URL.'
    )
#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# URI > URL Mapping  
#---------------------------------------------------  
    uri_string = models.CharField(
        max_length=255, 
        blank=True, 
        help_text='This is the URI representing a resource'
    )
    
    url_string = models.URLField(
        blank=True,
        verbose_name = 'URL',
        help_text='This is a URL to which a direct match of this URI should be resolved'
    )
#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# Content Negotiation (For the Future)
#---------------------------------------------------
    representations = models.ManyToManyField(
        'representation_type', 
        through='accept_mapping', 
        blank=True, 
        null=True
    )
    
    def uri_link(self):
        return '<a href=' + self.uri_string + '>' + self.uri_string + '</a>'
    uri_link.allow_tags = True
    uri_link.short_description = 'URI'
    
    def __unicode__(self):
        return self.uri_string

#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# Representation Types are MIME Types
#---------------------------------------------------
class representation_type(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Representation Type'
        verbose_name_plural = 'Representation Types'
        
    name = models.CharField(
        max_length=100,
        verbose_name='MIME Type/Sub-Type'
    )
    extension = models.CharField(
        max_length=10,
        verbose_name='File Extension'
    )

    def __unicode__(self):
        return self.name + ': .' + self.extension
        
#---------------------------------------------------
# Accept Mappings are to perform redirections
#  where Content Negotiaion is enabled
# This is a Many-to-Many relationship manager
#---------------------------------------------------
class accept_mapping(models.Model):
    class Meta:
        verbose_name = 'Content Negotiation'
        verbose_name_plural = 'Content Negotiation'
        
    redirection = models.ForeignKey('redirection')
    representation_type = models.ForeignKey(
        'representation_type',
        verbose_name = 'MIME Type'
    )
    redirect_to = models.URLField(help_text='The URL to which the specified Representation Type should resolve.')
    
    def __unicode__(self):
        return self.representation_type.name

#---------------------------------------------------
# Registry of Name Authorities and Resource Types
#---------------------------------------------------
class name_authority(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Name Authority'
        verbose_name_plural = 'Name Authorities'
        
    name = models.CharField(
        max_length=100, 
        verbose_name='Name Authority', 
        help_text='A sequence of characters that identifies the naming authority for the identified resource.'
    )
    
    def __unicode__(self):
        return self.name
        
class resource_type(models.Model):
    class Meta:
        ordering = ['label']
        verbose_name = 'Resource Type'
        verbose_name_plural = 'Resource Types'
        
    token = models.CharField(
        max_length=100,
        help_text='The token name will appear in URIs.'
    )
    
    label = models.CharField(
        max_length=100,
        help_text='A human-readable label for the resource type.'
    )
    
    description = models.TextField(
        blank=True,
        help_text='(Optional) A description of the resource type.'
    )
    
    def __unicode__(self):
        return self.label    
