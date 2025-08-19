# Chatroom_Reflex.py
import reflex as rx
from .db_manager import db
from typing import List, Dict


class State(rx.State):
    """El estado de la aplicación."""

    username: str = ""
    current_message: str = ""
    messages: List[Dict[str, str]] = []
    status: str = "Cargando..."
    replying_to: str = ""  # ID del mensaje al que se responde

    def on_load(self):
        """Cargar mensajes al iniciar."""
        self.load_messages()

    def load_messages(self):
        """Cargar mensajes desde Neo4j."""
        try:
            if db.driver is None:
                self.status = "❌ Sin conexión"
                self.messages = []
                return

            result = db.get_messages_with_replies()
            self.messages = result if result else []
            self.status = f"✅ Conectado ({len(self.messages)} mensajes)"

        except Exception as e:
            print(f"Error al cargar mensajes: {e}")
            self.messages = []
            self.status = "❌ Error al cargar"

    def post_message(self):
        """Enviar un nuevo mensaje."""
        if not self.username.strip() or not self.current_message.strip():
            return

        if db.driver is None:
            self.status = "❌ Sin conexión"
            return

        try:
            # Generar un ID único para el mensaje usando State.uuid4()
            import uuid

            message_id = f"msg_{uuid.uuid4()}"

            # Crear el mensaje usando el nuevo método
            result = db.create_message(
                message_id=message_id,
                user=self.username,
                text=self.current_message,
                reply_to=self.replying_to if self.replying_to else None,
            )

            if result is not None:
                self.current_message = ""
                self.replying_to = ""  # Limpiar el mensaje al que se responde
                self.load_messages()

        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            self.status = "❌ Error al enviar"

    def reconnect(self):
        """Intentar reconectar."""
        db._connect()
        self.load_messages()

    def set_reply_to(self, message_id: str):
        """Establecer a qué mensaje se está respondiendo."""
        self.replying_to = message_id


def message_card(message: Dict) -> rx.Component:
    """Tarjeta para mostrar un mensaje."""
    return rx.box(
        rx.vstack(
            # Si es una respuesta, mostrar el mensaje original
            rx.cond(
                message.get("parent_user") is not None,
                rx.box(
                    rx.text(
                        f"↳ Respuesta a {message['parent_user']}: {message['parent_text']}",
                        font_size="0.8em",
                        color="gray",
                        font_style="italic",
                    ),
                    padding="0.5rem",
                    bg="#EAEAEA",
                    border_radius="md",
                    margin_bottom="0.5rem",
                ),
            ),
            # Mensaje actual
            rx.hstack(
                rx.avatar(name=message["user"], size="2"),
                rx.vstack(
                    rx.text(message["user"], weight="bold", font_size="0.9em"),
                    rx.text(message["text"], font_size="1em"),
                    align_items="flex-start",
                ),
                rx.spacer(),
                rx.button(
                    "↩ Responder",
                    on_click=lambda: State.set_reply_to(message["id"]),
                    size="1",
                    variant="ghost",
                ),
                spacing="3",
                width="100%",
            ),
        ),
        bg="#F5F5F5",
        padding="1rem",
        border_radius="lg",
        width="100%",
        margin_bottom="0.5rem",
    )


def index() -> rx.Component:
    """Interfaz principal."""
    return rx.container(
        rx.vstack(
            rx.heading("Chatroom Global 💬", size="8", margin_bottom="1rem"),
            # Estado de conexión
            rx.box(
                rx.hstack(
                    rx.text(State.status, font_size="0.9em"),
                    rx.cond(
                        State.status.contains("❌"),
                        rx.button("🔄 Reconectar", on_click=State.reconnect, size="1"),
                    ),
                    justify="between",
                ),
                bg="#F0F9FF",
                padding="0.75rem",
                border_radius="md",
                width="100%",
                margin_bottom="1rem",
            ),
            # Área de mensajes
            rx.box(
                rx.cond(
                    State.messages.length() > 0,
                    rx.foreach(State.messages, message_card),
                    rx.text(
                        "No hay mensajes. ¡Escribe el primero!",
                        color="gray",
                        text_align="center",
                        padding="2rem",
                    ),
                ),
                height="50vh",
                width="100%",
                border="1px solid #CCCCCC",
                border_radius="lg",
                padding="1rem",
                overflow_y="auto",
                margin_bottom="1rem",
            ),
            # Mostrar a quién estamos respondiendo
            rx.cond(
                State.replying_to != "",
                rx.box(
                    rx.hstack(
                        rx.text("Respondiendo a un mensaje", color="gray"),
                        rx.button(
                            "❌ Cancelar",
                            on_click=lambda: State.set_replying_to(""),
                            size="1",
                            variant="ghost",
                        ),
                    ),
                    bg="#EAEAEA",
                    padding="0.5rem",
                    border_radius="md",
                    width="100%",
                ),
            ),
            # Formulario de entrada
            rx.hstack(
                rx.input(
                    placeholder="Tu nombre",
                    value=State.username,
                    on_change=State.set_username,
                    width="30%",
                ),
                rx.input(
                    placeholder="Escribe un mensaje...",
                    value=State.current_message,
                    on_change=State.set_current_message,
                    width="70%",
                ),
                width="100%",
            ),
            rx.button(
                "Enviar Mensaje",
                on_click=State.post_message,
                width="100%",
                margin_top="0.5rem",
                size="3",
            ),
            spacing="4",
            align="center",
            width="100%",
            max_width="800px",
        ),
        padding_top="2rem",
        bg="#EAE7E7",
        min_height="100vh",
    )


# Página de health check
def healthz():
    """Health check endpoint."""
    return rx.text("OK")


# Configuración de la app
app = rx.App()
app.add_page(index, on_load=State.on_load)
app.add_page(healthz, route="/healthz")
