# contem as rotas e endpoints
from flask import request, jsonify
from config import app,db
from models import Medicamento
from pipeline import etl

import os

@app.route('/')
def index_page():
    return "<h1> Flask API </h1>"
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

@app.route("/upload", methods=["POST"])
def upload():
    # 1. Validação do arquivo
    if 'file' not in request.files:
        return jsonify({"message": "Nenhum arquivo enviado"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Arquivo sem nome"}), 400

    # 2. Caminhos (backend/uploads)
    upload_path = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)

    file_path = os.path.join(upload_path, file.filename)
    file.save(file_path)

    try:
        # 3. O Pipeline aciona o Banco de Dados
        # Passe o caminho completo do arquivo para o seu processador
        etl(fileName=file_path) 

        # 4. Retorno de sucesso para o React
        # O React receberá esse 201 e saberá que os dados já estão no banco
        return jsonify({
            "message": "Arquivo processado e dados salvos no banco com sucesso!"
        }), 201

    except Exception as e:
        # Se o banco de dados falhar, o erro cai aqui
        print(f"Erro no pipeline: {e}")
        return jsonify({"message": f"Erro ao salvar no banco: {str(e)}"}), 500



#To run the aplication:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)