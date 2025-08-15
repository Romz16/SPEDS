# schemas.py

# Mapeamento dos campos dos registros para os nossos arquivos SPED mockados.
# Esta versão é simplificada para bater EXATAMENTE com os dados dos exemplos.
SCHEMAS = {
    '0000': [
        'REG', 'COD_VER', 'COD_FIN', 'DT_INI', 'DT_FIN', 'NOME', 'CNPJ', 
        'CPF', 'UF', 'IE', 'COD_MUN', 'IM', 'SUFRAMA', 'IND_PERFIL', 'IND_ATIV'
    ],
    # O C100 do nosso exemplo tem 26 campos
    'C100': [
        'REG', 'IND_OPER', 'IND_EMIT', 'COD_PART', 'COD_MOD', 'COD_SIT', 
        'SER', 'SUB', 'NUM_DOC', 'CHV_NFE', 'DT_DOC', 'DT_E_S', 'VL_DOC', 
        'IND_PGTO', 'VL_DESC', 'VL_ABAT_NT', 'VL_MERC', 'IND_FRT', 'VL_FRT', 
        'VL_SEG', 'VL_OUT_DA', 'VL_BC_ICMS', 'VL_ICMS', 'VL_BC_ICMS_ST', 
        'VL_ICMS_ST', 'VL_IPI'
    ],
    # O C170 do nosso exemplo tem 21 campos
    'C170': [
        'REG', 'NUM_ITEM', 'COD_ITEM', 'DESCR_COMPL', 'QTD', 'UNID', 'VL_ITEM',
        'VL_DESC', 'IND_MOV', 'CST_ICMS', 'CFOP', 'COD_NAT', 'VL_BC_ICMS',
        'ALIQ_ICMS', 'VL_ICMS', 'VL_BC_ICMS_ST', 'ALIQ_ST', 'VL_ICMS_ST',
        'IND_APUR', 'CST_IPI', 'COD_ENQ'
    ],
    # O D100 do nosso exemplo tem 21 campos
    'D100': [
        'REG', 'IND_OPER', 'IND_EMIT', 'COD_PART', 'COD_MOD', 'COD_SIT', 'SER', 'SUB',
        'NUM_DOC', 'CHV_CTE', 'DT_DOC', 'DT_A_P', 'TP_CT-E', 'CHV_CTE_REF',
        'VL_DOC', 'VL_DESC', 'IND_FRT', 'VL_SERV', 'VL_BC_ICMS', 'VL_ICMS', 'VL_NT'
    ],
    # O E110 do nosso exemplo tem 15 campos
    'E110': [
        'REG', 'VL_TOT_DEBITOS', 'VL_AJ_DEBITOS', 'VL_TOT_AJ_DEBITOS', 
        'VL_ESTORNOS_CRED', 'VL_TOT_CREDITOS', 'VL_AJ_CREDITOS', 
        'VL_TOT_AJ_CREDITOS', 'VL_ESTORNOS_DEB', 'VL_SLD_CREDOR_ANT', 
        'VL_SLD_APURADO', 'VL_TOT_DED', 'VL_ICMS_RECOLHER', 'VL_SLD_CREDOR_TRANSPORTAR', 
        'DEB_ESP'
    ],
    'H005': ['REG', 'DT_INV', 'VL_INV', 'MOT_INV'],
    'H010': [
        'REG', 'COD_ITEM', 'UNID', 'QTD', 'VL_UNIT', 'VL_ITEM', 'IND_PROP', 
        'COD_PART', 'TXT_COMPL', 'COD_CTA'
    ]
}