from django.contrib.sessions.backends.base import SessionBase, CreateError
from docb.exceptions import QueryError

from .models import Session


class SessionStore(SessionBase):
    """
    Implements DynamoDB session store.
    """

    def load(self):
        """
        Loads session data from DynamoDB, runs it through the session
        data de-coder (base64->dict), sets ``self.session``.
        :rtype: dict
        :returns: The de-coded session data, as a dict.
        """
        try:
            s = Session.objects().get({'session_key': self.session_key})
            return self.decode(s.data)
        except QueryError:
            self.create()
            return {}

    def exists(self, session_key):
        """
        Checks to see if a session currently exists in DynamoDB.
        :rtype: bool
        :returns: ``True`` if a session with the given key exists in the DB,
            ``False`` if not.
        """
        try:
            Session.objects().get({'session_key': self.session_key})
            return True
        except QueryError:
            return False

    def create(self):
        """
        Creates a new entry in DynamoDB. This may or may not actually
        have anything in it.
        """

        while True:
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            self._session_cache = {}
            return

    def get_or_create_session(self):
        try:
            return Session.objects().get({'session_key': self.session_key})
        except QueryError:
            s = Session(session_key=self.session_key)
            s.save()
            return s

    def save(self, must_create=False):
        """
        Saves the current session data to the database.
        :keyword bool must_create: If ``True``, a ``CreateError`` exception
            will be raised if the saving operation doesn't create a *new* entry
            (as opposed to possibly updating an existing entry).
        :raises: ``CreateError`` if ``must_create`` is ``True`` and a session
            with the current session key already exists.
        """

        # If the save method is called with must_create equal to True, I'm
        # setting self._session_key equal to None and when
        # self.get_or_create_session_key is called the new
        # session_key will be created.
        if must_create:
            self._session_key = None

        self._get_or_create_session_key()

        s = self.get_or_create_session()
        s.data = self.encode(self._get_session(no_load=must_create))
        s.save()

    def delete(self, session_key=None):
        """
        Deletes the current session, or the one specified in ``session_key``.
        :keyword str session_key: Optionally, override the session key
            to delete.
        """

        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            s = Session.objects().get({'session_key': session_key})
            s.delete()
        except QueryError:
            pass
