from abc import ABC, abstractmethod
from datetime import datetime


# Classes
class AccountsIterator:  # ContasIterador
    def __init__(self, accounts):  # contas
        self.accounts = accounts  # contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            account = self.accounts[self._index]  # conta
            return f"""\
            Agência:\t{account.agency}  # agência
            Número:\t\t{account.number}  # número
            Titular:\t{account.client.name}  # titular
            Saldo:\t\tR$ {account.balance:.2f}  # saldo
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Client(ABC):  # Cliente
    def __init__(self, address):  # endereço
        self.address = address  # endereço
        self.accounts = []  # contas

    def perform_transaction(self, account, transaction):  # realizar_transacao
        transaction.register(account)  # registrar

    def add_account(self, account):  # adicionar_conta
        self.accounts.append(account)  # contas

    @classmethod
    @abstractmethod
    def create_user(cls, name, birth_date, cpf, address):  # criar_usuario
        pass


class Individual(Client):  # PessoaFisica
    def __init__(self, name, birth_date, cpf, address):  # nome, data_nascimento, cpf, endereco
        super().__init__(address)  # endereco
        self.name = name  # nome
        self.birth_date = birth_date  # data_nascimento
        self.cpf = cpf

    @classmethod
    def create_user(cls, name, birth_date, cpf, address):  # criar_usuario
        return cls(name, birth_date, cpf, address)  # nome, data_nascimento, cpf, endereco


class Account(ABC):  # Conta
    def __init__(self, number, client):  # numero, cliente
        self._balance = 0  # saldo
        self._number = number  # numero
        self._agency = "0001"  # agencia
        self._client = client  # cliente
        self._history = History()  # historico

    @classmethod
    def new_account(cls, client, number):  # nova_conta
        return cls(number, client)  # numero, cliente

    @property
    def balance(self):  # saldo
        return self._balance

    @property
    def number(self):  # numero
        return self._number

    @property
    def agency(self):  # agencia
        return self._agency

    @property
    def client(self):  # cliente
        return self._client

    @property
    def history(self):  # historico
        return self._history

    def withdraw(self, amount):  # sacar, valor
        balance = self.balance  # saldo
        exceeded_balance = amount > balance  # excedeu_saldo

        if exceeded_balance:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif amount > 0:
            self._balance -= amount  # saldo
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def deposit(self, amount):  # depositar, valor
        if amount > 0:
            self._balance += amount  # saldo
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class CheckingAccount(Account):  # ContaCorrente
    def __init__(self, number, client, limit=500, withdrawal_limit=3):  # numero, cliente, limite, limite_saques
        super().__init__(number, client)  # numero, cliente
        self._limit = limit  # limite
        self._withdrawal_limit = withdrawal_limit  # limite_saques

    @classmethod
    def new_account(cls, client, number, limit, withdrawal_limit):  # nova_conta
        return cls(number, client, limit, withdrawal_limit)  # numero, cliente, limite, limite_saques

    def withdraw(self, amount):  # sacar, valor
        num_withdrawals = len(
            [transaction for transaction in self.history.transactions if transaction["type"] == Withdrawal.__name__]
        )  # numero_saques

        exceeded_limit = amount > self._limit  # excedeu_limite
        exceeded_withdrawals = num_withdrawals >= self._withdrawal_limit  # excedeu_saques

        if exceeded_limit:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif exceeded_withdrawals:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().withdraw(amount)  # sacar, valor

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agency}  # agencia
            C/C:\t\t{self.number}  # numero
            Titular:\t{self.client.name}  # cliente.nome
        """


class History:  # Historico
    def __init__(self):
        self._transactions = []  # transacoes

    @property
    def transactions(self):  # transacoes
        return self._transactions

    def add_transaction(self, transaction):  # adicionar_transacao
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,  # tipo
                "amount": transaction.amount,  # valor
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),  # data
            }
        )


class Transaction(ABC):  # Transacao
    @property
    @abstractmethod
    def amount(self):  # valor
        pass

    @abstractmethod
    def register(self, account):  # registrar
        pass


class Withdrawal(Transaction):  # Saque
    def __init__(self, amount):  # valor
        self._amount = amount  # valor

    @property
    def amount(self):  # valor
        return self._amount

    def register(self, account):  # registrar
        success = account.withdraw(self.amount)  # sacar, valor

        if success:
            account.history.add_transaction(self)  # historico, adicionar_transacao


