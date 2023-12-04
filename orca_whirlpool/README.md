# Orca Whirlpool AMM contract

## Set up the environment inside the directory

- Run the following commands inside the directory:
  - `pipenv --python 3.11 && pipenv shell`
  - `pip install open-aea[all]`
  - `pip install open-aea-ledger-solana`
  - `pip install zstandard --force-reinstall` (This is related to M1 Mac)

Housekeeping and Setup
- Use the following command to find out where pipenv is located:
  - `pipenv --venv` (Add this to .vscode settings and launch for testing)
- For testing errors, `pytest --collect-only` is your friend

Set interpreter to your venv environment from the above command

Notes about the protocol

UI: [Orca](https://www.orca.so/)
Docs: [Orca Documentation](https://docs.orca.so/)
Analytics: [Gecko Terminal - Orca Pools](https://www.geckoterminal.com/solana/orca/pools)
