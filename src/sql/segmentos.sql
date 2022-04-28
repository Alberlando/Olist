SELECT 
    t1.*,
    CASE 
        WHEN pct_receita <= 0.5 AND pct_freq <= 0.5 THEN 'IMPRODUTIVO'
        WHEN pct_receita > 0.5 AND pct_freq <= 0.5 THEN 'ALTO VALOR'
        WHEN pct_receita <= 0.5 AND pct_freq > 0.5 THEN 'ALTA FREQUENCIA'
        WHEN pct_receita > 0.5 AND pct_freq > 0.5 THEN 'PRODUTIVO'
        ELSE 'SUPER PRODUTIVO'
    END AS segmento_valor_freq,

    CASE 
        WHEN Qtde_dias_base <= 60 THEN 'INICIO'
        WHEN Qtde_dias_ult_venda >= 300 THEN 'RETENCAO'
        ELSE 'ATIVO'
    END AS segmento_vida,

    '{date_end}' AS dt_sgmt

FROM (
    SELECT 
        t1.*,
        percent_rank() OVER (ORDER BY Valor ASC) AS pct_receita,
        percent_rank() OVER (ORDER BY Qtde_pedidos ASC) AS pct_freq
    FROM (
        SELECT 
            t2.seller_id AS Id, 
            SUM( t2.price ) AS Valor,
            COUNT( DISTINCT( t1.order_id ) ) AS Qtde_pedidos,
            COUNT( t2.product_id ) AS Qtde_itens,
            MIN( CAST( julianday( '{date_end}' ) - julianday( t1.order_approved_at ) AS INT ) ) AS Qtde_dias_ult_venda,
            MAX( CAST( julianday( '{date_end}' ) - julianday( t3.dt_inicio ) AS INT ) ) AS Qtde_dias_base
        FROM tb_orders t1
        LEFT JOIN tb_order_items t2
        ON t1.order_id = t2.order_id

        LEFT JOIN (
            SELECT 
                t2.seller_id, 
                MIN(DATE(t1.order_approved_at)) AS dt_inicio
            FROM tb_orders t1
            LEFT JOIN tb_order_items t2
            ON t1.order_id = t2.order_id
            GROUP BY t2.seller_id
        ) AS t3
        ON t2.seller_id = t3.seller_id

        WHERE t1.order_approved_at BETWEEN '{date_init}' AND '{date_end}'
        GROUP BY t2.seller_id
        ORDER BY Valor DESC
    ) AS t1
) AS t1
WHERE Id IS NOT NULL