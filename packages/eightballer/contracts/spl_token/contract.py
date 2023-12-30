# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the scaffold contract definition."""

from dataclasses import dataclass

from aea.common import JSONLike
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from packages.eightballer.contracts.spl_token import PUBLIC_ID

@dataclass
class SplToken:
    address: str
    symbol: str
    decimals: int


    def to_human(self, amount):
        return amount / 10**self.decimals
    
    def to_machine(self, amount):
        return int(amount * 10**self.decimals)
        


class SolanaProgramLibraryToken(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PUBLIC_ID

    @classmethod
    def get_token(
        cls, ledger_api: LedgerApi, contract_address: str, symbol: str,
    ) -> JSONLike:
        """
        Handler method for the 'GET_STATE' requests.

        Implement this method in the sub class if you want
        to handle the contract requests manually.

        :param ledger_api: the ledger apis.
        :param contract_address: the contract address.
        :param kwargs: the keyword arguments.
        :return: the tx  # noqa: DAR202
        """

        decimals = ledger_api.get_state(contract_address).data.parsed['info']['decimals']
        token = SplToken(address=contract_address, symbol=symbol, decimals=decimals)
        return token.__dict__
