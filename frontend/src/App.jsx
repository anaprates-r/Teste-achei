import { useState, useEffect } from 'react'
import MedicamentoList from './MedicamentoList' 
import UploadFile from './upload'
import './App.css'

function App() {
  // 1. Estados para os dados da API
  const [medicamentos, setMedicamentos] = useState([])
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  // 2. Estados para os Filtros
  const [filtros, setFiltros] = useState({
    q: '',
    catmat: '',
    estabelecimento: ''
  })

  // 3. Função de busca atualizada para aceitar parâmetros
  const fetchMedicamentos = async () => {
    setLoading(true)
    
    // Constrói a URL com os filtros atuais
    const params = new URLSearchParams({
      page: page,
      q: filtros.q,
      catmat: filtros.catmat,
      estabelecimento: filtros.estabelecimento
    })

    try {
      // Importante: verifique se a rota no Flask é /medicamento ou /medicamentos
      const response = await fetch(`https://achei-api.onrender.com/medicamentos?${params.toString()}`)
      const data = await response.json()
      
      // Ajuste conforme o formato que o seu Flask retorna (data.items ou data.Medicamento)
      setMedicamentos(data.items || []) 
      setTotalPages(data.pages || 1)
    } catch (error) {
      console.error("Erro ao buscar dados:", error)
    } finally {
      setLoading(false)
    }
  }

  // 4. Efeito disparado quando a página ou os filtros mudam
  useEffect(() => {
    fetchMedicamentos()
  }, [page, filtros])

  // Função para atualizar os filtros de forma centralizada
  const handleFilterChange = (novoFiltro) => {
    setFiltros(prev => ({ ...prev, ...novoFiltro }))
    setPage(1) // Sempre volta para a primeira página ao filtrar
  }

  return (
    <div className="container">
      <UploadFile />
      
      <hr />

      {/* Passamos os dados e as funções de controle para o componente de lista */}
      <MedicamentoList 
        Medicamento={medicamentos} 
        onFilterChange={handleFilterChange}
        page={page}
        setPage={setPage}
        totalPages={totalPages}
        loading={loading}
      />
    </div>
  )
}

export default App