# ==========================================
# Actividad de visualizacion
# ==========================================

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración general
st.set_page_config(page_title="University Dashboard", layout="wide")
sns.set(style="whitegrid")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("university_student_data.csv")
    return df

df = load_data()

#  Encabezado
st.title("🎓 University Student Data Dashboard")
st.markdown("Visualización interactiva de admisiones, matrícula, retención y satisfacción estudiantil.")

# Filtros interactivos
col1, col2 = st.columns(2)
years = sorted(df["Year"].unique())
terms = sorted(df["Term"].unique())

with col1:
    year_filter = st.multiselect("Selecciona año(s):", years, default=years)
with col2:
    term_filter = st.multiselect("Selecciona período(s):", terms, default=terms)

# Filtrar datos según selección
filtered_df = df[(df["Year"].isin(year_filter)) & (df["Term"].isin(term_filter))]

# KPIs 
avg_retention = filtered_df["Retention Rate (%)"].mean()
avg_satisfaction = filtered_df["Student Satisfaction (%)"].mean()
total_enrolled = filtered_df["Enrolled"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("📈 Retención promedio", f"{avg_retention:.2f}%")
col2.metric("😊 Satisfacción promedio", f"{avg_satisfaction:.2f}%")
col3.metric("👥 Total matriculados", f"{total_enrolled:,}")

# Gráficos
st.subheader("📊 Tendencia de Retención y Satisfacción por Año")

# Gráfico 1
fig, ax = plt.subplots()
sns.lineplot(
    data=filtered_df.groupby("Year")["Retention Rate (%)"].mean().reset_index(),
    x="Year", y="Retention Rate (%)", marker="o", ax=ax
)
ax.set_title("Tendencia de la Tasa de Retención por Año")
st.pyplot(fig)

# Gráfico 2
fig, ax = plt.subplots()
sns.barplot(
    data=filtered_df.groupby("Year")["Student Satisfaction (%)"].mean().reset_index(),
    x="Year", y="Student Satisfaction (%)", palette="coolwarm", ax=ax
)
ax.set_title("Satisfacción Promedio de Estudiantes por Año")
st.pyplot(fig)

# Gráfico 3: Comparación entre términos
st.subheader("📅 Comparación entre Términos (Spring vs Fall)")
fig, ax = plt.subplots()
sns.boxplot(data=filtered_df, x="Term", y="Retention Rate (%)", palette="pastel", ax=ax)
ax.set_title("Tasa de Retención por Término Académico")
st.pyplot(fig)

# Gráfico 4: Matrícula por facultad
st.subheader("🏫 Matrícula por Facultad")
faculty_cols = ["Engineering Enrolled", "Business Enrolled", "Arts Enrolled", "Science Enrolled"]
faculty_data = (
    filtered_df.groupby("Year")[faculty_cols]
    .mean()
    .reset_index()
    .melt(id_vars="Year", var_name="Faculty", value_name="Students")
)

fig, ax = plt.subplots()
sns.lineplot(data=faculty_data, x="Year", y="Students", hue="Faculty", marker="o", ax=ax)
ax.set_title("Evolución de Matrícula por Facultad")
st.pyplot(fig)

# 6️⃣ Pie de página
st.markdown("---")
st.caption("Desarrollado por Henry Angulo, Christian Perez — Universidad de la Costa")
