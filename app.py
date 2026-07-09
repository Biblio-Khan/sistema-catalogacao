import streamlit as st
from libsql_client import Client

st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

# --- CONFIGURAÇÃO DO BANCO ---
def get_db():
    if "TURSO_URL" not in st.secrets or "TURSO_TOKEN" not in st.secrets:
        st.error("Erro: Credenciais do Turso (URL/TOKEN) não encontradas nos Secrets.")
        st.stop() # Para a execução aqui e avisa o erro
    
    return Client(url=st.secrets["TURSO_URL"], auth_token=st.secrets["TURSO_TOKEN"])
# --- FUNÇÕES DE DADOS ---
def salvar_no_turso(dados):
    db = get_db()
    db.execute("""
        INSERT INTO fichas (
            instituicao, autor, titulo, subtitulo, tipo_trabalho, 
            area_concentracao, ano_defesa, num_folhas, orientadores, 
            coorientadores, keywords, ilustracoes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        dados['instituicao'], dados['autor'], dados['titulo'], dados['subtitulo'],
        dados['tipo_trabalho'], dados['area_concentracao'], dados['ano_defesa'],
        dados['num_folhas'], ", ".join(dados['orientadores']), 
        ", ".join(dados['coorientadores']), ", ".join(dados['keywords']), dados['ilustracoes']
    ))

def carregar_fichas():
    db = get_db()
    return db.execute("SELECT * FROM fichas WHERE status = 'Pendente'").rows

# --- FUNÇÕES ---

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["SENHA_BIBLIOTECARIA"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False
            st.error("Senha incorreta")

    if "password_correct" not in st.session_state:
        st.sidebar.text_input("Senha da Bibliotecária", type="password", on_change=password_entered, key="password")
        return False
    return st.session_state["password_correct"]

def interface_bibliotecaria():
    st.header("📋 Painel de Processamento Técnico")
    fichas = carregar_fichas()
    
    if not fichas:
        st.info("Nenhuma ficha pendente no momento.")
        return

    for ficha in fichas:
        # ficha[0]=id, ficha[2]=autor, ficha[3]=titulo
        with st.container(border=True):
            st.write(f"**Autor:** {ficha[2]}")
            st.write(f"**Título:** {ficha[3]}")
            
            with st.popover("Gerar Ficha / Catalogar"):
                st.write(f"### Catalogando: {ficha[3]}")
                
                # Campos para a bibliotecária preencher
                cdd = st.text_input("CDD", key=f"cdd_{ficha[0]}")
                cutter = st.text_input("Cutter", key=f"cut_{ficha[0]}")
                
                if st.button("Finalizar Ficha e Aprovar", key=f"btn_{ficha[0]}"):
                    # Atualiza o banco no Turso
                    db = get_db()
                    db.execute(
                        "UPDATE fichas SET cdd = ?, cutter = ?, status = 'Aprovado' WHERE id = ?", 
                        (cdd, cutter, ficha[0])
                    )
                    st.success("Ficha catalogada com sucesso!")
                    st.rerun() # Atualiza a página para remover a ficha da lista

def formulario_aluno():
    st.title("Formulário de Catalogação: Centro de Desenvolvimento de Tecnologia Nuclear")

    # --- Dados da Banca ---
    st.subheader("Dados da Banca Examinadora")
    st.info("""
    **Instruções para Banca:**
    Selecione o número de membros e preencha seus respectivos nomes e titulações. 
    As informações devem seguir o padrão acadêmico, indicando corretamente o título (Dr., Dra., Me., Ma.).
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
        st.info("""
        **Instruções para o campo Autor:**
        Digite o nome começando pelo último sobrenome, seguido por vírgula e o restante dos prenomes.
        * Parentesco: (Ex: João Pires Filho) -> Pires Filho, João
        * Sobrenome Composto: (Ex: Ana Castelo Branco) -> Castelo Branco, Ana
        * Origem Hispânica: (Ex: Gabriel García Márquez) -> García Marquez, Gabriel
        """)
        autor = st.text_input("Nome completo do autor (formato de citação)", placeholder="Sobrenome(s), Nome")

        st.subheader("Dados do Trabalho")
        titulo = st.text_input("Título do trabalho", placeholder="Apenas a primeira letra da primeira palavra e nomes próprios em maiúsculas")
        st.caption("Ex: Da invisibilidade social à visibilidade discursiva: Estudo enunciativo a respeito das ações da família na comunidade rural - Maués/AM")
        subtitulo = st.text_input("Subtítulo (se houver)", placeholder="Insira o subtítulo, se existir")
        
        tipo_trabalho = st.selectbox("Tipo de trabalho e titulação", ("Trabalho de conclusão de curso (Graduação)", "Trabalho de conclusão de curso (Especialização)", "Dissertação (Mestrado)", "Tese (Doutorado)"))
        area_concentracao = st.radio("Área de concentração", ("Ciência e Tecnologia das Radiações e Reatores Nucleares", "Ciência e Tecnologia dos Minerais e Meio Ambiente", "Ciência e Tecnologia dos Materiais"))
        ano_defesa = st.text_input("Ano da defesa", help="Digite o ano que está informado na folha de rosto", placeholder="Ex: 2026")
        
        num_folhas = st.number_input("Número total de folhas", min_value=1, step=1)
        st.caption("Informe o número total de folhas do seu trabalho, começando a contagem a partir da folha de rosto.")
        st.info("Nota: Inserir o número da última folha numerada. Olhe a numeração do documento e não a contagem de páginas.")
        
        paginas_bibliografia = st.text_input("Páginas da Bibliografia", placeholder="Ex: 142 - 147")
        st.caption("Informe o intervalo de páginas onde a Bibliografia se encontra")
        
        st.subheader("Palavras-chave")
        st.info("""
        **Instruções para Palavras-chave:**
        Pode-se usar termo simples ou composto, retirado da linguagem natural. A Bibliotecária responsável consultará esses termos em vocabulário controlado.
        * Dica: Não usar fórmulas. Em caso de termo científico, utilizar também o nome popular.
        * Formatação: Primeira letra maiúscula e o resto em minúsculo (exceto nome próprio).
        * Siglas: Seguidas de hífen e seu significado.
        """)
        num_keywords = st.selectbox("Quantidade de palavras-chave", options=[1, 2, 3, 4])
        keywords = [st.text_input(f"Palavra-chave {i+1}", key=f"kw_{i}") for i in range(num_keywords)]
        
        # ... (dentro do with st.form("form_dados_gerais"):)

        ilustracoes = st.radio("Possui ilustrações?", ("Não", "Sim"))
        
        # DEFINA O BOTÃO APENAS UMA VEZ
        submit_button = st.form_submit_button("Enviar dados para Bibliotecária")
        
        if submit_button:
            # Validação básica
            if not (autor and titulo and ano_defesa and num_folhas):
                st.error("Por favor, preencha todos os campos obrigatórios (Autor, Título, Ano, Folhas).")
            elif "," not in autor:
                st.warning("Atenção: O formato do nome do autor parece estar incorreto (falta a vírgula).")
            else:
                # Preparar os dados para o banco
                dados = {
                    "instituicao": instituicao,
                    "autor": autor,
                    "titulo": titulo,
                    "subtitulo": subtitulo,
                    "tipo_trabalho": tipo_trabalho,
                    "area_concentracao": area_concentracao,
                    "ano_defesa": ano_defesa,
                    "num_folhas": num_folhas,
                    "paginas_bibliografia": pag_bibliografia,
                    "orientadores": ", ".join(lista_orientadores),
                    "coorientadores": ", ".join(lista_coorientadores),
                    "keywords": ", ".join(keywords),
                    "ilustracoes": ilustracoes
                }
                
                # Salvar no Turso
                try:
                    salvar_no_turso(dados)
                    st.success("Dados enviados com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao salvar no banco: {e}")
if __name__ == "__main__":
    formulario_aluno()


# --- FLUXO PRINCIPAL ---
if check_password():
    st.sidebar.success("Acesso Liberado: Bibliotecária")
    if st.sidebar.button("Sair do Painel"):
        st.session_state["password_correct"] = False
        st.rerun()
    interface_bibliotecaria()
else:
    formulario_aluno()
