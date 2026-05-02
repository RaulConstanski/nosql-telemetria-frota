/*
Consulta Q2: Monitoramento de Velocidade
Objetivo: Obter o histórico de telemetria de um caminhão específico, 
filtrando por velocidade.

Explicação:
  Como definimos PKs (dia, velocidade e data_hora) 
  e CK velocidade e data_hora, devemos consultar 
  filtrando por dia e velocidade. Conforme objetivo proposto.

  A consulta é eficiente porque o Cassandra pode usar a Clustering Key
  para acessar diretamente os dados sem precisar escanear toda a tabela.
*/
SELECT 
    id_caminhao,
    velocidade,
    data_hora,
    gps 
FROM gestao_frota.alerta_por_excesso_velocidade 
WHERE 
  dia = %s 
  AND velocidade > %s
  ORDER BY velocidade DESC, data_hora DESC
  LIMIT 10;