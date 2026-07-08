import streamlit as st

st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

st.title("📚 Formulário de Catalogação: Centro de Desenvolvimento de Tecnologia Nuclear")

with st.form("form_cadastro"):
    # ... dentro do with st.form("form_cadastro"):
    st.subheader("Dados da Instituição")
    
    inst_opcoes = ["Centro de Desenvolvimento de Tecnologia Nuclear (CDTN)", "Outro"]
    instituicao_selecionada = st.selectbox("Instituição/Unidade acadêmica", inst_opcoes)
    
    # Campo condicional
    instituicao = instituicao_selecionada
    if instituicao_selecionada == "Outro":
        instituicao = st.text_input("Digite o nome da instituição:")
    # ... restante do código

    st.subheader("Dados do Autor")
    
    # ... (restante dos campos permanecem iguais)
    st.info("""
    **Instruções para o campo Autor:**
    Digite o nome começando pelo último sobrenome, seguido por vírgula e o restante dos prenomes.
    * **Parentesco:** (Ex: João Pires Filho) -> `Pires Filho, João`
    * **Sobrenome Composto:** (Ex: Ana Castelo Branco) -> `Castelo Branco, Ana`
    * **Origem Hispânica:** (Ex: Gabriel García Márquez) -> `García Marquez, Gabriel`
    """)
    
    autor = st.text_input("Nome completo do autor (formato de citação)", placeholder="Sobrenome(s), Nome")

    st.subheader("Dados do Trabalho")
    titulo = st.text_input("Título do trabalho", placeholder="Apenas a primeira letra da primeira palavra e nomes próprios em maiúsculas")
    st.caption("Ex: Da invisibilidade social à visibilidade discursiva: Estudo enunciativo a respeito das ações da família na comunidade rural - Maués/AM")
    
    subtitulo = st.text_input("Subtítulo (se houver)", placeholder="Insira o subtítulo, se existir")
    
    tipo_trabalho = st.selectbox("Tipo de trabalho e titulação", ("Trabalho de conclusão de curso (Graduação)", "Trabalho de conclusão de curso (Especialização)", "Dissertação (Mestrado)", "Tese (Doutorado)"))
    
    ano_defesa = st.text_input("Ano da defesa", help="Digite o ano que está informado na folha de rosto", placeholder="Ex: 2026")
    
    num_folhas = st.number_input("Número total de folhas", min_value=1, step=1)
    st.caption("Informe o número total de folhas do seu trabalho, começando a contagem a partir da folha de rosto.")
    st.info("💡 **Dica:** Inserir o número da última folha numerada. Olhe a numeração do documento e não a contagem de páginas.")
    
    ilustracoes = st.radio("Possui ilustrações?", ("Não", "Sim"))
    
    submit_button = st.form_submit_button("Enviar dados")

if submit_button:
    # Ajuste na validação para considerar a instituição digitada no "Outro"
    if autor and titulo and ano_defesa and num_folhas and (instituicao_selecionada != "Outro" or instituicao):
        if "," not in autor:
            st.warning("⚠️ Atenção: O formato do nome do autor parece estar incorreto (falta a vírgula).")
        else:
            st.success("Dados registrados com sucesso!")
            st.write(f"**Instituição:** {instituicao}")
            st.write(f"**Tipo de trabalho:** {tipo_trabalho}")
            st.write(f"**Autor:** {autor}")
            st.write(f"**Título:** {titulo}")
            if subtitulo:
                st.write(f"**Subtítulo:** {subtitulo}")
            st.write(f"**Ano da defesa:** {ano_defesa}")
            
            resumo_folhas = f"{num_folhas} f."
            if ilustracoes == "Sim":
                resumo_folhas += " il."
            st.write(f"**Número de folhas:** {resumo_folhas}")
    else:
        st.error("Por favor, preencha todos os campos obrigatórios.")
