# Credit Risk MLOps
Projeto de ponta a ponta para predição de risco de crédito, utilizando técnicas de Machine Learning e práticas de MLOps para automação do pipeline e disponibilização do modelo em produção.

---

# 🏗️ Arquitetura do Projeto

A figura abaixo apresenta a arquitetura da solução desenvolvida para o pipeline de Machine Learning e MLOps, destacando o fluxo desde a ingestão dos dados até o treinamento e disponibilização do modelo.

<p>
  <img src="images/arquitetura.png" alt="Arquitetura do Projeto" width="900">
</p>

---

# 📊 Monitoramento dos Dados e do Modelo

O monitoramento do pipeline foi dividido em quatro camadas, permitindo identificar rapidamente problemas na ingestão dos dados, degradação do modelo e impactos no negócio.

Os principais objetivos são:

- ✅ Detectar falhas na execução do pipeline;
- ✅ Garantir a qualidade e integridade dos dados;
- ✅ Identificar mudanças na distribuição dos dados (*data drift*);
- ✅ Detectar degradação da performance do modelo (*concept drift*);
- ✅ Monitorar o impacto do modelo nos indicadores de negócio.

---

## 1. Monitoramento da Arquitetura

Como o pipeline é orquestrado pelo **Apache Airflow**, cada etapa do processo possui controle de execução.

### Estratégia

- Caso qualquer *task* apresente falha, a execução da DAG é interrompida.
- A falha fica registrada na interface do Airflow, facilitando a investigação.
- É possível configurar notificações automáticas para o time de engenharia via:
  - 📧 E-mail
  - 💬 Microsoft Teams
  - 📱 Slack
  - 🔔 Outros sistemas de alerta

---

## 2. Monitoramento dos Dados (Entrada)

### ✅ Validação de Schema *(Implementado)*

Foi implementado um **Contrato de Dados** utilizando **Pydantic**.

Durante a ingestão da camada **RAW** e **SILVER**, cada registro é validado antes de seguir para as próximas etapas do pipeline.

São verificados:

- presença de todas as features obrigatórias;
- tipo de dado de cada atributo;
- valores permitidos e restrições definidas no contrato.

Caso algum registro seja inválido:

- a predição é bloqueada;
- a DAG `home_credit_data_pipeline` falha;
- o problema pode ser identificado imediatamente.

---

### 📈 Qualidade dos Dados

Além da validação estrutural, recomenda-se acompanhar continuamente indicadores de qualidade, como:

- percentual de valores nulos;
- distribuição de valores numéricos (idade, renda, crédito etc.);
- cardinalidade das variáveis categóricas;
- reaparecimento de valores sentinela, por exemplo:
  - `DAYS_EMPLOYED = 365243`
  - `ORGANIZATION_TYPE = XNA`

---

### 📉 Data Drift

Mudanças na distribuição dos dados podem degradar o desempenho do modelo.

O monitoramento pode ser realizado utilizando o **Population Stability Index (PSI)** para cada feature, comparando os dados atuais com aqueles utilizados durante o treinamento.

| Valor do PSI | Interpretação |
|--------------|---------------|
| **PSI < 0,10** | Distribuição estável |
| **0,10 ≤ PSI < 0,25** | Atenção |
| **PSI ≥ 0,25** | Drift crítico |

As principais variáveis a serem monitoradas incluem:

- `EXT_SOURCE_*`
- razões entre renda e crédito
- idade
- demais features utilizadas pelo modelo

---

## 3. Monitoramento do Modelo

### 📊 Prediction Drift

Monitorar a distribuição das probabilidades previstas (**Probabilidade de Default- PD**) ao longo do tempo.

Indicadores importantes:

- distribuição da PD;
- percentual de clientes em cada faixa de risco (A–E);
- mudanças bruscas na concentração de clientes nas classes de maior risco.

---

### 📈 Performance do Modelo

