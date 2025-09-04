# Taller USTA — Raspberry Pi 3 Model B: Exploración, instalación de Raspberry Pi OS y prueba de Grafana con Streamlit

> **Objetivo del punto 3.** Explorar la Raspberry Pi 3 Model B de los laboratorios USTA, instalar Raspberry Pi OS y realizar una prueba de **Grafana** y **Streamlit** como demo de visualización en red local.

---

## 0. Materiales y condiciones
- Raspberry Pi 3 Model B con fuente oficial de 5 V y 2.5 A
- microSD de 16 GB o superior, clase 10
- Conexión a Internet por Ethernet o Wi‑Fi
- Monitor, teclado y mouse del laboratorio
- PC para preparar la microSD con **Raspberry Pi Imager**

> **Nota sobre arquitectura.** La Raspberry Pi 3 soporta modo de 64 bits. Usar **Raspberry Pi OS de 64 bits** mejora la compatibilidad de paquetes modernos como Streamlit. Si se requiere 32 bits por política de laboratorio, más abajo se incluye una **ruta alternativa** para Streamlit. 


---

## 1. Preparación de la microSD con Raspberry Pi Imager

1) En el PC, descarga e instala **Raspberry Pi Imager**.  
2) Abre el Imager → **Choose OS** → selecciona **Raspberry Pi OS 64‑bit**.  
3) **Choose Storage** → selecciona la microSD.  
4) Pulsa el ícono de **configuración** y completa:
   - Hostname: `rpi3-usta`
   - Usuario y contraseña
   - Wi‑Fi: SSID y contraseña del laboratorio
   - Región, idioma y **zona horaria: America/Bogota**
   - Habilita **SSH**
5) Escribe la imagen y, al terminar, **expulsa** la microSD e **insértala** en la Raspberry Pi.  

> Con Imager puedes dejar listo Wi‑Fi y SSH antes del primer arranque, lo que agiliza el proceso. 

**Primer arranque**
```bash
# Iniciar sesión localmente o por SSH
# Usuario por defecto si así se configuró: pi
sudo apt update && sudo apt full-upgrade -y
sudo raspi-config   # Comprobar localización, teclado y habilitar interfaces extra si se requieren
```

**Verifica red y datos básicos**
```bash
hostname -I           # IP en la red
cat /proc/cpuinfo | grep -E 'Model|Revision'
vcgencmd measure_temp # Temperatura del SoC
free -h               # Memoria disponible
df -h /               # Espacio en microSD
```


---

## 2. Exploración “rápida” de hardware y GPIO

### 2.1. LED parpadeante en GPIO 17
**Cableado:** LED + resistencia de 220 Ω a **GPIO 17** (pin físico 11), y GND al pin físico 6.  
**Código de prueba** `gpio_led.py`:
```python
from gpiozero import LED
from time import sleep

led = LED(17)  # GPIO BCM 17
try:
    while True:
        led.toggle()
        sleep(0.5)
except KeyboardInterrupt:
    led.off()
```
Ejecución:
```bash
python3 -m venv ~/venv_gpio && source ~/venv_gpio/bin/activate
pip install gpiozero
python gpio_led.py
```

### 2.2. Lectura de temperatura del SoC desde Python
**Archivo** `cpu_temp.py`:
```python
import subprocess

def get_temp_c():
    out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
    return float(out.split("=")[1].split("'")[0])

if __name__ == "__main__":
    print(f"Temperatura CPU: {get_temp_c():.2f} °C")
```


---

## 3. Entorno de Python para visualizaciones

Crea un entorno aislado para Streamlit y evita “ensuciar” el sistema:
```bash
python3 -m venv ~/vis_env
source ~/vis_env/bin/activate
python -m pip install --upgrade pip
```


---

## 4. Streamlit: ruta recomendada y ruta alternativa

### 4.1. **Ruta recomendada** — Raspberry Pi OS **64‑bit**
Instala Streamlit en el entorno:
```bash
pip install streamlit pandas plotly
```

Prueba rápida:
```bash
streamlit hello
```
Si abre correctamente, crea la app de ejemplo `app_streamlit.py` (más abajo) y ejecútala:
```bash
streamlit run app_streamlit.py --server.address 0.0.0.0 --server.port 8501
```
- En la Raspberry: http://localhost:8501  
- En otra PC de la red USTA: `http://IP_DE_TU_RASPBERRY:8501` 


### 4.2. **Ruta alternativa** — Raspberry Pi OS de **32 bits**
En algunos equipos de 32 bits, `pip install streamlit` puede fallar por falta de binarios. Opciones:
- **Probar versión anterior** de Streamlit compatible con tu Python:
  ```bash
  pip install "streamlit<1.25" pandas "plotly<5.20"
  ```
- **Ejecutar sin dependencias pesadas** si aparecen errores con `pyarrow` o `libatomic`:
  ```bash
  pip install --no-deps streamlit
  pip install pandas numpy plotly protobuf blinker watchdog tornado
  # y probar con:
  LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1 streamlit run app_streamlit.py
  ```
Si aun así no es viable en 32 bits, documenta el intento y justifica el uso de **Dash** como plan B.


---

## 5. App de ejemplo con Streamlit

**Archivo** `app_streamlit.py`  
Visualiza temperatura simulada y KPIs, con actualización ligera.

