# Predicción de Diagnóstico de Cáncer: Del Modelo al Umbral Clínico

**Caso práctico optativo · Inteligencia Artificial · Ingeniería Matemática · UAX 2025/2026**

---

## Propuesta del proyecto

La mayoría de los estudios de viabilidad en ML se detienen en la misma pregunta: *¿qué modelo obtiene mejor AUC-ROC?* Este proyecto parte de una pregunta distinta y más útil:

> **¿A qué umbral de probabilidad debería activarse una alarma clínica, y cuántas vidas se ganan o se pierden con esa decisión?**

Para responderla, construimos el pipeline completo requerido por el enunciado y añadimos una capa de análisis clínico que convierte las métricas estadísticas en recomendaciones operativas reales.

---

## Diferenciadores técnicos

### 1. Oracle Score — el techo teórico del dataset
El fichero `metadata.md` expone los pesos exactos del modelo logístico que generó la variable objetivo. Esto nos permite construir un **predictor teórico óptimo** y medir qué fracción del techo de información alcanzan nuestros modelos. Ningún modelo real puede superar al Oracle; cuanto más se acerque, mejor ha aprendido la señal real.

### 2. Decision Curve Analysis (DCA)
La curva ROC mide discriminación. La DCA mide **utilidad clínica neta**: ¿es mejor usar el modelo que tratar a todos los pacientes, o no tratar a ninguno? Es la herramienta que los comités clínicos reales usan para adoptar o rechazar modelos de cribado. Se genera para todos los modelos y permite una recomendación de despliegue justificada clínicamente.

### 3. Optimización de umbral con coste asimétrico
En oncología, un Falso Negativo (cáncer no detectado) tiene un coste clínico mucho mayor que un Falso Positivo (alarma innecesaria). En lugar de aplicar el umbral por defecto de 0.5 o de maximizar F1 ciegamente, definimos una **matriz de costes asimétrica** y derivamos el umbral óptimo de operación para cada modelo desde esa función de coste.

---

## Estructura del proyecto

```
caso cancer/
│
├── cancer_prediction.ipynb     ← notebook principal, ejecutable de inicio a fin
│
├── outputs/
│   ├── figures/                ← todas las visualizaciones generadas
│   └── tables/                 ← tablas de métricas exportadas (.csv)
│
├── dashboard/                  ← dashboard HTML estático (fase final)
│   └── index.html
│
├── cancer.pdf                  ← enunciado del caso
├── metadata.md                 ← descripción completa del dataset
├── CASOCANCER_01_BIOQUIMICOS.csv
├── CASOCANCER_02_CLINICOS.csv
├── CASOCANCER_03_GENETICOS.csv
├── CASOCANCER_04_ECONOMICOS.csv
├── CASOCANCER_05_GENERALES.csv
├── CASOCANCER_06_SOCIODEMOGRAFICOS.csv
└── README.md
```

---

## Mapa de ruta del notebook

El notebook está organizado como un estudio clínico, no como una lista de experimentos. Cada sección tiene una pregunta que responder y una conclusión accionable.

### Sección 0 — Configuración y reproducibilidad
Seeds fijos, constantes globales, versiones de librerías. El notebook debe ejecutarse con *Restart & Run All* sin errores.

### Sección 1 — Carga y validación de datos
Carga individual de los 5 CSVs disponibles, validación de integridad (50.001 filas, sin nulos, `paciente_id` único en cada colección), merge final y verificación del dataset maestro.

### Sección 2 — EDA + construcción del Oracle Score
Análisis exploratorio orientado a decisión: distribución del target, análisis univariante (Chi² para binarias, Mann-Whitney para continuas), identificación de variables con señal nula.

**Construcción del Oracle Score**: a partir de los pesos del modelo generativo documentados en `metadata.md`, se calcula para cada paciente la probabilidad teórica óptima. Este score actúa como referencia de techo durante toda la evaluación.

### Sección 3 — Ingeniería de features
- `n_mutaciones`: suma de las 6 mutaciones útiles (excluida ALK por señal nula). Predictor monotónico confirmado: 0 mutaciones → 9.6% cáncer, 4 mutaciones → 81.4%.
- `n_comorbilidades`: suma de comorbilidades clínicas.
- `actividad_fisica_ord`: codificación ordinal (Alta=2, Moderada=1, Baja=0).
- `edad_bin`: discretización en cuatro franjas de riesgo.
- Interacciones de alto valor clínico: `fumador × obesidad`, `BRCA1 × TP53`, `edad × fumador`.

### Sección 4 — Preprocesado formal
Split estratificado 80/20 (primera y única operación sobre los datos). ColumnTransformer ajustado exclusivamente sobre train. StandardScaler para numéricas, OneHotEncoder para categóricas, passthrough para binarias y genéticas. Cálculo de `class_weight` para gestionar el desbalance (ratio 4.19:1).

### Sección 5 — Modelos clásicos con Optuna
Tres modelos complejos optimizados con **Optuna** (búsqueda bayesiana de hiperparámetros, más eficiente que RandomizedSearchCV):
- **Random Forest**
- **XGBoost**
- **LightGBM**

Más baseline de **Regresión Logística** para justificar la complejidad añadida.

Antes de abrir el test: tabla de resultados en validación cruzada (F1 y AUC-ROC medio ± desviación).

### Sección 6 — Red Neuronal Multicapa (MLP)
Arquitectura: `Input → Dense(128) → BN+ReLU+Drop(0.30) → Dense(64) → BN+ReLU+Drop(0.25) → Dense(32) → BN+ReLU+Drop(0.20) → Sigmoid`

