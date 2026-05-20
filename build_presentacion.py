# -*- coding: utf-8 -*-
"""Build the final HTML presentation with embedded charts."""
import base64, os

def b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

confusion   = b64('outputs/slides2/s2_confusion_rf.png')
mlp_curves  = b64('outputs/slides2/s3_mlp_curves.png')
metrics_bar = b64('outputs/slides2/s4_metrics_bar.png')
roc         = b64('outputs/slides2/s4_roc.png')
pr          = b64('outputs/slides2/s4_pr.png')

html = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Prediccion de Diagnostico de Cancer -- UAX 2025-26</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap">
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg:#0a0f1e; --bg2:#0d1526; --card:#111d35; --border:#1a2d50;
  --cyan:#00d4ff; --green:#00e87a; --red:#ff4d6a; --yellow:#ffb700;
  --purple:#a78bfa; --orange:#f97316;
  --ink:#e8f0fe; --dim:#8ba3cc; --mut:#4a6080;
  --sans:'IBM Plex Sans',system-ui,sans-serif;
  --mono:'JetBrains Mono',monospace;
}
html,body { width:100%;height:100%;background:var(--bg);color:var(--ink);font-family:var(--sans);overflow:hidden; }

/* Deck */
#deck { width:100vw;height:100vh;position:relative; }
.slide {
  position:absolute;inset:0;display:flex;flex-direction:column;
  padding:34px 44px 22px;
  opacity:0;pointer-events:none;transition:opacity 0.38s ease;
}
.slide.active { opacity:1;pointer-events:all; }

/* Header */
.sh { display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;flex-shrink:0; }
.sh .badge { font-family:var(--mono);font-size:10.5px;color:var(--mut);letter-spacing:.08em;text-transform:uppercase; }
.sh .ctr   { font-family:var(--mono);font-size:10.5px;color:var(--mut); }

/* Title */
h1 { font-size:26px;font-weight:600;color:var(--ink);line-height:1.25;margin-bottom:20px;flex-shrink:0;letter-spacing:-.02em; }
h1 em { color:var(--cyan);font-style:normal; }

/* Card */
.card { background:var(--card);border:1px solid var(--border);border-radius:10px;padding:14px 18px; }
.ct { font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;color:var(--mut);margin-bottom:8px; }

/* Tables */
table { width:100%;border-collapse:collapse; }
thead th { font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut);padding:5px 10px;text-align:left;border-bottom:1px solid var(--border); }
thead th.r { text-align:right; }
tbody td { padding:7px 10px;font-size:12.5px;color:var(--dim);border-bottom:1px solid rgba(26,45,80,.45); }
tbody td.r { text-align:right;font-family:var(--mono);font-size:12px; }
tbody td.mono { font-family:var(--mono);font-size:11.5px; }
tbody tr:last-child td { border-bottom:none; }
tbody tr:hover td { background:rgba(255,255,255,.02); }

/* Pills */
.pill { display:inline-block;padding:2px 8px;border-radius:999px;font-family:var(--mono);font-size:10px;letter-spacing:.05em;white-space:nowrap; }
.pg { background:rgba(0,232,122,.12);color:var(--green);border:1px solid rgba(0,232,122,.3); }
.py { background:rgba(255,183,0,.12);color:var(--yellow);border:1px solid rgba(255,183,0,.3); }
.pr { background:rgba(255,77,106,.12);color:var(--red);border:1px solid rgba(255,77,106,.3); }
.pm { background:rgba(74,96,128,.12);color:var(--mut);border:1px solid rgba(74,96,128,.25); }

/* Chart images */
.cimg { width:100%;height:100%;object-fit:contain;border-radius:6px;display:block;cursor:zoom-in; }

/* Footer */
.sf { flex-shrink:0;margin-top:12px;display:flex;align-items:center;gap:10px;padding-top:10px;border-top:1px solid var(--border); }
.sf span { font-family:var(--mono);font-size:10px;color:var(--mut); }
.sf .rule { flex:1;height:1px;background:var(--border); }

/* Nav */
.nav { position:fixed;top:50%;transform:translateY(-50%);background:rgba(17,29,53,.85);border:1px solid var(--border);color:var(--dim);width:36px;height:52px;border-radius:7px;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:18px;transition:background .2s,color .2s;z-index:100;user-select:none; }
.nav:hover { background:var(--card);color:var(--cyan); }
#bp { left:10px; }
#bn { right:10px; }
.nav.hidden { opacity:0;pointer-events:none; }

/* Dots */
#dots { position:fixed;bottom:16px;left:50%;transform:translateX(-50%);display:flex;gap:7px;z-index:100; }
.dot { width:6px;height:6px;border-radius:50%;background:var(--border);transition:background .25s,transform .25s;cursor:pointer; }
.dot.active { background:var(--cyan);transform:scale(1.4); }

/* Lightbox */
#lb { display:none;position:fixed;inset:0;background:rgba(5,8,18,.93);z-index:999;align-items:center;justify-content:center;padding:30px;cursor:zoom-out; }
#lb.open { display:flex; }
#lb img { max-width:100%;max-height:100%;object-fit:contain;border-radius:8px; }
</style>
</head>
<body>
<div id="deck">

<!-- ═══════════════════════════════════════════════
     PORTADA
