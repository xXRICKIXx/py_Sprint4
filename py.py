import json
import os
from datetime import datetime

ARQUIVO_LEITOS = "leitos.json"

# Manipulação de Arquivos 

def salvar_leitos(leitos):
    try:
        with open(ARQUIVO_LEITOS, "w", encoding="utf-8") as f:
            json.dump(leitos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar os leitos: {e}")

def carregar_leitos():
    if not os.path.exists(ARQUIVO_LEITOS):
        return []
    try:
        with open(ARQUIVO_LEITOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar os leitos: {e}")
        return []

# Funções de Leito

def adicionar_leito(leitos, numero):
    for leito in leitos:
        if leito["numero"] == numero:
            print(f"Leito {numero} já existe.")
            return
    leito = {"numero": numero, "ocupado": False, "paciente": None, "historico": []}
    leitos.append(leito)
    salvar_leitos(leitos)
    print(f"Leito {numero} adicionado.")

def ocupar_leito(leitos, numero, paciente):
    for leito in leitos:
        if leito["numero"] == numero:
            if not leito["ocupado"]:
                leito["ocupado"] = True
                leito["paciente"] = paciente
                leito["historico"].append({
                    "paciente": paciente,
                    "tempo": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                salvar_leitos(leitos)
                print(f"Leito {numero} ocupado por {paciente}.")
            else:
                print(f"Leito {numero} já está ocupado.")
            return
    print(f"Leito {numero} não encontrado.")

def liberar_leito(leitos, numero):
    for leito in leitos:
        if leito["numero"] == numero:
            if leito["ocupado"]:
                leito["ocupado"] = False
                leito["paciente"] = None
                salvar_leitos(leitos)
                print(f"Leito {numero} liberado.")
            else:
                print(f"Leito {numero} já está disponível.")
            return
    print(f"Leito {numero} não encontrado.")

def visualizar_leitos(leitos):
    print("\nStatus dos Leitos:")
    for leito in leitos:
        status = "Ocupado" if leito["ocupado"] else "Disponível"
        paciente_info = f" - Paciente: {leito['paciente']}" if leito["ocupado"] else ""
        print(f"Leito {leito['numero']}: {status}{paciente_info}")

def visualizar_leitos_ocupados(leitos):
    print("\nLeitos Ocupados:")
    tem_ocupado = False
    for leito in leitos:
        if leito["ocupado"]:
            print(f"Leito {leito['numero']} - Paciente: {leito['paciente']}")
            tem_ocupado = True
    if not tem_ocupado:
        print("Nenhum leito ocupado.")

def visualizar_historico(leitos):
    print("\nHistórico de Leitos:")
    for leito in leitos:
        print(f"\nLeito {leito['numero']}:")
        if leito["historico"]:
            for h in leito["historico"]:
                print(f"  Paciente: {h['paciente']} - Tempo: {h['tempo']}")
        else:
            print("  Nenhum histórico registrado.")

# Função de Login 

def login_usuario(tipo):
    usuario = input(f"Digite o nome do {tipo}: ")
    senha = input(f"Digite a senha do {tipo}: ")
    print(f"{tipo} {usuario} logado com sucesso.")
    return usuario

# Função Principal 

def main():
    leitos = carregar_leitos()

    if not leitos:
        print("Nenhum dado encontrado. Adicionando 10 leitos iniciais.")
        for i in range(1, 11):
            adicionar_leito(leitos, str(i))

    try:
        tipo_usuario = input("\nVocê é um paciente ou enfermeiro? (digite exatamente 'paciente' ou 'enfermeiro'): ")

        if tipo_usuario != "paciente" and tipo_usuario != "enfermeiro":
            raise ValueError("Tipo de usuário inválido.")

        usuario_logado = login_usuario(tipo_usuario)

        while True:
            print("\nMenu:")
            if tipo_usuario == 'enfermeiro':
                print("1. Adicionar Leito")
                print("2. Ocupação de Leito")
                print("3. Liberação de Leito")
            print("4. Visualizar Leitos")
            print("5. Visualizar Leitos Ocupados")
            print("6. Visualizar Histórico de Leitos")
            print("7. Sair")

            opcao = input("Escolha uma opção: ")

            if tipo_usuario == 'enfermeiro' and opcao == '1':
                numero = input("Digite o número do novo leito: ")
                adicionar_leito(leitos, numero)

            elif tipo_usuario == 'enfermeiro' and opcao == '2':
                numero = input("Digite o número do leito a ser ocupado: ")
                paciente = input("Digite o nome do paciente: ")
                ocupar_leito(leitos, numero, paciente)

            elif tipo_usuario == 'enfermeiro' and opcao == '3':
                numero = input("Digite o número do leito a ser liberado: ")
                liberar_leito(leitos, numero)

            elif opcao == '4':
                visualizar_leitos(leitos)

            elif opcao == '5':
                visualizar_leitos_ocupados(leitos)

            elif opcao == '6':
                visualizar_historico(leitos)

            elif opcao == '7':
                print("Saindo do sistema...")
                break

            else:
                print("Opção inválida. Tente novamente.")

    except ValueError as ve:
        print(f"Erro: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Execução 

if __name__ == "__main__":
    main()

