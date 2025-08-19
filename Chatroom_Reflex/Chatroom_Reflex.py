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
                        font_size=["0.7em", "0.8em"],
                        color="gray.600",
                        font_style="italic",
                    ),
                    padding=["0.3rem", "0.5rem"],
                    bg="rgba(234, 234, 234, 0.7)",
                    border_radius="md",
                    margin_bottom="0.5rem",
                    width="100%",
                ),
            ),
            # Mensaje actual
            rx.hstack(
                rx.avatar(
                    name=message["user"],
                    size=["1", "2"],
                    bg="blue.500",
                ),
                rx.vstack(
                    rx.text(
                        message["user"],
                        weight="bold",
                        font_size=["0.8em", "0.9em"],
                        color="gray.800",
                    ),
                    rx.text(
                        message["text"],
                        font_size=["0.9em", "1em"],
                        color="gray.700",
                    ),
                    align_items="flex-start",
                ),
                rx.spacer(),
                rx.button(
                    "↩ Responder",
                    on_click=lambda: State.set_reply_to(message["id"]),
                    size="1",
                    variant="ghost",
                    color="blue.500",
                    _hover={"bg": "blue.50"},
                ),
                spacing=["2", "3"],
                width="100%",
            ),
        ),
        bg="white",
        padding=["0.75rem", "1rem"],
        border_radius="lg",
        width="100%",
        margin_bottom="0.5rem",
        box_shadow="0 1px 3px rgba(0,0,0,0.12)",
        _hover={"box_shadow": "0 2px 4px rgba(0,0,0,0.15)"},
    )


def index() -> rx.Component:
    """Interfaz principal."""
    return rx.box(
        rx.container(
            rx.vstack(
                rx.heading(
                    "Chatroom Global 💬",
                    size=["6", "8"],
                    margin_bottom="1rem",
                    background="linear-gradient(135deg, #2563EB, #1D4ED8)",
                    background_clip="text",
                    padding=["0.5rem", "1rem"],
                ),
                # Estado de conexión
                rx.box(
                    rx.hstack(
                        rx.text(
                            State.status,
                            font_size=["0.8em", "0.9em"],
                            color="gray.700",
                        ),
                        rx.cond(
                            State.status.contains("❌"),
                            rx.button(
                                "🔄 Reconectar",
                                on_click=State.reconnect,
                                size="1",
                                color_scheme="blue",
                            ),
                        ),
                        justify="between",
                    ),
                    bg="blue.50",
                    padding=["0.5rem", "0.75rem"],
                    border_radius="md",
                    width="100%",
                    margin_bottom="1rem",
                    border="1px solid",
                    border_color="blue.100",
                ),
                # Área de mensajes
                rx.box(
                    rx.cond(
                        State.messages.length() > 0,
                        rx.foreach(State.messages, message_card),
                        rx.text(
                            "No hay mensajes. ¡Escribe el primero!",
                            color="gray.500",
                            text_align="center",
                            padding="2rem",
                            font_size=["0.9em", "1em"],
                        ),
                    ),
                    height=["60vh", "50vh"],
                    width="100%",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="lg",
                    padding=["0.75rem", "1rem"],
                    overflow_y="auto",
                    margin_bottom="1rem",
                    bg="gray.50",
                ),
                # Área de respuesta
                rx.cond(
                    State.replying_to != "",
                    rx.box(
                        rx.hstack(
                            rx.text(
                                "Respondiendo a un mensaje",
                                color="gray.600",
                                font_size=["0.8em", "0.9em"],
                            ),
                            rx.button(
                                "❌ Cancelar",
                                on_click=lambda: State.set_replying_to(""),
                                size="1",
                                variant="ghost",
                                color="red.500",
                            ),
                        ),
                        bg="gray.100",
                        padding=["0.4rem", "0.5rem"],
                        border_radius="md",
                        width="100%",
                    ),
                ),
                # Formulario de entrada
                rx.vstack(
                    rx.hstack(
                        rx.input(
                            placeholder="Tu nombre",
                            value=State.username,
                            on_change=State.set_username,
                            width=["100%", "30%"],
                            bg="white",
                            border_color="gray.300",
                            _hover={"border_color": "blue.500"},
                        ),
                        rx.input(
                            placeholder="Escribe un mensaje...",
                            value=State.current_message,
                            on_change=State.set_current_message,
                            width=["100%", "70%"],
                            bg="white",
                            border_color="gray.300",
                            _hover={"border_color": "blue.500"},
                        ),
                        width="100%",
                        flex_direction=["column", "row"],
                        spacing=["2", "3"],
                    ),
                    rx.button(
                        "Enviar Mensaje",
                        on_click=State.post_message,
                        width="100%",
                        margin_top="0.5rem",
                        size="3",
                        bg="blue.500",
                        color="white",
                        _hover={"bg": "blue.600"},
                    ),
                    width="100%",
                ),
                spacing="4",
                align="center",
                width="100%",
                max_width="800px",
            ),
            padding=["1rem", "2rem"],
            width="100%",
        ),
        bg="gray.100",
        min_height="100vh",
        padding_y="2rem",
    )


# Página de health check
def healthz():
    """Health check endpoint."""
    return rx.text("OK")


# Configuración de la app
app = rx.App()
app.add_page(index, on_load=State.on_load)
app.add_page(healthz, route="/healthz")
