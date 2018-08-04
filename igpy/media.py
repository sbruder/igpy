import logging
from .baseapi import BaseApi

class Media:
    def __init__(self, shortcode, session_id):
        self.baseapi = BaseApi(session_id=session_id)
        self.cache = dict()
        self.shortcode = shortcode

    def info(self):
        try:
            return self.cache['info']
        except KeyError:
            logging.info('Getting information of %s', self.shortcode)
            info = self.baseapi.short_info(
                identifier=self.shortcode,
                category='shortcode'
            )
            self.cache['info'] = info
            return info

    def display_url(self):
        info = self.info()

        if info['__typename'] == 'GraphSidecar':
            return [edge['node']['display_url'] for edge in info['edge_sidecar_to_children']['edges']]
        if info['__typename'] == 'GraphVideo':
            return [info['video_url']]

        # GraphImage
        return [info['display_url']]

    def tags(self):
        info = self.info()

        if info['__typename'] == "GraphImage":
            items = [info['edge_media_to_tagged_user']['edges']]
        elif info['__typename'] == "GraphSidecar":
            items = [item['node']['edge_media_to_tagged_user']['edges'] for item in info['edge_sidecar_to_children']['edges']]
        else:
            # video has no tags
            items = []

        tags = []
        for item in items:
            item_tags = []
            for tag in [tag['node'] for tag in item]:
                cleaned_tag = dict()
                cleaned_tag['username'] = tag['user']['username']
                cleaned_tag['x'] = tag['x']
                cleaned_tag['y'] = tag['y']

                item_tags.append(cleaned_tag)

            tags.append(item_tags)

        return tags

    def likes(self):
        logging.info('Getting likes of %s', self.shortcode)
        likes = self.baseapi.graphql_depaginate(
            query_hash='1cb6ec562846122743b61e492c85999f',
            variables={
                'shortcode': self.shortcode
            }
        )
        return [user['username'] for user in likes]

    def comments(self):
        logging.info('Getting comments of %s', self.shortcode)
        comments = self.baseapi.graphql_depaginate(
            query_hash='33ba35852cb50da46f5b5e889df7d159',
            variables={
                'shortcode': self.shortcode
            }
        )

        cleaned_comments = []
        for comment in comments:
            cleaned_comment = dict()

            cleaned_comment['text'] = comment['text']
            cleaned_comment['time'] = comment['created_at']
            cleaned_comment['user'] = comment['owner']['username']

            cleaned_comments.append(cleaned_comment)

        return cleaned_comments

    def location(self):
        try:
            location = self.info()['location']['id']
        except KeyError:
            return None

        logging.info('Getting location of %s', self.shortcode)
        location = self.baseapi.short_info(
            identifier=location,
            category='location'
        )

        return {
            'name': location['name'],
            'lat': location['lat'],
            'lon': location['lng']
        }

    def caption(self):
        try:
            return self.info()['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError: # no caption
            return ''