Como a variável **TARGET** somente é conhecida meses após a concessão do crédito, a avaliação da performance ocorre com defasagem.

Para cada safra, recomenda-se recalcular métricas como:

- AUC
- KS
- Gini

Comparando-as com o baseline obtido durante o treinamento.

| Métrica | Valor de referência |
|----------|---------:|
| AUC | **0,762** |
| KS | **0,390** |
| Gini | **0,524** |

Quedas significativas nessas métricas podem indicar que a relação entre as características dos clientes e o risco de inadimplência mudou ao longo do tempo (**Concept Drift**), reduzindo a capacidade do modelo de realizar previsões precisas.

---

### 🎯 Calibração

Além da capacidade discriminatória, é importante verificar se as probabilidades previstas continuam bem calibradas.

Comparar:

- Probabilidade de Default prevista (PD)
- inadimplência observada

por faixas de risco.

Caso exista divergência significativa, o modelo deverá ser recalibrado.

---

### ⚙️ Monitoramento Operacional

Também devem ser acompanhados indicadores relacionados à disponibilidade da aplicação.

Exemplos:

- tempo de resposta da interface de predição;
- taxa de erros;
- disponibilidade;
- timeouts;
- versão do modelo em produção;
- versão da ABT utilizada para predição.

---

## 4. Monitoramento de Negócio

Por fim, é importante acompanhar indicadores que refletem o impacto financeiro do modelo.

Os principais indicadores incluem:

- taxa de aprovação;
- volume total de crédito concedido;
- exposição financeira (R$);
- perda esperada;
- perda realizada;
- taxa de inadimplência por safra.

Esses indicadores permitem verificar se o modelo continua gerando valor para o negócio e apoiando decisões de crédito de forma eficiente.

---

## 📋 Resumo

| Camada | Objetivo | Exemplos |
|---------|----------|-----------|
| Arquitetura | Detectar falhas na execução | Falha de DAG, notificações |
| Dados | Garantir qualidade e consistência | Pydantic, qualidade, PSI |
| Modelo | Monitorar desempenho | Prediction Drift, AUC, KS, Gini, calibração |
| Negócio | Avaliar impacto financeiro | Aprovação, perdas, inadimplência |

## ⚠️ Possíveis Falhas e Monitoramento do Modelo
| Falha / Risco                     | Sintoma                                                                  | Como detectar                      |
|-----------------------------------|--------------------------------------------------------------------------|------------------------------------|
| Arquitetura fora do ar            | Falha na execução geral das dags                                         | Impossibilidade de acessar airflow |
| Pipeline quebrado / dado inválido | Feature ausente ou fora do tipo esperado                                 | Validação de schema (Pydantic)     |
| Data drift (mudança econômica)    | Distribuição das variáveis muda                                          | PSI por feature                    |
| Concept drift                     | Relação entre risco e variáveis muda                                     | Queda de AUC/KS por safra          |
| Descalibração                     | Probabilidade de inadimplência (PD) não corresponde à inadimplência real | Curva de calibração por faixa      |
| Modelo desatualizado              | Muito tempo sem retreino                                                 | Tempo desde o último treinamento   |
| Falha operacional                 | Sistema de Predição indisponível ou lento                                | Latência, taxa de erros e uptime   |

## ⚙️ Como operacionalizar o monitoramento

Para que os indicadores apresentados possam ser acompanhados continuamente, é recomendado:

- Registrar cada predição realizada, incluindo:
  - dados de entrada;
  - probabilidade de inadimplência (PD);
  - faixa de risco;
  - decisão tomada;
  - versão do modelo utilizada.
- Armazenar essas informações em um banco de dados ou Data Lake para possibilitar análises históricas.
- Criar dashboards para acompanhar os indicadores de qualidade dos dados, desempenho do modelo e métricas de negócio. Pode ser utilizado o Grafana, por exemplo.
- Configurar alertas automáticos para que o time seja notificado quando algum indicador ultrapassar os limites definidos, permitindo uma resposta rápida a problemas como falhas no pipeline, *data drift* ou degradação da performance do modelo.

