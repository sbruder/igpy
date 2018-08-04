igpy - instagram for python
===========================

igpy is a simple object-oriented API for instagram using the end-user GraphQL
API.

It works by using the graphql api utilized by the instagram web client.
Authentication is done via the `sessionid` cookie of the instagram web client.

Installation
------------

```
pip3 install igpy
```

How to obtain the session id
----------------------------

Open a browser (Firefox or Chrome), go to the instagram website and log in.

### Firefox

Open the web developer tools (F12), open the *Web Storage* tab, open the
*Cookies* accordion menu and select `https://www.instagram.com`. You should be
able to copy the value of the `sessionid` cookie in the table on the left side.

### Chrome/Chromium

Open the web developer tools (F12), open the *Application* tab, open the
*Cookies* accordion menu and select `https://www.instagram.com`. You should be
able to copy the value of the `sessionid` cookie in the table on the left side.


Examples
--------

```python
import igpy
ig = igpy.Api(
    session_id='your session id',
    loglevel=20 # set log level to info (https://docs.python.org/3/library/logging.html#logging-levels)
)

user = ig.user('unsplash')
print(user.following()) # print the users unsplash is following
media = ig.media('Blx7dvdhbUB')
print(media.likes()) # print the users who liked the picture with the shortcode Blx7dvdhbUB
```

License
-------

[The MIT License](https://opensource.org/licenses/MIT). For more details,
please see the `LICENSE` file

Legal
-----

This code is in no way affiliated with, authorized, maintained, sponsored or
endorsed by Instagram/Facebook or any of its affiliates or subsidiaries. This
is an independent and unofficial software. Use at your own risk.
