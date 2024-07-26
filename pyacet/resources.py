import pkg_resources

def get_font_path(filename):
    return pkg_resources.resource_filename(__name__, f'pyacet/fonts/{filename}')