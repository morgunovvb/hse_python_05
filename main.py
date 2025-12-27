from datetime import datetime

class Account:
    def __init__(self, account_holder: str, balance: float = 0.0):
        self.holder = account_holder
        self._balance = balance
        self.operations_history = 

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        self._balance += amount
        operation = {
            'type': 'deposit',
            'amount': amount,
            'timestamp': datetime.now(),
            'new_balance': self._balance,
            'status': 'success'
        }
        self.operations_history.append(operation)

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if self._balance - amount < 0:
            operation = {
                'type': 'withdraw',
                'amount': amount,
                'timestamp': datetime.now(),
                'new_balance': self._balance,
                'status': 'fail'
            }
            self.operations_history.append(operation)
            return False
        self._balance -= amount
        operation = {
            'type': 'withdraw',
            'amount': amount,
            'timestamp': datetime.now(),
            'new_balance': self._balance,
            'status': 'success'
        }
        self.operations_history.append(operation)
        return True

    def get_balance(self) -> float:
        return self._balance

    def get_history(self) -> list:
        return [op for op in self.operations_history]


class CreditAccount(Account):
    def __init__(self, account_holder: str, balance: float, credit_limit: float):
        super().__init__(account_holder, balance)
        if balance < -credit_limit:
            raise ValueError(f"Начальный баланс не может быть ниже {-credit_limit}")
        self.credit_limit = credit_limit

    def get_available_credit(self) -> float:
        available = self.credit_limit - self._balance
        return available if available >= 0 else 0

    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        
        # Проверяем, не превышает ли сумма кредитный лимит
        if (self._balance + amount) > self.credit_limit:
            operation = {
                'type': 'withdraw',
                'amount': amount,
                'timestamp': datetime.now(),
                'new_balance': self._balance,
                'status': 'fail',
                'used_credit': True
            }
            self.operations_history.append(operation)
            return False

        self._balance += amount
        operation = {
            'type': 'withdraw',
            'amount': amount,
            'timestamp': datetime.now(),
            'new_balance': self._balance,
            'status': 'success',
            'used_credit': False
        }
        self.operations_history.append(operation)
        return True
