# 📚 Prueba Tecnica para Cientifico Datos XpertGroup

Este proyecto implementa una prueba técnica para el cargo de Científico de Datos en la compañía XpertGroup. Donde se evalúan diferentes habilidades respecto a Python, SQL y conocimientos en Machine Learning. 
---

##  Flujo principal

1. **Generación de datos sintéticos**
   - Clientes (`customers.csv`)
   - Transacciones (`transactions.csv`)

2. **Preprocesamiento y validación**
   - Validación de duplicados y valores faltantes
   - Validación de columnas de fecha

3. **Feature Engineering**
   - Métricas RFM (`recency`, `frequency`, `monetary`)
   - Ventanas de 180 días
   - Construcción de la variable objetivo `will_return_30d`

4. **Entrenamiento de modelos**
   - Modelos implementados: **Regresión Logística**, **Random Forest**
   - Métricas evaluadas: **Precision-Recall AUC (PR-AUC)** y **ROC-AUC**
   - Manejo de desbalanceo con `class_weight='balanced'`

5. **Interpretabilidad**
   - Importancia de variables (`feature importance`)

## 📊 Resultados esperados

- Distribución de la variable objetivo en train/test
- Métricas comparativas entre modelos
- Curvas ROC y Precision-Recall
- Importancia de las principales variables predictoras


## 📁 Estructura del Proyecto

├── data/
│   └── raw/                
│       ├── customers.csv       # Datos crudos de clientes: signup_date, género, edad, canal, premium, etc.
│       └── transactions.csv    # Datos crudos de transacciones: órdenes, fechas, montos, categoría, etc.
│
├── notebooks/              
│   └── explore.ipynb           # Notebook principal: EDA, generación de features, modelo baseline, métricas y hallazgos.
│
├── sql/                        
│   ├── category_revenues.sql   # Query SQL (1a): categorías top por ingresos en 30 días previos al cutoff.
│   └── recency.sql             # Query SQL (1b): recency por cliente (días desde última compra al cutoff).
│
├── src/                        # Código fuente modularizado
│   ├── explorer.py             # Funciones de análisis exploratorio rápido:
│   │                           #   - Revisión de duplicados y faltantes
│   │                           #   - Estadísticas descriptivas (clientes, transacciones, ticket promedio, % premium)
│   │                           #   - Histogramas y distribuciones para variables clave
│   │
│   ├── features.py             # Ingeniería de features:
│   │                           #   - Construcción de Recency, Frequency_180d, Monetary_180d
│   │                           #   - Join con atributos de clientes (is_premium, age, channel one-hot)
│   │                           #   - Creación de la variable objetivo `will_return_30d`
│   │
│   ├── paths.py                # Centraliza rutas de acceso a datos y resultados:
│   │                           #   - Rutas a `data/raw`, `data/processed`, `results/`
│   │                           #   - Facilita reproducibilidad sin hardcodear paths
│   │
│   └── validations.py          # Validaciones de integridad:
│                               #   - Chequeo de rangos de fechas (no usar data > cutoff en train)
│                               #   - Validación de columnas obligatorias en datasets
│                               #   - Tipos de datos correctos en features numéricas y categóricas
│
├── requirements.txt            # Dependencias del proyecto (pandas, scikit-learn, matplotlib, etc.)
└── README.md                   # Guía de uso, entregables y criterios de evaluación

---

## 🚀 Instalación y uso

1. Clonar el repositorio:
```bash
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio


python -m venv .venv
source .venv/bin/activate  # En Linux/Mac
.venv\\Scripts\\activate   # En Windows

pip install -r requirements.txt
