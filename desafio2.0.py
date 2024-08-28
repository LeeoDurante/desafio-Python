
# Operações Bancárias

def withdraw(*, balance, amount, statement, limit, num_withdrawals, max_withdrawals):
    if amount > balance:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif amount > limit:
        print("Operação falhou! O valor do saque excede o limite.")
    elif num_withdrawals >= max_withdrawals:
        print("Operação falhou! Número máximo de saques excedido.")
    elif amount > 0:
        balance -= amount
        statement += f"Saque: R$ {amount:.2f}\n"
        num_withdrawals += 1
    else:
        print("Operação falhou! O valor informado é inválido.")
    return balance, statement

def deposit(balance, amount, statement):
    if amount > 0:
        balance += amount
        statement += f"Depósito: R$ {amount:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
    return balance, statement

def display_statement(balance, *, statement):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not statement else statement)
    print(f"\nSaldo: R$ {balance:.2f}")
    print("==========================================")

# Funções para Criação de contas e correntistas

users = []

def create_user(name, birth_date, cpf, address):
    for user in users:
        if user["cpf"] == cpf:
            print("Operação falhou! Já existe um usuário com esse CPF.")
            return
    users.append({"name": name, "birth_date": birth_date, "cpf": cpf, "address": address})
    print("Usuário criado com sucesso!")

accounts = []
account_number = 1

def create_account(cpf):
    global account_number
    for user in users:
        if user["cpf"] == cpf:
            accounts.append({"agency": "0001", "account_number": account_number, "user": user})
            account_number += 1
            print("Conta criada com sucesso!")
            return
    print("Operação falhou! Usuário não encontrado.")

# Menu Principal

menu = """
Ola, Seja Bem Vindo(a) ao Banco Python!
escolha uma das opcoes abaixo,

[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Usuário
[5] Criar Conta
[0] Sair

=> """

balance = 0
limit = 500
statement = ""
num_withdrawals = 0
MAX_WITHDRAWALS = 3

while True:
    option = input(menu)

    if option == "1":
        amount = float(input("Informe o valor do depósito: R$"))
        balance, statement = deposit(balance, amount, statement)

    elif option == "2":
        amount = float(input("Informe o valor do saque: R$"))
        balance, statement = withdraw(balance=balance, amount=amount, statement=statement, limit=limit, num_withdrawals=num_withdrawals, max_withdrawals=MAX_WITHDRAWALS)

    elif option == "3":
        display_statement(balance, statement=statement)

    elif option == "4":
        name = input("Informe o nome: ")
        birth_date = input("Informe a data de nascimento (dd-mm-aaaa): ")
        cpf = input("Informe o CPF (somente números): ")
        address = input("Informe o endereço (logradouro, nro, bairro, cidade/sigla estado): ")
        create_user(name, birth_date, cpf, address)

    elif option == "5":
        cpf = input("Informe o CPF do usuário: ")
        create_account(cpf)

    elif option == "0":
        print("Obrigado por utilizar nossos serviços!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
