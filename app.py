import streamlit as st

st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

st.title("📚 Formulário de Catalogação: Centro de Desenvolvimento de Tecnologia Nuclear")

with st.form("form_cadastro"):
    st.subheader("Dados da Instituição")
    instituicao = "Centro de Desenvolvimento de Tecnologia Nuclear (CDTN)"
    st.write(f"**Instituição:** {instituicao}")

    st.subheader("Dados do Autor")
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
    area_concentracao = st.radio("Área de concentração", ("Ciência e Tecnologia das Radiações e Reatores Nucleares", "Ciência e Tecnologia dos Minerais e Meio Ambiente", "Ciência e Tecnologia dos Materiais"))
    ano_defesa = st.text_input("Ano da defesa", help="Digite o ano que está informado na folha de rosto", placeholder="Ex: 2026")
    
    # Banca Examinadora
    st.subheader("Dados da Banca Examinadora")
    titulos_opcoes = ["Dr.", "Dra.", "Me.", "Ma."]
    
    # Orientadores
    st.write("### Orientador(es)")
    num_orientadores = st.selectbox("Quantos orientadores tem no seu trabalho?", options=[1, 2, 3], key="num_o")
    lista_orientadores = []
    for i in range(num_orientadores):
        col1, col2 = st.columns([3, 1])
        nome = col1.text_input(f"Nome do orientador {i+1}", key=f"nome_o_{i}")
        titulacao = col2.selectbox(f"Título", titulos_opcoes, key=f"tit_o_{i}")
        if nome:
            lista_orientadores.append(f"{titulacao} {nome}")

    # Coorientadores
    st.write("### Coorientador(es)")
    num_coorientadores = st.selectbox("Quantos coorientadores tem no seu trabalho?", options=[0, 1, 2, 3], key="num_c")
    lista_coorientadores = []
    if num_coorientadores > 0:
        for i in range(num_coorientadores):
            col1, col2 = st.columns([3, 1])
            nome_c = col1.text_input(f"Nome do coorientador {i+1}", key=f"nome_c_{i}")
            titulacao_c = col2.selectbox(f"Título", titulos_opcoes, key=f"tit_c_{i}")
            if nome_c:
                lista_coorientadores.append(f"{titulacao_c} {nome_c}")

    # Folhas e Bibliografia
    num_folhas = st.number_input("Número total de folhas", min_value=1, step=1)
    st.caption("Informe o número total de folhas do seu trabalho, começando a contagem a partir da folha de rosto.")
    st.info("💡 **Dica:** Inserir o número da última folha numerada. Olhe a numeração do documento e não a contagem de páginas.")
    
    paginas_bibliografia = st.text_input("Páginas da Bibliografia", placeholder="Ex: 142 - 147")
    st.caption("Informe o intervalo de páginas onde a Bibliografia se encontra")
    
    # Palavras-chave
    st.subheader("Palavras-chave")
    st.info("""
    **Instruções para Palavras-chave:**
    Pode-se usar termo simples ou composto, retirado da linguagem natural, não incluído na relação de descritores padronizados. A Bibliotecária responsável consultará esses termos em vocabulário controlados havendo mudanças dos termos escolhidos se prezará para que o sentido do termo seja mantido.
    
    **Dica:** Não usar fórmulas. Em caso de termo científico, utilizar também o nome popular. Inserir palavra-chave com a primeira letra maiúscula e o resto em minúsculo exceto quando for nome próprio. Em caso de sigla, usar maiúscula e seguido de hífen e seu significado.
    """)
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
        st.error("Os campos Autor, Título, Ano e Número de folhas são obrigatórios.")