Callbacks: EarlyStopping (patience=12), ReduceLROnPlateau (factor=0.5, patience=6), ModelCheckpoint. Split interno 85/15 para validación. Curvas de pérdida y AUC por época como entregable obligatorio.

### Sección 7 — Evaluación estándar en test
Métricas requeridas por el enunciado para todos los modelos sobre el mismo conjunto de test:
- Precisión, Recall, F1-Score (clase `cancer=1`)
- AUC-ROC
- Accuracy (solo como referencia)
- Curvas ROC superpuestas
- Curvas Precision-Recall superpuestas
- Matrices de confusión (mejor modelo clásico y MLP)

### Sección 8 — Capa clínica (diferenciador principal)
Esta sección convierte los resultados estadísticos en decisiones operativas.

**8.1 Análisis de coste asimétrico**
Definición de la matriz de costes clínica (coste FN >> coste FP). Cálculo del umbral de operación óptimo por modelo desde la función de coste, en lugar de desde F1.

**8.2 Decision Curve Analysis**
DCA para todos los modelos. Comparación con las estrategias extremas: "tratar a todos" y "no tratar a ninguno". Identificación del rango de umbrales de probabilidad en que cada modelo aporta beneficio neto real.

**8.3 Oracle vs modelos reales**
Comparación directa de cada modelo con el Oracle Score. ¿Qué fracción del techo teórico alcanza el mejor modelo? ¿Dónde está el límite del dataset?

**8.4 Traducción clínica del modelo elegido**
Ejemplo concreto: *"Con el modelo X operando al umbral Y, de cada 1.000 pacientes procesados, se detectarían Z casos de cáncer que el cribado estándar perdería, generando W falsas alarmas adicionales."*

### Sección 9 — Interpretabilidad (SHAP)
SHAP values sobre el mejor modelo clásico: importancia global con signo, dirección del efecto por variable. Waterfall plots para tres casos individuales: verdadero positivo correcto, falso negativo (cáncer no detectado), falso positivo (sano mal clasificado). Validación cruzada con el Oracle: ¿aprende el modelo las variables que realmente importan?

### Sección 10 — Conclusiones y limitaciones
¿Son los datos suficientes para anticipar el cáncer? ¿Qué modelo implantaríamos y a qué umbral? Limitaciones del dataset sintético. Qué datos adicionales mejorarían el sistema en un entorno clínico real.

---

## Dataset

| Característica | Valor |
|---|---|
| Pacientes | 50.001 |
| Ficheros origen | 5 CSVs disponibles (CSV nº4 no proporcionado) |
| Variable objetivo | `cancer` (en CASOCANCER_02_CLINICOS.csv) |
| Prevalencia | ≈ 19.3% |
| Ratio de desbalance | 4.19 : 1 |

### Política de selección de variables

| Variable | Decisión | Motivo |
|---|---|---|
| glucosa, hemoglobina, leucocitos | ✅ Incluir | Correlación causal documentada en metadata |
| colesterol, triglicéridos, plaquetas, creatinina | ✅ Incluir | Predictores bioquímicos |
| mut_BRCA1, mut_TP53, mut_KRAS, mut_EGFR, mut_PIK3CA, mut_BRAF | ✅ Incluir | Máximo peso predictivo |
| fumador, actividad_fisica, edad | ✅ Incluir | Factores de riesgo causales |
| diabetes, hipertensión, obesidad, epoc, enfermedad_cardiaca | ✅ Incluir con nota | Comorbilidades con correlación causal real |
| mut_ALK | ❌ Excluir | Chi²=0.0, p=0.93 — señal estadísticamente nula |
| alcohol | ❌ Excluir | Constante en todo el dataset (100% = 1) |
| vive | ❌ Excluir | Consecuencia del diagnóstico → data leakage temporal |
| coste_total, coste_farmaco, dias_hospital, num_ingresos | ❌ Excluir | Consecuencias del diagnóstico → data leakage severo |
| nivel_educativo, nivel_ingresos, zona, estado_civil | ⚠️ Incluir con nota | Sin señal en este dataset sintético (documentado como limitación) |

---

## Stack tecnológico

| Categoría | Librerías |
|---|---|
| Datos | pandas, numpy |
| Modelado | scikit-learn, xgboost, lightgbm, tensorflow/keras |
| Optimización | optuna |
| Interpretabilidad | shap |
| Visualización | matplotlib, seaborn |
| Análisis clínico | dcurves (Decision Curve Analysis) |

---

## Fases del proyecto

- [x] Lectura del enunciado y metadata
- [x] Análisis de proyectos de referencia
- [x] Diseño de la identidad y diferenciadores
- [ ] Construcción del notebook principal
- [ ] Validación de resultados y figuras
- [ ] Elaboración de las 5 diapositivas
- [ ] Dashboard HTML estático (fase final)

---

## Entregables

1. `cancer_prediction.ipynb` — notebook ejecutable y comentado
2. 5 diapositivas en PDF/PowerPoint con el estudio de viabilidad
3. `dashboard/index.html` — resumen visual interactivo en HTML estático *(fase final)*

---

## Advertencia

Sistema basado en datos sintéticos generados con criterios epidemiológicos pero no validados clínicamente. No apto para uso en entorno médico real sin validación externa prospectiva con datos clínicos reales y supervisión de un comité de ética.
