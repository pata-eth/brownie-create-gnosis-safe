from brownie import accounts, network, config, interface
from scripts.utils import get_safe_create_data, get_safe_owners
from web3 import Web3
import secrets

threshold = 1

amountToFund = Web3.toWei(0.1, "ether")


def main():

    owners = get_safe_owners()

    GnosisSafeMaster = interface.IGnosisSafe(
        config["networks"][network.show_active()]["gnosis_safe"]
    )

    safeTxData = get_safe_create_data(GnosisSafeMaster, owners, threshold)

    GnosisSafeProxy = interface.IGnosisSafeProxyFactory(
        config["networks"][network.show_active()]["gnosis_proxy_factory"]
    )

    # saltNonce Nonce that will be used to generate the salt to calculate the address of the new proxy contract.
    saltNonce = secrets.SystemRandom().randint(0, 2**256 - 1)

    safe_create_tx = GnosisSafeProxy.createProxyWithNonce(
        GnosisSafeMaster.address, safeTxData, saltNonce, {"from": owners[0]}
    )

    safe_create_tx.info()

    safeAddress = safe_create_tx.events["ProxyCreation"]["proxy"]

    fund_tx = owners[0].transfer(to=safeAddress, amount=amountToFund)

    fund_tx.info()

    # Create an account object from the address of the newly created safe
    safeAccount = accounts.at(safeAddress, True)

    # Check that it was funded as planned
    fundedAmount = Web3.fromWei(safeAccount.balance(), "ether")

    print(
        f"The Gnosis Safe was created at '{safeAddress}' and has been funded with {fundedAmount} ether."
    )
