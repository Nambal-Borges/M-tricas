import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO

# Título e descrição
st.title("Dashboard de Métricas de Campanhas Publicitárias")
st.write("Monitore o desempenho das suas campanhas de maneira interativa.")

# Seção para entrada de dados da campanha
st.sidebar.header("Insira os dados da campanha")
alcance = st.sidebar.number_input("Alcance (Número de pessoas únicas):", min_value=0)
impressoes = st.sidebar.number_input("Impressões (Total de visualizações):", min_value=0)
cliques = st.sidebar.number_input("Cliques no anúncio:", min_value=0)
valor_investido = st.sidebar.number_input("Valor investido na campanha (R$):", min_value=0.0, format="%.2f")
valor_faturado = st.sidebar.number_input("Valor faturado (R$):", min_value=0.0, format="%.2f")

# Cálculos de métricas
if impressoes > 0:
    cpc = valor_investido / cliques if cliques > 0 else 0
    ctr = (cliques / impressoes) * 100
    roas = valor_faturado / valor_investido if valor_investido > 0 else 0
else:
    cpc = 0
    ctr = 0
    roas = 0

# Exibir os resultados
st.header("Resultados da Campanha")
st.metric(label="Custo por Clique (CPC)", value=f"R$ {cpc:.2f}")
st.metric(label="Taxa de Cliques (CTR)", value=f"{ctr:.2f}%")
st.metric(label="ROAS", value=f"{roas:.2f}")

# Gráfico interativo - evolução das métricas ao longo do tempo
st.header("Evolução das Métricas ao Longo do Tempo")
df = pd.DataFrame({
    'Dia': ['Dia 1', 'Dia 2', 'Dia 3', 'Dia 4', 'Dia 5'],
    'Cliques': [50, 75, 100, 125, 150],
    'Impressões': [500, 600, 700, 800, 900],
    'Investimento (R$)': [100, 150, 200, 250, 300]
})

chart = alt.Chart(df).mark_line().encode(
    x='Dia',
    y=alt.Y('Cliques', title='Número de Cliques'),
    tooltip=['Dia', 'Cliques', 'Impressões', 'Investimento (R$)']
).interactive()

st.altair_chart(chart, use_container_width=True)

# Botão para baixar relatório CSV
st.sidebar.header("Baixar Relatório")
@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df)

st.sidebar.download_button(
    label="Baixar relatório em CSV",
    data=csv,
    file_name='relatorio_campanha.csv',
    mime='text/csv',
)

# Upload de arquivo CSV para comparar campanhas
st.header("Comparar Campanhas")
uploaded_file = st.file_uploader("Faça upload de um arquivo CSV", type="csv")

if uploaded_file:
    comparacao_df = pd.read_csv(uploaded_file)
    st.write("Dados da Campanha Carregada:")
    st.dataframe(comparacao_df)

    # Gráfico de comparação de campanhas
    comparison_chart = alt.Chart(comparacao_df).mark_bar().encode(
        x='Campanha',
        y=alt.Y('ROAS', title='ROAS'),
        color='Campanha'
    )
    st.altair_chart(comparison_chart, use_container_width=True)

# Relatório de resumo em PDF (opcional)
import matplotlib.pyplot as plt

def generate_pdf_report():
    fig, ax = plt.subplots()
    ax.bar(df['Dia'], df['Cliques'], label="Cliques")
    ax.set_xlabel('Dia')
    ax.set_ylabel('Cliques')
    ax.set_title('Evolução dos Cliques')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='pdf')
    buffer.seek(0)
    return buffer

st.sidebar.header("Baixar Relatório em PDF")
if st.sidebar.button("Gerar PDF"):
    pdf = generate_pdf_report()
    st.sidebar.download_button("Baixar PDF", data=pdf, file_name="relatorio.pdf", mime="application/pdf")


