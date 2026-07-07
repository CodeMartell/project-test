# consulta.py

usuarios = [
    {
        "nome": "João Silva",
        "cpf": "12345678900",
        "email": "joao@email.com"
    },
    {
        "nome": "Maria Souza",
        "cpf": "98765432100",
        "email": "maria@email.com"
    },
    {
        "nome": "Carlos Lima",
        "cpf": "11122233344",
        "email": "carlos@email.com"
    }
]


def consultar_usuario():
    print("=" * 40)
    print("CONSULTA DE USUÁRIOS")
    print("=" * 40)

    pesquisa = input("Digite o nome ou CPF: ").strip().lower()

    encontrado = False

    for usuario in usuarios:
        if (pesquisa in usuario["nome"].lower()) or (pesquisa == usuario["cpf"]):

            print("\nUsuário encontrado")
            print(f"Nome : {usuario['nome']}")
            print(f"CPF  : {usuario['cpf']}")
            print(f"E-mail: {usuario['email']}")
            encontrado = True

    if not encontrado:
        print("\nNenhum usuário encontrado.")


if __name__ == "__main__":
    consultar_usuario()