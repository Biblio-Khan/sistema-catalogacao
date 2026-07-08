import streamlit as st

st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

st.title("📚 Formulário de Catalogação: Centro de Desenvolvimento de Tecnologia Nuclear")

with st.form("form_cadastro"):
    st.subheader("Dados da Instituição")
    instituicao = "Centro de Desenvolvimento de Tecnologia Nuclear (CDTN)"
    st.write(f"**Instituição:** {instituicao}")

    st.subheader("Dados do Autor")
    # ... (Instruções mantidas)
    autor = st.text_input("Nome completo do autor (formato de citação)", placeholder="Sobrenome(s), Nome")

    st.subheader("Dados do Trabalho")
    titulo = st.text_input("Título do trabalho", placeholder="Apenas a primeira letra da primeira palavra e nomes próprios em maiúsculas")
    subtitulo = st.text_input("Subtítulo (se houver)", placeholder="Insira o subtítulo, se existir")
    
    tipo_trabalho = st.selectbox("Tipo de trabalho e titulação", ("Trabalho de conclusão de curso (Graduação)", "Trabalho de conclusão de curso (Especialização)", "Dissertação (Mestrado)", "Tese (Doutorado)"))
    area_concentracao = st.radio("Área de concentração", ("Ciência e Tecnologia das Radiações e Reatores Nucleares", "Ciência e Tecnologia dos Minerais e Meio Ambiente", "Ciência e Tecnologia dos Materiais"))
    ano_defesa = st.text_input("Ano da defesa", placeholder="Ex: 2026")
    
    # --- Nova seção: Banca Examinadora ---
    st.subheader("Dados da Banca Examinadora")
    num_orientadores = st.selectbox("Quantos orientadores tem no seu trabalho?", options=[1, 2, 3])
    
    orientadores = []
    for i in range(num_orientadores):
        orientadores.append(st.text_input(f"Nome do orientador {i+1}"))
    # -------------------------------------

    num_folhas = st.number_input("Número total de folhas", min_value=1, step=1)
    paginas_bibliografia = st.text_input("Páginas da Bibliografia", placeholder="Ex: 142 - 147")
    
    st.subheader("Palavras-chave")
    num_keywords = st.selectbox("Quantidade de palavras-chave", options=[1, 2, 3, 4])
    keywords = [st.text_input(f"Palavra-chave {i+1}") for i in range(num_keywords)]
    
    ilustracoes = st.radio("Possui ilustrações?", ("Não", "Sim"))
    
    submit_button = st.form_submit_button("Enviar dados")

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
            st.write(f"**Orientador(es):** " + ", ".join([o for o in orientadores if o]))
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
