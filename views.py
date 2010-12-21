from uriresolve.models import redirection
from uriresolve.utils import HttpResponseSeeOtherRedirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_list_or_404, render_to_response
from django.template import Context, loader
from django.db.models import Q

def index(request):
    return HttpResponseRedirect("http://google.com")
    
def resolver(request, given_uri):
    # return HttpResponse(given_uri)
    
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
            return HttpResponseRedirect(match[0].url_string)
            
        elif len(match) == 1 and i !=0:
            # Some of the requested URI matches a single redirect rule, try the redirect URL with additions
            return HttpResponseRedirect(match[0].url_string + '/'.join(elements[components-i:]))
        
        #Otherwise, there were no matches. Iterate
    
    #Should never get here. If you did, the code is flawed, but lets just 404
    raise Http404
                
def detail(request, given_uri):
    # return HttpResponse(given_uri)
    return HttpResponse('Hello')
    
    resolveme = get_list_or_404(redirection, Q(uri_string = '/uri-gin/' + given_uri) | Q(uri_string = '/uri-gin/' + given_uri + '/'))
    if len(resolveme) > 1:
        return render_to_response(
            'uriresolve/duplicateuri.html',
            { 'requestedUri': '/uri-gin/' + given_uri, 'resources': resolveme, }
        )
    else:
        return render_to_response('uriresolve/detail.html', { 'given_uri': resolveme[0] })
        
def base_detail(request):
    return HttpResponseSeeOtherRedirect('http://catalog.usgin.org')