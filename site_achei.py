import subprocess
import os
import sys
import signal
from pathlib import Path

def site_achei():
    # 1. Configuração de Caminhos (Sem usar chdir toda hora)
    raiz = Path(__file__).parent.absolute()
    backend_path = raiz / "backend"
    frontend_path = raiz / "frontend"
    venv_path = raiz / ".venv"
    
    if os.name == "nt":
        python_venv = venv_path / "Scripts" / "python.exe"
        pip_venv = venv_path / "Scripts" / "pip.exe"
    else:
        python_venv = venv_path / "bin" / "python"
        pip_venv = venv_path / "bin" / "pip"

    # 2. Preparação do Ambiente
    if not venv_path.exists():
        print("Criando venv...")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

    print("Instalando dependências do backend...")
    subprocess.run([str(pip_venv), "install", "-r", str(raiz / "requirements.txt")], check=True)

    # Lista para guardar os processos e matá-los depois
    processos = []

    try:
        # 3. Rodar Backend (Corrigido para usar o python da venv)
        print("Iniciando Backend...")
        # Note: removi a aspa simples extra de "main'.py"
        proc_back = subprocess.Popen(
            [str(python_venv), "main.py"], 
            cwd=backend_path
        )
        processos.append(proc_back)

        # 4. Rodar Frontend
        if frontend_path.exists():
            print("Instalando dependências do frontend...")
            subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
            
            print("Iniciando Frontend...")
            proc_front = subprocess.Popen(["npm", "run", "dev"], cwd=frontend_path)
            processos.append(proc_front)

        print("\n--- TUDO RODANDO ---")
        print("Pressione Ctrl+C para encerrar os servidores.")
        
        # Mantém o script pai vivo enquanto os processos rodam
        for p in processos:
            p.wait()

    except KeyboardInterrupt:
        print("\nEncerrando servidores...")
    
    finally:
        # 5. MATAR OS PROCESSOS (A mágica acontece aqui)
        for p in processos:
            try:
                if os.name == "nt":
                    # No Windows, terminate() às vezes não fecha os filhos do npm
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
                else:
                    # No Linux/Mac, mata o grupo de processos
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
            except:
                p.terminate()
        print("Ambiente limpo. Até logo!")

if __name__ == "__main__":
    site_achei()