═══════════════════════════════════════════════ -->
<div class="slide active" id="s0" style="justify-content:center;align-items:center;gap:0;">
  <div style="max-width:820px;width:100%;text-align:center;display:flex;flex-direction:column;align-items:center;gap:28px;">

    <div style="font-family:var(--mono);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--mut);">
      UAX &nbsp;&middot;&nbsp; Ingenieria Matematica &nbsp;&middot;&nbsp; 2025&ndash;26
    </div>

    <div>
      <div style="font-size:13px;font-family:var(--mono);color:var(--cyan);letter-spacing:.1em;text-transform:uppercase;margin-bottom:14px;">
        Inteligencia Artificial &nbsp;&middot;&nbsp; Caso practico optativo
      </div>
      <h1 style="font-size:42px;font-weight:700;line-height:1.2;letter-spacing:-.03em;margin:0;">
        Prediccion de<br>Diagnostico de <em style="color:var(--cyan)">Cancer</em>
      </h1>
      <div style="margin-top:16px;font-size:18px;color:var(--dim);font-weight:300;line-height:1.5;">
        Viabilidad del proyecto mediante<br>
        <strong style="color:var(--ink);font-weight:500;">Machine Learning y Redes Neuronales</strong>
      </div>
    </div>

    <div style="display:flex;gap:20px;justify-content:center;flex-wrap:wrap;">
      <div style="padding:12px 22px;background:var(--card);border:1px solid var(--border);border-radius:10px;text-align:center;">
        <div style="font-family:var(--mono);font-size:22px;font-weight:700;color:var(--cyan);">50.001</div>
        <div style="font-size:11px;color:var(--mut);margin-top:3px;">pacientes sinteticos</div>
      </div>
      <div style="padding:12px 22px;background:var(--card);border:1px solid var(--border);border-radius:10px;text-align:center;">
        <div style="font-family:var(--mono);font-size:22px;font-weight:700;color:var(--yellow);">5</div>
        <div style="font-size:11px;color:var(--mut);margin-top:3px;">algoritmos evaluados</div>
      </div>
      <div style="padding:12px 22px;background:var(--card);border:1px solid var(--border);border-radius:10px;text-align:center;">
        <div style="font-family:var(--mono);font-size:22px;font-weight:700;color:var(--green);">0.835</div>
        <div style="font-size:11px;color:var(--mut);margin-top:3px;">AUC-ROC mejor modelo</div>
      </div>
      <div style="padding:12px 22px;background:var(--card);border:1px solid var(--border);border-radius:10px;text-align:center;">
        <div style="font-family:var(--mono);font-size:22px;font-weight:700;color:var(--orange);">99.8%</div>
        <div style="font-size:11px;color:var(--mut);margin-top:3px;">del techo teorico</div>
      </div>
    </div>

    <div style="margin-top:8px;font-size:11px;color:var(--mut);font-family:var(--mono);">
      Pulsa &rarr; o la flecha para comenzar
    </div>
  </div>
</div>


<!-- ═══════════════════════════════════════════════
     SLIDE 1 -- OBJETIVO Y DATOS
