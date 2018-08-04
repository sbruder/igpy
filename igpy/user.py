import logging
from .baseapi import BaseApi

class User:
    def __init__(self, username, session_id):
        self.baseapi = BaseApi(session_id=session_id)
        self.cache = dict()
        self.username = username

    def user_id(self):
        try:
            return self.cache['user_id']
        except KeyError:
            logging.info('Getting user ID of %s', self.username)
            user_id = self.baseapi.short_info(self.username, 'user')['id']
            self.cache['user_id'] = user_id
            return user_id

    def info(self):
        try:
            return self.cache['info']
        except KeyError:
            logging.info('Getting user info of %s', self.username)
            info = self.baseapi.user_info(self.user_id())
            self.cache['info'] = info
            return info

    def following(self):
        logging.info('Getting users followed by %s', self.username)
        following = self.baseapi.graphql_depaginate(
            query_hash='58712303d941c6855d4e888c5f0cd22f',
            variables={
                'id': self.user_id()
            }
        )
        return [user['username'] for user in following]

    def followers(self):
        logging.info('Getting followers of %s', self.username)
        followers = self.baseapi.graphql_depaginate(
            query_hash='37479f2b8209594dde7facb0d904896a',
            variables={
                'id': self.user_id()
            }
        )
        return [user['username'] for user in followers]

    def media(self):
        logging.info('Getting media of %s', self.username)
        media = self.baseapi.graphql_depaginate(
            query_hash='bd0d6d184eefd4d0ce7036c11ae58ed9',
            variables={
                'id': self.user_id()
            }
        )
        return [item['shortcode'] for item in media]
