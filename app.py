import streamlit as st
import httpx

st.set_page_config(page_title="Formulário de Catalogação", page_icon="📚")

# --- CONFIGURAÇÃO DO BANCO ---
def get_db():
    # Esta versão é síncrona e funciona perfeitamente no fluxo do Streamlit
    return libsql.connect(
        database="fichas.db", # Pode ser o nome do seu banco
        sync_url=st.secrets["TURSO_URL"],
        auth_token=st.secrets["TURSO_TOKEN"]
    )

def salvar_no_turso(dados):
    base_url = st.secrets['TURSO_URL'].replace("libsql://", "https://")
    url = f"{base_url}/v1/execute"
    
    token = st.secrets['TURSO_TOKEN']
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # O Turso espera os argumentos neste formato: [{"type": "text", "value": "exemplo"}]
    # ou simplesmente uma lista de valores. Vamos tentar o formato esperado pela API REST:
    # Ajuste: A API espera 'stmt' (o SQL) e 'args' (os valores)
    payload = {
        "stmt": {
            "sql": """
            INSERT INTO fichas (
                instituicao, autor, titulo, subtitulo, tipo_trabalho, 
                area_concentracao, ano_defesa, num_folhas, paginas_bibliografia, 
                orientadores, coorientadores, keywords, ilustracoes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            "args": [
                {"type": "text", "value": dados['instituicao']},
                {"type": "text", "value": dados['autor']},
                {"type": "text", "value": dados['titulo']},
                {"type": "text", "value": dados['subtitulo']},
                {"type": "text", "value": dados['tipo_trabalho']},
                {"type": "text", "value": dados['area_concentracao']},
                {"type": "text", "value": str(dados['ano_defesa'])},
                {"type": "text", "value": str(dados['num_folhas'])},
                {"type": "text", "value": dados['paginas_bibliografia']},
                {"type": "text", "value": dados['orientadores']},
                {"type": "text", "value": dados['coorientadores']},
                {"type": "text", "value": dados['keywords']},
                {"type": "text", "value": dados['ilustracoes']}
            ]
        }
    }

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload)
        
    if response.status_code == 200:
        st.success("Dados enviados com sucesso!")
    else:
        st.error(f"Erro ao salvar: {response.text}")

def carregar_fichas():
    # URL configurada para consulta
    base_url = st.secrets['TURSO_URL'].replace("libsql://", "https://")
    url = f"{base_url}/v1/execute"
    
    headers = {
        "Authorization": f"Bearer {st.secrets['TURSO_TOKEN']}",
        "Content-Type": "application/json"
    }
    
    # Payload para realizar a consulta (SELECT)
    payload = {
        "stmt": {
            "sql": "SELECT * FROM fichas ORDER BY id DESC"
        }
    }
    
    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        # O Turso retorna os resultados dentro de 'results' -> 'rows'
        return data.get("results", {}).get("rows", [])
    else:
        st.error(f"Erro ao carregar fichas: {response.text}")
        return []

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
    titulos_opcoes = ["Dr.", "Dra.", "Me.", "Ma."]

    st.write("### Orientador(es)")
    # REMOVI A KEY OU MUDAMOS PARA ALGO MAIS ESPECÍFICO
    num_orientadores = st.selectbox("Quantos orientadores tem no seu trabalho?", options=[1, 2, 3]) 
    
    lista_orientadores = []
    for i in range(num_orientadores):
        col1, col2 = st.columns([3, 1])
        # Adicionamos um prefixo único para garantir que não haja conflito
        nome_o = col1.text_input(f"Nome do orientador {i+1}", key=f"orientador_nome_{i}")
        tit_o = col2.selectbox("Título", titulos_opcoes, key=f"orientador_tit_{i}")
        if nome_o:
            lista_orientadores.append(f"{tit_o} {nome_o}")

    st.write("### Coorientador(es)")
    num_coorientadores = st.selectbox("Quantos coorientadores tem no seu trabalho?", options=[0, 1, 2, 3])
    
    lista_coorientadores = []
    if num_coorientadores > 0:
        for i in range(num_coorientadores):
            col1, col2 = st.columns([3, 1])
            nome_c = col1.text_input(f"Nome do coorientador {i+1}", key=f"coorientador_nome_{i}")
            tit_c = col2.selectbox("Título", titulos_opcoes, key=f"coorientador_tit_{i}")
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
                    "paginas_bibliografia": paginas_bibliografia,
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




# --- FLUXO PRINCIPAL ---
if check_password():
    st.sidebar.success("Acesso Liberado: Bibliotecária")
    if st.sidebar.button("Sair do Painel"):
        st.session_state["password_correct"] = False
        st.rerun()
    interface_bibliotecaria()
else:
    formulario_aluno()