═══════════════════════════════════════════════ -->
<div class="slide" id="s1">
  <div class="sh">
    <span class="badge">Prediccion de Cancer &middot; Estudio de Viabilidad ML</span>
    <span class="ctr">01 / 05</span>
  </div>
  <h1>Objetivo y <em>datos del proyecto</em></h1>

  <div style="display:grid;grid-template-columns:1fr 1.15fr;gap:16px;flex:1;min-height:0;">

    <!-- LEFT -->
    <div style="display:flex;flex-direction:column;gap:12px;min-height:0;">

      <div class="card" style="flex-shrink:0;">
        <div class="ct">Contexto del caso</div>
        <p style="font-size:13px;color:var(--dim);line-height:1.65;">
          Un hospital universitario recoge datos multimodales de
          <strong style="color:var(--ink);">50.001 pacientes sinteticos</strong>
          y quiere saber si esos datos son suficientes para anticipar un diagnostico de cancer.
          El objetivo es <strong style="color:var(--ink);">evaluar la viabilidad comparando algoritmos clasicos
          frente a una Red Neuronal Multicapa</strong> y recomendar la estrategia optima para un sistema de cribado real.
        </p>
      </div>

      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;flex-shrink:0;">
        <div class="card" style="padding:12px 14px;text-align:center;">
          <div style="font-family:var(--mono);font-size:9px;color:var(--mut);text-transform:uppercase;letter-spacing:.1em;">Pacientes</div>
          <div style="font-family:var(--mono);font-size:24px;font-weight:700;color:var(--cyan);line-height:1.2;margin:4px 0;">50.001</div>
          <div style="font-size:10.5px;color:var(--mut);">sinteticos</div>
        </div>
        <div class="card" style="padding:12px 14px;text-align:center;">
          <div style="font-family:var(--mono);font-size:9px;color:var(--mut);text-transform:uppercase;letter-spacing:.1em;">Prevalencia</div>
          <div style="font-family:var(--mono);font-size:24px;font-weight:700;color:var(--yellow);line-height:1.2;margin:4px 0;">19.3%</div>
          <div style="font-size:10.5px;color:var(--mut);">clase cancer</div>
        </div>
        <div class="card" style="padding:12px 14px;text-align:center;border-color:rgba(255,77,106,.3);">
          <div style="font-family:var(--mono);font-size:9px;color:var(--mut);text-transform:uppercase;letter-spacing:.1em;">Desbalance</div>
          <div style="font-family:var(--mono);font-size:24px;font-weight:700;color:var(--red);line-height:1.2;margin:4px 0;">4.19:1</div>
          <div style="font-size:10.5px;color:var(--mut);">sano : cancer</div>
        </div>
      </div>

      <div class="card" style="flex:1;overflow:hidden;min-height:0;">
        <div class="ct">Colecciones &middot; inclusion / exclusion</div>
        <table>
          <thead><tr><th>Coleccion</th><th class="r">Variables</th><th>Decision</th></tr></thead>
          <tbody>
            <tr><td>Bioquimica</td><td class="r">7 / 7</td><td><span class="pill pg">Incluida</span></td></tr>
            <tr><td>Clinica</td><td class="r">7 / 7</td><td><span class="pill pg">Incluida</span></td></tr>
            <tr><td>Genetica</td><td class="r">6 / 7</td><td><span class="pill py">Parcial &middot; ALK excluida</span></td></tr>
            <tr><td>Economica</td><td class="r">0 / 5</td><td><span class="pill pr">Excluida &middot; data leakage</span></td></tr>
            <tr><td>Generales</td><td class="r">2 / 4</td><td><span class="pill py">Parcial &middot; vive excluida</span></td></tr>
            <tr><td>Sociodemografia</td><td class="r">7 / 7</td><td><span class="pill pm">Sin senal real</span></td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- RIGHT -->
    <div style="display:flex;flex-direction:column;gap:12px;min-height:0;">

      <div class="card" style="flex-shrink:0;border-color:rgba(0,212,255,.25);background:linear-gradient(160deg,rgba(0,212,255,.04),var(--card));">
        <div class="ct">Variable objetivo</div>
        <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
          <div style="font-family:var(--mono);font-size:20px;font-weight:700;color:var(--cyan);">cancer</div>
          <div style="font-size:12px;color:var(--dim);">Binaria &nbsp;&middot;&nbsp; 0 = sano &nbsp;&middot;&nbsp; 1 = diagnostico de cancer</div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
          <div style="flex:1;height:9px;border-radius:4px;overflow:hidden;background:var(--bg2);">
            <div style="width:80.7%;height:100%;background:var(--mut);border-radius:4px 0 0 4px;"></div>
          </div>
          <span style="font-family:var(--mono);font-size:11px;color:var(--mut);width:48px;text-align:right;">80.7%</span>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <div style="flex:1;height:9px;border-radius:4px;overflow:hidden;background:var(--bg2);">
            <div style="width:19.3%;height:100%;background:var(--red);border-radius:4px 0 0 4px;"></div>
          </div>
          <span style="font-family:var(--mono);font-size:11px;color:var(--red);width:48px;text-align:right;">19.3%</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:4px;font-size:10.5px;color:var(--mut);">
          <span>Sano (clase 0)</span><span style="color:var(--red);">Cancer (clase 1)</span>
        </div>
      </div>

      <div class="card" style="flex:1;overflow:hidden;min-height:0;">
        <div class="ct">Decisiones sobre variables &middot; justificacion</div>
        <table>
          <thead><tr><th>Variable(s)</th><th>Decision</th><th>Motivo</th></tr></thead>
          <tbody>
            <tr>
              <td class="mono" style="font-size:11px;">coste_total &middot; dias_hospital</td>
              <td><span class="pill pr">Excluir</span></td>
              <td style="font-size:12px;">Consecuencias del diagnostico &rarr; leakage severo</td>
            </tr>
            <tr>
              <td class="mono" style="font-size:11px;">vive</td>
              <td><span class="pill pr">Excluir</span></td>
              <td style="font-size:12px;">Determinada por el diagnostico &rarr; leakage temporal</td>
            </tr>
            <tr>
              <td class="mono" style="font-size:11px;">mut_ALK</td>
              <td><span class="pill pr">Excluir</span></td>
              <td style="font-size:12px;">Chi&sup2; = 0.0 &middot; p = 0.93 &middot; senal nula</td>
            </tr>
            <tr>
              <td class="mono" style="font-size:11px;">mut_BRCA1 &middot; mut_TP53 &middot; &hellip;</td>
              <td><span class="pill pg">Incluir</span></td>
              <td style="font-size:12px;">Maximo peso predictivo en el generador</td>
            </tr>
            <tr>
              <td class="mono" style="font-size:11px;">nivel_educativo &middot; zona &middot; &hellip;</td>
              <td><span class="pill pm">Con nota</span></td>
              <td style="font-size:12px;">Sin senal real en este dataset sintetico</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="card" style="flex-shrink:0;padding:11px 18px;">
        <div class="ct">Pipeline ML</div>
        <div style="display:flex;align-items:center;gap:0;font-size:11px;font-family:var(--mono);flex-wrap:wrap;gap:6px;">
          <span style="padding:4px 10px;background:var(--bg2);border-radius:5px;color:var(--cyan);">Carga &amp; Merge</span>
          <span style="color:var(--mut);">&rarr;</span>
          <span style="padding:4px 10px;background:var(--bg2);border-radius:5px;color:var(--dim);">EDA</span>
          <span style="color:var(--mut);">&rarr;</span>
          <span style="padding:4px 10px;background:var(--bg2);border-radius:5px;color:var(--dim);">Features</span>
          <span style="color:var(--mut);">&rarr;</span>
          <span style="padding:4px 10px;background:var(--bg2);border-radius:5px;color:var(--dim);">Preproceso</span>
          <span style="color:var(--mut);">&rarr;</span>
          <span style="padding:4px 10px;background:var(--bg2);border-radius:5px;color:var(--yellow);">ML + MLP</span>
          <span style="color:var(--mut);">&rarr;</span>
          <span style="padding:4px 10px;background:var(--bg2);border-radius:5px;color:var(--green);">Evaluacion</span>
        </div>
      </div>

    </div>
  </div>

  <div class="sf">
    <span>UAX &middot; Ingenieria Matematica &middot; 2025&ndash;26</span>
    <div class="rule"></div>
    <span>01 &middot; objetivo y datos</span>
  </div>
</div>


<!-- ═══════════════════════════════════════════════
     SLIDE 2 -- MODELOS ML
