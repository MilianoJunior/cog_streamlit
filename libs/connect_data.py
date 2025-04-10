'''
Através da API, faz a coleta dos dados e retorna um dataframe com os dados coletados.
Endpoint:
    http://192.168.1.100:5000/readCLP/leituras
    body:{
        "conexao": {ip: "IP_ADDRESS", porta: "5000"},
        "registers": {"REAL": {"Turbina posição do distribuidor": 13317, "Turbina Velocidade": 13321},"INT": {"Turbina Velocidade": 13321, "Turbina Vazão": 13323}}
    }
    http://192.168.1.100:5000/readCLP/alarmes
    body:{
        "conexao": {ip: "IP_ADDRESS", porta: "5000"},
        "registers":{"BOOLEAN": {"[01.00] - PCP-U1 - Botão de Emergência Acionado": 24289,"[01.01] - PCP-U1 - Botão de Emergência Acionado - SuperSEP": 24290}}
    }

'''
import pandas as pd
import json
import time
import httpx
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def connect_postgres():
    try:
        pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            port=os.getenv('POSTGRES_PORT')
        )
        return pool
    except Exception as e:
        error_msg = f"Erro ao inicializar pool PostgreSQL: {str(e)}"
        raise Exception(error_msg)
    
def save_postgres(ip, unidade, port, json_data, table_name):
    query = f'''
                INSERT INTO {table_name} (ip, unidade, porta, leituras)
                VALUES (%s, %s, %s, %s)
            '''
    params = (ip, unidade, port, json_data)
    pool = connect_postgres()
    try:
        with pool.getconn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
    except Exception as e:
        error_msg = f"Erro ao salvar dados no PostgreSQL: {str(e)}"
        raise Exception(error_msg)


async def json_to_dataframe(json_data):
    df = pd.DataFrame(json_data)
    return df


def generate_data(body):
    import random
    registers = body['registers']
    for register in registers:
        if register == 'REAL':
            for key, value in registers[register].items():
                registers[register][key] = random.uniform(0, 100)
        elif register == 'INT':
            for key, value in registers[register].items():
                registers[register][key] = random.randint(0, 100)
    # print(registers)
    return registers

async def get_data(ip, port, data, tipo, unidade):
    inicio = time.time()
    body = {
        "conexao": data['conexao'],
        "registers": data[tipo]
    }
    
    async with httpx.AsyncClient(verify=False) as client:
        try:
            # Leituras
            # response = await client.post(f"http://{ip}:{port}/readCLP/{tipo}", json=body)
            # leituras_data = response.json()
            # save_postgres(ip, unidade, port, leituras_data, tipo)
            # leituras_dataframe = await json_to_dataframe(leituras_data)
            fim = time.time() - inicio
            data = generate_data(body)
            leituras_dataframe = await json_to_dataframe(data)
            return leituras_dataframe, fim
        except Exception as e:
            fim = time.time() - inicio
            return generate_data(body), fim
        
'''
        
    Assim, então para resumir, eu faço adesão ao consorcio, espero até a  proxima
'''
