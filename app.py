from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__, template_folder="templates")

# Configuración de la base de datos
DB_PATH = "tfg_data.db"

def init_db():
    """Inicializa la base de datos"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                altura REAL,
                creatinina REAL,
                grupo TEXT,
                tfg REAL,
                estadio TEXT,
                recomendacion TEXT
            )
        """)
        conn.commit()

init_db()

def calcular_tfg(creatinina, altura):
    """Calcula la TFG usando la nueva fórmula"""
    return (altura * 0.413) / creatinina

def interpretar_tfg(tfg):
    """Clasifica la TFG en estadios y genera recomendaciones"""
    if tfg >= 90:
        return "Estadio 1", "Los riñoncitos de tu pequeño se encuentran bien. Revisión anual recomendada."
    elif 60 <= tfg < 90:
        return "Estadio 2", "Leve disminución de la función renal. Control cada 3 a 6 meses con chequeos médicos."
    elif 30 <= tfg < 60:
        return "Estadio 3", "Disminución moderada. Seguimiento cada 3 meses con valoración nefrológica y nutricional."
    elif 15 <= tfg < 30:
        return "Estadio 4", "Daño severo. Manejo especializado y preparación para terapia sustitutiva renal."
    else:
        return "Estadio 5", "Falla renal. Inicio de diálisis, hemodiálisis o trasplante con vigilancia integral."

@app.route('/calcular_tfg', methods=['POST'])
def calcular():
    """Endpoint para calcular TFG con interpretación de estadios"""
    data = request.json
    try:
        creatinina = float(data["creatinina"])
        altura = float(data["altura"])

        tfg = calcular_tfg(creatinina, altura)
        estadio, recomendacion = interpretar_tfg(tfg)

        # Guardar en historial
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO historial (altura, creatinina, tfg, estadio, recomendacion) 
                VALUES (?, ?, ?, ?, ?)
            """, (altura, creatinina, round(tfg, 2), estadio, recomendacion))
            conn.commit()

        return jsonify({"TFG": round(tfg, 2), "Estadio": estadio, "Recomendación": recomendacion})
    
    except (KeyError, ValueError):
        return jsonify({"error": "Datos inválidos"}), 400


@app.route('/historial', methods=['GET'])
def obtener_historial():
    """Endpoint para obtener el historial de cálculos con estadios"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT altura, creatinina, grupo, tfg, estadio, recomendacion FROM historial ORDER BY id DESC LIMIT 10")
        datos = cursor.fetchall()

    historial = [{"altura": d[0], "creatinina": d[1], "grupo": d[2], "TFG": d[3], "Estadio": d[4], "Recomendación": d[5]} for d in datos]
    return jsonify(historial)

@app.route('/')
def home():
    """Interfaz gráfica infantil"""
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)