═══════════════════════════════════════════════ -->
<div class="slide" id="s2">
  <div class="sh">
    <span class="badge">Modelos de Machine Learning &middot; Optuna TPE &middot; 20 trials</span>
    <span class="ctr">02 / 05</span>
  </div>
  <h1>Resultados de los <em>modelos ML complejos</em></h1>

  <div style="display:grid;grid-template-columns:1.25fr 1fr;gap:16px;flex:1;min-height:0;">

    <!-- LEFT -->
    <div style="display:flex;flex-direction:column;gap:12px;min-height:0;">

      <div class="card" style="flex-shrink:0;">
        <div class="ct">Tabla comparativa &middot; conjunto de test (20%) &middot; umbral 0.5</div>
        <table>
          <thead>
            <tr><th>Modelo</th><th class="r">Precision</th><th class="r">Recall</th><th class="r">F1</th><th class="r">AUC-ROC</th></tr>
          </thead>
          <tbody>
            <tr>
              <td style="color:var(--cyan);">LogReg baseline</td>
              <td class="r">0.432</td>
              <td class="r" style="color:var(--cyan);font-weight:600;font-family:var(--mono);">0.747</td>
              <td class="r">0.548</td>
              <td class="r" style="color:var(--cyan);font-weight:600;font-family:var(--mono);">0.835</td>
            </tr>
            <tr>
              <td style="color:var(--purple);">XGBoost</td>
              <td class="r">0.435</td>
              <td class="r" style="color:var(--purple);font-weight:600;font-family:var(--mono);">0.745</td>
              <td class="r">0.549</td>
              <td class="r mono">0.832</td>
            </tr>
            <tr>
              <td style="color:var(--green);">LightGBM</td>
              <td class="r">0.448</td>
              <td class="r mono">0.710</td>
              <td class="r">0.549</td>
              <td class="r mono">0.829</td>
            </tr>
            <tr style="background:rgba(255,183,0,.04);">
              <td style="color:var(--yellow);font-weight:600;">Random Forest &#9733;</td>
              <td class="r" style="color:var(--yellow);font-weight:600;font-family:var(--mono);">0.469</td>
              <td class="r mono">0.685</td>
              <td class="r" style="color:var(--yellow);font-weight:600;font-family:var(--mono);">0.557</td>
              <td class="r mono">0.827</td>
            </tr>
          </tbody>
        </table>
        <div style="margin-top:8px;font-size:11px;color:var(--mut);">&#9733; Random Forest &middot; mejor F1 global (0.557)</div>
      </div>

      <div class="card" style="flex-shrink:0;">
        <div class="ct">Validacion cruzada &middot; 5 folds &middot; F1 y AUC medio &plusmn; std</div>
        <table>
          <thead>
            <tr><th>Modelo</th><th class="r">F1 CV</th><th class="r">AUC CV</th></tr>
          </thead>
          <tbody>
            <tr>
              <td style="color:var(--cyan);">LogReg baseline</td>
              <td class="r mono">0.541 <span style="color:var(--mut);">&plusmn; 0.004</span></td>
              <td class="r mono">0.832 <span style="color:var(--mut);">&plusmn; 0.003</span></td>
            </tr>
            <tr>
              <td style="color:var(--purple);">XGBoost</td>
              <td class="r mono">0.537 <span style="color:var(--mut);">&plusmn; 0.003</span></td>
              <td class="r mono">0.826 <span style="color:var(--mut);">&plusmn; 0.003</span></td>
            </tr>
            <tr>
              <td style="color:var(--green);">LightGBM</td>
              <td class="r mono">0.539 <span style="color:var(--mut);">&plusmn; 0.002</span></td>
              <td class="r mono">0.823 <span style="color:var(--mut);">&plusmn; 0.002</span></td>
            </tr>
            <tr style="background:rgba(255,183,0,.04);">
              <td style="color:var(--yellow);">Random Forest</td>
              <td class="r" style="font-family:var(--mono);color:var(--yellow);">0.543 <span style="color:var(--mut);">&plusmn; 0.004</span></td>
              <td class="r mono">0.823 <span style="color:var(--mut);">&plusmn; 0.003</span></td>
            </tr>
          </tbody>
        </table>
        <div style="margin-top:8px;font-size:11px;color:var(--mut);">Resultados estables entre folds &middot; sin sobreajuste</div>
      </div>

      <div class="card" style="flex:1;border-color:rgba(255,77,106,.2);background:rgba(255,77,106,.025);">
        <div class="ct" style="color:var(--red);">Impacto del desbalance de clases (ratio 4.19:1)</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
          <div style="font-size:12.5px;color:var(--dim);line-height:1.6;">
            Sin correccion, el modelo ignora la clase minoritaria.
            Se aplica <span style="font-family:var(--mono);color:var(--ink);">class_weight='balanced'</span>
            y <span style="font-family:var(--mono);color:var(--ink);">scale_pos_weight=4.19</span>.
          </div>
          <div style="display:flex;flex-direction:column;gap:10px;justify-content:center;">
            <div>
              <div style="font-size:11px;color:var(--mut);margin-bottom:4px;">Sin class_weight</div>
              <div style="height:8px;border-radius:4px;background:var(--bg2);overflow:hidden;">
                <div style="width:0%;height:100%;background:var(--red);"></div>
              </div>
              <div style="font-family:var(--mono);font-size:12px;color:var(--red);margin-top:3px;">F1 = 0.000</div>
            </div>
            <div>
              <div style="font-size:11px;color:var(--mut);margin-bottom:4px;">Con class_weight</div>
              <div style="height:8px;border-radius:4px;background:var(--bg2);overflow:hidden;">
                <div style="width:55.7%;height:100%;background:var(--green);"></div>
              </div>
              <div style="font-family:var(--mono);font-size:12px;color:var(--green);margin-top:3px;">F1 = 0.557</div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- RIGHT: confusion matrix -->
    <div style="display:flex;flex-direction:column;gap:12px;min-height:0;">
      <div class="card" style="flex:1;display:flex;flex-direction:column;min-height:0;">
        <div class="ct">Matriz de confusion &middot; Random Forest (mejor F1)</div>
        <div style="flex:1;min-height:0;display:flex;align-items:center;justify-content:center;padding:6px 0;">
          <img src="CONFUSION_IMG" class="cimg" alt="Confusion matrix RF" style="max-height:300px;width:auto;">
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;flex-shrink:0;">
          <div style="padding:8px 10px;background:var(--bg2);border-radius:6px;border-left:2px solid var(--green);">
            <div style="font-size:10.5px;color:var(--mut);margin-bottom:2px;">Verdaderos Positivos</div>
            <span style="font-family:var(--mono);font-size:15px;font-weight:700;color:var(--green);">1.321</span>
            <span style="font-size:10.5px;color:var(--mut);margin-left:4px;">detectados</span>
          </div>
          <div style="padding:8px 10px;background:var(--bg2);border-radius:6px;border-left:2px solid var(--red);">
            <div style="font-size:10.5px;color:var(--mut);margin-bottom:2px;">Falsos Negativos</div>
            <span style="font-family:var(--mono);font-size:15px;font-weight:700;color:var(--red);">608</span>
            <span style="font-size:10.5px;color:var(--mut);margin-left:4px;">no detectados</span>
          </div>
        </div>
      </div>
    </div>

  </div>

  <div class="sf">
    <span>UAX &middot; Ingenieria Matematica &middot; 2025&ndash;26</span>
    <div class="rule"></div>
    <span>02 &middot; modelos ML</span>
  </div>
