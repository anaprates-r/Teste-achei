import { useState } from "react"

const UploadFile = () => {
  const [file, setFile] = useState(null)

  const onFileChange = (e) => {
    // Access the first file from the input's file list
    setFile(e.target.files[0])
  }

  const onSubmit = async (e) => {
    e.preventDefault(); // Impede o browser de recarregar antes da hora
    
    if (!file) return alert("Por favor, selecione um arquivo primeiro!");

    // Ajuste para a porta 8000 se estiver usando o seu script Uvicorn
    const url = "https://estoque-api-r0sv.onrender.com/upload"; 

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        // O alert bloqueia a execução. O código abaixo só roda após o "OK"
        alert("Arquivo enviado com sucesso!");
        
        // Recarrega a página atual
        window.location.reload(); 
      } else {
        const data = await response.json();
        alert(data.message || "Falha no upload");
      }
    } catch (error) {
      console.error("Erro ao enviar:", error);
      alert("Erro: " + error.message);
    }
  };

  return <div>
    <p> Atualize o banco de dados</p>
        <form onSubmit={onSubmit}>
      <label htmlFor="file">Selecione um arquivo</label>
      <input type="file" name="file" id="file" onChange={onFileChange} />
      <input type="submit" value="upload" />
    </form>
  </div>

}

export default UploadFile
