import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def _obter_colunas(registros: List[Dict[str, Any]]) -> List[str]:
    """
    Identifica todas as colunas existentes nos registros,
    preservando a ordem em que foram encontradas.
    """
    colunas: List[str] = []

    for registro in registros:
        for coluna in registro.keys():
            if coluna not in colunas:
                colunas.append(coluna)

    return colunas


def _normalizar_valor(valor: Any) -> str:
    """
    Converte valores para um formato adequado ao arquivo CSV.
    """
    if valor is None:
        return ""

    if isinstance(valor, bool):
        return "Sim" if valor else "Não"

    texto = str(valor)

    # Evita que programas de planilha interpretem o valor como fórmula.
    if texto.startswith(("=", "+", "-", "@")):
        return "'" + texto

    return texto


def exportar_dados(
    registros: List[Dict[str, Any]],
    nome_arquivo: Optional[str] = None,
    diretorio_saida: str = "exportacoes",
) -> Optional[Path]:
    """
    Exporta uma lista de registros para um arquivo CSV.

    Parâmetros:
        registros:
            Lista de dicionários contendo os dados dos usuários.

        nome_arquivo:
            Nome opcional do arquivo CSV.

        diretorio_saida:
            Pasta onde o arquivo será gerado.

    Retorno:
        Caminho do arquivo gerado ou None quando não houver exportação.
    """

    if not registros:
        print("Exportação não realizada: nenhum registro disponível.")
        return None

    if not all(isinstance(registro, dict) for registro in registros):
        raise TypeError(
            "Cada registro deve ser representado por um dicionário."
        )

    colunas = _obter_colunas(registros)

    if not colunas:
        print(
            "Exportação não realizada: "
            "os registros não possuem campos."
        )
        return None

    pasta_saida = Path(diretorio_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    if nome_arquivo is None:
        horario = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"usuarios_{horario}.csv"
    elif not nome_arquivo.lower().endswith(".csv"):
        nome_arquivo += ".csv"

    caminho_saida = pasta_saida / nome_arquivo

    try:
        with caminho_saida.open(
            mode="w",
            newline="",
            encoding="utf-8-sig",
        ) as arquivo:
            escritor = csv.DictWriter(
                arquivo,
                fieldnames=colunas,
                delimiter=";",
                extrasaction="ignore",
                restval="",
            )

            escritor.writeheader()

            for registro in registros:
                registro_normalizado = {
                    coluna: _normalizar_valor(
                        registro.get(coluna)
                    )
                    for coluna in colunas
                }

                escritor.writerow(registro_normalizado)

    except OSError as erro:
        print(f"Falha ao gerar o arquivo CSV: {erro}")
        return None

    print(
        "Exportação concluída com sucesso: "
        f"{caminho_saida.resolve()}"
    )
    print(
        f"Total de registros exportados: {len(registros)}"
    )

    return caminho_saida


if __name__ == "__main__":
    usuarios_exemplo = [
        {
            "nome": "Ana Souza",
            "cpf": "12345678900",
            "email": "ana.souza@email.com",
            "ativo": True,
        },
        {
            "nome": "Carlos Lima",
            "cpf": "98765432100",
            "email": "carlos.lima@email.com",
            "ativo": False,
        },
    ]

    print("Teste 1: exportação com registros")
    exportar_dados(usuarios_exemplo)

    print("\nTeste 2: exportação sem registros")
    exportar_dados([])