</div>


<!-- ═══════════════════════════════════════════════
     SLIDE 3 -- MLP
═══════════════════════════════════════════════ -->
<div class="slide" id="s3">
  <div class="sh">
    <span class="badge">Red Neuronal Multicapa &middot; TensorFlow / Keras</span>
    <span class="ctr">03 / 05</span>
  </div>
  <h1>Resultados de la <em>Red Neuronal (MLP)</em></h1>

  <div style="display:grid;grid-template-columns:1.6fr 1fr;gap:16px;flex:1;min-height:0;">

    <!-- LEFT: training curves -->
    <div class="card" style="display:flex;flex-direction:column;min-height:0;">
      <div class="ct">Curvas de entrenamiento &middot; perdida y AUC-ROC por epoca</div>
      <div style="flex:1;min-height:0;display:flex;align-items:center;padding:6px 0;">
        <img src="MLP_CURVES_IMG" class="cimg" alt="MLP training curves">
      </div>
    </div>

    <!-- RIGHT -->
    <div style="display:flex;flex-direction:column;gap:12px;min-height:0;">

      <div class="card" style="flex-shrink:0;">
        <div class="ct">Arquitectura &middot; 17.665 parametros</div>
        <div style="font-family:var(--mono);font-size:11px;line-height:1.9;color:var(--dim);">
          <div><span style="color:var(--cyan);">Input</span><span style="color:var(--mut);">(49)</span></div>
          <div style="margin-left:10px;">&rarr; Dense(128) + BN + ReLU + Drop(30%)</div>
          <div style="margin-left:10px;">&rarr; Dense(64)  + BN + ReLU + Drop(25%)</div>
          <div style="margin-left:10px;">&rarr; Dense(32)  + BN + ReLU + Drop(20%)</div>
          <div style="margin-left:10px;">&rarr; <span style="color:var(--green);">Sigmoid</span><span style="color:var(--mut);">(1)</span></div>
        </div>
        <div style="margin-top:7px;font-size:11px;color:var(--mut);">EarlyStopping patience=12 &middot; ReduceLROnPlateau factor=0.5</div>
      </div>

      <div class="card" style="flex-shrink:0;">
        <div class="ct">Metricas en test &middot; umbral 0.70 (optimizado en validacion)</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:4px;">
          <div style="text-align:center;padding:8px;background:var(--bg2);border-radius:6px;">
            <div style="font-family:var(--mono);font-size:19px;font-weight:700;color:var(--orange);">0.559</div>
            <div style="font-size:10px;color:var(--mut);margin-top:2px;">Recall</div>
          </div>
          <div style="text-align:center;padding:8px;background:var(--bg2);border-radius:6px;">
            <div style="font-family:var(--mono);font-size:19px;font-weight:700;color:var(--orange);">0.551</div>
            <div style="font-size:10px;color:var(--mut);margin-top:2px;">Precision</div>
          </div>
          <div style="text-align:center;padding:8px;background:var(--bg2);border-radius:6px;">
            <div style="font-family:var(--mono);font-size:19px;font-weight:700;color:var(--orange);">0.555</div>
            <div style="font-size:10px;color:var(--mut);margin-top:2px;">F1-Score</div>
          </div>
          <div style="text-align:center;padding:8px;background:var(--bg2);border-radius:6px;">
            <div style="font-family:var(--mono);font-size:19px;font-weight:700;color:var(--orange);">0.832</div>
            <div style="font-size:10px;color:var(--mut);margin-top:2px;">AUC-ROC</div>
          </div>
        </div>
        <div style="margin-top:7px;font-size:11px;color:var(--mut);">Epoca 21/200 &middot; mejor epoca: 9 &middot; umbral barrido en val (anti-leakage)</div>
      </div>

      <div class="card" style="flex:1;border-color:rgba(255,183,0,.2);background:rgba(255,183,0,.02);overflow:hidden;">
        <div class="ct">Comparacion directa &middot; MLP vs. Random Forest</div>
        <table style="margin-top:4px;">
          <thead><tr><th>Metrica</th><th class="r">MLP</th><th class="r">RF</th><th class="r">&Delta;</th></tr></thead>
          <tbody>
            <tr>
              <td>Recall</td>
              <td class="r mono">0.559</td>
              <td class="r" style="font-family:var(--mono);color:var(--yellow);">0.685</td>
              <td class="r" style="font-family:var(--mono);color:var(--red);">&minus;0.126</td>
            </tr>
            <tr>
              <td>F1-Score</td>
              <td class="r mono">0.555</td>
              <td class="r" style="font-family:var(--mono);color:var(--yellow);">0.557</td>
              <td class="r" style="font-family:var(--mono);color:var(--red);">&minus;0.002</td>
            </tr>
            <tr>
              <td>AUC-ROC</td>
              <td class="r" style="font-family:var(--mono);color:var(--orange);">0.832</td>
              <td class="r mono">0.827</td>
              <td class="r" style="font-family:var(--mono);color:var(--green);">+0.005</td>
            </tr>
          </tbody>
        </table>
        <div style="margin-top:8px;padding:7px 10px;background:var(--bg2);border-radius:6px;font-size:11.5px;color:var(--dim);line-height:1.55;">
          En datos tabulares, <strong style="color:var(--ink);">gradient boosting iguala o supera al MLP</strong>
          con menor coste computacional. La MLP recupera AUC pero pierde Recall significativamente.
        </div>
      </div>

    </div>
  </div>

  <div class="sf">
    <span>UAX &middot; Ingenieria Matematica &middot; 2025&ndash;26</span>
    <div class="rule"></div>
    <span>03 &middot; red neuronal MLP</span>
  </div>
