import pandas as pd

def processar_r84(arquivo):
    # Melhora 1: Tenta ler xlsx (openpyxl) ou xls (xlrd) automaticamente
    try:
        df = pd.read_excel(arquivo, header=None) 
    except Exception:
        df = pd.read_excel(arquivo, header=None, engine="xlrd")

    estabelecimento_atual = None
    medicamento_atual = None
    registros = []

    for _, row in df.iterrows():
        # A coluna 1 parece conter os rótulos de texto
        col_texto = str(row[1]).strip() if pd.notna(row[1]) else ""

        # Detectar estabelecimento
        if "Estabelecimento de Saúde:" in col_texto:
            estabelecimento_atual = col_texto.split(":", 1)[1].strip()
            continue

        # Detectar medicamento (BR + código)
        if col_texto.startswith("BR"):
            partes = col_texto.split(" ", 1)
            catmat = partes[0].strip()
            nome_med = partes[1].strip() if len(partes) > 1 else ""
            medicamento_atual = (catmat, nome_med)
            continue

        # Detectar linha Total (onde a quantidade costuma estar na coluna 12)
        if "Total:" in col_texto and estabelecimento_atual and medicamento_atual:
            qtd_bruta = row[12]
            
            if pd.notna(qtd_bruta):
                # Melhora 2: Conversão segura para inteiro
                try:
                    qtd_final = int(float(qtd_bruta))
                    registros.append({
                        "estabelecimento_saude": estabelecimento_atual,
                        "catmat": medicamento_atual[0],
                        "medicamento": medicamento_atual[1],
                        "quantidade": qtd_final
                    })
                except ValueError:
                    continue

    resultado = pd.DataFrame(registros)

    if resultado.empty:
        return resultado

    # Agrupa para consolidar caso o mesmo item apareça em blocos diferentes
    return resultado.groupby(
        ["estabelecimento_saude", "catmat", "medicamento"], 
        as_index=False
    )["quantidade"].sum()