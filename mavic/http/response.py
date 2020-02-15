# -*- coding:utf-8 -*-


class Response(object):
    """ Response """

    def __init__(self, url, status=200, headers=None, body=b'', encoding=None, request=None):
        self._set_url(url)
        self.status = int(status)
        self.headers = dict(headers) if headers else {}
        self._set_body(body)
        self._encoding = encoding
        self.request = request

    @property
    def meta(self):
        try:
            return self.request.meta
        except AttributeError:
            raise AttributeError("Response.meta not available")

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        if isinstance(url, str):
            self._url = url
        else:
            raise TypeError('%s url must be str, got %s:' % (type(self).__name__, type(url).__name__))

    url = property(_get_url, _set_url)

    def _get_body(self):
        return self._body

    def _set_body(self, body):
        if body is None:
            self._body = b''
        elif not isinstance(body, bytes):
            raise TypeError('Response body must be bytes.')
        else:
            self._body = body

    body = property(_get_body, _set_body)

    @property
    def text(self, errors='strict'):
        return self._body.decode(self._encoding, errors=errors)

    def __str__(self):
        return "<%d %s>" % (self.status, self._url)

    __repr__ = __str__