</div>


<!-- ═══════════════════════════════════════════════
     SLIDE 4 -- COMPARATIVA GLOBAL
═══════════════════════════════════════════════ -->
<div class="slide" id="s4">
  <div class="sh">
    <span class="badge">Comparativa global &middot; ML vs. Red Neuronal</span>
    <span class="ctr">04 / 05</span>
  </div>
  <h1>Comparativa global <em>ML vs. Red Neuronal</em></h1>

  <div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;flex:1;min-height:0;">

    <!-- TOP-LEFT: metrics bar -->
    <div class="card" style="display:flex;flex-direction:column;min-height:0;">
      <div class="ct">Comparativa de metricas &middot; todos los modelos</div>
      <div style="flex:1;min-height:0;display:flex;align-items:center;padding:4px 0;">
        <img src="METRICS_BAR_IMG" class="cimg" alt="Metrics bar chart">
      </div>
    </div>

    <!-- TOP-RIGHT: ranking table -->
    <div class="card" style="display:flex;flex-direction:column;overflow:hidden;">
      <div class="ct">Ranking &middot; ordenado por F1</div>
      <table style="margin-top:4px;">
        <thead><tr><th>#</th><th>Modelo</th><th class="r">Precision</th><th class="r">Recall</th><th class="r">F1</th><th class="r">AUC</th></tr></thead>
        <tbody>
          <tr style="background:rgba(255,183,0,.04);">
            <td style="font-family:var(--mono);color:var(--yellow);">1</td>
            <td style="color:var(--yellow);font-weight:600;">Random Forest</td>
            <td class="r mono">0.469</td>
            <td class="r mono">0.685</td>
            <td class="r" style="font-family:var(--mono);color:var(--yellow);font-weight:600;">0.557</td>
            <td class="r mono">0.827</td>
          </tr>
          <tr>
            <td style="font-family:var(--mono);color:var(--mut);">2</td>
            <td style="color:var(--orange);">MLP</td>
            <td class="r mono">0.551</td>
            <td class="r mono">0.559</td>
            <td class="r" style="font-family:var(--mono);color:var(--orange);">0.555</td>
            <td class="r mono">0.832</td>
          </tr>
          <tr>
            <td style="font-family:var(--mono);color:var(--mut);">3</td>
            <td style="color:var(--purple);">XGBoost</td>
            <td class="r mono">0.435</td>
            <td class="r mono">0.745</td>
            <td class="r" style="font-family:var(--mono);color:var(--purple);">0.549</td>
            <td class="r mono">0.832</td>
          </tr>
          <tr>
            <td style="font-family:var(--mono);color:var(--mut);">4</td>
            <td style="color:var(--green);">LightGBM</td>
            <td class="r mono">0.448</td>
            <td class="r mono">0.710</td>
            <td class="r" style="font-family:var(--mono);color:var(--green);">0.549</td>
            <td class="r mono">0.829</td>
          </tr>
          <tr>
            <td style="font-family:var(--mono);color:var(--mut);">5</td>
            <td style="color:var(--cyan);">LogReg</td>
            <td class="r mono">0.432</td>
            <td class="r" style="font-family:var(--mono);color:var(--cyan);">0.747</td>
            <td class="r mono">0.548</td>
            <td class="r" style="font-family:var(--mono);color:var(--cyan);">0.835</td>
          </tr>
        </tbody>
      </table>
      <div style="margin-top:10px;padding:8px 10px;background:var(--bg2);border-radius:6px;font-size:11.5px;color:var(--dim);line-height:1.5;flex-shrink:0;">
        Todos alcanzan el <span style="font-family:var(--mono);color:var(--yellow);">98&ndash;99%</span> del
        Oracle AUC = <span style="font-family:var(--mono);color:var(--yellow);">0.836</span>.
        La brecha residual es ruido <span style="font-family:var(--mono);">&#949;&#126;N(0,0.8)</span> irrecuperable por diseno.
      </div>
    </div>

    <!-- BOTTOM-LEFT: ROC -->
    <div class="card" style="display:flex;flex-direction:column;min-height:0;">
      <div class="ct">Curvas ROC superpuestas</div>
      <div style="flex:1;min-height:0;display:flex;align-items:center;padding:4px 0;">
        <img src="ROC_IMG" class="cimg" alt="ROC curves">
      </div>
    </div>

    <!-- BOTTOM-RIGHT: PR -->
    <div class="card" style="display:flex;flex-direction:column;min-height:0;">
      <div class="ct">Espacio Precision-Recall</div>
      <div style="flex:1;min-height:0;display:flex;align-items:center;padding:4px 0;">
        <img src="PR_IMG" class="cimg" alt="Precision-Recall curves">
      </div>
    </div>

  </div>

  <div class="sf">
    <span>UAX &middot; Ingenieria Matematica &middot; 2025&ndash;26</span>
    <div class="rule"></div>
    <span>04 &middot; comparativa global</span>
  </div>
</div>


<!-- ═══════════════════════════════════════════════
     SLIDE 5 -- VIABILIDAD
