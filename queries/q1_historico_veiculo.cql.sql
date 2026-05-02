/*
Consulta Q1: Histórico Completo do Veículo
Objetivo: Obter o histórico completo de telemetria de um caminhão específico.

Explicação:
  Como definimos PKs (id_caminhao, data_hora) 
  e CK é data_hora, devemos consultar 
  filtrando por períodos específicos. Conforme objetivo proposto. 

  A consulta é eficiente porque o Cassandra pode usar a Clustering Key
  para acessar diretamente os dados sem precisar escanear toda a tabela.
*/
SELECT 
  data_hora,
  velocidade,
  rpm,
  temperatura_motor,
  gps 
FROM gestao_frota.telemetria_por_caminhao 
WHERE 
  id_caminhao = %s -- Filtro do caminhão específico
  AND data_hora > %s -- Filtro de tempo, geralmente maior que um tempo atrás
ORDER BY data_hora DESC;