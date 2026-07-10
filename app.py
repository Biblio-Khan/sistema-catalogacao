import streamlit as st
import httpx

URL_LOGO = "https://github.com/Biblio-Khan/sistema-catalogacao/blob/main/Logotipo-CDTN.png?raw=true"

st.set_page_config(page_title="Sistema de Catalogação", layout="wide")

# --- TOPO (Apenas a imagem) ---
st.image(URL_LOGO, width=200)

# --- BARRA LATERAL ---
with st.sidebar:
    # A assinatura fixa no rodapé
    st.markdown("""
        <div style="position: absolute; bottom: 20px; width: 85%; text-align: center;">
            <hr style="border: 1px solid #003366;">
            <p style="font-size: 0.75rem; color: #003366;">
                <strong>Sistema de Catalogação v1.0</strong><br>
                Desenvolvido por: <strong>Sabrina Lobeu</strong><br>
                <em>© 2026 - BiblioKhan</em>
            </p>
        </div>
    """, unsafe_allow_html=True)
# --- CONFIGURAÇÃO DO BANCO ---
def atualizar_ficha_no_turso(dados):
    base_url = st.secrets['TURSO_URL'].replace("libsql://", "https://")
    url = f"{base_url}/v1/execute"
    
    token = st.secrets['TURSO_TOKEN']
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Mantendo rigorosamente o seu formato de payload
    payload = {
        "stmt": {
            "sql": """
            UPDATE fichas SET 
                instituicao = ?, autor = ?, titulo = ?, subtitulo = ?, 
                tipo_trabalho = ?, area_concentracao = ?, ano_defesa = ?, 
                num_folhas = ?, paginas_bibliografia = ?, orientadores = ?, 
                coorientadores = ?, keywords = ?, ilustracoes = ?
            WHERE id = ?
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
                {"type": "text", "value": dados['ilustracoes']},
                {"type": "integer", "value": dados['id']} # O id que garante a atualização correta
            ]
        }
    }

    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload)
        
    if response.status_code == 200:
        st.success("Ficha atualizada com sucesso!")
    else:
        st.error(f"Erro ao atualizar: {response.text}")
def carregar_fichas():
    base_url = st.secrets['TURSO_URL'].replace("libsql://", "https://")
    url = f"{base_url}/v1/execute"
    
    headers = {
        "Authorization": f"Bearer {st.secrets['TURSO_TOKEN']}",
        "Content-Type": "application/json"
    }
    
    # Agora pedimos todos os dados
    payload = {"stmt": {"sql": "SELECT * FROM fichas"}}
    
    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        
        # Acesso direto ao formato que você enviou:
        # O Turso entrega em 'result' (singular) e dentro dele 'rows'
        rows = data.get("result", {}).get("rows", [])
        
        # Se você quiser transformar isso em algo mais fácil de usar (dicionários):
        # As colunas estão em data["result"]["cols"]
        cols = [c["name"] for c in data.get("result", {}).get("cols", [])]
        
        # Converte cada linha (que é uma lista de objetos) para um dicionário
       # Converte cada linha para um dicionário de forma segura
        fichas_formatadas = []
        for row in rows:
            # Usamos .get("value") para evitar erro caso o campo seja NULL
            linha_dict = {}
            for i, item in enumerate(row):
                col_name = cols[i]
                # Se 'value' não existir (for NULL), salva como None
                linha_dict[col_name] = item.get("value") if item is not None else None
            fichas_formatadas.append(linha_dict)
            
        return fichas_formatadas
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

# Adicione esta função ao seu script
import streamlit as st
import httpx

# --- CONFIGURAÇÃO ---
st.set_page_config(layout="wide")
st.title("📚 Sistema de Gestão de Fichas")

# --- FUNÇÃO DE ATUALIZAÇÃO (APIs REST TURSO) ---
def atualizar_ficha_no_turso(dados):
    base_url = st.secrets['TURSO_URL'].replace("libsql://", "https://")
    url = f"{base_url}/v1/execute"
    token = st.secrets['TURSO_TOKEN']
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    payload = {
        "stmt": {
            "sql": """
            UPDATE fichas SET 
                instituicao = ?, autor = ?, titulo = ?, subtitulo = ?, 
                tipo_trabalho = ?, area_concentracao = ?, ano_defesa = ?, 
                num_folhas = ?, orientadores = ?, coorientadores = ?, keywords = ?
            WHERE id = ?
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
                {"type": "text", "value": dados['orientadores']},
                {"type": "text", "value": dados['coorientadores']},
                {"type": "text", "value": dados['keywords']},
                {"type": "integer", "value": dados['id']}
            ]
        }
    }
    with httpx.Client() as client:
        response = client.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        st.success("Ficha atualizada com sucesso!")
    else:
        st.error(f"Erro ao atualizar: {response.text}")


# O método execute do libsql-client retorna o objeto de resposta diretamente
resultado = db.execute("SELECT id, titulo, autor FROM fichas")

