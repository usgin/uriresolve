from django.db import models

class rewrite_rule(models.Model):
    class Meta:
        ordering = ['label']
        verbose_name = 'Rewrite Rule'
        verbose_name_plural = 'Rewrite Rules'
        
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
# URI components - Use to construct USGIN URIs
#---------------------------------------------------    
    name_authority = models.ForeignKey('name_authority', blank=True, null=True)
    
    resource_type = models.ForeignKey(
        'resource_type',
        verbose_name='Resource Type',
        help_text='A token that indicates the resource type.', 
        blank=True, 
        null=True
    )
        
    pattern = models.CharField(
        max_length=1000, 
        blank=True, 
        help_text='Regular Expression for this URI to capture. See http://docs.python.org/release/2.5.2/lib/re-syntax.html for syntax guidelines.'
    )
#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# URI Expression Itself 
#---------------------------------------------------  
    uri_expression = models.CharField(
        max_length=255, 
        blank=True, 
        help_text='This is the URI representing a resource'
    )
#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# Content Negotiation
#---------------------------------------------------
    representations = models.ManyToManyField(
        'representation_type', 
        through='accept_mapping',
    )
      
    def __unicode__(self):
        return self.uri_expression

#---------------------------------------------------
#---------------------------------------------------

#---------------------------------------------------
# Representation Types are MIME Types
#---------------------------------------------------
class representation_type(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name = 'Media Type'
        verbose_name_plural = 'Media Types'
        
    name = models.CharField(
        max_length=100,
    )
        
    def __unicode__(self):
        return self.name
        
#---------------------------------------------------
# Accept Mappings are to perform redirections
#  where Content Negotiaion is enabled
# This is a Many-to-Many relationship manager
#---------------------------------------------------
class accept_mapping(models.Model):
    class Meta:
        verbose_name = 'Accept-Mapping'
        verbose_name_plural = 'Accept-Mapping'
        
    rewrite_rule = models.ForeignKey('rewrite_rule')
    representation_type = models.ForeignKey(
        'representation_type',
        verbose_name = 'Media Type'
    )
    redirect_to = models.CharField(
        max_length=2000,
        help_text='The URL to which the specified Representation Type should resolve.'
    )
    
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
        help_text='A sequence of characters that identifies the naming authority for the identified resource.',
        unique=True,
    )
    
    def __unicode__(self):
        return self.name
        
class resource_type(models.Model):
    class Meta:
        ordering = ['label',]
        verbose_name = 'Resource Type'
        verbose_name_plural = 'Resource Types'
    
    name_authority = models.ForeignKey(
        'name_authority',
        verbose_name = 'Name Authority'
    )
    
    label = models.CharField(
        max_length=100,
        help_text='A human-readable label for the resource type.'
    )
    
    token = models.CharField(
        max_length=100,
        help_text='The token name will appear in URIs.'
    )
    
    description = models.TextField(
        blank=True,
        help_text='(Optional) A description of the resource type.'
    )
    
    def __unicode__(self):
        return self.name_authority.name + ': ' + self.label