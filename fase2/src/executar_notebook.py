"""Executa o notebook com o Python do ambiente atual e salva suas saídas."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

RAIZ = Path(__file__).resolve().parents[2]
CAMINHO = RAIZ / "fase2/notebooks/classificador_risco.ipynb"


def main():
    notebook = nbformat.read(CAMINHO, as_version=4)
    km = KernelManager(kernel_name="python3")
    km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
    cliente = NotebookClient(notebook, timeout=180, km=km, resources={"metadata": {"path": str(RAIZ)}})
    try:
        cliente.execute()
        nbformat.write(notebook, CAMINHO)
    finally:
        if km.has_kernel:
            km.shutdown_kernel(now=True)
    print("Notebook executado:", CAMINHO)


if __name__ == "__main__":
    main()
