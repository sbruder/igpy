import json
import logging
import progressbar
import requests

class BaseApi:
    """BaseApi is the low-level component.

    It does HTTP requests, authentication and endpoint handling.
    """
    # children elements for known hashes
    children_by_hash = {
        '37479f2b8209594dde7facb0d904896a': ['user', 'edge_followed_by'],
        '58712303d941c6855d4e888c5f0cd22f': ['user', 'edge_follow'],
        'bd0d6d184eefd4d0ce7036c11ae58ed9': ['user', 'edge_owner_to_timeline_media'],
        '1cb6ec562846122743b61e492c85999f': ['shortcode_media', 'edge_liked_by'],
        '33ba35852cb50da46f5b5e889df7d159': ['shortcode_media', 'edge_media_to_comment']
    }

    def __init__(self, session_id):
        self.cookies = {
            'sessionid': session_id
        }

    def __authenticated_request(self, url, payload={}):
        """Performs an HTTP request with authentication and payload."""
        logging.debug('Performing authenticated request to %s with payload %s '
                      'and cookies %s', url, payload, self.cookies)
        r = requests.get(url, params=payload, cookies=self.cookies)
        logging.debug('Response: %s', r.text)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 403:
            raise PermissionError('You are unauthorized to perform this '
                                  'action. Your Session ID may not be valid.')
        if r.status_code == 404:
            raise FileNotFoundError('The Object you requested does not exist.')
        else:
            raise Exception(f'An unknown error occured (got HTTP status {r.status_code})')

    def graphql_request(self, query_hash, variables={}):
        """Requests information at GraphQL endpoint with known hash and variables."""
        payload = {
            'query_hash': query_hash,
            'variables': json.dumps(variables)
        }
        r = self.__authenticated_request(
            url='https://www.instagram.com/graphql/query/',
            payload=payload
        )

        try:
            data = r['data']
        except KeyError:
            raise KeyError('Response is invalid: missing ‘data’')
        return data

    def graphql_depaginate(self, query_hash, variables={}):
        """Performs a graphql request and resolves pagination.

        It needs the hash and children elements in children_by_hash.
        """
        variables['first'] = 50
        children = self.children_by_hash[query_hash]
        has_next_page = True
        edges = []

        if logging.getLogger().getEffectiveLevel() <= logging.INFO:
            bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)

        while has_next_page:
            try:
                data = self.graphql_request(
                    query_hash=query_hash,
                    variables=variables
                )[children[0]][children[1]]
            except KeyError:
                raise KeyError(f'Children keys (‘{children[0]}’ and ‘{children[1]})’ do not exist')

            has_next_page = data['page_info']['has_next_page']
            variables['after'] = data['page_info']['end_cursor']

            edges.extend([edge['node'] for edge in data['edges']])

            if 'bar' in locals():
                bar.max_value = data['count']
                bar.update(len(edges))

        if 'bar' in locals():
            bar.finish()

        return edges

    def short_info(self, identifier, category):
        """Short info (?__a=1) for items.

        Supports the following as categories:
         - user
         - shortcode (media)
         - location
        """
        if category == 'user':
            path = identifier
            graphql_id = 'user'
        elif category == 'shortcode':
            path = f'p/{identifier}'
            graphql_id = 'shortcode_media'
        elif category == 'location':
            path = f'explore/locations/{identifier}'
            graphql_id = 'location'
        else:
            raise KeyError(f'Invalid category ‘{category}’')

        r = self.__authenticated_request(f'https://www.instagram.com/{path}/?__a=1')
        try:
            data = r['graphql'][graphql_id]
        except KeyError:
            raise KeyError(f'Response is invalid: missing ‘graphql’ and ‘{graphql_id}’')
        return data

    def user_info(self, userid):
        """Get basic user info.

        This is not possible with the GraphQL endpoint or the short info, which
        are missing e.g. the full-resolution profile picture.
        """
        r = self.__authenticated_request(f'https://i.instagram.com/api/v1/users/{userid}/info/')
        try:
            data = r['user']
        except KeyError:
            raise KeyError('Response is invalid: missing ‘user’')
        return data