═══════════════════════════════════════════════ -->
<div class="slide" id="s5">
  <div class="sh">
    <span class="badge">Conclusiones &middot; Viabilidad y Recomendacion</span>
    <span class="ctr">05 / 05</span>
  </div>
  <h1>Viabilidad del proyecto y <em>decision</em></h1>

  <div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;flex:1;min-height:0;">

    <!-- TL: datos suficientes -->
    <div class="card" style="border-color:rgba(0,232,122,.25);background:linear-gradient(160deg,rgba(0,232,122,.04),var(--card));overflow:hidden;">
      <div class="ct" style="color:var(--green);">Son los datos suficientes para anticipar el cancer?</div>
      <div style="display:flex;align-items:flex-start;gap:14px;margin-top:4px;">
        <div style="font-family:var(--mono);font-size:40px;font-weight:700;color:var(--green);line-height:1;flex-shrink:0;">SI</div>
        <div style="font-size:12.5px;color:var(--dim);line-height:1.65;">
          AUC-ROC = <strong style="color:var(--ink);font-family:var(--mono);">0.835</strong>,
          estable en validacion cruzada 5 folds (desv. tipica &lt;0.003).
          Los modelos alcanzan el <strong style="color:var(--ink);font-family:var(--mono);">98&ndash;99.8%</strong> del techo teorico del dataset.
          La senal predictiva esta completamente capturada; la brecha restante es ruido gaussiano irrecuperable por diseno.
        </div>
      </div>
    </div>

    <!-- TR: modelo recomendado -->
    <div class="card" style="border-color:rgba(0,212,255,.25);background:linear-gradient(160deg,rgba(0,212,255,.04),var(--card));overflow:hidden;">
      <div class="ct" style="color:var(--cyan);">Que modelo implantariais en el hospital?</div>
      <div style="font-size:14px;font-weight:600;color:var(--cyan);margin-bottom:8px;">
        Regresion Logistica &middot; umbral 0.46
      </div>
      <div style="font-size:12px;color:var(--dim);line-height:1.6;margin-bottom:10px;">
        Maximiza Recall (0.747) y tiene el mejor AUC (0.835). El umbral 0.46 deriva de la funcion de coste asimetrica
        <strong style="color:var(--ink);">FN = 5x, FP = 1x</strong> &mdash; detectar un cancer vale cinco veces mas que evitar una falsa alarma.
        Ademas es interpretable y trazable en entorno clinico.
      </div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;font-size:11px;text-align:center;">
        <div style="padding:7px;background:var(--bg2);border-radius:6px;">
          <div style="font-family:var(--mono);font-size:17px;font-weight:700;color:var(--green);">~150</div>
          <div style="color:var(--mut);margin-top:2px;">detectados</div>
        </div>
        <div style="padding:7px;background:var(--bg2);border-radius:6px;">
          <div style="font-family:var(--mono);font-size:17px;font-weight:700;color:var(--red);">~42</div>
          <div style="color:var(--mut);margin-top:2px;">perdidos</div>
        </div>
        <div style="padding:7px;background:var(--bg2);border-radius:6px;">
          <div style="font-family:var(--mono);font-size:17px;font-weight:700;color:var(--yellow);">~219</div>
          <div style="color:var(--mut);margin-top:2px;">falsas alarmas</div>
        </div>
      </div>
      <div style="margin-top:6px;font-size:10px;color:var(--mut);">Por cada 1.000 pacientes procesados</div>
    </div>

    <!-- BL: limitaciones -->
    <div class="card" style="overflow:hidden;">
      <div class="ct">Limitaciones del sistema actual</div>
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:4px;">
        <div style="display:flex;gap:9px;align-items:flex-start;">
          <span style="color:var(--red);flex-shrink:0;font-size:13px;margin-top:1px;">&#9654;</span>
          <span style="font-size:12px;color:var(--dim);line-height:1.55;"><strong style="color:var(--ink);">Dataset sintetico:</strong> variables sociodemograficas sin senal real; distribucion no validada clinicamente.</span>
        </div>
        <div style="display:flex;gap:9px;align-items:flex-start;">
          <span style="color:var(--red);flex-shrink:0;font-size:13px;margin-top:1px;">&#9654;</span>
          <span style="font-size:12px;color:var(--dim);line-height:1.55;"><strong style="color:var(--ink);">Calibracion deficiente:</strong> Brier score 0.15&ndash;0.17. Las probabilidades no son fiables como estimadores de riesgo absoluto.</span>
        </div>
        <div style="display:flex;gap:9px;align-items:flex-start;">
          <span style="color:var(--red);flex-shrink:0;font-size:13px;margin-top:1px;">&#9654;</span>
          <span style="font-size:12px;color:var(--dim);line-height:1.55;"><strong style="color:var(--ink);">31.5% de FN silenciosos</strong> irrecuperables: 0 mutaciones, glucosa normal, no fumador; indistinguibles de sanos por diseno del generador.</span>
        </div>
      </div>
    </div>

    <!-- BR: datos adicionales -->
    <div class="card" style="overflow:hidden;">
      <div class="ct">Que datos adicionales mejorarian el sistema?</div>
      <div style="display:flex;flex-direction:column;gap:8px;margin-top:4px;">
        <div style="display:flex;gap:9px;align-items:flex-start;">
          <span style="color:var(--cyan);flex-shrink:0;font-size:13px;margin-top:1px;">&#9654;</span>
          <span style="font-size:12px;color:var(--dim);line-height:1.55;"><strong style="color:var(--ink);">Marcadores tumorales:</strong> PSA, CEA, CA-125, AFP &mdash; alta especificidad diagnostica, ya validados clinicamente.</span>
        </div>
        <div style="display:flex;gap:9px;align-items:flex-start;">
          <span style="color:var(--cyan);flex-shrink:0;font-size:13px;margin-top:1px;">&#9654;</span>
          <span style="font-size:12px;color:var(--dim);line-height:1.55;"><strong style="color:var(--ink);">Historial familiar</strong> de cancer y <strong style="color:var(--ink);">biomarcadores epigeneticos</strong> (metilacion ADN) para capturar predisposicion hereditaria.</span>
        </div>
        <div style="display:flex;gap:9px;align-items:flex-start;">
          <span style="color:var(--cyan);flex-shrink:0;font-size:13px;margin-top:1px;">&#9654;</span>
          <span style="font-size:12px;color:var(--dim);line-height:1.55;"><strong style="color:var(--ink);">Imagenes diagnosticas</strong> (mamografia, TAC) mediante modelos multimodales para superar el techo del dataset tabular.</span>
        </div>
        <div style="margin-top:8px;padding:7px 10px;background:rgba(0,212,255,.05);border-radius:6px;font-size:11px;color:var(--dim);border-left:2px solid var(--cyan);line-height:1.5;">
          Cualquier uso en entorno clinico real requiere validacion prospectiva externa y supervision de un comite de etica.
        </div>
      </div>
    </div>

  </div>

  <div class="sf">
    <span>UAX &middot; Ingenieria Matematica &middot; 2025&ndash;26</span>
    <div class="rule"></div>
    <span>05 &middot; viabilidad y decision</span>
  </div>
