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
    
    submit_button = st.form_submit_button("Enviar dados")

if submit_button:
    if autor:
        if "," not in autor:
            st.warning("⚠️ Atenção: O formato do nome parece estar incorreto. Verifique se você usou a vírgula após o sobrenome.")
        else:
            st.success("Autor registrado!")
            st.write(f"**Autor:** {autor}")
    else:
        st.error("O campo Autor é obrigatório.") 
