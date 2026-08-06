# -*- coding: utf-8 -*-
"""
DEMO — Portal para un DESPACHO CONTABLE ("Contadores y Asociados").

Es una DEMOSTRACION para vender: todos los datos son de EJEMPLO (inventados).
Mismo estilo que el portal de Eduardo, pero con modulos que si usa un despacho:
facturacion (CFDI), impuestos (IVA/ISR), estados financieros, clientes,
obligaciones ante el SAT y un tablero.

Correr:  py -m streamlit run app.py
"""
from __future__ import annotations

import datetime as dt

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

MARCA = "Contadores y Asociados"
COLOR = "#2F88E0"

st.set_page_config(page_title=f"Portal {MARCA}", page_icon="📘", layout="wide",
                   initial_sidebar_state="expanded")


# --------------------------------------------------------------------------- #
# Datos de EJEMPLO (inventados, solo para el demo)
# --------------------------------------------------------------------------- #
def _clientes() -> pd.DataFrame:
    return pd.DataFrame([
        {"RFC": "GARC850312AB1", "Cliente": "Comercializadora García SA de CV",
         "Régimen": "General de Ley PM", "Al corriente": "Sí"},
        {"RFC": "LOMJ900715K23", "Cliente": "Juan López Martínez",
         "Régimen": "RESICO PF", "Al corriente": "Sí"},
        {"RFC": "SERV880920QT4", "Cliente": "Servicios Integrales del Norte",
         "Régimen": "General de Ley PM", "Al corriente": "No"},
        {"RFC": "TERM770101HH8", "Cliente": "Distribuidora Termar",
         "Régimen": "General de Ley PM", "Al corriente": "Sí"},
        {"RFC": "ROGA950505MN2", "Cliente": "Ana Rodríguez Gómez",
         "Régimen": "Actividad Empresarial", "Al corriente": "Sí"},
        {"RFC": "IMPC820404LP9", "Cliente": "Importadora del Centro SA",
         "Régimen": "General de Ley PM", "Al corriente": "No"},
    ])


def _facturas() -> pd.DataFrame:
    return pd.DataFrame([
        {"Folio": "A-1042", "Fecha": "2026-08-03", "Tipo": "Emitida",
         "Cliente": "Comercializadora García SA", "Subtotal": 45000.0, "IVA": 7200.0, "Total": 52200.0, "Estatus": "Vigente"},
        {"Folio": "A-1043", "Fecha": "2026-08-04", "Tipo": "Emitida",
         "Cliente": "Distribuidora Termar", "Subtotal": 18000.0, "IVA": 2880.0, "Total": 20880.0, "Estatus": "Vigente"},
        {"Folio": "P-8871", "Fecha": "2026-08-02", "Tipo": "Recibida",
         "Cliente": "Papelería Corporativa", "Subtotal": 3200.0, "IVA": 512.0, "Total": 3712.0, "Estatus": "Vigente"},
        {"Folio": "A-1044", "Fecha": "2026-08-05", "Tipo": "Emitida",
         "Cliente": "Servicios Integrales del Norte", "Subtotal": 62500.0, "IVA": 10000.0, "Total": 72500.0, "Estatus": "Vigente"},
        {"Folio": "P-8872", "Fecha": "2026-08-05", "Tipo": "Recibida",
         "Cliente": "Combustibles del Bajío", "Subtotal": 9800.0, "IVA": 1568.0, "Total": 11368.0, "Estatus": "Vigente"},
        {"Folio": "A-1041", "Fecha": "2026-08-01", "Tipo": "Emitida",
         "Cliente": "Importadora del Centro SA", "Subtotal": 28000.0, "IVA": 4480.0, "Total": 32480.0, "Estatus": "Cancelada"},
    ])


_MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago"]


def _ingresos_mes() -> pd.DataFrame:
    ingresos = [180000, 205000, 168000, 220000, 240000, 198000, 260000, 143580]
    return pd.DataFrame({"Mes": _MESES, "Ingresos": ingresos}).set_index("Mes")


def _money(x) -> str:
    try:
        return "$" + format(float(x), ",.2f")
    except (TypeError, ValueError):
        return str(x)


