import streamlit as st

st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

st.title("📚 Formulário de Catalogação: Centro de Desenvolvimento de Tecnologia Nuclear")

# --- Dados da Banca (FORA do form para garantir reatividade) ---
st.subheader("Dados da Banca Examinadora")
titulos_opcoes = ["Dr.", "Dra.", "Me.", "Ma."]

st.write("### 🎓 Orientador(es)")
num_orientadores = st.selectbox("Quantos orientadores tem no seu trabalho?", options=[1, 2, 3], key="qtd_o")
lista_orientadores = []
for i in range(num_orientadores):
    col1, col2 = st.columns([3, 1])
    nome_o = col1.text_input(f"Nome do orientador {i+1}", key=f"nome_o_{i}")
    tit_o = col2.selectbox("Título", titulos_opcoes, key=f"tit_o_{i}")
    if nome_o:
        lista_orientadores.append(f"{tit_o} {nome_o}")

st.write("### 🤝 Coorientador(es)")
num_coorientadores = st.selectbox("Quantos coorientadores tem no seu trabalho?", options=[0, 1, 2, 3], key="qtd_c")
lista_coorientadores = []
if num_coorientadores > 0:
    for i in range(num_coorientadores):
        col1, col2 = st.columns([3, 1])
        nome_c = col1.text_input(f"Nome do coorientador {i+1}", key=f"nome_c_{i}")
        tit_c = col2.selectbox("Título", titulos_opcoes, key=f"tit_c_{i}")
        if nome_c:
            lista_coorientadores.append(f"{tit_c} {nome_c}")

# --- Início do Formulário de Envio ---
with st.form("form_dados_gerais"):
    st.subheader("Dados da Instituição")
    instituicao = "Centro de Desenvolvimento de Tecnologia Nuclear (CDTN)"
    st.write(f"**Instituição:** {instituicao}")

    st.subheader("Dados do Autor")
    st.info("**Instruções para o Autor:** Sobrenome(s), Nome (Ex: Pires Filho, João)")
    autor = st.text_input("Nome completo do autor", placeholder="Sobrenome(s), Nome")

    st.subheader("Dados do Trabalho")
    titulo = st.text_input("Título do trabalho")
    subtitulo = st.text_input("Subtítulo (se houver)")
    
    tipo_trabalho = st.selectbox("Tipo de trabalho e titulação", ("Trabalho de conclusão de curso (Graduação)", "Trabalho de conclusão de curso (Especialização)", "Dissertação (Mestrado)", "Tese (Doutorado)"))
    area_concentracao = st.radio("Área de concentração", ("Ciência e Tecnologia das Radiações e Reatores Nucleares", "Ciência e Tecnologia dos Minerais e Meio Ambiente", "Ciência e Tecnologia dos Materiais"))
    ano_defesa = st.text_input("Ano da defesa", placeholder="Ex: 2026")
    
    num_folhas = st.number_input("Número total de folhas", min_value=1, step=1)
    st.caption("Informe o número total de folhas começando pela folha de rosto.")
    
    paginas_bibliografia = st.text_input("Páginas da Bibliografia", placeholder="Ex: 142 - 147")
    st.caption("Informe o intervalo de páginas onde a Bibliografia se encontra")
    
    st.subheader("Palavras-chave")
    num_keywords = st.selectbox("Quantidade de palavras-chave", options=[1, 2, 3, 4])
    keywords = [st.text_input(f"Palavra-chave {i+1}", key=f"kw_{i}") for i in range(num_keywords)]
    
    ilustracoes = st.radio("Possui ilustrações?", ("Não", "Sim"))
    
    submit_button = st.form_submit_button("Enviar dados")

# --- Processamento Final ---
if submit_button:
    if autor and titulo and ano_defesa and num_folhas:
        if "," not in autor:
            st.warning("⚠️ Atenção: O formato do nome do autor parece estar incorreto (falta a vírgula).")
        else:
            st.success("Dados registrados com sucesso!")
            st.write(f"**Instituição:** {instituicao}")
            st.write(f"**Tipo de trabalho:** {tipo_trabalho}")
            st.write(f"**Área de Concentração:** {area_concentracao}")
            st.write(f"**Autor:** {autor}")
            st.write(f"**Orientador(es):** " + ", ".join(lista_orientadores))
            if lista_coorientadores:
                st.write(f"**Coorientador(es):** " + ", ".join(lista_coorientadores))
            st.write(f"**Título:** {titulo}")
            if subtitulo:
                st.write(f"**Subtítulo:** {subtitulo}")
            st.write(f"**Ano da defesa:** {ano_defesa}")
            st.write(f"**Palavras-chave:** " + ", ".join([k for k in keywords if k]))
            
            resumo_folhas = f"{num_folhas} f."
            if ilustracoes == "Sim":
                resumo_folhas += " il."
            st.write(f"**Número de folhas:** {resumo_folhas}")
            
            if paginas_bibliografia:
                st.write(f"**Bibliografia:** p. {paginas_bibliografia}")
    else:
        st.error("Por favor, preencha todos os campos obrigatórios.")
