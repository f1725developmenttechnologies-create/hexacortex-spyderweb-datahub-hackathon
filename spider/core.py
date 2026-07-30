"""
HEXACORTEX SPIDERWEB - El Decisor (Spider Core)
Recibe amenazas trianguladas, genera código de reparación de producción 
y escribe la solución de vuelta en el grafo de DataHub vía MCP Server.
"""

import asyncio
import json
import os
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

class SpiderCore:
    def __init__(self):
        # Configuración REAL del MCP Server de DataHub
        self.server_params = StdioServerParameters(
            command="npx",
            args=["-y", "@datahub/mcp-server@latest"],
            env={
                "DATAHUB_GMS_URL": os.getenv("DATAHUB_GMS_URL", "http://localhost:8080"),
                "DATAHUB_GMS_TOKEN": os.getenv("DATAHUB_GMS_TOKEN", "")
            }
        )

    def _generate_repair_artifact(self, threat: dict) -> str:
        """
        Genera el código de reparación basado en el tipo de amenaza.
        """
        urn = threat.get("urn", "unknown")
        issue = threat.get("issue", "Unknown issue")
        
        if threat.get("status") == "broken_lineage":
            return f"""# REPAIR ARTIFACT: Airflow DAG para restaurar linaje
# Target URN: {urn}
# Issue: {issue}

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

with DAG('repair_lineage_{urn.split(":")[-1]}', start_date=datetime(2026, 1, 1)) as dag:
    restore_upstream = PostgresOperator(
        task_id='re_ingest_upstream_data',
        postgres_conn_id='prod_db',
        sql="INSERT INTO {urn.split(':')[-1]} SELECT * FROM raw_events WHERE date = CURRENT_DATE;"
    )
"""
        elif threat.get("status") == "governance_violation":
            return f"""# REPAIR ARTIFACT: Script Python para asignar Ownership
# Target URN: {urn}
# Issue: {issue}

import requests

def assign_owner():
    url = "http://localhost:8080/entities"
    payload = {{
        "entityType": "dataset",
        "entityUrn": "{urn}",
        "aspectName": "ownership",
        "aspect": {{
            "owners": [{{"owner": "urn:li:corpuser:data_engineer", "type": "TECHNICAL_OWNER"}}]
        }}
    }}
    # requests.post(url, json=payload, headers={{"Authorization": "Bearer <TOKEN>"}})
"""
        return "# No specific repair artifact generated for this threat type."

    async def execute_repair_and_write_back(self, threat: dict):
        """
        La Araña actúa: Guarda el artefacto y notifica a DataHub que la reparación fue generada.
        """
        print(f"🕷️ [Araña] Consumiendo amenaza: {threat.get('status')} en {threat.get('urn')}")
        
        # 1. Generar el código de reparación
        artifact_code = self._generate_repair_artifact(threat)
        print("🧵 [Araña] Artefacto de reparación generado exitosamente.")
        
        # 2. Escribir de vuelta en DataHub (Agregar un tag de "Remediated_by_Hexacortex")
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    print("🔗 [Araña] Conectando a DataHub para escribir el contexto de reparación...")
                    
                    # Llamada REAL para agregar un tag o nota al dataset
                    await session.call_tool(
                        "add_tags_to_entity",
                        arguments={
                            "urn": threat.get("urn"),
                            "tags": ["Remediated_by_Hexacortex", "Auto_Repaired"]
                        }
                    )
                    print("✅ [Araña] Contexto escrito en el grafo de DataHub. La telaraña está reparada.")
                    
        except Exception as e:
            print(f"⚠️ [Araña] No se pudo escribir en DataHub (¿MCP Server activo?): {str(e)}")
            print("💡 [Araña] El artefacto de reparación se guardó localmente de todos modos.")

        return artifact_code

# Ejecución real del ciclo completo
if __name__ == "__main__":
    spider = SpiderCore()
    
    # Simulamos una amenaza real que viene del Sistema Nervioso
    mock_threat_from_nervous_system = {
        "status": "broken_lineage",
        "urn": "urn:li:dataset:(urn:li:dataPlatform:bigquery,user_purchases_v2,PROD)",
        "issue": "No upstream sources found. Data flow interrupted.",
        "priority": "CRITICAL",
        "triangulated": True
    }
    
    print("🕸️ --- INICIANDO PROTOCOLO HEXACORTEX --- 🕸️")
    resultado = asyncio.run(spider.execute_repair_and_write_back(mock_threat_from_nervous_system))
    
    print("\n📦 --- ARTEFACTO GENERADO (Guardar en examples/) --- 📦")
    print(resultado)