class Deposit(Transaction):  # Deposito
    def __init__(self, amount):  # valor
        self._amount = amount  # valor

    @property
    def amount(self):  # valor
        return self._amount

    def register(self, account):  # registrar
        success = account.deposit(self.amount)  # depositar, valor

        if success:
            account.history.add_transaction(self)  # historico, adicionar_transacao


# Funções
def log_transaction(func):  # log_transacao
    def wrapper(*args, **kwargs):
        print(f"Executando {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"{func.__name__} executado com sucesso!")
        return result
    return wrapper


def filter_client(cpf, clients):  # filtrar_cliente
    for client in clients:
        if client.cpf == cpf:
            return client
    return None


def retrieve_client_account(client):  # recuperar_conta_cliente
    if client.accounts:
        return client.accounts[0]
    print("\n@@@ Cliente não possui conta! @@@")
    return None


@log_transaction  # log_transacao
def withdraw(clients):  # sacar, clientes
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)  # cliente, filtrar_cliente

    if not client:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    amount = float(input("Informe o valor do saque: "))  # valor
    transaction = Withdrawal(amount)  # Saque

    account = retrieve_client_account(client)  # conta, recuperar_conta_cliente
    if not account:
        return

    client.perform_transaction(account, transaction)  # realizar_transacao


@log_transaction  # log_transacao
def deposit(clients):  # depositar, clientes
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)  # cliente, filtrar_cliente

    if not client:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    amount = float(input("Informe o valor do depósito: "))  # valor
    transaction = Deposit(amount)  # Deposito

    account = retrieve_client_account(client)  # conta, recuperar_conta_cliente
    if not account:
        return

    client.perform_transaction(account, transaction)  # realizar_transacao


@log_transaction  # log_transacao
def display_statement(clients):  # exibir_extrato, clientes
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)  # cliente, filtrar_cliente

    if not client:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    account = retrieve_client_account(client)  # conta, recuperar_conta_cliente
    if not account:
        return

    print("\n================ EXTRATO ================")
    if not account.history.transactions:
        print("Não foram realizadas movimentações.")
    else:
        for transaction in account.history.transactions:
            print(f"{transaction['date']} - {transaction['type']}: R$ {transaction['amount']:.2f}")
    print(f"\nSaldo: R$ {account.balance:.2f}")
    print("==========================================")


def create_user(clients):  # criar_usuario
    name = input("Informe o nome do cliente: ")
    birth_date = input("Informe a data de nascimento (dd/mm/aaaa): ")
    cpf = input("Informe o CPF: ")
    address = input("Informe o endereço: ")
    
    if filter_client(cpf, clients):
        print("\n@@@ Cliente já existe! @@@")
        return

    client = Individual.create_user(name, birth_date, cpf, address)  # nome, data_nascimento, cpf, endereco
    clients.append(client)
    print("\n=== Usuário criado com sucesso! ===")


def create_account(clients, accounts):  # criar_conta
    cpf = input("Informe o CPF do cliente: ")
    client = filter_client(cpf, clients)  # cliente, filtrar_cliente

    if not client:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    number = input("Informe o número da conta: ")
    limit = float(input("Informe o limite da conta corrente (ou 0 para uma conta padrão): "))
    withdrawal_limit = int(input("Informe o limite de saques (ou 0 para um limite padrão): "))

    account = CheckingAccount.new_account(client, number, limit, withdrawal_limit)  # numero, cliente, limite, limite_saques
    client.add_account(account)  # adicionar_conta
    accounts.append(account)
    print("\n=== Conta criada com sucesso! ===")


# Função para exibir o menu e controlar as opções
def menu():  # Menu
    clients = []  # Lista de clientes
    accounts = []  # Lista de contas

    while True:
        print("""
        Olá, Seja Bem Vindo(a) ao Banco Python!
        Escolha uma das opções abaixo,

        [1] Depositar
        [2] Sacar
        [3] Extrato
        [4] Criar Usuário
        [5] Criar Conta
        [0] Sair
        """)
        option = input("Informe a opção desejada: ")

        if option == "1":
            deposit(clients)  # depositar
        elif option == "2":
            withdraw(clients)  # sacar
        elif option == "3":
            display_statement(clients)  # exibir_extrato
        elif option == "4":
            create_user(clients)  # criar_usuario
        elif option == "5":
            create_account(clients, accounts)  # criar_conta
        elif option == "0":
            print("\n=== Saindo do sistema... ===")
            break
        else:
            print("\n@@@ Opção inválida! Por favor, tente novamente. @@@")

# Executar o menu
menu()
