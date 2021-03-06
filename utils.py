from django.http import HttpResponse, Http404
from django.utils.encoding import iri_to_uri
from uriresolve.models import *
import re

class HttpResponseSeeOtherRedirect(HttpResponse):
    status_code = 303

    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['Location'] = iri_to_uri(redirect_to)
        
def findMatchingRewriteRule(given_uri):
    # Get the set of rewrite_rules, loop through looking for a match
    rules = rewrite_rule.objects.all()
    for rule in rules:
        if  re.match(rule.uri_expression, given_uri) != None:
            # Got a match
            return rule
    
    # If there were no matches, return None
    return None
    
class redirect(HttpResponseSeeOtherRedirect):
    def __init__(self, rule, given_uri, accept_mapping):
        match = re.match(rule.uri_expression, given_uri)
        redirect_to = accept_mapping.redirect_to
                
        if match == None:
            raise Http404
            
        if match.lastindex != None:            
            # There were capture groups to take into account.            
            # Loop through each captured group and adjust the rule's URL String, replacing appropriately
            for i in range(match.lastindex):
                redirect_to = re.sub('\$' + str(i + 1), match.group(i + 1), redirect_to)
            
        HttpResponseSeeOtherRedirect.__init__(self, redirect_to)
        
class HttpResponseNotAcceptable(HttpResponse):
    status_code = 406