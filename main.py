from fastapi import FastAPI
import yfinance as yf
import threading
import time

app = FastAPI()
latest_price = None  # Variable para almacenar el precio actualizado

# Función para actualizar el precio periódicamente
def actualizar_precio():
    global latest_price
    while True:
        ticker = yf.Ticker("MXN=X")
        data = ticker.history(period="1d")
        if not data.empty:
            latest_price = data["Close"].iloc[-1]
        time.sleep(60)  # Actualiza cada 60 segundos

# Iniciar la actualización en un hilo separado para no bloquear el servidor
threading.Thread(target=actualizar_precio, daemon=True).start()

@app.get("/precio")
def obtener_precio():
    if latest_price is not None:
        return {"precio_mxn_usd": latest_price}
    return {"error": "No se pudo obtener el precio"}
