import requests
import logging

from ..Transaction import Transaction
from ..RedeError import RedeError

logger = logging.getLogger(__name__)


class TransactionService:
    GET = "get"
    POST = "post"
    PUT = "put"

    def __init__(self, store):
        """

        :type store: `erede.Store.Store`
        """
        self.store = store

    def execute(self):
        raise NotImplementedError("Not implemented")

    def get_uri(self):
        return "{}/transactions".format(self.store.environment.endpoint)

    def send_request(self, method, body=None):
        headers = {'User-Agent': "eRede/1.0 (SDK; Python) Store/{}".format(self.store.filliation),
                   "Accept": "application/json",
                   "Content-Type": "application/json"}

        logger.debug(body)
        response = getattr(requests, method)(self.get_uri(),
                                             auth=(self.store.filliation, self.store.token),
                                             data=body,
                                             headers=headers)
        '''
        :type response: `requests.Response`
        '''

        if response.status_code >= 400:
            error = response.json()

            raise RedeError(error.get("returnMessage", "opz"), error.get("returnCode", 0))

        logger.info(response.json())
        return Transaction.unserialize(response.json())
