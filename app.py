import streamlit as st

st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

st.title("📚 Cadastro de Obra")

with st.form("form_cadastro"):
    st.subheader("Dados do Autor")
    
    st.info("""
    **Instruções para o campo Autor:**
    Digite o nome começando pelo último sobrenome, seguido por vírgula e o restante dos prenomes.
    * **Parentesco:** (Ex: João Pires Filho) -> `Pires Filho, João`
    * **Sobrenome Composto:** (Ex: Ana Castelo Branco) -> `Castelo Branco, Ana`
    * **Origem Hispânica:** (Ex: Gabriel García Márquez) -> `García Marquez, Gabriel`
    """)
    
    autor = st.text_input(
        "Nome completo do autor (formato de citação)", 
        placeholder="Sobrenome(s), Nome"
    )

    st.subheader("Dados do Trabalho")
    titulo = st.text_input(
        "Título do trabalho", 
        placeholder="Apenas a primeira letra da primeira palavra e nomes próprios em maiúsculas"
    )
    st.caption("Ex: Da invisibilidade social à visibilidade discursiva: Estudo enunciativo a respeito das ações da família na comunidade rural - Maués/AM")
    
    subtitulo = st.text_input(
        "Subtítulo (se houver)", 
        placeholder="Insira o subtítulo, se existir"
    )
    
    submit_button = st.form_submit_button("Enviar dados")

if submit_button:
    if autor and titulo:
        if "," not in autor:
            st.warning("⚠️ Atenção: O formato do nome do autor parece estar incorreto (falta a vírgula).")
        else:
            st.success("Dados registrados com sucesso!")
            st.write(f"**Autor:** {autor}")
            st.write(f"**Título:** {titulo}")
            if subtitulo:
                st.write(f"**Subtítulo:** {subtitulo}")
    else:
        st.error("Os campos Autor e Título são obrigatórios.")
