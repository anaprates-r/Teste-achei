from processamento import processar_r84
from models import Medicamento
from config import db, app
from sqlalchemy.dialects.postgresql import insert
import traceback

def etl(fileName):
    # 1. Extração e Transformação (Pandas)
    try:
        df_limpo = processar_r84(fileName)
        registros = df_limpo.to_dict(orient="records")
    except Exception as e:
        print(f"Erro no ETL: {e}")
        traceback.print_exc() # Isso vai te mostrar a LINHA EXATA do erro

    if not registros:
        return

    with app.app_context():
        # 2. Prepara a instrução de inserção
        stmt = insert(Medicamento).values(registros)

        # 3. Configura o Upsert (ON CONFLICT DO UPDATE)
        upsert_stmt = stmt.on_conflict_do_update(
            # Nome da constraint ou colunas que formam a chave única
            index_elements=['catmat', 'estabelecimento_saude'],
            
            # O que atualizar se o registro já existir
            set_={
                'quantidade': stmt.excluded.quantidade,
                'medicamento': stmt.excluded.medicamento
            }
        )

        # 4. Executa no banco em uma única transação
        db.session.execute(upsert_stmt)
        db.session.commit()