---

# 🤖 Ações Automatizadas Baseadas nas Previsões do Modelo

Após realizar a predição da **Probabilidade de Default (PD)**, o modelo pode acionar automaticamente diferentes fluxos de negócio de acordo com a faixa de risco do cliente.

Essa abordagem integra **Machine Learning**, **automação de processos** e **agentes de IA**, permitindo que decisões de crédito sejam tomadas de forma mais rápida e padronizada. Casos de maior risco ou maior impacto podem ser encaminhados para análise humana.

## Possíveis ações automatizadas

| Faixa | Probabilidade de Default (PD) | Ações sugeridas                                                                                                                                                       |
|--------|-------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **A** | < 5% | Aprovação automática do crédito, aumento de limite, oferta de produtos premium e liberação imediata do contrato digital.                                              |
| **B–C** | 5% – 30% | Aprovação com limite ajustado, solicitação automática de documentos pendentes, validação cadastral complementar e oferta de garantia opcional.                        |
| **D** | 30% – 60% | Encaminhamento para análise humana, redução do limite aprovado, solicitação de garantias para o crédito e geração automática de um resumo do cliente utilizando IA. |
| **E** | > 60% | Recusa automática, geração de explicação da decisão utilizando IA, oferta de produtos de menor risco e disponibilização de conteúdo de educação financeira. |


## 🤖 Automação e Agentes de IA

Além das ações automatizadas por faixa de risco, o sistema pode integrar agentes de IA para executar tarefas específicas ao longo do processo de concessão de crédito, tornando a análise mais rápida, padronizada e eficiente.

### 👨‍💼 Agente de Apoio à Análise de Crédito

Auxilia o analista na avaliação de casos que exigem revisão manual (por exemplo, clientes da faixa **D**).

Principais responsabilidades:

- gerar um resumo do perfil do cliente;
- apresentar o histórico financeiro e cadastral;
- destacar as variáveis que mais influenciaram a predição;
- sugerir uma recomendação de decisão.

---

### 💬 Agente de Atendimento

Interage diretamente com o cliente durante o processo de análise.

Pode realizar ações como:

- solicitar documentos pendentes;
- informar o andamento da solicitação;
- responder dúvidas sobre a análise de crédito;
- orientar o cliente sobre os próximos passos.

---

### 📊 Agente de Monitoramento

Monitora continuamente o pipeline e o modelo de Machine Learning.

Entre suas funções estão:

- acompanhar métricas como PSI, AUC, KS e Gini;
- detectar falhas nas DAGs do Airflow;
- monitorar disponibilidade da API de predição;
- gerar alertas quando indicadores ultrapassarem limites definidos;
- abrir chamados automaticamente para investigação;
- acionar o fluxo de retreinamento do modelo quando houver degradação significativa da performance.

---

### 💳 Agente de Decisão de Crédito

Executa automaticamente ações de negócio com base na faixa de risco prevista pelo modelo.

Exemplos:

- definir o limite de crédito aprovado;
- ajustar a taxa de juros conforme o risco;
- solicitar garantias adicionais quando necessário;
- encaminhar casos para análise humana quando apropriado.

---

### 🔍 Agente de Explicabilidade

Gera explicações em linguagem natural sobre as decisões do modelo.

Essas explicações podem ser utilizadas para:

- apoiar analistas de crédito;
- fornecer transparência às decisões;
- auxiliar auditorias e requisitos regulatórios;
- justificar a decisão ao cliente, quando aplicável.

---

### 📈 Agente de Auditoria e Governança

Responsável por manter a rastreabilidade das decisões tomadas pelo modelo.

Entre suas atividades estão:

- registrar todas as predições e decisões em banco de dados;
- manter o histórico das versões do modelo utilizadas;
- disponibilizar informações para auditorias e monitoramento contínuo.