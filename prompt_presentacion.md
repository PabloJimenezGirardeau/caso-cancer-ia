Diseña una presentación de **5 diapositivas** en formato 16:9 para un proyecto universitario de Machine Learning sobre predicción de diagnóstico de cáncer (UAX, Ingeniería Matemática, 2025-26).

**IDENTIDAD VISUAL:** Tema oscuro. Fondo `#0a0f1e`, cards `#0d1526`, acentos cyan `#00d4ff`, verde `#00e87a`, rojo `#ff4d6a`, amarillo `#ffb700`. Tipografía técnica, valores numéricos en monospace. Estilo producto de datos clínico, no académico genérico. El **Oracle Score** (AUC=0.8362) aparece como badge de referencia recurrente en slides 2, 3 y 4 con el texto "X% del Oracle".

---

**SLIDE 1 — Objetivo y datos**

Título: *"¿Pueden los datos anticipar el cáncer? Estudio de viabilidad ML"*

- Pipeline ML completo sobre 50.001 pacientes sintéticos con datos multimodales
- Tabla de colecciones: Bioquímica (7 vars, incluida), Clínica (7, incluida), Genética (6/7, incluida — ALK excluida chi²=0), Económica (5, EXCLUIDA leakage), Generales (2/4, parcial), Sociodemografía (7, sin señal real)
- Variable objetivo: `cancer` · Prevalencia: 19.3% · Desbalance: 4.19:1 · Baseline trivial F1=0.000
- Diferenciador: **Oracle Score** AUC=0.8362 — predictor teórico construido desde los pesos exactos del modelo generativo. Define el techo informativo irrecuperable del dataset.

---

**SLIDE 2 — Modelos ML complejos**

Título: *"Tres modelos complejos + baseline logístico · Optuna TPE 20 trials"*

| Modelo | Recall | Precisión | F1 | AUC-ROC | % Oracle |
|---|---|---|---|---|---|
| LogReg baseline | **0.747** | 0.432 | 0.548 | 0.835 | 99.8% |
| XGBoost | 0.745 | 0.435 | 0.549 | 0.832 | 99.4% |
| LightGBM | 0.710 | 0.448 | 0.549 | 0.829 | 99.2% |
| Random Forest | 0.685 | 0.469 | **0.557** | 0.827 | 98.9% |

- Matriz de confusión Random Forest (mejor F1): TP=1321 FP=1494 **FN=608** TN=6578
- Impacto desbalance 4.19:1: `class_weight='balanced'` y `scale_pos_weight=4.19` aplicados. Sin esto el modelo ignoraría la clase minoritaria.
- Todos los modelos alcanzan el 98-99% del Oracle AUC=0.8362 — la señal está casi completamente capturada.
- Insertar gráfico: `slide_metrics.png` y `slide_confusion.png`

---

**SLIDE 3 — Red Neuronal MLP**

Título: *"MLP: 3 capas ocultas · 17.665 parámetros · umbral optimizado en validación"*

Arquitectura:
```
Input(49) → Dense(128)+BN+ReLU+Drop(30%) → Dense(64)+BN+ReLU+Drop(25%) → Dense(32)+BN+ReLU+Drop(20%) → Sigmoid
```

Métricas en test (umbral 0.70): Recall=0.559 · Precisión=0.551 · F1=0.555 · AUC-ROC=0.832 · **99.5% del Oracle**

Umbral: barrido [0.10–0.90] paso 0.01 sobre **validación** (no test). Umbral 0.70 maximiza F1 en validación. Aplicado una sola vez en test — procedimiento anti-data leakage.

Entrenamiento: detenido época 21/200 (EarlyStopping patience=12). Mejor época: 9. ReduceLROnPlateau actuó en época 15.

Comparación directa: Random Forest gana en Recall (+0.126) y F1 (+0.002). En tabular data estructurada, gradient boosting iguala o supera a MLP.

- Insertar gráfico: `slide_mlp_curves.png`

---

**SLIDE 4 — Comparativa global ML vs Red Neuronal**

Título: *"El límite no es el modelo. Es el ruido biológico irrecuperable."*

- Gráfico de barras: Recall/Precisión/F1/AUC-ROC/PR-AUC para todos los modelos, con línea punteada amarilla = Oracle. Insertar: `slide_metrics.png`
- Curvas ROC superpuestas: todos los AUC entre 0.827–0.835, Oracle=0.8362. Insertar: `slide_roc.png`
- Análisis Precision-Recall: PR-AUC oscila entre 0.570 (RF) y 0.593 (LogReg). Todos los modelos superan ampliamente la baseline de prevalencia (19.3%), confirmando señal predictiva real. Oracle PR-AUC=0.591. Insertar: `slide_pr.png`
- Decision Curve Analysis: beneficio neto positivo en rango clínico 0.10–0.35 para todos los modelos. Insertar: `slide_dca.png`
- Tabla ranking final ordenada por Recall con columna "% Oracle"
- Mensaje clave: los modelos se agrupan en 98–99% del techo teórico. La brecha es ε~N(0,0.8) irrecuperable por diseño.

---

**SLIDE 5 — Viabilidad y decisión**

Título: *"Sí, los datos son suficientes. Aquí está la recomendación."*

**¿Son los datos suficientes?** SÍ. AUC-ROC=0.835, 99.8% del techo teórico Oracle. Señal estable en validación cruzada 5 folds.

**Modelo recomendado:** LogReg baseline al umbral 0.46 (optimizado por coste asimétrico FN=5×, FP=1×)
Por cada 1.000 pacientes: detecta ~150 cánceres, pierde ~42, genera ~219 falsas alarmas.

**Limitaciones:**
- Dataset sintético: variables sociodemográficas sin señal real
- Calibración deficiente (error 0.17–0.23)
- 31.5% FN son casos silenciosos irrecuperables (0 mutaciones, glucosa normal, no fumador)

**Datos que mejorarían el sistema:** marcadores tumorales (PSA, CEA, CA-125), historial familiar, imágenes diagnósticas, biomarcadores epigenéticos.

---

**GRÁFICOS DISPONIBLES** (carpeta `outputs/slides/`):
- `slide_roc.png` → slide 4
- `slide_pr.png` → slide 4
- `slide_confusion.png` → slide 2
- `slide_metrics.png` → slides 2 y 4
- `slide_mlp_curves.png` → slide 3
- `slide_dca.png` → slide 4
