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

import base64
import json
from typing import Any

import requests
from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea_ledger_solana import SolanaApi
from solders.transaction import VersionedTransaction


class JupitarSwapContract(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("dassy23/jupitar_swap:0.1.0")

    @classmethod
    def get_swap_transaction(
        cls,
        ledger_api: SolanaApi,
        authority,
        input_mint,
        output_mint,
        amount,
        slippageBps,
        **kwargs: Any,
    ) -> JSONLike:
        """Get the deposit transaction."""

        if ledger_api.identifier == SolanaApi.identifier:
            url = f"https://quote-api.jup.ag/v6/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps={slippageBps}"
            resp = requests.get(url)
            quote = resp.json()
            swap_transaction = requests.post(
                "https://quote-api.jup.ag/v6/swap",
                headers={"Content-Type": "application/json"},
                json={
                    "quoteResponse": quote,
                    "userPublicKey": authority,
                    "wrapAndUnwrapSol": True,
                },
            ).json()

            swapTransactionBuf = base64.b64decode(swap_transaction["swapTransaction"])
            tx = VersionedTransaction.from_bytes(swapTransactionBuf)
            return json.loads(tx.to_json())
