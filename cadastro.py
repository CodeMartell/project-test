import os
import openpyxl


# Caminho do arquivo Excel (mesmo diretório do script)
ARQUIVO_XLSX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Dados do Roteiro 06.xlsx")
NOME_PLANILHA = "Usuarios"


def cadastrar_usuario():
	"""
	Solicita os dados do usuário via terminal e insere uma nova linha
	na planilha 'Usuarios' do arquivo 'Dados do Roteiro 06.xlsx',
	respeitando a estrutura de colunas existente:
	  A: Nome
	  B: Sobrenome
	  C: CPF
	  D: E-mail
	  E: Telefone
	  F: Nascimento
	  G: Status
	  H: Observação
	  I: Endereço
	"""

	print("=" * 50)
	print("       CADASTRO DE NOVO USUÁRIO")
	print("=" * 50)

	# Coleta dos dados
	nome       = input("Nome: ").strip()
	sobrenome  = input("Sobrenome: ").strip()
	cpf        = input("CPF (somente números): ").strip()
	email      = input("E-mail: ").strip()
	telefone   = input("Telefone (somente números): ").strip()
	nascimento = input("Data de Nascimento (DD/MM/AAAA): ").strip()

	# Status aceita apenas ATIVO ou INATIVO
	while True:
		status = input("Status (ATIVO / INATIVO): ").strip().upper()
		if status in ("ATIVO", "INATIVO"):
			break
		print("  ⚠  Valor inválido. Digite ATIVO ou INATIVO.")

	observacao = input("Observação: ").strip()
	endereco   = input("Endereço: ").strip()

	# Validações básicas
	if not nome or not sobrenome:
		print("\n❌ Nome e Sobrenome são obrigatórios. Cadastro cancelado.")
		return

	if len(cpf) != 11 or not cpf.isdigit():
		print("\n❌ CPF deve conter exatamente 11 dígitos numéricos. Cadastro cancelado.")
		return

	if "@" not in email or "." not in email:
		print("\n❌ E-mail inválido. Cadastro cancelado.")
		return

	# Abre a planilha existente
	try:
		wb = openpyxl.load_workbook(ARQUIVO_XLSX)
	except FileNotFoundError:
		print(f"\n❌ Arquivo '{ARQUIVO_XLSX}' não encontrado.")
		return

	ws = wb[NOME_PLANILHA]

	# Verifica se o CPF já existe para evitar duplicatas
	for row in ws.iter_rows(min_row=2, max_col=3, values_only=True):
		if row[2] == cpf:
			print(f"\n❌ CPF {cpf} já cadastrado. Cadastro cancelado.")
			wb.close()
			return

	# Insere a nova linha após a última linha preenchida
	nova_linha = [
		nome,
		sobrenome,
		cpf,
		email,
		telefone,
		nascimento,
		status,
		observacao,
		endereco,
	]
	ws.append(nova_linha)

	# Salva o arquivo
	wb.save(ARQUIVO_XLSX)
	wb.close()

	print("\n✅ Usuário cadastrado com sucesso!")
	print(f"   {nome} {sobrenome} — CPF: {cpf}")


if __name__ == "__main__":
	cadastrar_usuario()
