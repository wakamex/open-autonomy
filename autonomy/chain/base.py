# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
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

"""Chain interaction base classes."""

import json
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional

from aea.crypto.base import Crypto, LedgerApi

from autonomy.chain.config import ContractConfig
from autonomy.data import DATA_DIR


ABI_DIR = DATA_DIR / "abis"

ContractInterfaceType = Any


def get_abi(filename: str) -> Dict:
    """Service contract ABI."""
    with (ABI_DIR / filename).open(mode="r", encoding="utf-8") as fp:
        return json.load(fp=fp)


class BaseContract:  # pylint: disable=too-few-public-methods
    """Base contract interface."""

    _contract_interface: ContractInterfaceType

    def __init__(
        self, ledger_api: LedgerApi, contract_config: ContractConfig, crypto: Crypto
    ) -> None:
        """Initialize contract interface."""

        self.ledger_api = ledger_api
        self.crypto = crypto

        self._contract_interface = ledger_api.api.eth.contract(
            address=contract_config.contract_address,
            abi=get_abi(
                filename=contract_config.abi_file,
            ),
        )

    @property
    def contract(
        self,
    ) -> ContractInterfaceType:
        """Contract interface."""

        return self._contract_interface


class RegistryManager(BaseContract):
    """Registry manager contract interface."""

    class UnitType(Enum):
        """Unit type."""

        COMPONENT = 0
        AGENT = 1

    def create(
        self,
        component_type: UnitType,
        metadata_hash: str,
        owner: Optional[str] = None,
        dependencies: Optional[List[int]] = None,
    ) -> None:
        """Create component."""

        owner = owner or self.crypto.address
        tx_hash = self._contract_interface.functions.create(
            unitType=component_type.value,
            unitOwner=owner,
            unitHash=metadata_hash,
            dependencies=(dependencies or []),
        ).transact({"from": owner})

        self.ledger_api.api.eth.wait_for_transaction_receipt(tx_hash)


class ComponentRegistry(BaseContract):
    """Component registry contract interface."""

    def get_create_unit_event_filter(
        self,
    ) -> Iterable[Dict]:
        """Returns `CreateUnit` event filter."""
        return self._contract_interface.events.CreateUnit.createFilter(
            fromBlock="latest"
        ).get_all_entries()
