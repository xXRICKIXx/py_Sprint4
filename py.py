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
    leito = {
        "numero": numero,
        "ocupado": False,
        "paciente": None,
        "historico": [],
        "problemas": []
    }
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

# Funções Técnicas

def registrar_problema(leitos, numero, descricao, responsavel):
    for leito in leitos:
        if leito["numero"] == numero:
            leito.setdefault("problemas", []).append({
                "descricao": descricao,
                "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "resolvido": False,
                "registrado_por": responsavel
            })
            salvar_leitos(leitos)
            print(f"Problema registrado no leito {numero}.")
            return
    print(f"Leito {numero} não encontrado.")

def visualizar_problemas(leitos):
    print("\nLeitos com Problemas Técnicos:")
    problemas_encontrados = False
    for leito in leitos:
        for problema in leito.get("problemas", []):
            if not problema["resolvido"]:
                print(f"Leito {leito['numero']} - {problema['descricao']} (registrado por {problema['registrado_por']}) em {problema['data']}")
                problemas_encontrados = True
    if not problemas_encontrados:
        print("Nenhum problema técnico registrado.")

def resolver_problema(leitos, numero):
    for leito in leitos:
        if leito["numero"] == numero:
            for problema in leito.get("problemas", []):
                if not problema["resolvido"]:
                    problema["resolvido"] = True
                    salvar_leitos(leitos)
                    print(f"Problema do leito {numero} marcado como resolvido.")
                    return
            print(f"Leito {numero} não possui problemas pendentes.")
            return
    print(f"Leito {numero} não encontrado.")

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
        tipo_usuario = input("\nVocê é um paciente, enfermeiro, tecnico ou manutencao?: ")

        tipos_validos = ["paciente", "enfermeiro", "tecnico", "manutencao"]
        if tipo_usuario not in tipos_validos:
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

            elif tipo_usuario == 'tecnico':
                print("1. Visualizar Leitos")
                print("2. Visualizar Leitos Ocupados")
                print("3. Visualizar Histórico de Leitos")
                print("4. Registrar Problema Técnico")
                print("5. Sair")

            elif tipo_usuario == 'manutencao':
                print("1. Visualizar Leitos")
                print("2. Visualizar Histórico de Leitos")
                print("3. Visualizar Problemas Técnicos")
                print("4. Resolver Problema de Leito")
                print("5. Sair")

            elif tipo_usuario == 'paciente':
                print("1. Visualizar Leitos")
                print("2. Visualizar Leitos Ocupados")
                print("3. Sair")

            opcao = input("Escolha uma opção: ")

            # ENFERMEIRO
            if tipo_usuario == 'enfermeiro':
                if opcao == '1':
                    numero = input("Digite o número do novo leito: ")
                    adicionar_leito(leitos, numero)
                elif opcao == '2':
                    numero = input("Digite o número do leito a ser ocupado: ")
                    paciente = input("Digite o nome do paciente: ")
                    ocupar_leito(leitos, numero, paciente)
                elif opcao == '3':
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
                    print("Opção inválida.")

            # TECNICO
            elif tipo_usuario == 'tecnico':
                if opcao == '1':
                    visualizar_leitos(leitos)
                elif opcao == '2':
                    visualizar_leitos_ocupados(leitos)
                elif opcao == '3':
                    visualizar_historico(leitos)
                elif opcao == '4':
                    numero = input("Digite o número do leito com problema: ")
                    descricao = input("Descreva o problema: ")
                    registrar_problema(leitos, numero, descricao, usuario_logado)
                elif opcao == '5':
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida.")

            # MANUTENCAO
            elif tipo_usuario == 'manutencao':
                if opcao == '1':
                    visualizar_leitos(leitos)
                elif opcao == '2':
                    visualizar_historico(leitos)
                elif opcao == '3':
                    visualizar_problemas(leitos)
                elif opcao == '4':
                    numero = input("Digite o número do leito a ser resolvido: ")
                    resolver_problema(leitos, numero)
                elif opcao == '5':
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida.")

            # PACIENTE
            elif tipo_usuario == 'paciente':
                if opcao == '1':
                    visualizar_leitos(leitos)
                elif opcao == '2':
                    visualizar_leitos_ocupados(leitos)
                elif opcao == '3':
                    print("Saindo do sistema...")
                    break
                else:
                    print("Opção inválida.")

    except ValueError as ve:
        print(f"Erro: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# Execução

if __name__ == "__main__":
    main()