```python
import time
import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Demo Streamlit en Raspberry Pi", layout="centered")

st.title("Demo de Streamlit en Raspberry Pi 3")
st.caption("Serie de temperatura simulada con KPIs simples")

# Estado persistente en la sesión
if "serie" not in st.session_state:
    base = 24.0
    st.session_state.serie = [round(base + random.uniform(-0.3, 0.3), 2) for _ in range(24)]

def nueva_muestra(valor):
    paso = random.uniform(-0.35, 0.6)
    nuevo = max(min(valor + paso, 30.0), 18.0)
    return round(nuevo, 2)

placeholder = st.empty()

for _ in range(1):  # ejecuta una sola vez en run; usa el botón de refresco o st.autorefresh si lo prefieres
    last = st.session_state.serie[-1]
    st.session_state.serie.append(nueva_muestra(last))
    if len(st.session_state.serie) > 120:
        st.session_state.serie = st.session_state.serie[-120:]

    df = pd.DataFrame({
        "muestra": list(range(len(st.session_state.serie))),
        "temperatura_c": st.session_state.serie
    })
    fig = px.line(df, x="muestra", y="temperatura_c", title="Temperatura simulada")
    fig.update_traces(mode="lines+markers")

    col1, col2, col3 = st.columns(3)
    col1.metric("Última", f"{df['temperatura_c'].iloc[-1]:.2f} °C")
    col2.metric("Promedio", f"{df['temperatura_c'].mean():.2f} °C")
    col3.metric("Rango", f"{df['temperatura_c'].min():.2f} — {df['temperatura_c'].max():.2f} °C")

    st.plotly_chart(fig, use_container_width=True)

st.info("Ejecuta con:  streamlit run app_streamlit.py --server.address 0.0.0.0 --server.port 8501")
```

> Si prefieres auto‑refresco, agrega `st.experimental_rerun()` o `st_autorefresh(interval=5000)` desde `streamlit_extras` o usa un botón de “Actualizar”.


---

## 6. Instalación de Grafana en Raspberry Pi OS

Añade el repositorio oficial y habilita el servicio:

```bash
sudo apt-get install -y software-properties-common wget gpg
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/grafana.gpg
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
sudo apt-get update
sudo apt-get install -y grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
sudo systemctl status grafana-server --no-pager
```

Accede desde el navegador:
- En la Raspberry: `http://localhost:3000`
- Desde otra PC: `http://IP_DE_TU_RASPBERRY:3000`

Credenciales iniciales: usuario `admin` y contraseña `admin`  
Cambia la contraseña al primer inicio.


---

## 7. Primer panel en Grafana

1) En la barra lateral, **Connections → Data sources**.  
2) Agrega **TestData DB** para generar datos de prueba.  
3) Crea **New dashboard → Add panel**.  
4) Elige visualización: línea, barras o gauge.  
5) Guarda y verifica la vista.  

> Si deseas integrar con datos reales, considera **InfluxDB** o **Prometheus** como fuentes de series de tiempo.


---

## 8. Entregables sugeridos para el informe del taller
- Capturas del **Imager** con la configuración usada y de la **primera sesión** en la RPi.  
- Salida de `hostname -I`, `vcgencmd measure_temp` y `cat /proc/cpuinfo`.  
- Foto o captura del LED en GPIO 17 y ejecución de `gpio_led.py`.  
- Evidencia de Streamlit en `localhost:8501` y desde otra máquina de la red.  
- Pantalla de inicio de Grafana, creación del **Data Source** y del **Dashboard**.  
- Comentario corto: consumo de CPU y RAM durante la demo y pasos que funcionaron o fallaron.


---

## 9. Requisitos de Python opcionales
**requirements.txt:**
```
streamlit
pandas
plotly
gpiozero
```

Instalación rápida:
```bash
python3 -m venv ~/vis_env && source ~/vis_env/bin/activate
pip install -r requirements.txt
```


---

## Notas y referencias
- Raspberry Pi Imager permite dejar preconfigurados Wi‑Fi, SSH y regionalización, lo que acelera el primer arranque. citeturn0search1turn0search14
- Streamlit se instala con `pip install streamlit`. En equipos de 64 bits suele funcionar sin ajustes. citeturn0search2
- En sistemas de 32 bits se han reportado incompatibilidades. La comunidad sugiere alternativas como ejecutar sin `pyarrow` o usar `LD_PRELOAD` para `libatomic`. Otra opción es usar Raspberry Pi OS de 64 bits en la RPi 3. citeturn0search7turn0search17turn0search12turn0search11
- Instalación de Grafana mediante repositorio APT oficial. citeturn0search0

---

### Apéndice: ejecución como servicio de usuario para Streamlit (opcional)
Crea `~/.config/systemd/user/streamlit.service`:
```ini
[Unit]
Description=Streamlit demo
After=network.target

[Service]
Environment=PATH=%h/vis_env/bin
ExecStart=%h/vis_env/bin/streamlit run %h/app_streamlit.py --server.address 0.0.0.0 --server.port 8501
Restart=on-failure

[Install]
WantedBy=default.target
```
Habilita e inicia:
```bash
systemctl --user enable streamlit
systemctl --user start streamlit
loginctl enable-linger "$USER"
```
