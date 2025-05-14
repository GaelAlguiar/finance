from fastapi import FastAPI
import yfinance as yf
import threading
import time

app = FastAPI()
latest_price = None           # Último precio ajustado
raw_price = None              # Precio real sin ajustar
previous_price = None         # Precio anterior para comparar
last_update_time = None       # Último timestamp de cambio

# Función para actualizar el precio periódicamente
def actualizar_precio():
    global latest_price, raw_price, previous_price, last_update_time
    while True:
        ticker = yf.Ticker("MXN=X")
        data = ticker.history(period="1d")
        if not data.empty:
            new_price = data["Close"].iloc[-1]
            if new_price != raw_price:
                previous_price = raw_price
                raw_price = new_price
                latest_price = new_price + 0.05
                last_update_time = time.time()
        time.sleep(5)

# Iniciar el hilo de actualización al arrancar el servidor
threading.Thread(target=actualizar_precio, daemon=True).start()

@app.get("/precio")
def obtener_precio():
    if latest_price is not None:
        # Verifica si el precio no ha cambiado en más de 10 segundos
        if last_update_time and time.time() - last_update_time > 20:
            return {
                "error": "El precio no se ha actualizado recientemente. Puede ser necesario reiniciar el servidor."
            }
        return {"MXN=X": latest_price}
    return {"error": "No se pudo obtener el precio."}
