from locale import normalize
from brownie import ZERO_ADDRESS, accounts, network, config, web3, Contract, convert
from eth_utils import is_checksum_address
import click

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["arbitrum-main-fork"]

LIVE_BLOCKCHAIN_ENVIRONMENTS = ["arbitrum-main", "arbitrum-test"]

BLOCKCHAIN_ENVIRONMENTS = LOCAL_BLOCKCHAIN_ENVIRONMENTS + LIVE_BLOCKCHAIN_ENVIRONMENTS

EMPTY_DATA = "0x"


def get_safe_owners():

    assert network.show_active() in BLOCKCHAIN_ENVIRONMENTS, (
        "The network must be either of the following: %s" % BLOCKCHAIN_ENVIRONMENTS
    )

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        owner1 = accounts.at(config["wallets"]["owner1"], True)

    if network.show_active() in LIVE_BLOCKCHAIN_ENVIRONMENTS:
        brownieAccts = click.Choice(accounts.load())
        owner1 = accounts.load(click.prompt("Select Safe Owner 1", type=brownieAccts))

    owner2 = accounts.at(config["wallets"]["owner2"], True)

    print(f"owner1 address is [{owner1.address}]")
    print(f"owner2 address is [{owner2.address}]")
    return [owner1, owner2]


def get_safe_create_data(GnosisSafeMaster: Contract, owners: list, threshold: int):

    assert len(owners) > 0, "We need at least one owner."

    assert threshold > 0, "'threshold' must be a positive integer"

    assert (
        len(owners) >= threshold
    ), "'threshold' must be equal or less than the number of safe owners."

    ii = len(owners)

    ownerAddress = []

    for ii in owners:
        ownerAddress.append(ii.address)

    # /// @dev Setup function sets initial storage of contract.
    # /// @param _owners List of Safe owners.
    # /// @param _threshold Number of required confirmations for a Safe transaction.
    # /// @param to Contract address for optional delegate call.
    # /// @param data Data payload for optional delegate call.
    # /// @param fallbackHandler Handler for fallback calls to this contract
    # /// @param paymentToken Token that should be used for the payment (0 is ETH)
    # /// @param payment Value that should be paid
    # /// @param paymentReceiver Adddress that should receive the payment (or 0 if tx.origin)

    safeTxData = GnosisSafeMaster.setup.encode_input(
        ownerAddress,
        threshold,
        ZERO_ADDRESS,
        EMPTY_DATA,
        config["networks"][network.show_active()]["gnosis_fallback"],
        ZERO_ADDRESS,
        0,
        ZERO_ADDRESS,
    )

    return safeTxData
