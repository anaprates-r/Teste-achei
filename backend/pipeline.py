from processamento import processar_r84
from models import Medicamento
from config import db, app

def etl(fileName):
    # Chama o processamento do arquivo e retorna um DataFrame limpo
    df_limpo = processar_r84(fileName)
    
    with app.app_context():
        # carrega tudo uma vez
        existentes = {
            (m.catmat, m.estabelecimento_saude): m
            for m in Medicamento.query.all()
        }

        for row in df_limpo.to_dict(orient="records"):
            chave = (row['catmat'], row['estabelecimento_saude'])
            existente = existentes.get(chave)
            if existente:
                # Atualiza a quantidade se já existir
                existente.quantidade = row['quantidade']
                existente.medicamento = row['medicamento']
            else:
                # Cria novo se não existir
                novo = Medicamento(
                    catmat=row['catmat'],
                    medicamento=row['medicamento'],
                    quantidade=row['quantidade'],
                    estabelecimento_saude=row['estabelecimento_saude']
                )
                db.session.add(novo)
        
        db.session.commit()