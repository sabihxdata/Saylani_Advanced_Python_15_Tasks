
from dataclasses import dataclass


# Immutable transaction record
@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    action: str
    amount: float
    resulting_balance: float


class Account:

    def __init__(self, account_number, owner, balance=0):

        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.account_number = account_number
        self.owner = owner
        self.__balance = balance
        self.__transactions = []

    # Read-only balance
    @property
    def balance(self):
        return self.__balance

    # Read-only transaction history
    @property
    def transactions(self):
        return tuple(self.__transactions)

    # Update account and record transaction
    def _apply_transaction(self, transaction):

        if transaction.action in ("Deposit", "Transfer In"):
            self.__balance += transaction.amount

        elif transaction.action in ("Withdrawal", "Transfer Out"):
            self.__balance -= transaction.amount

        self.__transactions.append(transaction)

    # Save account state for atomic transfers
    def _snapshot(self):
        return self.__balance, len(self.__transactions)

    # Restore account state if a transfer fails
    def _restore(self, snapshot):
        self.__balance = snapshot[0]
        del self.__transactions[snapshot[1]:]


class Bank:

    def __init__(self):
        self.accounts = {}
        self.transaction_counter = 1

    # Create account
    def create_account(self, account_number, owner, balance=0):

        if account_number in self.accounts:
            raise ValueError("Account already exists")

        account = Account(account_number, owner, balance)
        self.accounts[account_number] = account

        return account

    # Find account
    def get_account(self, account_number):

        if account_number not in self.accounts:
            raise ValueError("Account does not exist")

        return self.accounts[account_number]

    # Generate unique transaction ID
    def generate_transaction_id(self):

        transaction_id = "TXN" + str(self.transaction_counter)
        self.transaction_counter += 1

        return transaction_id

    # Validate amount
    def validate_amount(self, amount):

        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Amount must be a number")

        if amount <= 0:
            raise ValueError("Amount must be positive")

    # Deposit money
    def deposit(self, account_number, amount):

        account = self.get_account(account_number)
        self.validate_amount(amount)

        transaction_id = self.generate_transaction_id()

        transaction = Transaction(
            transaction_id,
            "Deposit",
            amount,
            account.balance + amount
        )

        account._apply_transaction(transaction)

        return transaction_id

    # Withdraw money
    def withdraw(self, account_number, amount):

        account = self.get_account(account_number)
        self.validate_amount(amount)

        if amount > account.balance:
            raise ValueError("Insufficient funds")

        transaction_id = self.generate_transaction_id()

        transaction = Transaction(
            transaction_id,
            "Withdrawal",
            amount,
            account.balance - amount
        )

        account._apply_transaction(transaction)

        return transaction_id

    # Transfer money atomically
    def transfer(self, from_account, to_account, amount):

        source = self.get_account(from_account)
        destination = self.get_account(to_account)

        if from_account == to_account:
            raise ValueError("Cannot transfer to the same account")

        self.validate_amount(amount)

        if amount > source.balance:
            raise ValueError("Insufficient funds")

        transaction_id = self.generate_transaction_id()

        # Prepare transaction records
        outgoing = Transaction(
            transaction_id,
            "Transfer Out",
            amount,
            source.balance - amount
        )

        incoming = Transaction(
            transaction_id,
            "Transfer In",
            amount,
            destination.balance + amount
        )

        # Take snapshots before updating either account
        source_snapshot = source._snapshot()
        destination_snapshot = destination._snapshot()

        try:
            source._apply_transaction(outgoing)
            destination._apply_transaction(incoming)

        except Exception:
            # Restore both accounts if anything fails
            source._restore(source_snapshot)
            destination._restore(destination_snapshot)
            raise

        return transaction_id

    # Print account statement
    def statement(self, account_number):

        account = self.get_account(account_number)

        print("\nACCOUNT STATEMENT")
        print("-" * 60)
        print("Account Number:", account.account_number)
        print("Owner:", account.owner)
        print("Current Balance:", account.balance)
        print("-" * 60)

        for transaction in account.transactions:
            print(transaction)


# MAIN PROGRAM

bank = Bank()

# Create two accounts
account_a = bank.create_account("A", "Ali", 1000)
account_b = bank.create_account("B", "Sara", 200)

print("INITIAL BALANCES")
print("Account A:", account_a.balance)
print("Account B:", account_b.balance)

# Transfer 350 from A to B
transaction_id = bank.transfer("A", "B", 350)

print("\nTRANSFER SUCCESSFUL")
print("Transaction ID:", transaction_id)

print("\nFINAL BALANCES")
print("Account A:", account_a.balance)
print("Account B:", account_b.balance)

# Print account statements
bank.statement("A")
bank.statement("B")


# ERROR TESTS

print("\nERROR TESTS")

try:
    bank.withdraw("A", 5000)
except ValueError as error:
    print("Withdrawal Error:", error)

try:
    bank.deposit("A", -100)
except ValueError as error:
    print("Deposit Error:", error)

try:
    bank.transfer("A", "C", 100)
except ValueError as error:
    print("Transfer Error:", error)

try:
    bank.transfer("A", "A", 100)
except ValueError as error:
    print("Same Account Error:", error)


# Check balances after rejected transactions
print("\nBALANCES AFTER ERROR TESTS")
print("Account A:", account_a.balance)
print("Account B:", account_b.balance)
