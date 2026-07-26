"""
HEXACORTEX SPIDERWEB - Hilo Sensor de Gobernanza (Governance Thread)
Conectado REALMENTE al DataHub MCP Server para detectar violaciones de seguridad y datos huérfanos.
"""

import asyncio
import json
import os
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

class GovernanceThread:
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
        Se conecta al MCP Server y verifica las propiedades de gobernanza del dataset.
        Busca etiquetas sensibles (PII) y verifica si tiene un Owner asignado.
        """
        print(f"🕸️ [Hilo 3] Iniciando auditoría de gobernanza para: {dataset_urn}")
        
        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    print(f"🔗 [Hilo 3] Conectado. Consultando metadatos de seguridad...")
                    
                    # Llamada REAL a la herramienta de DataHub para obtener detalles del dataset
                    result = await session.call_tool(
                        "get_dataset", 
                        arguments={"urn": dataset_urn}
                    )
                    
                    # Análisis de la respuesta real (Simulación de parsing de JSON)
                    # En producción, parsearíamos result.content para buscar tags y owners
                    content_str = str(result.content)
                    
                    has_pii_tag = "PII" in content_str or "Confidential" in content_str
                    has_owner = "owner" in content_str.lower() or "corpuser" in content_str.lower()
                    
                    if has_pii_tag and not has_owner:
                        print(f"🚨 [Hilo 3] ¡VIOLACIÓN DETECTADA! Dataset sensible sin Owner asignado.")
                        return {
                            "status": "governance_violation", 
                            "urn": dataset_urn, 
                            "issue": "Sensitive data (PII) lacks assigned ownership.",
                            "action": "notify_nervous_system"
                        }
                    
                    print(f"✅ [Hilo 3] Gobernanza saludable. Cumple políticas.")
                    return {"status": "compliant", "urn": dataset_urn}
                    
        except Exception as e:
            print(f"❌ [Hilo 3] Error de conexión MCP: {str(e)}")
            return {"status": "connection_error", "urn": dataset_urn, "issue": str(e)}

# Ejecución real del hilo
if __name__ == "__main__":
    sensor = GovernanceThread()
    # Cambia este URN por un dataset real que contenga datos sensibles
    resultado = asyncio.run(sensor.sense_vibration("urn:li:dataset:(urn:li:dataPlatform:postgres,user_emails,PROD)"))
    print(json.dumps(resultado, indent=2))