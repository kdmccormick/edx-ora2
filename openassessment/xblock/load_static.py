"""
Helper class for loading generated file from webpack.
"""
import json
import logging

from pkg_resources import resource_string
from django.conf import settings

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class LoadStatic:
    """
    Helper class for loading generated file from webpack.
    """

    _manifest = dict()
    _base_url = ''
    _is_loaded = False

    @staticmethod
    def reload_manifest():
        """
        Reload from manifest file
        """
        root_url, base_url = '', '/static/dist/'
        if hasattr(settings, 'LMS_ROOT_URL'):
            root_url = settings.LMS_ROOT_URL
        else:
            logger.error('LMS_ROOT_URL is undefined')

        try:
            json_data = resource_string(__name__, 'static/dist/manifest.json').decode("utf8")
            LoadStatic._manifest = json.loads(json_data)
            LoadStatic._is_loaded = True
        except IOError:
            logger.error('Cannot find static/dist/manifest.json')
        finally:
            LoadStatic._base_url = root_url + base_url

    @staticmethod
    def get_url(key):
        """
        get url from key
        """
        if not LoadStatic._is_loaded:
            LoadStatic.reload_manifest()
        url = LoadStatic._manifest[key] if LoadStatic._is_loaded else key
        return LoadStatic._base_url + url