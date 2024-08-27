menu = """
Ola, Seja Bem Vindo(a) ao Banco Python!
escolha uma das opcoes abaixo,

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> """


bank_balance = 0             #saldo    
limit= 500                   #limite
extract = ""                 #extrato
quantity_withdrawals = 0     #quantidade de saques

LIMITE_SAQUES = 3            #constante, pois é regra do desafio

while True:

    option = input(menu)

    if option == "1":
        value = float(input("Informe o valor do depósito: R$"))

        if value > 0:
            bank_balance += value
            extract += f"Depósito: R$ {value:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif option == "2":
        value = float(input("Informe o valor do saque: R$"))

        exceeded_balance = value > bank_balance                       #excedeu o saldo

        exceeded_limit = value > limit                                #excedeu o limite

        exceeded_withdrawals = quantity_withdrawals >= LIMITE_SAQUES  #excedeu os saques

        if exceeded_balance:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif exceeded_limit:
            print("Operação falhou! O valor do saque excede o limite.")

        elif exceeded_withdrawals :
            print("Operação falhou! Número máximo de saques excedido.")

        elif value > 0:
            bank_balance -= value
            extract+= f"Saque: R$ {value:.2f}\n"
            quantity_withdrawals += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif option == "3":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extract else extract)
        print(f"\nSaldo: R$ {bank_balance:.2f}")
        print("==========================================")

    elif option == "0":
        print("Obrigado por utilizar nossos serviços!")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")