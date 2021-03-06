from iota import *
from requests.exceptions import ConnectionError

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IotaWrapper:
    def __init__(self, url, seed):
        self.__url = url
        self.__seed = seed
        self.__node_info = None
        self.__api = None
        self.__tag = "xCarx"

    def connect(self):
        try:
            self.__api = Iota(self.__url, self.__seed)
            self.__node_info = self.__api.get_node_info()
            logger.info("Node information: {info}".format(info=self.__node_info))
        except ConnectionError as e:
            logger.exception("Connection error: {e}".format(e=e))
        except BadApiResponse as e:
            logger.exception("Bad Api Response: {e}".format(e=e))
        else:
            logger.info("Connected.")
            return self.__node_info

    def get_retarded_tag(self):
        # Don't ask, I've wasted 2 hours of making this work
        # IOTA API is great. Seriously.
        tryte_tag = TryteString.from_string(self.__tag)
        while len(tryte_tag) < 27:
            tryte_tag += "9"
        return tryte_tag

    def create_transfers(self, address, message, value=0):
        return [
            ProposedTransaction(
                # All hail the glory of IOTA and their dummy transactions for tag retrieval.
                address=Address("SQAZ9SXUWMPPVHKIWMZWZXSFLPURWIFTUEQCMKGJAKODCMOGCLEAQQQH9BKNZUIFKLOPKRVHDJMBTBFYW"),
                value=0
            ),
            ProposedTransaction(
                address=Address(address),
                value=value,
                message=message,
                tag=self.get_retarded_tag()
            )
        ]

    def send_transfer(self, transfers, inputs=[], depth=3, min_weight_magnitude=16):
        try:
            if transfers is None:
                logger.error("You need to specify transfers dummy!")
                return
            response = self.__api.send_transfer(
                depth=depth,
                min_weight_magnitude=min_weight_magnitude,
                inputs=inputs,
                transfers=transfers
            )
        except ConnectionError as e:
            logger.exception("Connection error: {e}".format(e=e))
        except BadApiResponse as e:
            logger.exception("Bad Api Response: {e}".format(e=e))
        else:
            return response

    # For now looking only using tag, for hackathon needs
    def find_transactions(self, tags):
        try:
            response = self.__api.find_transactions(tags=tags)
        except ConnectionError as e:
            logger.exception("Connection error: {e}".format(e=e))
        except BadApiResponse as e:
            logger.exception("Bad Api Response: {e}".format(e=e))
        else:
            return response
