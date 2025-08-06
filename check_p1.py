import subprocess
import csv
import os

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)

# Usuario de GitHub (lo podemos obtener de una variable de entorno en Actions)
github_user = os.getenv("GITHUB_ACTOR", "desconocido")

nota = 10
comentarios = []

# 1. Comprobar commits
commits = run_cmd("git log --oneline").stdout.strip().split("\n")
if len(commits) == 0 or commits == ['']:
    nota = 0
    comentarios.append("No hay commits")
else:
    # 2. Comprobar mensaje distinto a 'Initial commit'
    mensajes = [c for c in commits if "Initial commit" not in c]
    if len(mensajes) == 0:
        nota -= 5
        comentarios.append("Solo tiene 'Initial commit'")

# 3. Comprobar README.md
if not os.path.exists("README.md"):
    nota -= 3
    comentarios.append("No existe README.md")
else:
    with open("README.md", "r", encoding="utf-8") as f:
        if len(f.read().strip()) == 0:
            nota -= 2
            comentarios.append("README.md vacío")

# 4. Comprobar estado limpio
status = run_cmd("git status --porcelain").stdout.strip()
if status != "":
    nota -= 2
    comentarios.append("Cambios sin commitear")

# No bajar de 0
nota = max(nota, 0)

# Guardar CSV
with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Usuario GitHub", "Practica", "Nota", "Comentarios"])
    writer.writerow([github_user, "P1", nota, "; ".join(comentarios) if comentarios else "Todo correcto"])