# As linhas retornadas estão dentro de 'rows'
fichas = resultado.rows
cursor.execute("SELECT id, titulo, autor FROM fichas")
fichas = cursor.fetchall()

st.sidebar.subheader("Catálogo")
selecao_nome = st.sidebar.selectbox("Selecione a obra:", list(mapeamento.keys()))
id_selecionado = mapeamento[selecao_nome]

# Carrega a ficha no estado
if 'id_atual' not in st.session_state or st.session_state.id_atual != id_selecionado:
resultado_detalhe = db.execute("SELECT * FROM fichas WHERE id = ?", (id_selecionado,))
# O primeiro item da lista de linhas é a sua ficha
dados_banco = resultado_detalhe.rows[0]
    st.session_state.ficha = dict(dados_banco)
    st.session_state.id_atual = id_selecionado
    st.session_state.modo_edicao = False

# --- PAINEL CENTRAL ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("👁️ Preview da Ficha")
    st.json(st.session_state.ficha)

with col2:
    st.subheader("⚙️ Edição")
    if st.button("✏️ Editar campos desta ficha"):
        st.session_state.modo_edicao = True
    
    if st.session_state.modo_edicao:
        with st.form("form_edicao"):
            st.session_state.ficha['instituicao'] = st.text_input("Instituição", st.session_state.ficha['instituicao'])
            st.session_state.ficha['autor'] = st.text_input("Autor", st.session_state.ficha['autor'])
            st.session_state.ficha['titulo'] = st.text_input("Título", st.session_state.ficha['titulo'])
            st.session_state.ficha['subtitulo'] = st.text_input("Subtítulo", st.session_state.ficha['subtitulo'])
            st.session_state.ficha['tipo_trabalho'] = st.text_input("Tipo de Trabalho", st.session_state.ficha['tipo_trabalho'])
            st.session_state.ficha['area_concentracao'] = st.text_input("Área de Concentração", st.session_state.ficha['area_concentracao'])
            st.session_state.ficha['ano_defesa'] = st.text_input("Ano de Defesa", st.session_state.ficha['ano_defesa'])
            st.session_state.ficha['num_folhas'] = st.text_input("Nº de Folhas", st.session_state.ficha['num_folhas'])
            st.session_state.ficha['orientadores'] = st.text_input("Orientadores", st.session_state.ficha['orientadores'])
            st.session_state.ficha['coorientadores'] = st.text_input("Coorientadores", st.session_state.ficha['coorientadores'])
            st.session_state.ficha['keywords'] = st.text_area("Palavras-chave", st.session_state.ficha['keywords'])

            if st.form_submit_button("Salvar no Banco"):
                atualizar_ficha_no_turso(st.session_state.ficha)
                st.session_state.modo_edicao = False
                st.rerun()

# Atualize a interface:
def interface_bibliotecaria():
    st.title("Painel da Bibliotecária")
    fichas = carregar_fichas()
    
    if not fichas:
        st.info("Nenhuma ficha pendente no momento.")
        return

    for i, ficha in enumerate(fichas):
        f_id = ficha.get('id')
        # Título do expander
        titulo_expander = f"{ficha.get('autor', 'Sem autor')} - {ficha.get('titulo', 'Sem título')}"
        
        with st.expander(titulo_expander):
            # 1. Campos de edição (identificados de forma única)
            novo_cdd = st.text_input("CDD", value=ficha.get('cdd', ''), key=f"cdd_{f_id}_{i}")
            novo_cutter = st.text_input("Cutter", value=ficha.get('cutter', ''), key=f"cut_{f_id}_{i}")
            
            # 2. Botão de Preview: armazena os valores no session_state
            if st.button("Pré-visualizar Ficha", key=f"prev_{f_id}_{i}"):
                st.session_state.preview_ficha = ficha
                st.session_state.preview_cdd = novo_cdd
                st.session_state.preview_cutter = novo_cutter
                st.rerun()

            # 3. Exibição do Preview (apenas se for o clique desta ficha)
            if "preview_ficha" in st.session_state and st.session_state.preview_ficha.get('id') == f_id:
                st.write("---")
                st.write("### Preview da Ficha")
                abrir_visualizacao_ficha(
                    st.session_state.preview_ficha, 
                    st.session_state.preview_cdd, 
                    st.session_state.preview_cutter
                )
                
                # 4. Botão de Salvar (exibido apenas no bloco de visualização)
                if st.button("Finalizar e Aprovar", key=f"save_{f_id}_{i}"):
                    response = atualizar_ficha(f_id, st.session_state.preview_cdd, st.session_state.preview_cutter)
                    if response.status_code == 200:
                        st.success("Ficha catalogada com sucesso!")
                        # Limpa o estado para esconder o preview e o botão salvar
                        if "preview_ficha" in st.session_state:
                            del st.session_state.preview_ficha
                        st.rerun()
                    else:
                        st.error("Erro ao salvar no banco.")
                    
def formulario_aluno():
    st.title("Formulário de Ficha Catalográfica")

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
