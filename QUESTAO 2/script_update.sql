UPDATE tb_titulos 
SET 
    dt_vencimento = substr(dt_vencimento, 7, 4) || '-' || substr(dt_vencimento, 4, 2) || '-' || substr(dt_vencimento, 1, 2)
WHERE 
    dt_vencimento IS NOT NULL AND dt_vencimento != '';

UPDATE tb_titulos 
SET 
    dt_pagamento = substr(dt_pagamento, 7, 4) || '-' || substr(dt_pagamento, 4, 2) || '-' || substr(dt_pagamento, 1, 2)
WHERE 
    dt_pagamento IS NOT NULL AND dt_pagamento != '';
