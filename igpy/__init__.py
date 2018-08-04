"""
igpy is a simple object-oriented API for instagram using the end-user GraphQL
API.
"""
import logging

from .user import User
from .media import Media

class Api:
    """Preferred API class for end users (unifies authentication and logging)."""
    def __init__(self, session_id, loglevel=logging.WARNING):
        logging.basicConfig(format='%(levelname)s: %(message)s', level=loglevel)
        self.session_id = session_id

    def user(self, username):
        """Returns the user API with given authentication and logging settings."""
        return User(username, self.session_id)

    def media(self, shortcode):
        """Returns the user API with given authentication and logging settings."""
        return Media(shortcode, self.session_id)