</div>


<!-- ═══════════════════════════════════════════════
     FINAL
═══════════════════════════════════════════════ -->
<div class="slide" id="s6" style="justify-content:center;align-items:center;">
  <div style="max-width:700px;width:100%;text-align:center;display:flex;flex-direction:column;align-items:center;gap:32px;">

    <div style="font-size:13px;font-family:var(--mono);color:var(--mut);letter-spacing:.15em;text-transform:uppercase;">
      Conclusion principal
    </div>

    <div style="padding:28px 36px;background:var(--card);border:1px solid var(--border);border-radius:14px;border-top:3px solid var(--cyan);">
      <div style="font-size:17px;color:var(--dim);line-height:1.7;">
        Los datos son <strong style="color:var(--green);font-size:19px;">suficientes</strong> para anticipar el cancer.<br>
        Los cinco modelos alcanzan el
        <strong style="font-family:var(--mono);color:var(--yellow);font-size:18px;">98&ndash;99.8%</strong>
        del techo teorico.<br>
        La brecha restante no es limitacion del algoritmo:
        es <strong style="color:var(--ink);">ruido biologico irrecuperable</strong> por diseno del dataset.
      </div>
    </div>

    <div style="display:flex;gap:20px;justify-content:center;">
      <div style="padding:14px 24px;background:var(--card);border:1px solid rgba(0,232,122,.3);border-radius:10px;text-align:center;">
        <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:var(--cyan);">0.835</div>
        <div style="font-size:11px;color:var(--mut);margin-top:4px;">AUC-ROC mejor modelo</div>
      </div>
      <div style="padding:14px 24px;background:var(--card);border:1px solid rgba(0,232,122,.3);border-radius:10px;text-align:center;">
        <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:var(--yellow);">99.8%</div>
        <div style="font-size:11px;color:var(--mut);margin-top:4px;">del techo teorico Oracle</div>
      </div>
      <div style="padding:14px 24px;background:var(--card);border:1px solid rgba(0,232,122,.3);border-radius:10px;text-align:center;">
        <div style="font-family:var(--mono);font-size:28px;font-weight:700;color:var(--green);">LogReg</div>
        <div style="font-size:11px;color:var(--mut);margin-top:4px;">modelo recomendado</div>
      </div>
    </div>

    <div style="font-family:var(--mono);font-size:11px;color:var(--mut);letter-spacing:.08em;">
      UAX &nbsp;&middot;&nbsp; Ingenieria Matematica &nbsp;&middot;&nbsp; Inteligencia Artificial &nbsp;&middot;&nbsp; 2025&ndash;26
    </div>
  </div>
</div>

</div><!-- /deck -->

<div class="nav hidden" id="bp" onclick="go(-1)">&#8249;</div>
<div class="nav" id="bn" onclick="go(+1)">&#8250;</div>
<div id="dots"></div>
<div id="lb" onclick="closeLb()"><img id="lbi" src="" alt=""></div>

<script>
const slides = Array.from(document.querySelectorAll('.slide'));
const TOTAL = slides.length;
let cur = 0;

// Build dots
const dotsEl = document.getElementById('dots');
slides.forEach((_, i) => {
  const d = document.createElement('div');
  d.className = 'dot' + (i===0?' active':'');
  d.onclick = () => goTo(i);
  dotsEl.appendChild(d);
});

function goTo(n) {
  slides[cur].classList.remove('active');
  dotsEl.children[cur].classList.remove('active');
  cur = n;
  slides[cur].classList.add('active');
  dotsEl.children[cur].classList.add('active');
  document.getElementById('bp').classList.toggle('hidden', cur === 0);
  document.getElementById('bn').classList.toggle('hidden', cur === TOTAL - 1);
}
function go(d) { goTo(Math.max(0, Math.min(TOTAL-1, cur+d))); }

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ') go(+1);
  if (e.key === 'ArrowLeft') go(-1);
});

document.querySelectorAll('.cimg').forEach(img => {
  img.addEventListener('click', () => {
    document.getElementById('lbi').src = img.src;
    document.getElementById('lb').classList.add('open');
  });
});
function closeLb() { document.getElementById('lb').classList.remove('open'); }
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLb(); });
</script>
</body>
</html>
'''

html = html.replace('CONFUSION_IMG', confusion)
html = html.replace('MLP_CURVES_IMG', mlp_curves)
html = html.replace('METRICS_BAR_IMG', metrics_bar)
html = html.replace('ROC_IMG', roc)
html = html.replace('PR_IMG', pr)

out = 'presentacion/Caso Cancer.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(out) // 1024
print(f'Written: {out}  ({size_kb} KB)')
