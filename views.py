from uriresolve.models import *
from uriresolve import mimeparse
from uriresolve.utils import *
from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotAllowed, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
import re
    
def resolver(request, given_uri):
    if request.META['REQUEST_METHOD'] != 'GET':
        return HttpResponseNotAllowed(['GET'])
        
    # return HttpResponse('Resolver: ' + given_uri)
    rule = findMatchingRewriteRule(given_uri)
    if rule == None:
        raise Http404
    
    # Look for Accept-Mappings for this rewrite rule
    listing = []
    lookup = {}
    for availableRepresentations in rule.representations.all():
        listing.append(availableRepresentations.name)
        lookup[availableRepresentations.name] = availableRepresentations.pk
        
    if len(listing) > 0:
        # The rewrite rule has some Accept-Mappings. Try to match the request's accept-header
        match = mimeparse.best_match(listing, request.META.get('HTTP_ACCEPT', '*'))
        if match == '':
            # There is no suitable match. 406.
            return HttpResponseNotAcceptable('406 Error: Not Acceptable')
        else:
            # Get the appropriate accept_mapping object
            mapping = accept_mapping.objects.filter(rewrite_rule=rule).filter(representation_type=lookup[match])
            if len(mapping) != 1:
                # You would only get here if there is more than one accept mapping for a single media type. 500.
                return HttpResponseServerError('500 Error: Internal Server Error - More than one accept-mapping defined for a single media type.')
            else:
                #return HttpResponse('Resolver: ' + mapping[0].redirect_to)
                return redirect(rule, given_uri, mapping[0])
    else:
        # There were no accept mappings defined. This is a misconfigured rule.
        return HttpResponseServerError('500 Error: Internal Server error - No mappings defined for this URI.')
                
def description(request, given_uri=''):
    if request.META['REQUEST_METHOD'] != 'GET':
        return HttpResponseNotAllowed(['GET'])
        
    # Handle the case for the uri-gin/ URI - different template
    if given_uri == '':
        return render_to_response('uriresolve/index.html', {}, context_instance=RequestContext(request))
        
    #return HttpResponse('Description: ' + given_uri)
    
    # Find the matching rule
    rule = findMatchingRewriteRule(given_uri)
    if rule == None:
        raise Http404
        
    # Build Breadcrumbs
    requested = given_uri.split('/')
    noOfParts = len(requested)
    breadcrumb = '/ <a href="/uri-gin/uri-description/">uri-gin</a> / '
    uriPart = ''
    
    for i in range(noOfParts):
        if requested[i] == '':
            continue
        
        uriPart += requested[i] + '/'
        thisRule = findMatchingRewriteRule(uriPart)
        if thisRule == None:
            breadcrumb += requested[i] + ' / '
        else:
            breadcrumb += '<a href="/uri-gin/' + uriPart + 'uri-description/">' + requested[i] + '</a> / '
    # If this is a resource type registry, use a different template
    
    if given_uri[len(given_uri)-5:] == 'type/' and len(given_uri.split('/')) == 3:
        # Find all the resource types that are defined in this guy's name authority
        authorityName = given_uri.split('/')[0]
        authority = name_authority.objects.get(name=authorityName)
        types = resource_type.objects.filter(name_authority=authority)
        
        # Render the registry details page
        return render_to_response('uriresolve/registrydetail.html', { 'given_uri': rule, 'breadcrumbs': breadcrumb, 'resource_types': types })
    else:
        # Find all the accept-mappings for this URI
        mappings = accept_mapping.objects.filter(rewrite_rule=rule)
        
        # Render the URI details page
        return render_to_response('uriresolve/detail.html', { 'given_uri': rule, 'breadcrumbs': breadcrumb, 'mappings': mappings })
    
def jsonTypesByAuthority(request, authority_name):
    if request.META['REQUEST_METHOD'] != 'GET':
        return HttpResponseNotAllowed(['GET'])
        
    authority = name_authority.objects.get(name=authority_name)
    result = serializers.serialize('json', resource_type.objects.filter(name_authority = authority))
    return HttpResponse(result, mimetype='application/json')