# --------------------------------------------------------------------------- #
# Estilo (tarjetas del menu como bloques, igual que el portal real)
# --------------------------------------------------------------------------- #
def _css() -> None:
    st.markdown(
        """
        <style>
          [data-testid='stAppDeployButton']{display:none;}
          [data-testid='stMainMenuButton']{display:none;}
          footer{display:none;}
          .st-key-menu div[data-testid="stButton"] button{
              min-height: 104px; justify-content:flex-start; text-align:left;
              padding:18px 22px; border:1px solid #232B34; border-radius:14px;
              background:#171C22; color:#EAF0F6; font-weight:600;
          }
          .st-key-menu div[data-testid="stButton"] button:hover{
              border-color:#2F88E0; background:#1B222B;
          }
          /* Menu lateral (barra izquierda) como el portal real */
          [data-testid="stSidebar"] div[data-testid="stButton"] button{
              justify-content:flex-start; text-align:left; font-weight:600;
              border:1px solid #232B34; border-radius:12px; background:#171C22; color:#EAF0F6;
          }
          [data-testid="stSidebar"] div[data-testid="stButton"] button:hover{
              border-color:#2F88E0; background:#1B222B;
          }
          /* La flecha para abrir/cerrar el menu lateral SIEMPRE visible (en celular no hay hover) */
          [data-testid="stSidebarCollapseButton"]{ visibility:visible !important; opacity:1 !important; }
          .st-key-login_box{ max-width: 400px; margin: 0 auto; }
        </style>
        """.replace("#2F88E0", COLOR),
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- #
# LOGIN (de mentiritas, solo para que el demo se vea completo)
# --------------------------------------------------------------------------- #
def login() -> None:
    st.write("")
    with st.container(key="login_box"):
        st.markdown(
            f"<div style='text-align:center'>"
            f"<div style='display:inline-flex;width:74px;height:74px;border-radius:16px;"
            f"background:{COLOR};align-items:center;justify-content:center;font-size:34px'>📘</div>"
            f"<h2 style='margin:.4rem 0 0'>{MARCA}</h2>"
            f"<p style='color:#8A97A6;margin:.2rem 0 1rem'>Bienvenido al portal de {MARCA}</p></div>",
            unsafe_allow_html=True,
        )
        with st.form("login"):
            st.text_input("Usuario", value="demo")
            st.text_input("Contraseña", value="demo", type="password")
            entrar = st.form_submit_button("Entrar", type="primary", use_container_width=True)
        st.caption("Demo: solo da clic en **Entrar**.")
        if entrar:
            st.session_state["entro"] = True
            st.rerun()


# --------------------------------------------------------------------------- #
# MODULOS
# --------------------------------------------------------------------------- #
_MENU = [
    ("tablero", "📊 Tablero"),
    ("facturas", "🧾 Facturación (CFDI)"),
    ("impuestos", "🧮 Cálculo de impuestos"),
    ("estados", "📈 Estados financieros"),
    ("clientes", "📁 Clientes del despacho"),
    ("obligaciones", "📅 Obligaciones SAT"),
]


def inicio() -> None:
    st.markdown(f"## Bienvenido 👋")
    st.caption(f"Portal contable · {MARCA} — toca un módulo para abrirlo.")
    with st.container(key="menu"):
        cols = st.columns(3)
        for i, (clave, titulo) in enumerate(_MENU):
            if cols[i % 3].button(titulo, key=f"m_{clave}", use_container_width=True):
                st.session_state["pag"] = clave
                st.rerun()


def _volver() -> None:
    if st.button("← Inicio"):
        st.session_state["pag"] = "inicio"
        st.rerun()


def tablero() -> None:
    _volver()
    st.title("📊 Tablero del despacho")
    c = st.columns(4)
    c[0].metric("Clientes activos", "6")
    c[1].metric("Facturas del mes", "24", "+3")
    c[2].metric("IVA por pagar (Ago)", _money(14320))
    c[3].metric("Clientes con adeudo", "2", "-1")
    st.markdown("#### Ingresos facturados por mes")
    st.bar_chart(_ingresos_mes(), color=COLOR)
    st.caption("Datos de ejemplo — demostración.")


def facturas() -> None:
    _volver()
    st.title("🧾 Facturación (CFDI)")
    df = _facturas()
    filtro = st.segmented_control("Ver", ["Todas", "Emitidas", "Recibidas"], default="Todas")
    if filtro == "Emitidas":
        df = df[df["Tipo"] == "Emitida"]
    elif filtro == "Recibidas":
        df = df[df["Tipo"] == "Recibida"]
    emitidas = df[df["Tipo"] == "Emitida"]["IVA"].sum()
    recibidas = df[df["Tipo"] == "Recibida"]["IVA"].sum()
    c = st.columns(3)
    c[0].metric("IVA trasladado (emitidas)", _money(emitidas))
    c[1].metric("IVA acreditable (recibidas)", _money(recibidas))
    c[2].metric("IVA a pagar", _money(max(emitidas - recibidas, 0)))
    st.dataframe(df, hide_index=True, use_container_width=True, column_config={
        "Subtotal": st.column_config.NumberColumn(format="dollar"),
        "IVA": st.column_config.NumberColumn(format="dollar"),
        "Total": st.column_config.NumberColumn(format="dollar")})
    st.download_button("⬇ Descargar (Excel)", df.to_csv(index=False).encode("utf-8-sig"),
                       file_name="facturas_demo.csv", mime="text/csv")


def impuestos() -> None:
    _volver()
    st.title("🧮 Cálculo de impuestos (mensual)")
    st.caption("Estimación sencilla de IVA e ISR provisional. Datos de ejemplo, edítalos.")
    c = st.columns(2)
    ingresos = c[0].number_input("Ingresos gravados del mes", value=143580.0, step=1000.0)
    gastos = c[1].number_input("Gastos y compras (con IVA)", value=68000.0, step=1000.0)
    tasa_iva = st.select_slider("Tasa de IVA", options=[0, 8, 16], value=16)
    iva_trasladado = round(ingresos * tasa_iva / 100, 2)
    iva_acreditable = round(gastos * tasa_iva / 100, 2)
    iva_pagar = max(round(iva_trasladado - iva_acreditable, 2), 0)
    base_isr = max(ingresos - gastos, 0)
    isr = round(base_isr * 0.30, 2)  # tasa PM ilustrativa
    c = st.columns(3)
    c[0].metric("IVA por pagar", _money(iva_pagar))
    c[1].metric("Base para ISR", _money(base_isr))
    c[2].metric("ISR provisional (30%)", _money(isr))
    st.info(f"Total estimado a pagar al SAT este mes: **{_money(iva_pagar + isr)}** "
            "· *(cálculo ilustrativo del demo)*")


def estados() -> None:
    _volver()
    st.title("📈 Estados financieros")
    st.markdown("#### Estado de resultados (Agosto 2026)")
    er = pd.DataFrame([
        {"Concepto": "Ingresos", "Importe": 143580.0},
        {"Concepto": "Costo de ventas", "Importe": -61200.0},
        {"Concepto": "Utilidad bruta", "Importe": 82380.0},
        {"Concepto": "Gastos de operación", "Importe": -34500.0},
        {"Concepto": "Utilidad de operación", "Importe": 47880.0},
        {"Concepto": "ISR estimado", "Importe": -14364.0},
        {"Concepto": "Utilidad neta", "Importe": 33516.0},
    ])
    st.dataframe(er, hide_index=True, use_container_width=True,
                 column_config={"Importe": st.column_config.NumberColumn(format="dollar")})
    c = st.columns(3)
    c[0].metric("Utilidad bruta", _money(82380))
    c[1].metric("Utilidad neta", _money(33516))
    c[2].metric("Margen neto", "23.3%")


def clientes() -> None:
    _volver()
    st.title("📁 Clientes del despacho")
    df = _clientes()
    st.caption(f"{len(df)} clientes · {int((df['Al corriente'] == 'Sí').sum())} al corriente.")
    st.dataframe(df, hide_index=True, use_container_width=True)


def obligaciones() -> None:
    _volver()
    st.title("📅 Obligaciones ante el SAT")
    ob = pd.DataFrame([
        {"Obligación": "Declaración mensual de IVA", "Periodo": "Julio 2026", "Vence": "2026-08-17", "Estatus": "🟠 Pendiente"},
        {"Obligación": "Pago provisional de ISR", "Periodo": "Julio 2026", "Vence": "2026-08-17", "Estatus": "🟠 Pendiente"},
        {"Obligación": "DIOT", "Periodo": "Julio 2026", "Vence": "2026-08-31", "Estatus": "🟠 Pendiente"},
        {"Obligación": "Contabilidad electrónica", "Periodo": "Julio 2026", "Vence": "2026-09-03", "Estatus": "🟢 Enviada"},
    ])
    st.dataframe(ob, hide_index=True, use_container_width=True)
    st.warning("⚠️ 3 obligaciones vencen esta semana.")


_RUTAS = {"tablero": tablero, "facturas": facturas, "impuestos": impuestos,
          "estados": estados, "clientes": clientes, "obligaciones": obligaciones}


def _sin_zoom() -> None:
    """Desactiva el zoom (pellizco en celular, doble toque y Ctrl+rueda en PC)."""
    components.html(
        """
        <script>
        (function () {
          const doc = window.parent.document;
          let meta = doc.querySelector('meta[name="viewport"]');
          if (!meta) { meta = doc.createElement('meta'); meta.name = 'viewport'; doc.head.appendChild(meta); }
          meta.setAttribute('content',
            'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0, user-scalable=no');
          const s = doc.createElement('style');
          s.textContent = 'html,body{touch-action:manipulation;}';
          doc.head.appendChild(s);
          const stop = (e) => { if (e.ctrlKey || e.metaKey) e.preventDefault(); };
          doc.addEventListener('wheel', stop, { passive: false });
          ['gesturestart','gesturechange','gestureend'].forEach((ev) =>
            doc.addEventListener(ev, (e) => e.preventDefault(), { passive: false }));
          doc.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && ['+','-','=','0'].includes(e.key)) e.preventDefault();
          });
        })();
        </script>
        """,
        height=0,
    )


def main() -> None:
    _css()
    _sin_zoom()
    if not st.session_state.get("entro"):
        login()
        return
    pag = st.session_state.get("pag", "inicio")
    with st.sidebar:
        st.markdown(f"### {MARCA}")
        st.caption("DEMOSTRACIÓN · datos de ejemplo")
        st.write("")
        if st.button("🏠 Inicio", use_container_width=True, key="nav_inicio"):
            st.session_state["pag"] = "inicio"
            st.rerun()
        for _clave, _titulo in _MENU:
            if st.button(_titulo, use_container_width=True, key=f"nav_{_clave}"):
                st.session_state["pag"] = _clave
                st.rerun()
        st.write("")
        st.divider()
        if st.button("Cerrar sesión", use_container_width=True, key="nav_salir"):
            st.session_state.clear()
            st.rerun()
    if pag == "inicio":
        inicio()
    else:
        _RUTAS.get(pag, inicio)()


if __name__ == "__main__":
    main()
