import re

def camel_to_underscore(s):
    return re.sub('(.)([A-Z]{1})', r'\1_\2', s).lower()

def underscore_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join([x.title() for x in parts[1:]])