from uriresolve.models import *
from uriresolve.utils import HttpResponseSeeOtherRedirect
from django.http import HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from django.template import Context, loader
from django.db.models import Q

def index(request):
    # Show a listing of URIs available on this server
    listing = redirection.objects.all()
    return render_to_response(
        'uriresolve/index.html',
        { 'redirection_list': listing, }
    )
    
def resolver(request, given_uri):
    # No matches, begin searching for a matching pattern
    elements = ('uri-gin/' + given_uri).split('/')
    components = len(elements)
    for i in range(components):
        # Generate the URI that we'll be searching for
        search = '/' + '/'.join(elements[:components-i])                
        if i > 0:
            search += '/'
        
        # If we've brought ourselved down to 'uri-gin', we're done, 404.
        if search == '/uri-gin/':
            raise Http404
            
        # Find any matching redirection objects
        match = redirection.objects.filter(uri_string = search)
        
        if len(match) > 1:
            # There are duplicate URIs defined
            return render_to_response(
                'uriresolve/duplicateuri.html',
                { 'requestedUri': search, 'resources': match, }
            )
        elif len(match) == 1 and i == 0:
            # The entire requested URI matches a redirect rule, easy return
            return HttpResponseSeeOtherRedirect(match[0].url_string)
            
        elif len(match) == 1 and i !=0:
            # Some of the requested URI matches a single redirect rule, try the redirect URL with additions
            return HttpResponseSeeOtherRedirect(match[0].url_string + '/'.join(elements[components-i:]))
        
        #Otherwise, there were no matches. Iterate
    
    #Should never get here. If you did, the code is flawed, but lets just 404
    raise Http404
                
def detail(request, given_uri=''):
    resolveme = get_list_or_404(redirection, Q(uri_string = '/uri-gin/' + given_uri) | Q(uri_string = '/uri-gin/' + given_uri + '/'))
    if len(resolveme) > 1:
        return render_to_response(
            'uriresolve/duplicateuri.html',
            { 'requestedUri': '/uri-gin/' + given_uri, 'resources': resolveme, }
        )
    else:
        # There is a result. Build the breadcrumbs.
        requested = resolveme[0].uri_string.split('/')
        components = len(requested)
        
        # Setup string variables
        breadcrumb = '/ '
        uriPart = '/'
        
        # Iterate through each of the parts of the URI
        for i in range(components):
            # This IF catches the first and last parts of the split URI, which will be blank
            if requested[i] == '':
                continue
            
            # We append the new segment to the previous ones, and search for that URI
            uriPart += requested[i] + '/'
            match = redirection.objects.filter(uri_string=uriPart)
            
            # If a URI for this part has been created, link it, otherwise, just text.
            if len(match) !=0:
                breadcrumb += '<a href="' + uriPart + 'uridetail.html">' + requested[i] + '</a>' + ' / '
            else:
                breadcrumb += requested[i] + ' / '
        
        # If this is a resource type registry, use a different template
        if given_uri[len(given_uri)-4:] == 'type' and len(given_uri.split('/')) == 2:
            # Find all the resource types that are defined in this guy's name authority
            authorityName = given_uri.split('/')[0]
            authority = name_authority.objects.get(name=authorityName)
            types = resource_type.objects.filter(name_authority=authority)
            
            # Render the registry details page
            return render_to_response('uriresolve/registrydetail.html', { 'given_uri': resolveme[0], 'breadcrumbs': breadcrumb, 'resource_types': types })
        else:
            return render_to_response('uriresolve/detail.html', { 'given_uri': resolveme[0], 'breadcrumbs': breadcrumb })