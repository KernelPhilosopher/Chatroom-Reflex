# db_manager.py
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# CONFIGURACIÓN DE BASE DE DATOS con valores por defecto
URI = os.getenv("NEO4J_URI", "neo4j://f7729929.databases.neo4j.io:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "599WXdyAaqWrMza5byKsFlkkZiX9Pjv9eOUVaVAFM3g")

# Validar que tenemos todas las variables necesarias
if not all([URI, USER, PASSWORD]):
    raise ValueError(
        "❌ Faltan variables de entorno necesarias. Asegúrate de configurar NEO4J_URI, NEO4J_USER y NEO4J_PASSWORD"
    )


class Neo4jManager:
    def __init__(self):
        self.driver = None
        self._connect()

    def _connect(self):
        """Conecta usando la configuración que probamos que funciona."""
        try:
            print("🔄 Conectando a Neo4j AuraDB con configuración exitosa...")

            # CONFIGURACIÓN GANADORA del test
            self.driver = GraphDatabase.driver(
                URI,
                auth=(USER, PASSWORD),
                trust="TRUST_ALL_CERTIFICATES",
                encrypted=True,
                connection_timeout=30,
            )

            # Verificar la conexión
            with self.driver.session() as session:
                result = session.run(
                    "RETURN 'Conexión exitosa!' AS mensaje, timestamp() AS tiempo"
                )
                record = result.single()
                print(f"✅ {record['mensaje']} - Timestamp: {record['tiempo']}")

        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            self.driver = None

    def close(self):
        if self.driver is not None:
            self.driver.close()
            print("Conexión cerrada.")

    def run_query(self, query, parameters=None):
        """Ejecuta consultas con manejo de errores."""
        if self.driver is None:
            if os.getenv("REFLEX_ENV") != "prod":
                print("❌ No hay conexión con la base de datos.")
            return []

        try:
            with self.driver.session() as session:
                result = session.run(query, parameters)
                return [record.data() for record in result]

        except Exception as e:
            if os.getenv("REFLEX_ENV") != "prod":
                print(f"❌ Error en consulta: {e}")
                print("🔄 Intentando reconectar...")
            self._connect()
            return []

    def test_connection(self):
        """Prueba la conexión."""
        if self.driver is None:
            print("❌ No hay driver inicializado")
            return False

        try:
            with self.driver.session() as session:
                result = session.run(
                    "RETURN 'Test exitoso!' AS test, timestamp() AS tiempo"
                )
                record = result.single()
                print(f"✅ {record['test']} - Tiempo: {record['tiempo']}")
                return True

        except Exception as e:
            print(f"❌ Test de conexión falló: {e}")
            return False

    def create_message(
        self, message_id: str, user: str, text: str, reply_to: str = None
    ):
        """Crear un mensaje nuevo, opcionalmente como respuesta a otro mensaje."""
        try:
            if reply_to:
                query = """
                CREATE (m:Message {
                    id: $message_id,
                    user: $user,
                    text: $text,
                    timestamp: timestamp()
                })
                WITH m
                MATCH (parent:Message {id: $parent_id})
                CREATE (m)-[:RESPONDE_A]->(parent)
                RETURN m
                """
                params = {
                    "message_id": message_id,
                    "user": user,
                    "text": text,
                    "parent_id": reply_to,
                }
            else:
                query = """
                CREATE (m:Message {
                    id: $message_id,
                    user: $user,
                    text: $text,
                    timestamp: timestamp()
                })
                RETURN m
                """
                params = {"message_id": message_id, "user": user, "text": text}

            result = self.run_query(query, params)
            return result[0] if result else None

        except Exception as e:
            print(f"❌ Error al crear mensaje: {e}")
            return None

    def get_messages_with_replies(self):
        """Obtener todos los mensajes con sus respuestas."""
        try:
            query = """
            MATCH (m:Message)
            OPTIONAL MATCH (m)-[r:RESPONDE_A]->(parent:Message)
            RETURN m.id AS id,
                   m.user AS user,
                   m.text AS text,
                   parent.user AS parent_user,
                   parent.text AS parent_text
            ORDER BY m.timestamp DESC
            LIMIT 50
            """
            return self.run_query(query)
        except Exception as e:
            print(f"❌ Error al obtener mensajes: {e}")
            return []


# Instancia global
db = Neo4jManager()

# Test automático al importar (opcional - puedes comentar esta línea)
if __name__ == "__main__":
    print("🧪 Probando conexión...")
    db.test_connection()
