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
    SolanaCrypto, SolanaApi, Context, Pubkey)
import multiprocessing as mp
import json
import struct
import math


class OrcaContract(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("dassy23/orca_whirlpool:0.1.0")

    @classmethod
    def get_swap_transaction(
        cls,
        ledger_api: SolanaApi,
        contract_address,
        minta,
        mintb,
        **kwargs: Any
    ) -> JSONLike:
        """Get the deposit transaction."""

        if ledger_api.identifier == SolanaApi.identifier:

            solana_api = ledger_api
            seeds= [
                bytes("whirlpool".encode('utf-8')),
                bytes(Pubkey.from_string("2LecshUwdy9xi7meFgHtFJQNSKk4KdTrcpvaB56dP2NQ")),
                bytes(Pubkey.from_string(minta)),
                bytes(Pubkey.from_string(mintb)),
                bytes(struct.pack("<H", 1))  # "<H" specifies little-endian unsigned short (2 bytes), tickspacing options are - 1,8,64,128
            ]
            whirlpool = Pubkey.find_program_address(seeds,program_id=Pubkey.from_string(contract_address))
            state = ledger_api.get_state(str(whirlpool[0]))
            instance = cls.get_instance(ledger_api, contract_address)
            whirlpool_instance = instance['program']
            pool = whirlpool_instance.coder.accounts.decode(state.data)
            mintinfoA = ledger_api.get_state(str(pool.token_mint_a))
            mintinfoB = ledger_api.get_state(str(pool.token_mint_b))
            vaultA = ledger_api.get_state(str(pool.token_vault_a))
            vaultB = ledger_api.get_state(str(pool.token_vault_b))
            rewardInfo = []
            for info in pool.reward_infos:
                if str(info.mint) != "11111111111111111111111111111111" and str(info.vault) != "11111111111111111111111111111111":
                    vault = ledger_api.get_state(str(info.vault))
                    rewardInfo.append({
                        "data":info,
                        "initialized":True,
                        "vaultAmount":int(vault.data.parsed['info']['tokenAmount']['amount'])
                    })
            swapMintKey = str(pool.token_mint_a)
            tickCurrentIndex = pool.tick_current_index
            tickSpacing = pool.tick_spacing
            atob = True
            contract = Pubkey.from_string(contract_address)
            whirlpool_address = str(whirlpool[0])
            
            shift = 0 if atob else tickSpacing
            offset = 0
            tickArrayAddresses = []
            for i in range(3):
                tickIndex = tickCurrentIndex+shift
                realIndex = math.floor(tickIndex / tickSpacing / 88)
                startTickIndex = (realIndex + offset) * tickSpacing * 88
                ticksInArray = 88 * tickSpacing
                minTickIndex = -443636 - ((-443636 % ticksInArray) + ticksInArray)
                if startTickIndex < minTickIndex:
                    raise ValueError(f"startTickIndex is too small - - {startTickIndex}")
                if startTickIndex > 443636:
                    raise ValueError(f"startTickIndex is too large - {startTickIndex}")
                
                seeds= [
                    bytes("tick_array".encode('utf-8')),
                    bytes(whirlpool[0]),
                    bytes(str(startTickIndex).encode('utf-8')),
                ]
                tickPDA = Pubkey.find_program_address(seeds,program_id=Pubkey.from_string(contract_address))
                tickArrayAddresses.append(str(tickPDA[0]))
                offset = offset - 1 if atob else offset + 1;
            
            tickData = []
            for address in tickArrayAddresses:
                data = ledger_api.get_state(address)
                tickData.append({
                        "address":address,
                        "data":data
                        })
            sqrtPriceLimit = 4295048016 if atob else 79226673515401279992447579055

            ## simulate swap
            
            #slice data 0-2?


            requestToIndices = []

            #https://github.com/orca-so/whirlpools/blob/3a15880bd6bf8499059045ebe8eadd8715278345/sdk/src/utils/public/swap-utils.ts#L159
                
            # still a WIP


                    





            print(whirlpool[0].__str__())

            print()


            return True

