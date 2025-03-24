import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")

    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)

    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)

    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)

    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)

    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)

    elif choice == "Relatórios":
        st.subheader("Relatórios Financeiros")

        # 1️⃣ Comparação Receita vs Despesa (Gráfico de Barras)
        st.subheader("Comparação Receita vs Despesa (Mês Atual)")
        df_finance = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now') GROUP BY tipo", conn)
        
        if not df_finance.empty:
            fig, ax = plt.subplots()
            ax.bar(df_finance["tipo"], df_finance["total"], color=["green", "red"])
            ax.set_ylabel("Valor (R$)")
            ax.set_title("Receita vs Despesa")
            st.pyplot(fig)

        # 2️⃣ Status das Contas a Pagar e Receber (Gráfico de Barras)
        st.subheader("Status das Contas a Pagar e Receber")
        df_status_pagar = pd.read_sql_query("SELECT status, COUNT(*) as quantidade FROM contas_pagar GROUP BY status", conn)
        df_status_receber = pd.read_sql_query("SELECT status, COUNT(*) as quantidade FROM contas_receber GROUP BY status", conn)

        if not df_status_pagar.empty and not df_status_receber.empty:
            fig, ax = plt.subplots()
            ax.bar(df_status_pagar["status"], df_status_pagar["quantidade"], color="red", label="Contas a Pagar")
            ax.bar(df_status_receber["status"], df_status_receber["quantidade"], color="green", alpha=0.7, label="Contas a Receber")
            ax.set_ylabel("Quantidade")
            ax.set_title("Status das Contas")
            ax.legend()
            st.pyplot(fig)

        # 3️⃣ Fluxo de Caixa por Mês (Gráfico de Linha)
        st.subheader("Fluxo de Caixa por Mês")
        df_fluxo = pd.read_sql_query("""
            SELECT strftime('%Y-%m', data) as mes, tipo, SUM(valor) as total
            FROM lancamentos
            GROUP BY mes, tipo
            ORDER BY mes ASC
        """, conn)

        if not df_fluxo.empty:
            fig, ax = plt.subplots()
            for tipo in df_fluxo["tipo"].unique():
                dados_filtrados = df_fluxo[df_fluxo["tipo"] == tipo]
                ax.plot(dados_filtrados["mes"], dados_filtrados["total"], marker='o', label=tipo)
            
            ax.set_ylabel("Valor (R$)")
            ax.set_xlabel("Mês")
            ax.set_title("Evolução da Receita e Despesa ao longo dos meses")
            ax.legend()
            plt.xticks(rotation=45)
            st.pyplot(fig)

    conn.close()


if __name__ == "__main__":
    main()
