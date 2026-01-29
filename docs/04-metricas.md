# Avaliação e Métricas

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

---

## Cenários de Teste

Testes simples de validação do agente

### Teste 1: Consulta de gastos específica
- **Pergunta:** "Quanto gastei com restaurantes?"
- **Resposta esperada:** Dário deve retornar o valor baseado no `transacoes.csv` e em novas informações fornecidas via prompt.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Consulta de limite
- **Pergunta:** "Quanto ainda tenho disponível para gastos livres?"
- **Resposta esperada:** Dário deve retornar a porcentagem e quantia líquida com base na renda total e no que já foi gasto.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Pergunta fora do escopo
- **Pergunta:** "Qual a previsão do tempo?"
- **Resposta esperada:** Dário deve informar que só trata de finanças e não tem isso tipo de informação.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 4: Informação inexistente
- **Pergunta:** "Quanto rende o produto financeiro Fundo Imobiliário?"
- **Resposta esperada:** Dário deve admitir que não tem essa informação.
- **Resultado:** [X] Correto  [ ] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- O agente consegue lidar muito bem com as informações que lhe foram passadas em `CSV` e `JSON`, interpreta-as exatamente da forma que foi instruído a fazer e consegue gerar novas informações a partir delas (como porcentagens e valores líquidos remanescentes, por exemplo). O reconhecimento de padrões também funciona suficientemente bem. Sua memória também é ótima, ele registra informações novas e as interpreta exatamente da mesma forma que interpreta as que já haviam lhe sido dadas anteriormente por injeção.

**O que pode melhorar:**
- A maior parte do que pode melhorar corresponde a desafios encontrados por conta das limitações do modelo de inteligência artificial utilizado (gpt-oss), que é open source e por isso possui muito menos parâmetros do que o comum. Pode cometer erros aritméticos, mas estes são facilmente corrigidos com um prompt de feedback. 

---
