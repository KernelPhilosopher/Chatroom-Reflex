# Chatroom_Reflex.py
import reflex as rx
from .db_manager import db
from typing import List, Dict

# Estilos personalizados
chat_styles = {
    "chat_container": {
        "background": "#111b21",  # Fondo oscuro estilo WhatsApp Web
        "min_height": "100vh",
        "display": "flex",
        "flex_direction": "column",
        "color": "#e9edef",  # Texto claro para fondo oscuro
    },
    "header": {
        "background": "#202c33",  # Color de encabezado de WhatsApp
        "padding": "1rem",
        "border_bottom": "1px solid #2f3b43",
        "position": "sticky",
        "top": "0",
        "z_index": "100",
    },
    "status_bar": {
        "background": "#005c4b",  # Verde WhatsApp para estados positivos
        "padding": "0.5rem",
        "border_radius": "md",
        "margin_bottom": "0.5rem",
        "font_size": "0.9em",
    },
    "messages_area": {
        "flex": "1",
        "overflow_y": "auto",
        "padding": "1rem",
        "background": "#111b21",
        "display": "flex",
        "flex_direction": "column",
        "gap": "0.5rem",
    },
    "message_card": {
        "background": "#202c33",
        "border_radius": "lg",
        "padding": "0.75rem",
        "max_width": "85%",
        "width": "fit-content",
        "margin": "0.25rem 0",
        "_hover": {"background": "#2a3942"},
    },
    "input_area": {
        "background": "#202c33",
        "padding": "1rem",
        "border_top": "1px solid #2f3b43",
        "position": "sticky",
        "bottom": "0",
        "width": "100%",
    },
    "input_style": {
        "background": "#2a3942",
        "border": "none",
        "color": "#e9edef",
        "padding": "0.75rem",
        "_placeholder": {"color": "#8696a0"},
        "_focus": {"border": "1px solid #00a884"},
    },
    "button_style": {
        "background": "#00a884",  # Verde WhatsApp
        "color": "white",
        "_hover": {"background": "#008f72"},
    },
}


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
    is_reply = message.get("parent_user") is not None
    return rx.box(
        rx.vstack(
            # Respuesta al mensaje original
            rx.cond(
                is_reply,
                rx.box(
                    rx.text(
                        f"↳ {message['parent_user']}: {message['parent_text']}",
                        font_size="0.8em",
                        color="#8696a0",
                        font_style="italic",
                    ),
                    padding="0.5rem",
                    background="#2a3942",
                    border_radius="md",
                    margin_bottom="0.5rem",
                    width="100%",
                ),
            ),
            # Contenido del mensaje
            rx.hstack(
                rx.avatar(
                    name=message["user"],
                    size="3",
                    bg="#00a884",
                    color="white",
                ),
                rx.vstack(
                    rx.text(
                        message["user"],
                        font_weight="bold",
                        color="#00a884",
                        font_size="0.9em",
                    ),
                    rx.text(
                        message["text"],
                        color="#e9edef",
                        font_size="0.95em",
                    ),
                    align_items="flex-start",
                    spacing="2",
                ),
                width="100%",
                spacing="3",
            ),
            # Botón de responder (solo visible en desktop)
            rx.button(
                "↩ Responder",
                on_click=lambda: State.set_reply_to(message["id"]),
                variant="ghost",
                color="#00a884",
                size="1",
                display=["none", "block"],
                position="absolute",
                right="0.5rem",
                top="0.5rem",
                _hover={"background": "#2a3942"},
            ),
            spacing="2",
            position="relative",
        ),
        style=chat_styles["message_card"],
    )


def index() -> rx.Component:
    return rx.box(
        # Encabezado
        rx.box(
            rx.heading(
                "Chatroom Global 💬",
                size="4",
                color="#e9edef",
            ),
            style=chat_styles["header"],
        ),
        # Estado de conexión
        rx.box(
            rx.hstack(
                rx.text(State.status),
                rx.cond(
                    State.status.contains("❌"),
                    rx.button(
                        "🔄 Reconectar",
                        on_click=State.reconnect,
                        size="2",
                        style=chat_styles["button_style"],
                    ),
                ),
                justify="between",
            ),
            style=chat_styles["status_bar"],
        ),
        # Área de mensajes
        rx.box(
            rx.cond(
                State.messages.length() > 0,
                rx.foreach(
                    State.messages,
                    message_card,
                ),
                rx.text(
                    "No hay mensajes. ¡Escribe el primero!",
                    color="#8696a0",
                    text_align="center",
                    padding="2rem",
                ),
            ),
            style=chat_styles["messages_area"],
        ),
        # Área de respuesta
        rx.cond(
            State.replying_to != "",
            rx.box(
                rx.hstack(
                    rx.text(
                        "Respondiendo a un mensaje",
                        color="#8696a0",
                        font_size="0.9em",
                    ),
                    rx.button(
                        "❌",
                        on_click=lambda: State.set_replying_to(""),
                        variant="ghost",
                        color="#ef4444",
                        size="1",
                    ),
                ),
                padding="0.5rem 1rem",
                background="#2a3942",
                border_bottom="1px solid #2f3b43",
            ),
        ),
        # Área de entrada
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="Tu nombre",
                        value=State.username,
                        on_change=State.set_username,
                        width=["100%", "30%"],
                        style=chat_styles["input_style"],
                    ),
                    rx.input(
                        placeholder="Escribe un mensaje...",
                        value=State.current_message,
                        on_change=State.set_current_message,
                        width=["100%", "70%"],
                        style=chat_styles["input_style"],
                    ),
                    spacing="3",
                ),
                rx.button(
                    "Enviar Mensaje",
                    on_click=State.post_message,
                    width="100%",
                    style=chat_styles["button_style"],
                ),
                spacing="3",
                width="100%",
            ),
            style=chat_styles["input_area"],
        ),
        style=chat_styles["chat_container"],
    )


# Página de health check
def healthz():
    """Health check endpoint."""
    return rx.text("OK")


# Configuración de la app
app = rx.App()
app.add_page(index, on_load=State.on_load)
app.add_page(healthz, route="/healthz")
