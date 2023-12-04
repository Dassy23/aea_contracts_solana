# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023 dassy23
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

from typing import Any, Optional
from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from attr import attrs

import time
from aea_ledger_solana import (
    SolanaCrypto, SolanaApi, Context, PublicKey)
import multiprocessing as mp
import json

class OrcaContract(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("dassy23/whirlpool:0.1.0")

    @classmethod
    def get_deposit_transaction(
        cls,
        ledger_api: SolanaApi,
        **kwargs: Any
    ) -> JSONLike:
        """Get the deposit transaction."""

        if ledger_api.identifier == SolanaApi.identifier:

            solana_api = ledger_api

            return True

