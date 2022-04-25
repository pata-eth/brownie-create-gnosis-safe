# Creating and Funding a Gnosis Safe<!-- omit in toc --> 

We create a Gnosis Safe with two owners and a threshold of 1. Such a setup
provides private key redundancy, which is convenient in case you lose access to
one account. A warning is warranted, however, as a hacker only needs to hack one
account to drain your safe. You've been warned!

We create and fund the safe in Arbitrum, although the code should also work for
Ethereum mainnet and other Ethereum L2 roll-ups.

The owner creating and funding the safe must have enough ETH in all target blockchains: Arbitrum Mainnet, Arbitrum Testnet and Arbitrum Fork. Funding the owner account is beyond the scope of this project.

After you are done with the [Developer Setup](#development-setup), you can run
the project on the forked network with:

```bash
workon gnosis_safe_env
brownie run scripts/create_and_fund.py
```

## Developer Setup<!-- omit in toc --> 

- [Create Python Environment](#create-python-environment)
- [Set your `.env` file](#set-your-env-file)
- [Updating your Brownie networks config](#updating-your-brownie-networks-config)

### Create Python Environment

To run this project you'll need ganache and brownie. For convenience,
you can install the same python environment we used following the instructions below. 

```bash
# Assumes that 'virtualenvwrapper' is properly installed.
#
# Create Python virtual environment
mkvirtualenv gnosis_safe_env
pip install -r requirements.txt --no-deps
```

Brownie v1.18.1 has a strict dependency on typing-extensions==4.0.1, which makes
the package environment inconsistent if you install as instructed. 
Alternatively, you can git clone the eth-brownie project and install from there 
after making that dependency more flexible.

```bash
# shows that the environment is inconsistent as there is conflict of brownie with typing-extensions. This conflict should not affect functionality.
pip check
```

To activate the environment:

```bash
workon gnosis_safe_env
```

To deactivate:

```
deactivate
```

Make sure your IDE uses `gnosis_safe_env` to avoid confusing the linter. If you
use Visual Code, you'll need to restart it for the environment to become available.

### Set your `.env` file

Create `.env` at the project's root and include:

```bash
SAFE_OWNER_1=<OWNER1_ADDRESS>
SAFE_OWNER_2=<OWNER2_ADDRESS>
```

### Updating your Brownie networks config

The following commands add the brownie network configurations needed:

```bash
brownie networks add Arbitrum arbitrum-main name=Mainnet host=https://arb1.arbitrum.io/rpc chainid=42161 explorer=https://api.arbiscan.io/api multicall2=0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858

brownie networks add Arbitrum arbitrum-test name=Testnet host=https://rinkeby.arbitrum.io/rpc chainid=421611 explorer=https://testnet.arbiscan.io/api multicall2=0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858

brownie networks add development arbitrum-main-fork name="Arbitrum Mainnet Fork" cmd=ganache-cli host=http://127.0.0.1 fork=arbitrum-main evm_version=istanbul mnemonic=brownie gas_limit=12000000 port=8545 accounts=10

# Check that the networks were succesfully declared:
brownie networks list
```