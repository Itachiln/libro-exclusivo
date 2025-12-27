from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_super_secreta_para_sesiones"  # cámbiala

USUARIO = "Marianne"
PASSWORD = "1234"  # cámbiala si quieres

def registrar_visita():
    if not os.path.exists("visitas.txt"):
        with open("visitas.txt", "w") as f:
            f.write("0")
    with open("visitas.txt", "r+") as f:
        contenido = f.read().strip() or "0"
        count = int(contenido)
        f.seek(0)
        f.write(str(count + 1))
        f.truncate()
    return count + 1

def guardar_valoracion(valor):
    ts = datetime.now().isoformat(timespec="seconds")
    linea = f"{ts} | {valor}\n"
    with open("valoraciones.txt", "a") as f:
        f.write(linea)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user", "")
        pwd = request.form.get("password", "")
        if user == USUARIO and pwd == PASSWORD:
            session["usuario"] = user
            return redirect(url_for("libro"))
    return render_template("login.html")

@app.route("/libro", methods=["GET", "POST"])
def libro():
    if "usuario" not in session:
        return redirect(url_for("login"))
    visitas = registrar_visita()
    if request.method == "POST":
        valor = request.form.get("rating")
        if valor in {"1","2","3","4","5"}:
            guardar_valoracion(valor)
    hay_pdf = os.path.exists(os.path.join("static", "libro.pdf"))
    return render_template("libro.html", visitas=visitas, hay_pdf=hay_pdf)

@app.route("/descargar")
def descargar():
    if "usuario" not in session:
        return redirect(url_for("login"))
    ruta = os.path.join("static", "libro.pdf")
    if os.path.exists(ruta):
        return send_from_directory("static", "libro.pdf", as_attachment=True)
    return "PDF no disponible aún. Súbelo a /static/libro.pdf", 404

@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
