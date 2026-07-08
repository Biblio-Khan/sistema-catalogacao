import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

# --- FUNÇÕES ---

def check_password():
    def password_entered():
        if st.session_state["password"] == "BIB@CDTN":
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
            st.error("Senha incorreta")

    if "password_correct" not in st.session_state:
        st.sidebar.text_input("Senha da Bibliotecária", type="password", on_change=password_entered, key="password")
        return False
    return st.session_state["password_correct"]

def interface_bibliotecaria():
    st.header("Painel de Controle da Bibliotecária")
    st.write("Aqui você processará as fichas pendentes.")

def formulario_aluno():
    st.title("Formulário de Elaboração de Ficha Catalográfica: Bib CDTN")
    st.info("Bem-vindo! Preencha o formulário abaixo.")
    
    st.subheader("Dados da Instituição")
    instituicao = "Centro de Desenvolvimento de Tecnologia Nuclear (CDTN)"
    st.write(f"Instituição: {instituicao}")

    # --- ORIENTAÇÕES DA BANCA ---
    st.subheader("Dados da Banca Examinadora")
    st.info("""
    **Instruções para Banca:**
    Selecione o número de membros e preencha seus respectivos nomes e titulações. 
    As informações devem seguir o padrão acadêmico, indicando corretamente o título (Dr., Dra., Me., Ma.).
    """)
    titulos_opcoes = ["Dr.", "Dra.", "Me.", "Ma."]

    st.write("### Orientador(es)")
    num_orientadores = st.selectbox("Quantos orientadores tem no seu trabalho?", options=[1, 2, 3], key="qtd_o")
    for i in range(num_orientadores):
        col1, col2 = st.columns([3, 1])
        col1.text_input(f"Nome do orientador {i+1}", key=f"nome_o_{i}")
        col2.selectbox("Título", titulos_opcoes, key=f"tit_o_{i}")

    st.write("### Coorientador(es)")
    num_coorientadores = st.selectbox("Quantos coorientadores tem no seu trabalho?", options=[0, 1, 2, 3], key="qtd_c")
    if num_coorientadores > 0:
        for i in range(num_coorientadores):
            col1, col2 = st.columns([3, 1])
            col1.text_input(f"Nome do coorientador {i+1}", key=f"nome_c_{i}")
            col2.selectbox("Título", titulos_opcoes, key=f"tit_c_{i}")

    with st.form("form_dados_gerais"):
        st.write("Outros campos do formulário...")
        st.form_submit_button("Enviar")

# --- FLUXO PRINCIPAL ---
if check_password():
    st.sidebar.success("Acesso Liberado: Bibliotecária")
    if st.sidebar.button("Sair do Painel"):
        st.session_state["password_correct"] = False
        st.rerun()
    interface_bibliotecaria()
else:
    formulario_aluno()
