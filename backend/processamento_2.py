import re
import pandas as pd


def limpeza_dos_dados(arquivo):
    # Lê o arquivo excel sem cabeçalho, selecionando apenas as colunas de interesse (1 e 12)
    df = pd.read_excel(arquivo, header=None, usecols=[1, 12])

    # Filtra linhas irrelevantes para reduzir o uso de memória
    df = df[df[1].str.startswith(('Estabelecimento', 'BR', 'Total:'), na=False)].copy()

    # Extrai e propaga o nome do estabelecimento_saude
    df["estabelecimento_saude"] = df[1].str.extract(r'Estabelecimento de Saúde:\s*(.*)', flags=re.IGNORECASE)
    df["estabelecimento_saude"] = df["estabelecimento_saude"].ffill().fillna("").astype(str).str.strip()

    # Separa o código CATMAT da descrição do medicamento
    df["catmat"] = df[1].str.extract(r'(BR\S*)')
    df["medicamento"] = df[1].str.extract(r'BR\S*\s+(.*)')
    
    # Propaga os dados do medicamento para as linhas de saldo (Total:)
    df["catmat"] = df["catmat"].ffill()
    df["medicamento"] = df["medicamento"].ffill().str.strip()

    # Mantém apenas as linhas de valores consolidados
    df = df[df[1].str.startswith('Total:', na=False)].copy()

    # Conversão segura para inteiro (trata erros como 0)
    df['quantidade'] = pd.to_numeric(df[12], errors='coerce').fillna(0).astype(int)

    # Consolida quantidades por chave única (garante fidelidade)
    df_consolidado = df.groupby(['estabelecimento_saude', 'catmat', 'medicamento'], as_index=False)['quantidade'].sum()

    return df_consolidado