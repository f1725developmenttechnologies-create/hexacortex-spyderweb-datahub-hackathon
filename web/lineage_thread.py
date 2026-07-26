"""
HEXACORTEX SPIDERWEB - Hilo Sensor de Linaje (Lineage Thread)
Conectado REALMENTE al DataHub MCP Server para detectar rupturas en el flujo de datos.
"""

import asyncio
import json
import os
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

class LineageThread:
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

    async def sense_vibration(self, dataset_urn: str):
        """
        Se conecta al MCP Server y consulta el linaje real del dataset.
        Retorna: Estado del flujo y datos si hay ruptura.
        """
        print(f"🕸️ [Hilo 2] Iniciando conexión MCP para: {dataset_urn}")
        
        try:
            # Conexión real al servidor MCP de DataHub
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    print(f"🔗 [Hilo 2] Conectado. Consultando linaje UPSTREAM...")
                    
                    # Llamada REAL a la herramienta de DataHub
                    result = await session.call_tool(
                        "get_lineage", 
                        arguments={"urn": dataset_urn, "direction": "UPSTREAM"}
                    )
                    
                    # Análisis de la respuesta real
                    if not result.content or len(result.content) == 0:
                        print(f"🚨 [Hilo 2] ¡RUPTURA DETECTADA! No hay fuentes upstream.")
                        return {
                            "status": "broken_lineage", 
                            "urn": dataset_urn, 
                            "issue": "No upstream sources found. Data flow interrupted.",
                            "action": "notify_nervous_system"
                        }
                    
                    print(f"✅ [Hilo 2] Flujo saludable. Linaje encontrado.")
                    return {"status": "healthy_flow", "urn": dataset_urn, "data": str(result.content)}
                    
        except Exception as e:
            print(f"❌ [Hilo 2] Error de conexión MCP: {str(e)}")
            return {"status": "connection_error", "urn": dataset_urn, "issue": str(e)}

# Ejecución real del hilo
if __name__ == "__main__":
    sensor = LineageThread()
    # Cambia este URN por uno real de tu instancia de DataHub
    resultado = asyncio.run(sensor.sense_vibration("urn:li:dataset:(urn:li:dataPlatform:bigquery,user_purchases_v2,PROD)"))
    print(json.dumps(resultado, indent=2))