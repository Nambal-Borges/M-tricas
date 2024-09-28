import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO
import matplotlib.pyplot as plt

# Funções adicionais
import plotly.express as px
import numpy as np

# Título e descrição
st.title("Dashboard de Métricas de Campanhas Publicitárias")
st.write("Monitore o desempenho das suas campanhas de maneira interativa e dinâmica.")

# Seção para entrada de dados da campanha
st.sidebar.header("Insira os dados da campanha")
alcance = st.sidebar.number_input("Alcance (Número de pessoas únicas):", min_value=0)
impressoes = st.sidebar.number_input("Impressões (Total de visualizações):", min_value=0)
cliques = st.sidebar.number_input("Cliques no anúncio:", min_value=0)
valor_investido = st.sidebar.number_input("Valor investido na campanha (R$):", min_value=0.0, format="%.2f")
valor_faturado = st.sidebar.number_input("Valor faturado (R$):", min_value=0.0, format="%.2f")

# Seção para filtrar por data
st.sidebar.header("Filtro por Data")
start_date = st.sidebar.date_input('Data de Início')
end_date = st.sidebar.date_input('Data de Fim')

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
    'Dia': pd.date_range(start=start_date, periods=5, freq='D').strftime('%d/%m/%Y'),
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

# Gráfico adicional com Plotly para análise de impressões
st.header("Gráfico de Impressões por Dia")
fig = px.bar(df, x='Dia', y='Impressões', title='Impressões ao Longo do Tempo')
st.plotly_chart(fig, use_container_width=True)

# Botão para baixar relatório CSV
st.sidebar.header("Baixar Relatório")
@st.cache_data
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

# Simulação de cenários
st.header("Simulação de Cenários")
investimento_simulado = st.slider('Simule o investimento futuro (R$)', 0, 10000, 5000)
cliques_simulados = np.random.poisson(lam=cliques, size=5)
df_simulacao = pd.DataFrame({
    'Dia': pd.date_range(start=start_date, periods=5, freq='D').strftime('%d/%m/%Y'),
    'Investimento (R$)': [investimento_simulado] * 5,
    'Cliques Simulados': cliques_simulados,
})

fig_simulacao = px.line(df_simulacao, x='Dia', y='Cliques Simulados', title='Simulação de Cliques Futuros')
st.plotly_chart(fig_simulacao, use_container_width=True)

