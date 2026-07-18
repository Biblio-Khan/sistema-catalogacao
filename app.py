import streamlit as st
import pandas as pd
import httpx
import requests
from fpdf import FPDF

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

# --- FUNÇÃO CENTRAL DE API (Com tratamento de erro) ---
# --- 1. CONFIGURAÇÃO E BUSCA ---
def executar_query(sql, args=None):
    base_url = st.secrets['TURSO_URL'].replace("libsql://", "https://")
    
    # O Turso exige que os argumentos tenham o formato {"type": "text", "value": "..."}
    # Vamos transformar seus argumentos caso eles venham como simples {"value": ...}
    formatted_args = []
    if args:
        for arg in args:
            if isinstance(arg, dict) and "type" not in arg:
                formatted_args.append({"type": "text", "value": str(arg["value"])})
            else:
                formatted_args.append(arg)

    payload = {"stmt": {"sql": sql, "args": formatted_args}}
    headers = {"Authorization": f"Bearer {st.secrets['TURSO_TOKEN']}", "Content-Type": "application/json"}
    
    resp = httpx.post(f"{base_url}/v1/execute", headers=headers, json=payload)
    return resp.json()

def carregar_fichas():
    # Retorna uma lista de dicionários pronta para uso
    data = executar_query("SELECT * FROM fichas")
    rows = data.get("result", {}).get("rows", [])
    cols = [c["name"] for c in data.get("result", {}).get("cols", [])]
    
    fichas = []
    for row in rows:
        fichas.append({cols[i]: (row[i].get("value") if row[i] else "") for i in range(len(row))})
    return fichas

# --- 2. ATUALIZAÇÃO ---
def atualizar_ficha(id_ficha, cdd, cutter):
    sql = "UPDATE fichas SET cdd=?, cutter=? WHERE id=?"
    return executar_query(sql, [{"value": cdd}, {"value": cutter}, {"value": id_ficha}])

# --- 3. PREVIEW ---
def exibir_preview_ficha(ficha):
    st.write("### Preview da Ficha Catalográfica")
    
    # 1. Limpeza de quebras de linha invisíveis
    keywords_raw = ficha.get('keywords', '').replace('\n', ',').replace('\r', ',').replace('<br>', ',')
    
    # 2. Formatação dos assuntos
    partes = [k.strip() for k in keywords_raw.split(',') if k.strip()]
    assuntos_formatados = " ".join([f"{i+1}. {parte}" for i, parte in enumerate(partes)])
    
    html_content = f"""
    <div style="display: flex; justify-content: center;">
        <!-- Container principal com as medidas EXATAS: 12.5cm x 7.5cm -->
        <div style="width: 12.5cm; height: 7.5cm; border: 1px solid #000; padding: 15px; font-family: 'Courier New', Courier, monospace; font-size: 11px; background-color: white; color: black; box-sizing: border-box; line-height: 1.2; position: relative; overflow: hidden;">
            
            <!-- LINHA 1: CDD em cima, Cutter e Autor na linha de baixo -->
            <div style="margin-bottom: 5px;">
                {ficha.get('cdd', '1234.56')}<br>
                {ficha.get('cutter', 'S677t')} {ficha.get('autor', 'Sobrenome, Nome, 1950 -')}
            </div>

            <!-- CORPO DA FICHA: Recuado para a direita e justificado -->
            <div style="padding-left: 45px; text-align: justify;">
                <p style="margin: 0;">{ficha.get('titulo', 'Título')} / {ficha.get('autor', '').split(',')[0]}. - {ficha.get('instituicao', 'CDTN')}, 2026.</p>
                <p style="margin: 0;">{ficha.get('num_folhas', '200')} p.</p>
                
                <p style="margin: 8px 0;">ISBN {ficha.get('isbn', '12-34567-89-0')}</p>
                
                <!-- ASSUNTOS E TÍTULO SECUNDÁRIO NA MESMA LINHA -->
                <p style="margin: 8px 0 0 0;">{assuntos_formatados} I. {ficha.get('titulo_titulo', 'Título')}.</p>
            </div>

            <!-- RODAPÉ: CDU fixado na parte inferior direita -->
            <div style="position: absolute; bottom: 15px; right: 15px; text-align: right;">
                CDU: {ficha.get('cdu', '123.456.7(89)-0')}
            </div>
            
        </div>
    </div>
    """
    
    import streamlit.components.v1 as components
    components.html(html_content, height=350)
    
# --- 3. PAINEL DE EDIÇÃO (Lógica de atualizar um campo específico) ---
def painel_edicao(ficha):
    # 1. Seção de Catalogação (CDD/Cutter) - Sempre visível e fácil
    with st.expander("Adicionar CDU e Cutter", expanded=True):
        with st.form(f"form_cdd_cutter_{ficha.get('id')}"):
            cdd = st.text_input("CDU", value=ficha.get('cdd') or "")
            cutter = st.text_input("Cutter", value=ficha.get('cutter') or "")
            if st.form_submit_button("Salvar Catalogação"):
                # Atualiza os dois campos de uma vez
                sql = "UPDATE fichas SET cdd=?, cutter=? WHERE id=?"
                executar_query(sql, [{"value": cdd}, {"value": cutter}, {"value": ficha.get('id')}])
                st.success("Dados de catalogação atualizados!")
                st.rerun()

    # 2. Seção de Edição de outros campos (Lista dinâmica)
    st.write("---")
    st.write("### ✏️ Edição de Ficha")
    campos_editaveis = [
        "titulo", "subtitulo", "autor", "instituicao", "tipo_trabalho", 
        "ano_defesa", "num_folhas", "paginas_bibliografia", "orientadores", "keywords"
    ]
    
    campo_escolhido = st.selectbox("Selecione um campo para corrigir:", campos_editaveis)
    
    with st.form(f"form_edicao_{ficha.get('id')}_{campo_escolhido}"):
        valor_atual = ficha.get(campo_escolhido, "")
        novo_valor = st.text_input(f"Editar {campo_escolhido.replace('_', ' ').capitalize()}:", value=valor_atual)
        
        if st.form_submit_button("Salvar alteração"):
            sql = f"UPDATE fichas SET {campo_escolhido}=? WHERE id=?"
            executar_query(sql, [{"value": novo_valor}, {"value": ficha.get('id')}])
            st.success(f"Campo '{campo_escolhido}' atualizado!")
            st.rerun()

# --- 4. PAINEL BIBLIOTECÁRIA (Onde tudo se junta) ---
def interface_bibliotecaria():
    st.title("Painel da Bibliotecária")
    fichas = carregar_fichas()
    
    if not fichas:
        st.info("Nenhuma ficha pendente.")
        return

    for ficha in fichas:
        with st.expander(f"{ficha.get('autor')} - {ficha.get('titulo')}"):
            col1, col2 = st.columns(2)
            with col1:
                # Aqui exibimos o preview
                exibir_preview_ficha(ficha)
            with col2:
                # Aqui exibimos a edição
                painel_edicao(ficha)
                    
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
