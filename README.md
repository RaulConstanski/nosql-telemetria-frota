# NoSQL: Arquitetura ACME LTDA

O projeto utiliza uma arquitetura de banco de dados híbrida para atender a diferentes necessidades de negócio:
- Telemetria de camihões: Apache Cassandra (Nuvem - DataStax Astra DB);
- MongoDB (local - Docker)

## Justificativa da Arquitetura NoSQL - Telemetria em Cassandra

Diferente de bancos relacionais, a modelagem no Cassandra é Query-Driven (orientada por consultas). Isso significa que os dados são organizados fisicamente para responder a perguntas específicas de negócio sem a necessidade de JOINS ou filtros custosos.  

Aplicamos o Teorema CAP, priorizando AP (Availability e Partition Tolerance) para garantir que o fluxo de dados dos sensores nunca seja interrompido, utilizando um Fator de Replicação (RF) de 3 e Nível de Consistência de Escrita (W) igual a 1.

### Modelagem de Dados e Consultas (Queries)
#### Q1: Análise Histórica por Veículo

1. Tabela: telemetria_por_caminhao

2. Consulta: Recuperar o histórico detalhado (velocidade, RPM, temperatura) de um caminhão específico em uma janela de tempo.  

3. Justificativa Técnica: 
    - Partition Key: id_caminhao agrupa todos os eventos de um veículo no mesmo nó, evitando buscas em múltiplos servidores.  

    - Clustering Key: data_hora garante a ordenação física dos dados no disco.

    - Ordenação: Definida como DESC para que as leituras mais recentes sejam recuperadas com latência mínima.  

#### Q2: Monitoramento de Excesso de Velocidade (Alertas)

1. Tabela: alertas_excesso_velocidade

2. Consulta: Identificar todos os veículos que excederam o benchmark de 80 km/h em uma data específica.  

3. Justificativa Técnica:

    - Refatoração: Originalmente modelada por ID, a tabela foi otimizada para usar dia como Partition Key.  

    - Performance: Ao clusterizar por velocidade, permitimos que o Cassandra realize Range Queries (buscas por faixa) altamente eficientes, filtrando apenas os registros que violam o limite estabelecido.  

#### Q3: Status Atual da Frota (Last Known State)

1. Tabela: telemetria_atual

2. Consulta: Verificar a localização e os sensores atuais de cada caminhão para monitoramento em tempo real.  

3. Justificativa Técnica:

    - Mecânica de Upsert: Definimos apenas o id_caminhao como chave primária.  

Eficiência: Cada nova mensagem enviada pelo caminhão sobrescreve o registro anterior, garantindo uma tabela enxuta (limitada a 50 mil linhas) que evita o processamento de agregação de grandes volumes históricos.  

## Manifesto de Carga e Cadastro de Motoristas - MongoDB

A flexibilidade do esquema JSON permite armazenar diferentes tipos de carga (perecíveis, eletrônicos, etc) sem necessidade de migrações complexas de esquema.

### Coleções (collection):
- motoristas: Armazena o cadastro principal atualizado do condutor.

- manifestos: Registra as viagens, incluindo um snapshot dos dados do motorista e detalhes de carga.

### Exemplos de consultas no MongoDB via mongosh, podendo ser aplicado em código
1. Consulta de motoristas que possuem carteira E
    - db["motoristas"].find({"cnh_categoria": "E"}, {"nome": 1, "cpf": 1,"_id": 1})

2. Consulta motorista dentro de manifesto que está viajando para curitiba
    - db["manifestos"].find({$and: [{"rota.destino": {"$regex": "Curitiba"}, "status":"Iniciado"}]}, {"motorista.nome": 1,"_id": 0})


## Replicação do Projeto

Para utilizar o Astra você precisa criar uma conta no site: https://accounts.datastax.com/session-service/v1/login

Crie um banco, veja o manual para conexão, este projeto utiliza conexão via bundle, necessário setar as variáveis de ambiente:

ASTRA_DB_CLIENT_ID = 'Verifique no site do datastax'

ASTRA_DB_CLIENT_SECRET = 'Verifique no site do datastax'

SECURE_CONNECT_BUNDLE_PATH = 'Verifique no site do datastax, baixe na raiz do projeto'

ASTRA_DB_KEYSPACE = 'gestao_frota' # ou o nome que desejar

MONGO_ROOT_USER= 'crie-seu-usuario-admin'

MONGO_ROOT_PASSWORD= 'insira sua senha'

MONGO_URI=mongodb://${MONGO_ROOT_USER}:${MONGO_ROOT_PASSWORD}@mongodb:27017/ #porta padrão mongodb
