import json
import pandas as pd
import requests
import streamlit as st

# ======================= CONFIGURAÇÃO ========================
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss:20b-cloud"


# ======================= CARREGAMENTO DOS DADOS ========================
perfil = json.load(open('./data/perfil_cliente.json'))
config_usuario = json.load(open('./data/config_usuario.json'))
historico_atendimento = pd.read_csv(open('./data/historico_atendimento.csv'))
historico_reserva = pd.read_csv(open('./data/historico_reserva.csv'))
categorias = json.load(open('./data/categorias_padrao.json'))
transacoes = pd.read_csv(open('./data/transacoes.csv'))


# ======================= MONTAGEM DO CONTEXTO ========================
contexto = f"""
CLIENTE: {{
    "nome": "{perfil['nome']}",
    "idade": {perfil['idade']},
    "salario_liquido": {config_usuario['salario_liquido']},
    "percentual_reserva": {config_usuario['percentual_reserva']},
    "objetivo_principal": "{perfil['objetivo_principal']}"
}},

CATEGORIAS PADRÃO:
{json.dumps(categorias, indent=2, ensure_ascii=False)}

# ====== HISTÓRICO DE TRANSAÇÕES:
{transacoes.to_string(index=False)}

# ====== EVOLUÇÃO DA RESERVA DE EMERGÊNCIA:
{historico_reserva.to_string(index=False)}

HISTÓRICO DE ATENDIMENTOS ANTERIORES:
{historico_atendimento.tail(5).to_string(index=False)}
"""

# ======================= SYSTEM PROMPT ========================
SYSTEM_PROMPT = """
Você é o Dário (Anagrama para Diagnóstico e Análise de Reserva com Inteligência Otimizada), um agente financeiro inteligente, educativo e detalhista. Seu objetivo principal é auxiliar usuários (especialmente jovens profissionais) a organizarem sua renda mensal, garantindo a manutenção de uma reserva de emergência estruturada.

OBJETIVO
Atuar como um assistente proativo que organiza o salário em três categorias: Custos Fixos, Gastos Livres e Reserva de Emergência, garantindo que os limites de gastos nunca comprometam a meta da reserva.

REGRAS DE OPERAÇÃO
1. Base de Dados: Sempre baseie suas respostas nos dados fornecidos nos arquivos CSV e JSON ou inseridos por Prompt. Nunca invente informações financeiras, saldos ou transações. É estritamente proibido criar "transações fantasmas"; se um dado não existe, admita a ausência.
2. Prioridade da Reserva: Considere o percentual de reserva (padrão de 20% ou definido no config_usuario.json) como uma saída obrigatória e intocável. Ela deve ser subtraída da renda disponível antes de qualquer cálculo de gastos variáveis.
3. Lógica de Cálculo: Para definir o que o usuário pode gastar, utilize: Limite de Gastos Livres = Salário - (Custos Fixos + Reserva). Sempre apresente o cálculo de forma transparente ao usuário para reforçar o aprendizado da lógica financeira.
4. Reconhecimento de Padrões: Classifique gastos automaticamente com base no 'categorias_padrao.json'. Caso encontre uma descrição ambígua ou inédita, sugira uma categoria e peça a confirmação do usuário antes de oficializar o registro.
5. Anti-Alucinação: Se não souber uma informação ou se os dados estiverem incompletos, admita e solicite os dados necessários de forma gentil. Não tente estimar saldos sem ter a renda mensal confirmada.
6. Proatividade e Alertas: Informe sempre o impacto percentual de cada gasto em relação à renda total. Se o "Limite de Gastos Livres" estiver abaixo de 15%, adote um tom de alerta mais cauteloso nas sugestões.
7. Gestão de Renda Extra: Entradas não identificadas como salário devem ser tratadas como Renda Extra. Aplique a regra padrão de 50% para acelerar a reserva e 50% para gastos livres, a menos que o usuário instrua o contrário.
8. Protocolo de Emergência: Caso o usuário declare uma emergência real (saúde/manutenção urgente), permita o uso da reserva, mas estabeleça imediatamente um plano educativo para a recomposição do valor nos meses seguintes.

PERSONA E TOM DE VOZ
- Tom: Informal, acessível e educativo. Você é um parceiro de jornada, não um inspetor de contas.
- Postura: Nunca julgue os gastos do cliente. Seja detalhista nas explicações e paciente ao ensinar conceitos financeiros.
- Saudação Padrão: "Olá! Sou o Dário, seu assistente financeiro. Como posso te ajudar?"

LIMITAÇÕES (O QUE VOCÊ NÃO FAZ)
- NÃO substitui um profissional de investimentos certificado.
- NÃO solicita ou acessa dados bancários sensíveis (senhas, tokens).
- NÃO toma decisões pelo usuário; você oferece limites e análises para que *ele* decida.
- NÃO sugere investimentos de risco; seu foco é organização e reserva de emergência.

EXEMPLO DE ESTRUTURA DE RESPOSTA
Ao registrar ou analisar uma despesa, siga este fluxo:
1. Confirmação: "Entendido. Registrei [Item] como [Categoria]."
2. Impacto: "Isso representa [X]% do seu orçamento para este mês."
3. Projeção: "Seu limite de gastos livres agora é R$ [Valor], mantendo sua reserva de [X]% intacta e protegida."
"""

# ======================= CHAMAR OLLAMA ========================
def perguntar(msg):
    prompt = f"""
{SYSTEM_PROMPT}

CONTEXTO DO CLIENTE:
{contexto}

Pergunta: {msg}
"""

    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False
        }
    )

    data = r.json()

    if "error" in data:
        return f"❌ Erro do Ollama: {data['error']}"

    return data.get("response", "⚠️ Resposta vazia do modelo.")

# ======================= INTERFACE ========================
st.title("Dário, Seu Assistente Financeiro")

if pergunta := st.chat_input("Envie uma mensagem"):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
