# NoSQL Telemetria de Frota: Arquitetura ACME LTDA

Este projeto implementa uma infraestrutura de Big Data para monitoramento de telemetria de uma frota de 50.000 caminhões, baseada em um estudo de caso para a ACME LTDA. O foco principal é a utilização do Apache Cassandra (via DataStax Astra DB) para lidar com alta taxa de ingestão e consultas de séries temporais com baixa latência.

## Justificativa da Arquitetura NoSQL

Diferente de bancos relacionais, a modelagem no Cassandra é Query-Driven (orientada por consultas). Isso significa que os dados são organizados fisicamente para responder a perguntas específicas de negócio sem a necessidade de JOINS ou filtros custosos.  

Aplicamos o Teorema CAP, priorizando AP (Availability e Partition Tolerance) para garantir que o fluxo de dados dos sensores nunca seja interrompido, utilizando um Fator de Replicação (RF) de 3 e Nível de Consistência de Escrita (W) igual a 1.

## Modelagem de Dados e Consultas (Queries)
### Q1: Análise Histórica por Veículo

1. Tabela: telemetria_por_caminhao

2. Consulta: Recuperar o histórico detalhado (velocidade, RPM, temperatura) de um caminhão específico em uma janela de tempo.  

3. Justificativa Técnica: 
    - Partition Key: id_caminhao agrupa todos os eventos de um veículo no mesmo nó, evitando buscas em múltiplos servidores.  

    - Clustering Key: data_hora garante a ordenação física dos dados no disco.

    - Ordenação: Definida como DESC para que as leituras mais recentes sejam recuperadas com latência mínima.  

### Q2: Monitoramento de Excesso de Velocidade (Alertas)

1. Tabela: alertas_excesso_velocidade

2. Consulta: Identificar todos os veículos que excederam o benchmark de 80 km/h em uma data específica.  

3. Justificativa Técnica:

    - Refatoração: Originalmente modelada por ID, a tabela foi otimizada para usar dia como Partition Key.  

    - Performance: Ao clusterizar por velocidade, permitimos que o Cassandra realize Range Queries (buscas por faixa) altamente eficientes, filtrando apenas os registros que violam o limite estabelecido.  

### Q3: Status Atual da Frota (Last Known State)

1. Tabela: telemetria_atual

2. Consulta: Verificar a localização e os sensores atuais de cada caminhão para monitoramento em tempo real.  

3. Justificativa Técnica:

    - Mecânica de Upsert: Definimos apenas o id_caminhao como chave primária.  

Eficiência: Cada nova mensagem enviada pelo caminhão sobrescreve o registro anterior, garantindo uma tabela enxuta (limitada a 50 mil linhas) que evita o processamento de agregação de grandes volumes históricos.  

## Arquitetura do Projeto
O projeto foi reestruturado seguindo princípios de Analytics Engineering, garantindo modularidade e segurança:

- src/common: Core de conectividade. Centraliza a autenticação via Secure Connect Bundle e gerencia sessões de forma segura usando variáveis de ambiente (.env).

- src/ingestion: Simulador de frota que atua como produtor de dados, gerando telemetria de GPS, RPM, velocidade e temperatura.

- src/reports: Motores de execução que transformam arquivos .cql em relatórios formatados no terminal.

- queries/: Repositório de artefatos SQL/CQL, desacoplando a lógica de banco de dados do código Python.