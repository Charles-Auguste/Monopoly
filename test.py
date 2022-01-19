import importlib.resources

def recup_path(template):
    with importlib.resources.path('monopoly.config',template) as p:
        path = p
    return path

print(recup_path('properties.txt'))
