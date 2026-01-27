# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve no Dário? |
|---------|---------|-------------------------|
| `config_usuario.json` | JSON | Armazena salário, percentual de reserva alvo e metas |
| `categorias_padrao.json`| JSON | Mapeia descrições de gastos para categorias (Fixos vs. Livres) |
| `transacoes.csv` | CSV | Base de dados bruta de entradas e saídas para cálculo de limites e impacto percentual |
| `historico_reserva.csv` | CSV | Registro histórico de quanto foi poupado mês a mês para acompanhar a meta total |
| `historico_atendimento.csv`| CSV | Contextualiza conversas passadas para que o Dário mantenha a continuidade do suporte |
| `perfil_cliente.json` | JSON | Dados demográficos e perfil comportamental |

---

## Estratégia de Integração

### Carregamento via Código (Python)

Para agentes rodando localmente (como no seu setup Streamlit + Ollama), os dados são carregados para compor o contexto da sessão:

```python
import pandas as pd
import json

# Carregamento de Tabelas
transacoes = pd.read_csv('data/transacoes.csv')
hist_atendimento = pd.read_csv('data/historico_atendimento.csv')
hist_reserva = pd.read_csv('data/historico_reserva.csv')

# Carregamento de Regras e Perfil
with open('data/config_usuario.json', 'r') as f:
    config = json.load(f)

with open('data/categorias_padrao.json', 'r') as f:
    categorias = json.load(f)
```

### Como os dados são usados no prompt?

Para facilitar, podemos também simplesmente injetar os dados via prompt.

```text
DADOS DE CONFIGURAÇÃO (config_usuario.json):
{
  "salario_liquido": 5000.00,
  "percentual_reserva": 0.20,
  "reserva_mensal_alvo": 1000.00
}

ÚLTIMAS TRANSAÇÕES (transacoes.csv):
data,descricao,categoria,valor,tipo
2025-10-15,Conta de Luz,moradia,180.00,saida
2025-10-20,Academia,saude,99.00,saida
2025-10-25,Combustível,transporte,250.00,saida
2025-10-30,Reserva de Emergência,investimento,1000.00,saida

HISTÓRICO DE RESERVA (historico_reserva.csv):
- Setembro: R$ 1.000,00
- Outubro: R$ 1.000,00 (Meta batida!)
```

---

## Exemplo de Contexto Montado

O exemplo de contexto montado abaixo se baseia nos dados originais da base de conhecimento, mas os sintetiza deixando apenas as informações mais relevantes e dessa forma otimizando o consumo de tokens. Entretanto, vale lembrar que, mais importante do que economizar tokens, é ter todas as informações disponíveis em seu contexto.

```
STATUS FINANCEIRO ATUAL:

Nome: João Silva
Renda Mensal: R$ 5.000,00
Reserva de Emergência: R$ 1.000,00 (20% protegidos)
Custos Fixos Identificados: R$ 1.634,90
Margem para Gastos Livres: R$ 2.365,10
Gastos Livres Consumidos: R$ 504,00
Saldo de Gastos Livres Disponível: R$ 1.861,10
```
