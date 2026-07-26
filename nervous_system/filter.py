"""
HEXACORTEX SPIDERWEB - Sistema Nervioso (Filter & Triangulation)
Recibe las vibraciones de los 3 hilos, filtra el ruido y triangula las amenazas reales 
para activar al Decisor (La Araña).
"""

import json
from typing import List, Dict

class NervousSystem:
    def __init__(self):
        # Estados que consideramos "ruido" o fondo saludable
        self.noise_statuses = ["stable", "healthy_flow", "compliant", "connection_error"]

    def filter_noise(self, signals: List[Dict]) -> List[Dict]:
        """
        Filtra las vibraciones normales. Solo deja pasar las amenazas reales.
        """
        threats = []
        for signal in signals:
            if signal.get("status") not in self.noise_statuses:
                threats.append(signal)
        return threats

    def triangulate(self, threats: List[Dict]) -> List[Dict]:
        """
        Asigna prioridad a las amenazas. 
        Si múltiples hilos están fallando simultáneamente, la prioridad sube a CRITICAL.
        """
        threat_level = "CRITICAL" if len(threats) > 1 else "HIGH"
        
        for threat in threats:
            threat["priority"] = threat_level
            threat["triangulated"] = True
            
        return threats

    def process_vibrations(self, signals: List[Dict]) -> List[Dict]:
        """
        Pipeline completo del sistema nervioso: Filtrar -> Triangular -> Alertar.
        """
        print("🧠 [Sistema Nervioso] Procesando vibraciones de la telaraña...")
        
        # 1. Filtrar ruido
        filtered_threats = self.filter_noise(signals)

        # 2. Si no hay amenazas, la araña sigue durmiendo
        if not filtered_threats:
            print("💤 [Sistema Nervioso] Solo ruido de fondo. La araña duerme.")
            return []

        # 3. Triangular y asignar prioridad
        print(f"️ [Sistema Nervioso] {len(filtered_threats)} amenaza(s) real(es) detectada(s). Triangulando...")
        return self.triangulate(filtered_threats)

# Prueba del sistema nervioso
if __name__ == "__main__":
    ns = NervousSystem()
    
    # Simulamos la entrada de datos que vendrían de los 3 hilos (schema, lineage, governance)
    mock_signals_from_threads = [
        {"status": "stable", "urn": "table_sales"},
        {"status": "broken_lineage", "urn": "table_users", "issue": "No upstream"},
        {"status": "governance_violation", "urn": "table_payments", "issue": "No owner"}
    ]
    
    # El sistema nervioso decide qué pasa al cerebro de la araña
    result = ns.process_vibrations(mock_signals_from_threads)
    print("\n️ [Salida para la Araña]:")
    print(json.dumps(result, indent=2))