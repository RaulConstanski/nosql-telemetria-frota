/* 
 * Consulta para monitoramento em tempo real do status atual de um caminhão específico.
 * Retorna o último registro disponível para o caminhão, incluindo data/hora, GPS, nível de combustível e velocidade.
 */
SELECT 
    id_caminhao,
    data_hora,
    gps,
    nivel_combustivel,
    velocidade,
    rpm,
    temperatura_motor 
FROM gestao_frota.telemetria_atual 
-- Filtro do caminhão específico
WHERE id_caminhao = %s;