import React, { useState, useEffect } from "react";

const MedicamentoList = () => {
  const [medicamentos, setMedicamentos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  // ESTADO QUE ESTAVA FALTANDO:
  const [listaEstabelecimentos, setListaEstabelecimentos] = useState([]);

  const [filtros, setFiltros] = useState({
    catmat: "",
    estabelecimento: "",
    q: ""
  });

  // 1. Busca os estabelecimentos para o Datalist (Roda 1 vez)
  useEffect(() => {
    const buscarSugestoes = async () => {
      try {
        const response = await fetch("https://estoque-api-r0sv.onrender.com/estabelecimentos");
        const data = await response.json();
        setListaEstabelecimentos(data);
      } catch (error) {
        console.error("Erro ao buscar estabelecimentos:", error);
      }
    };
    buscarSugestoes();
  }, []);

  // 2. Busca os medicamentos filtrados
  const carregarDados = async () => {
    setLoading(true);
    const params = new URLSearchParams({
      page: page,
      catmat: filtros.catmat,
      estabelecimento: filtros.estabelecimento,
      q: filtros.q
    });

    try {
      const response = await fetch(`https://estoque-api-r0sv.onrender.com/medicamentos?${params.toString()}`);
      const data = await response.json();
      setMedicamentos(data.items || []);
      setTotalPages(data.pages || 1);
    } catch (error) {
      console.error("Erro ao carregar medicamentos:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    carregarDados();
  }, [page, filtros]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFiltros(prev => ({ ...prev, [name]: value }));
    setPage(1);
  };

  return (
    <div>
      <h2>Gestão de Medicamentos</h2>

      <div style={{ marginBottom: "20px", display: "flex", gap: "10px", flexWrap: "wrap" }}>
        <input name="q" placeholder="Buscar descrição..." value={filtros.q} onChange={handleFilterChange} />
        <input name="catmat" placeholder="CATMAT" value={filtros.catmat} onChange={handleFilterChange} />
        
        <input 
          name="estabelecimento" 
          list="lista-estabelecimentos" 
          placeholder="Estabelecimento..." 
          value={filtros.estabelecimento} 
          onChange={handleFilterChange} 
        />
        <datalist id="lista-estabelecimentos">
          {listaEstabelecimentos.map((est, index) => (
            <option key={index} value={est} />
          ))}
        </datalist>
      </div>

      {loading ? <p>Carregando...</p> : (
        <>
          <table border="1" style={{ width: "100%", textAlign: "left", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ backgroundColor: "#f2f2f2" }}>
                <th>Estabelecimento</th>
                <th>CATMAT</th>
                <th>Medicamento</th>
                <th>Quantidade</th>
              </tr>
            </thead>
            <tbody>
              {medicamentos.length > 0 ? medicamentos.map((item, index) => (
                <tr key={`${item.catmat}-${item.estabelecimentoSaude}-${index}`}>
                  <td>{item.estabelecimentoSaude}</td>
                  <td>{item.catmat}</td>
                  <td>{item.medicamento}</td>
                  <td>{item.quantidade}</td>
                </tr>
              )) : (
                <tr><td colSpan="4" style={{textAlign: "center"}}>Nenhum dado encontrado</td></tr>
              )}
            </tbody>
          </table>

          <div style={{ marginTop: "15px" }}>
            <button disabled={page === 1} onClick={() => setPage(p => p - 1)}> Anterior </button>
            <span> Página {page} de {totalPages} </span>
            <button disabled={page === totalPages} onClick={() => setPage(p => p + 1)}> Próximo </button>
          </div>
        </>
      )}
    </div>
  );
};

export default MedicamentoList;