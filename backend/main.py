# contem as rotas e endpoints
from flask import request, jsonify
from config import app,db
from models import Medicamento
from pipeline import etl
import tempfile

import os


@app.route('/medicamentos', methods=['GET'])
def listar_medicamentos():
    # 1. Captura parâmetros de paginação
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int) # Itens por página

    # 2. Inicia a query base
    query = Medicamento.query

    # 3. Aplica os filtros dinâmicos (Catmat, estabelecimento, Busca)
    catmat = request.args.get('catmat')
    estabelecimento = request.args.get('estabelecimento')
    q = request.args.get('q')

    if catmat:
        query = query.filter(Medicamento.catmat.ilike(f"%{catmat}%"))
    if estabelecimento:
        query = query.filter(Medicamento.estabelecimento_saude.ilike(f"%{estabelecimento}%"))
    if q:
        query = query.filter(Medicamento.medicamento.ilike(f"%{q}%"))

    # 4. Aplica a PAGINAÇÃO no final da query filtrada
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 5. Monta a resposta com metadados
    return jsonify({
        "items": [m.to_json() for m in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": pagination.page,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev
    })

@app.route('/estabelecimentos', methods=['GET'])
def listar_estabelecimentos_unicas():
    # Busca apenas a coluna 'estabelecimento', remove duplicatas e ordena
    estabelecimentos = db.session.query(Medicamento.estabelecimento_saude).distinct().order_by(Medicamento.estabelecimento_saude).all()
    # Retorna uma lista simples: ["UBS Centro", "Hospital Norte", ...]
    return jsonify([u[0] for u in estabelecimentos if u[0]])

from multiprocessing import Process



def run_etl(file_path):
    try:
        etl(fileName=file_path)
        print("ETL finalizado com sucesso")
    except Exception as e:
        print(f"Erro no ETL: {e}")

@app.route("/upload", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Arquivo sem nome"}), 400

    upload_path = "uploads"
    os.makedirs(upload_path, exist_ok=True)

    temp_path = os.path.join(upload_path, file.filename)
    file.save(temp_path)

    #process
    p = Process(target=run_etl, args=(temp_path,))
    p.start()

    return jsonify({
        "message": "Arquivo enviado! Processamento em andamento..."
    }), 202

#To run the aplication:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


