# contem os modelos de banco de dados

from sqlalchemy import UniqueConstraint

from config import db

class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    catmat = db.Column(db.String(50), nullable = False)
    medicamento = db.Column(db.String(255), unique = False, nullable = False)
    quantidade = db.Column(db.Integer, unique=False, nullable = False)
    estabelecimento_saude = db.Column(db.String(200), unique=False, nullable = False)

    # RESTRIÇÃO: Impede CATMAT duplicado no MESMO estabelecimento
    __table_args__ = (
        UniqueConstraint('catmat', 'estabelecimento_saude', name='_catmat_estabelecimento_uc'),
    )

    def to_json(self):
        return {
            "catmat" : self.catmat,
            "medicamento" : self.medicamento,
            "quantidade" : self.quantidade,
            "estabelecimentoSaude": self.estabelecimento_saude
        }

