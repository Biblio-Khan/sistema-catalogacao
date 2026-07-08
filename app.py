import streamlit as st

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
    # A integração com o Turso virá aqui futuramente

def formulario_aluno():
    st.title("Formulário de Catalogação: Centro de Desenvolvimento de Tecnologia Nuclear")

    # --- Dados da Banca ---
    st.subheader("Dados da Banca Examinadora")
    st.info("""
    **Instruções para Banca:**
    Selecione o número de membros e preencha seus respectivos nomes e titulações. 
    As informações devem seguir o padrão acadêmico.
    """)
    titulos_opcoes = ["Dr.", "Dra.", "Me.", "Ma."]

    st.write("### Orientador(es)")
    num_orientadores = st.selectbox("Quantos orientadores tem no seu trabalho?", options=[1, 2, 3], key="qtd_o")
    lista_orientadores = []
    for i in range(num_orientadores):
        col1, col2 = st.columns([3, 1])
        nome_o = col1.text_input(f"Nome do orientador {i+1}", key=f"nome_o_{i}")
        tit_o = col2.selectbox("Título", titulos_opcoes, key=f"tit_o_{i}")
        if nome_o:
            lista_orientadores.append(f"{tit_o} {nome_o}")

    st.write("### Coorientador(es)")
    num_coorientadores = st.selectbox("Quantos coorientadores tem no seu trabalho?", options=[0, 1, 2, 3], key="qtd_c")
    lista_coorientadores = []
    if num_coorientadores > 0:
        for i in range(num_coorientadores):
            col1, col2 = st.columns([3, 1])
            nome_c = col1.text_input(f"Nome do coorientador {i+1}", key=f"nome_c_{i}")
            tit_c = col2.selectbox("Título", titulos_opcoes, key=f"tit_c_{i}")
            if nome_c:
                lista_coorientadores.append(f"{tit_c} {nome_c}")

    # --- Formulário de Envio ---
    with st.form("form_dados_gerais"):
        st.subheader("Dados da Instituição")
        instituicao = "Centro de Desenvolvimento de Tecnologia Nuclear (CDTN)"
        st.write(f"Instituição: {instituicao}")

        st.subheader("Dados do Autor")
        autor = st.text_input("Nome completo do autor (formato de citação)", placeholder="Sobrenome(s), Nome")

        st.subheader("Dados do Trabalho")
        titulo = st.text_input("Título do trabalho")
        subtitulo = st.text_input("Subtítulo (se houver)")
        tipo_trabalho = st.selectbox("Tipo de trabalho", ("Trabalho de conclusão de curso (Graduação)", "Trabalho de conclusão de curso (Especialização)", "Dissertação (Mestrado)", "Tese (Doutorado)"))
        area_concentracao = st.radio("Área de concentração", ("Ciência e Tecnologia das Radiações e Reatores Nucleares", "Ciência e Tecnologia dos Minerais e Meio Ambiente", "Ciência e Tecnologia dos Materiais"))
        ano_defesa = st.text_input("Ano da defesa")
        num_folhas = st.number_input("Número total de folhas", min_value=1, step=1)
        paginas_bibliografia = st.text_input("Páginas da Bibliografia")
        
        st.subheader("Palavras-chave")
        num_keywords = st.selectbox("Quantidade de palavras-chave", options=[1, 2, 3, 4])
        keywords = [st.text_input(f"Palavra-chave {i+1}", key=f"kw_{i}") for i in range(num_keywords)]
        ilustracoes = st.radio("Possui ilustrações?", ("Não", "Sim"))
        
        submit_button = st.form_submit_button("Enviar dados")

    if submit_button:
        if autor and titulo and ano_defesa and num_folhas:
            if "," not in autor:
                st.warning("Atenção: O formato do nome do autor parece estar incorreto (falta a vírgula).")
            else:
                st.success("Dados registrados com sucesso!")
                # Lógica de exibição e salvamento aqui...
        else:
            st.error("Os campos Autor, Título, Ano e Número de folhas são obrigatórios.")

# --- FLUXO PRINCIPAL ---
if check_password():
    st.sidebar.success("Acesso Liberado: Bibliotecária")
    if st.sidebar.button("Sair do Painel"):
        st.session_state["password_correct"] = False
        st.rerun()
    interface_bibliotecaria()
else:
    formulario_aluno()
