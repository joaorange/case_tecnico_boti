SELECT  
    r.nm_revendedor,
    COALESCE(ROUND(MAX(CASE 
        WHEN t.dt_vencimento BETWEEN date('now', '-30 days') AND date('now') 
        AND (t.dt_pagamento IS NULL OR t.dt_pagamento = '' OR date(t.dt_pagamento) > date(t.dt_vencimento) )
        THEN julianday('now') - julianday(t.dt_vencimento) 
    END)), 0) AS max_dias_atraso_ultimos_30_dias,
      COALESCE(ROUND(MAX(CASE 
        WHEN t.dt_vencimento BETWEEN date('now', '-90 days') AND date('now') 
        AND (t.dt_pagamento IS NULL OR t.dt_pagamento = '' OR date(t.dt_pagamento) > date(t.dt_vencimento) )
        THEN julianday('now') - julianday(t.dt_vencimento) 
    END)), 0) AS max_dias_atraso_ultimos_90_dias,   
    COALESCE(totals.total_faturado, 0) AS TOTAL_FATURADO_3M,
    COALESCE(boletos.qtd_titulos_boleto, 0) AS QTD_TITULOS_BOLETO_3M
FROM 
    tb_revendedor r
LEFT JOIN 
    tb_titulos t ON r.id_revendedor = t.id_revendedor
LEFT JOIN (
    SELECT 
        id_revendedor,
        SUM(vlr_pedido) AS total_faturado
    FROM 
        tb_titulos
    WHERE 
        dt_vencimento BETWEEN date('now', '-90 days') AND date('now')
    GROUP BY 
        id_revendedor
) AS totals ON r.id_revendedor = totals.id_revendedor
LEFT JOIN (
    SELECT 
        id_revendedor,
        COUNT(*) AS qtd_titulos_boleto
    FROM 
        tb_titulos
    WHERE 
        dt_vencimento BETWEEN date('now', '-90 days') AND date('now') AND forma_pagamento = 'Boleto a Prazo'
    GROUP BY 
        id_revendedor
) AS boletos ON r.id_revendedor = boletos.id_revendedor
GROUP BY 
    r.nm_revendedor;
