# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2022-2023 Valory AG
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

"""On-chain tools configurations."""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, cast

from autonomy.chain.constants import (
    CustomAddresses,
    EthereumAddresses,
    GoerliAddresses,
    HardhatAddresses,
)


DEFAULT_LOCAL_RPC = "http://127.0.0.1:8545"
DEFAULT_LOCAL_CHAIN_ID = 31337
CUSTOM_CHAIN_RPC = "CUSTOM_CHAIN_RPC"
GOERLI_CHAIN_RPC = "GOERLI_CHAIN_RPC"
ETHEREUM_CHAIN_RPC = "ETHEREUM_CHAIN_RPC"


def _get_chain_id_for_custom_chain() -> Optional[int]:
    """Get chain if for custom chain from environment"""
    chain_id = os.environ.get("CUSTOM_CHAIN_ID")
    if chain_id is None:
        return None
    return int(chain_id)


class ChainType(Enum):
    """Chain types."""

    LOCAL = "local"
    CUSTOM = "custom_chain"
    GOERLI = "goerli"
    ETHEREUM = "ethereum"


ADDRESS_CONTAINERS = {
    ChainType.LOCAL: HardhatAddresses,
    ChainType.CUSTOM: CustomAddresses,
    ChainType.GOERLI: GoerliAddresses,
    ChainType.ETHEREUM: EthereumAddresses,
}


@dataclass
class ContractConfig:
    """Contract config class."""

    name: str
    contracts: Dict[ChainType, str]


@dataclass
class ChainConfig:
    """Chain config"""

    chain_type: ChainType
    rpc: Optional[str]
    chain_id: Optional[int]


class ChainConfigs:  # pylint: disable=too-few-public-methods
    """Name space for chain configs."""

    local = ChainConfig(
        chain_type=ChainType.LOCAL,
        rpc=DEFAULT_LOCAL_RPC,
        chain_id=DEFAULT_LOCAL_CHAIN_ID,
    )

    custom_chain = ChainConfig(
        chain_type=ChainType.CUSTOM,
        rpc=os.environ.get(CUSTOM_CHAIN_RPC),
        chain_id=_get_chain_id_for_custom_chain(),
    )

    goerli = ChainConfig(
        chain_type=ChainType.GOERLI,
        rpc=os.environ.get(GOERLI_CHAIN_RPC),
        chain_id=5,
    )

    ethereum = ChainConfig(
        chain_type=ChainType.ETHEREUM,
        rpc=os.environ.get(ETHEREUM_CHAIN_RPC),
        chain_id=1,
    )

    _rpc_env_vars = {
        ChainType.CUSTOM: CUSTOM_CHAIN_RPC,
        ChainType.GOERLI: GOERLI_CHAIN_RPC,
        ChainType.ETHEREUM: ETHEREUM_CHAIN_RPC,
    }

    @classmethod
    def get(cls, chain_type: ChainType) -> ChainConfig:
        """Return chain config for given chain type."""

        return cast(ChainConfig, getattr(cls, chain_type.value))

    @classmethod
    def get_rpc_env_var(cls, chain_type: ChainType) -> Optional[str]:
        """Return chain config for given chain type."""

        return cls._rpc_env_vars.get(chain_type)


class ContractConfigs:  # pylint: disable=too-few-public-methods
    """A namespace for contract configs."""

    component_registry = ContractConfig(
        name="component_registry",
        contracts={
            chain_type: container.get("component_registry")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    agent_registry = ContractConfig(
        name="agent_registry",
        contracts={
            chain_type: container.get("agent_registry")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    service_registry = ContractConfig(
        name="service_registry",
        contracts={
            chain_type: container.get("service_registry")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    service_manager = ContractConfig(
        name="service_manager",
        contracts={
            chain_type: container.get("service_manager")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    registries_manager = ContractConfig(
        name="registries_manager",
        contracts={
            chain_type: container.get("registries_manager")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    gnosis_safe_proxy_factory = ContractConfig(
        name="gnosis_safe_proxy_factory",
        contracts={
            chain_type: container.get("gnosis_safe_proxy_factory")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    gnosis_safe_same_address_multisig = ContractConfig(
        name="gnosis_safe_same_address_multisig",
        contracts={
            chain_type: container.get("gnosis_safe_same_address_multisig")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    service_registry_token_utility = ContractConfig(
        name="service_registry_token_utility",
        contracts={
            chain_type: container.get("service_registry_token_utility")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    multisend = ContractConfig(
        name="multisend",
        contracts={
            chain_type: container.get("multisend")
            for chain_type, container in ADDRESS_CONTAINERS.items()
        },
    )

    @classmethod
    def get(cls, name: str) -> ContractConfig:
        """Return chain config for given chain type."""
        return cast(ContractConfig, getattr(cls, name))
