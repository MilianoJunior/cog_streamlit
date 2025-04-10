leituras = {
    "CGH APARECIDA": {
        "ip": "100.110.212.125",
        "port": 8010,
        "table": "cgh_aparecida",
        "CLPS":{
            "UG-01": {
                'conexao': {'ip': '192.168.10.2', 'port': 502}, 
                'leituras': {
                    "REAL": { "Potência Ativa Acumulada UG-01": 13241, "Nível Montante": 13519, "Nível Jusante": 13521},
                    "INT": {"Potência Ativa UG-01": 13407,"Turbina Velocidade UG-01": 13321},
                },
                "alarmes":{
                    "BOOLEAN": {
                        "[01.00] - PCP-U1 - Botão de Emergência Acionado": 24289,
                        "[01.01] - PCP-U1 - Botão de Emergência Acionado - SuperSEP": 24290,
                    }
                },
                "comandos":{
                    "BOOLEAN": {
                        "Reset SuperSEP": 12850,
                        "CalaSirene SuperSEP": 12852,
                        "Reset local": 12849,
                    }
                }
            }
        }
    },
    "CGH FAE": {
        "ip": "100.106.33.66",
        "port": 8010,
        "table": "cgh_fae",
        "CLPS":{
                    "UG-01": {
                        'conexao': {'ip': '192.168.10.2', 'port': 502}, 
                        'leituras': {
                                "REAL": {
                                    "Potência Ativa UG-01": 13407, 
                                    "Potência Ativa Acumulada UG-01": 13541, 
                                    "Turbina Velocidade UG-01": 13321
                                },
                                "INT": {},
                        },
                        "alarmes":{
                            "BOOLEAN": {
                                "[01.00] - PCP-U1 - Botão de Emergência Acionado": 24289,
                                "[01.01] - PCP-U1 - Botão de Emergência Acionado - SuperSEP": 24290,
                            }
                        },
                        "comandos":{
                            "BOOLEAN": {
                                "Reset SuperSEP": 12529,
                                "CalaSirene SuperSEP": 12532,
                            }
                        }
                    },
                    "UG-02": {
                        'conexao': {'ip': '192.168.10.3', 'port': 502}, 
                        'leituras': {
                                "REAL": {
                                    "Potência Ativa UG-02": 13407, 
                                    "Potência Ativa Acumulada UG-02": 13541, 
                                    "Turbina Velocidade UG-02": 13321
                                },
                                "INT": {},
                        },
                        "alarmes":{
                            "BOOLEAN": {
                                "[01.00] - PCP-U1 - Botão de Emergência Acionado": 24289,
                                "[01.01] - PCP-U1 - Botão de Emergência Acionado - SuperSEP": 24290,
                            }
                        },
                        "comandos":{
                            "BOOLEAN": {
                                "Reset SuperSEP": 12529,
                                "CalaSirene SuperSEP": 12532,
                            }
                        }
                    },
                    "PSA": {
                        'conexao': {'ip': '192.168.10.4', 'port': 502}, 
                        'leituras': {
                                "REAL": {
                                    "Nível Montante": 13353, 
                                    "Nível Jusante": 13379
                                },
                                "INT": {},
                        },
                        "alarmes":{
                                "BOOLEAN": {
                                    "[01.00]: PSA - Falha de Acionamento - KRD - Tensão no Serviço Auxiliar - Linha 23,1 kV - Alarme": 24289,
                                    "[01.01]: PSA - Falha de Acionamento - KRD - Tensão no Serviço Auxiliar - Linha 23,1 kV - Trip": 24290,
                                }
                        },
                        "comandos":{
                                "BOOLEAN": {
                                    "Reset SuperSEP": 12450,
                                }
                        }
                    }
                }
            }
        }