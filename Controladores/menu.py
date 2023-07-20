import repositorio.clientes as clientes_repositorio
from entidades.cliente import Cliente
from datetime import datetime
from servicos.servico_email import email_eh_valido, enviar_emails

def iniciar_menu_principal():
    while True:
        print("1 - Consultar clientes\n2 - Cadastrar cliente\n3 - Enviar cupons via email aos clientes aniversariantes\n4 - Sair")
        opcao_escolhida = input("Digite uma opção: ")

        match opcao_escolhida:
            case '1':
                iniciar_submenu_consulta_clientes()
            case '2':
                iniciar_cadastro_cliente()
            case '3':
                iniciar_envio_emails()
            case '4':
                break
            case other:
                print("Opção inválida")

def iniciar_submenu_consulta_clientes():
    print("\nCONSULTAR CLIENTES\n")
    while True:
        print("1 - Todos\n2 - Aniversariantes\n3 - Aniversariantes de um mês específico\n4 - Voltar para o menu principal")
        opcao_escolhida = input("Digite uma opção: ")
        match opcao_escolhida:
            case '1':
                mostrar_todos_clientes()
                break
            case '2':
                mostrar_clientes_aniversariantes()
                break
            case '3':
                mostrar_clientes_por_mes_aniversario()
                break
            case '4':
                break
            case other:
                print("Opção inválida")

def mostrar_todos_clientes():
    print("\nCONSULTAR TODOS OS CLIENTES\n")
    clientes = clientes_repositorio.get_todos_clientes()
    Cliente.mostrar_clientes(clientes)

def mostrar_clientes_aniversariantes():
    print("\nCONSULTAR CLIENTES ANIVERSARIANTES\n")
    aniversariantes = clientes_repositorio.get_clientes_aniversariantes()
    if len(aniversariantes) > 0:
        Cliente.mostrar_clientes(aniversariantes)
    else:
        print("Ninguém faz aniversário hoje")

def mostrar_clientes_por_mes_aniversario():
    print("\nCONSULTAR CLIENTES ANIVERSARIANTES DE UM MÊS ESPECÍFICO\n")
    mes = int(input("Digite o número do mês (1-12):"))

    aniversariantes = clientes_repositorio.get_clientes_por_mes_aniversario(mes)

    if len(aniversariantes) > 0:
        Cliente.mostrar_clientes(aniversariantes)
    else:
        print("Ninguém faz aniversário neste mês")
        
def iniciar_cadastro_cliente():
    print("\nCADASTRAR CLIENTE\n")

    nome_completo = input("Nome completo: ")
    data_nascimento = input("Data nascimento: ")
    email = input("Email: ")
    data_registro = datetime.today().strftime('%d/%m/%Y')

    novo_cliente = Cliente(
        data_criacao=data_registro,
        data_nascimento=data_nascimento,
        email=email,
        nome_completo=nome_completo
    )

    foi_salvo = clientes_repositorio.salvar_cliente(novo_cliente)
    if foi_salvo:
        print("Cliente salvo com sucesso")
    else:
        print("Cliente não foi salvo")

def iniciar_envio_emails():
    print("\nENVIAR CUPONS VIA EMAIL\n")
    
    aniversariantes = clientes_repositorio.get_clientes_aniversariantes()
    aniversariantes_com_email_valido = [aniversariante for aniversariante in aniversariantes if email_eh_valido(aniversariante.email)]

    quantidade = len(aniversariantes_com_email_valido)

    if quantidade == 0:
        print("Ninguém faz aniversário hoje")
        return

    escolha = input(f"{quantidade} email(s) para ser(em) enviado(s), deseja enviar ou ver os destinatários? (enviar/ver): ")
    escolha = escolha.upper()

    if escolha == "VER":
        Cliente.mostrar_clientes(aniversariantes_com_email_valido)
    elif escolha == "ENVIAR":
        destinatarios = [aniversariante.montar_objeto_email() for aniversariante in aniversariantes]

        quantidade_emails_enviados = enviar_emails(destinatarios)

        if quantidade_emails_enviados > 0:
            print(f"{quantidade_emails_enviados} email(s) enviado(s)")
        else:
            print("Nenhum email enviado")
    else:
        print("Escolha inválida")
    