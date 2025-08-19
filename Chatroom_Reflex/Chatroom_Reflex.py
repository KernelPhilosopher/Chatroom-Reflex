# Chatroom_Reflex.py
import reflex as rx
from .db_manager import db
from typing import List, Dict

# Colores y variables mejoradas con mejor contraste
theme = {
    "colors": {
        "bg": {
            "base": "#0B141A",
            "darker": "#0a1014",
            "dark": "#111b21",
            "message": "#202c33",
            "hover": "#2a3942",
            "input": "#2a3942",
            "accent": "#00a884",
            "accent_hover": "#00856a",
            "accent_light": "rgba(0, 168, 132, 0.1)",
            "border": "#3c4043",
            "reply": "#1f2937",
        },
        "text": {
            "primary": "#e9edef",
            "secondary": "#8696a0",
            "accent": "#00a884",
            "muted": "#6b7280",
            "error": "#ef4444",
        },
    },
    "fonts": {
        "body": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
    },
    "shadows": {
        "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    },
    "breakpoints": {
        "sm": "640px",
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
    },
}

# Estilo base mejorado
base_style = {
    "font_family": theme["fonts"]["body"],
    "background": theme["colors"]["bg"]["base"],
    "color": theme["colors"]["text"]["primary"],
    "min_height": "100vh",
    "display": "flex",
    "flex_direction": "column",
    "-webkit-font_smoothing": "antialiased",
    "-moz-osx-font_smoothing": "grayscale",
}

# Estilos mejorados y más responsivos
chat_styles = {
    "page_container": {
        "width": "100%",
        "min_height": "100vh",
        "height": "100vh",
        "background": theme["colors"]["bg"]["base"],
        "display": "flex",
        "justify_content": "center",
        "align_items": "center",
        "padding": "0",
        "position": "relative",
        "overflow": "hidden",
        # Responsive backgrounds
        "@media (max-width: 767px)": {
            "background": theme["colors"]["bg"]["base"],
            "align_items": "stretch",
        },
        "@media (min-width: 768px)": {
            "background": f"linear-gradient(135deg, {theme['colors']['bg']['darker']} 0%, #1a2830 50%, {theme['colors']['bg']['base']} 100%)",
            "padding": "1rem",
        },
    },
    "chat_container": {
        "width": "100%",
        "height": "100vh",
        "background": theme["colors"]["bg"]["dark"],
        "display": "flex",
        "flex_direction": "column",
        "position": "relative",
        "overflow": "hidden",
        "border": "none",
        # Responsive container
        "@media (max-width: 767px)": {
            "height": "100vh",
            "border_radius": "0",
        },
        "@media (min-width: 768px)": {
            "width": "90%",
            "max_width": "1200px",
            "height": "95vh",
            "border_radius": "1rem",
            "box_shadow": theme["shadows"]["xl"],
            "border": f"1px solid {theme['colors']['bg']['border']}",
        },
        "@media (min-width: 1024px)": {
            "width": "85%",
            "height": "90vh",
            "border_radius": "1.5rem",
        },
    },
    "header": {
        "width": "100%",
        "background": theme["colors"]["bg"]["message"],
        "border_bottom": f"1px solid {theme['colors']['bg']['border']}",
        "padding": "1rem 1.25rem",
        "display": "flex",
        "align_items": "center",
        "justify_content": "space-between",
        "backdrop_filter": "blur(10px)",
        "z_index": "10",
        "position": "sticky",
        "top": "0",
        # Safe area para móviles con notch
        "padding_top": "max(1rem, env(safe-area-inset-top))",
        "@media (min-width: 768px)": {
            "padding": "1.5rem 2rem",
            "background": theme["colors"]["bg"]["message"],
        },
    },
    "header_title": {
        "font_size": "1.5rem",
        "font_weight": "600",
        "margin": "0",
        "color": theme["colors"]["text"]["primary"],
        "display": "flex",
        "align_items": "center",
        "gap": "0.5rem",
        "@media (min-width: 768px)": {
            "font_size": "1.75rem",
        },
    },
    "status_badge": {
        "display": "flex",
        "align_items": "center",
        "gap": "0.5rem",
        "font_size": "0.9rem",
        "color": theme["colors"]["text"]["secondary"],
        "background": theme["colors"]["bg"]["hover"],
        "padding": "0.5rem 1rem",
        "border_radius": "2rem",
        "box_shadow": theme["shadows"]["sm"],
        "transition": "all 0.2s ease",
        "border": f"1px solid {theme['colors']['bg']['border']}",
        "@media (max-width: 767px)": {
            "font_size": "0.8rem",
            "padding": "0.4rem 0.8rem",
        },
        "_hover": {
            "transform": "translateY(-1px)",
            "box_shadow": theme["shadows"]["md"],
        },
    },
    "messages_area": {
        "flex": "1",
        "overflow_y": "auto",
        "overflow_x": "hidden",
        "padding": "1.5rem",
        "background": theme["colors"]["bg"]["dark"],
        "display": "flex",
        "flex_direction": "column",
        "gap": "1rem",
        "scroll_behavior": "smooth",
        "@media (max-width: 767px)": {
            "padding": "1rem",
            "gap": "0.75rem",
        },
        "@media (min-width: 1024px)": {
            "padding": "2rem",
        },
        # Improved scrollbar styling
        "&::-webkit-scrollbar": {
            "width": "6px",
        },
        "&::-webkit-scrollbar-track": {
            "background": "transparent",
        },
        "&::-webkit-scrollbar-thumb": {
            "background": theme["colors"]["bg"]["hover"],
            "border_radius": "3px",
            "_hover": {
                "background": theme["colors"]["bg"]["border"],
            },
        },
        # Firefox scrollbar
        "scrollbar_width": "thin",
        "scrollbar_color": f"{theme['colors']['bg']['hover']} transparent",
    },
    "message_card": {
        "background": theme["colors"]["bg"]["message"],
        "border_radius": "1rem",
        "padding": "1.25rem",
        "max_width": "80%",
        "width": "fit-content",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "box_shadow": theme["shadows"]["sm"],
        "border": f"1px solid {theme['colors']['bg']['border']}",
        "position": "relative",
        "@media (max-width: 767px)": {
            "border_radius": "0.875rem",
            "padding": "1rem",
            "max_width": "90%",
        },
        "@media (min-width: 1024px)": {
            "max_width": "65%",
        },
        "_hover": {
            "background": theme["colors"]["bg"]["hover"],
            "transform": "translateY(-2px)",
            "box_shadow": theme["shadows"]["md"],
        },
        # Improved focus states for accessibility
        "_focus_within": {
            "outline": f"2px solid {theme['colors']['bg']['accent']}",
            "outline_offset": "2px",
        },
    },
    "reply_indicator": {
        "background": theme["colors"]["bg"]["reply"],
        "padding": "0.75rem",
        "border_radius": "0.5rem",
        "margin_bottom": "0.75rem",
        "border_left": f"3px solid {theme['colors']['bg']['accent']}",
        "position": "relative",
        "_before": {
            "content": "''",
            "position": "absolute",
            "left": "-3px",
            "top": "0",
            "height": "100%",
            "width": "3px",
            "background": theme["colors"]["bg"]["accent"],
        },
    },
    "input_area": {
        "width": "100%",
        "background": theme["colors"]["bg"]["message"],
        "padding": "1.25rem",
        "border_top": f"1px solid {theme['colors']['bg']['border']}",
        "backdrop_filter": "blur(10px)",
        # Safe area para móviles
        "padding_bottom": "max(1rem, env(safe-area-inset-bottom))",
        "@media (min-width: 768px)": {
            "padding": "1.5rem 2rem",
        },
    },
    "input_container": {
        "display": "flex",
        "flex_direction": "column",
        "gap": "1rem",
        "width": "100%",
        "@media (min-width: 1024px)": {
            "flex_direction": "row",
        },
    },
    "input_style": {
        "background": theme["colors"]["bg"]["input"],
        "color": theme["colors"]["text"]["primary"],
        "border": f"2px solid {theme['colors']['bg']['border']}",
        "border_radius": "0.75rem",
        "padding": "0.875rem 1.25rem",
        "font_size": "1rem",
        "transition": "all 0.2s ease",
        "font_family": theme["fonts"]["body"],
        "@media (max-width: 767px)": {
            "border_radius": "0.5rem",
            "padding": "0.75rem 1rem",
        },
        "_placeholder": {
            "color": theme["colors"]["text"]["secondary"],
            "font_size": "0.95rem",
        },
        "_focus": {
            "background": theme["colors"]["bg"]["hover"],
            "border_color": theme["colors"]["bg"]["accent"],
            "box_shadow": f"0 0 0 3px {theme['colors']['bg']['accent_light']}",
            "outline": "none",
        },
        # High contrast mode support
        "@media (prefers-contrast: high)": {
            "border_width": "3px",
        },
    },
    "username_input": {
        "flex": "1",
        "min_width": "0",
        "@media (min-width: 1024px)": {
            "flex": "0 0 30%",
        },
    },
    "message_input": {
        "flex": "1",
        "min_width": "0",
        "@media (min-width: 1024px)": {
            "flex": "0 0 70%",
        },
    },
    "button_style": {
        "background": theme["colors"]["bg"]["accent"],
        "color": "white",
        "padding": "0.875rem 2rem",
        "border_radius": "0.75rem",
        "font_weight": "600",
        "font_size": "1rem",
        "letter_spacing": "0.025em",
        "transition": "all 0.2s ease",
        "box_shadow": theme["shadows"]["sm"],
        "border": "none",
        "cursor": "pointer",
        "width": "100%",
        "min_width": "fit-content",
        "@media (max-width: 767px)": {
            "padding": "0.75rem 1.5rem",
            "border_radius": "0.5rem",
            "font_size": "0.95rem",
        },
        "@media (min-width: 1024px)": {
            "width": "auto",
        },
        "_hover": {
            "background": theme["colors"]["bg"]["accent_hover"],
            "transform": "translateY(-2px)",
            "box_shadow": theme["shadows"]["md"],
        },
        "_active": {
            "transform": "translateY(-1px)",
            "box_shadow": theme["shadows"]["sm"],
        },
        "_disabled": {
            "background": theme["colors"]["text"]["muted"],
            "cursor": "not-allowed",
            "transform": "none",
        },
        # Focus for accessibility
        "_focus": {
            "outline": f"2px solid {theme['colors']['text']['primary']}",
            "outline_offset": "2px",
        },
    },
    "empty_state": {
        "display": "flex",
        "flex_direction": "column",
        "align_items": "center",
        "justify_content": "center",
        "padding": "3rem",
        "text_align": "center",
        "height": "100%",
        "min_height": "300px",
        "@media (max-width: 767px)": {
            "padding": "2rem",
        },
        "@media (min-width: 1024px)": {
            "padding": "4rem",
        },
    },
    "reply_banner": {
        "background": theme["colors"]["bg"]["reply"],
        "padding": "0.75rem 1rem",
        "border_bottom": f"1px solid {theme['colors']['bg']['border']}",
        "display": "flex",
        "align_items": "center",
        "gap": "0.5rem",
        "animation": "slideDown 0.3s ease-out",
    },
}

# Keyframes para animaciones
keyframes_style = """
@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes messageSlide {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
"""


class State(rx.State):
    """El estado de la aplicación."""

    username: str = ""
    current_message: str = ""
    messages: List[Dict[str, str]] = []
    status: str = "Cargando..."
    replying_to: str = ""
    is_loading: bool = False
    error_message: str = ""

    def on_load(self):
        """Cargar mensajes al iniciar."""
        self.load_messages()

    def load_messages(self):
        """Cargar mensajes desde Neo4j."""
        self.is_loading = True
        self.error_message = ""

        try:
            if db.driver is None:
                self.status = "❌ Sin conexión a la base de datos"
                self.messages = []
                return

            result = db.get_messages_with_replies()
            self.messages = result if result else []

            # Actualizar estado con información más detallada
            self.status = "✅ Conectado"

        except Exception as e:
            print(f"Error al cargar mensajes: {e}")
            self.messages = []
            self.status = "❌ Error de conexión"
            self.error_message = "No se pudieron cargar los mensajes"
        finally:
            self.is_loading = False

    def post_message(self):
        """Enviar un nuevo mensaje."""
        # Validación mejorada
        if not self.username.strip():
            self.error_message = "Por favor, ingresa tu nombre"
            return

        if not self.current_message.strip():
            self.error_message = "El mensaje no puede estar vacío"
            return

        if db.driver is None:
            self.status = "❌ Sin conexión a la base de datos"
            self.error_message = "No hay conexión con el servidor"
            return

        self.is_loading = True
        self.error_message = ""

        try:
            # Generar ID único
            import uuid

            message_id = f"msg_{uuid.uuid4()}"

            # Crear el mensaje
            result = db.create_message(
                message_id=message_id,
                user=self.username.strip(),
                text=self.current_message.strip(),
                reply_to=self.replying_to if self.replying_to else None,
            )

            if result is not None:
                self.current_message = ""
                self.replying_to = ""
                self.load_messages()
            else:
                self.error_message = "Error al enviar el mensaje"

        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
            self.status = "❌ Error al enviar"
            self.error_message = "No se pudo enviar el mensaje"
        finally:
            self.is_loading = False

    def reconnect(self):
        """Intentar reconectar."""
        self.is_loading = True
        self.error_message = ""
        try:
            db._connect()
            self.load_messages()
        except Exception as e:
            self.error_message = "Error al intentar reconectar"
        finally:
            self.is_loading = False

    def set_reply_to(self, message_id: str):
        """Establecer a qué mensaje se está respondiendo."""
        self.replying_to = message_id

    def clear_reply(self):
        """Limpiar respuesta."""
        self.replying_to = ""

    def clear_error(self):
        """Limpiar mensaje de error."""
        self.error_message = ""


def message_card(message: Dict) -> rx.Component:
    """Componente de tarjeta de mensaje mejorado."""
    is_reply = message.get("parent_user") is not None

    return rx.box(
        rx.vstack(
            # Indicador de respuesta mejorado
            rx.cond(
                is_reply,
                rx.box(
                    rx.hstack(
                        rx.icon(
                            "corner-down-right",
                            size=16,
                            color=theme["colors"]["text"]["secondary"],
                        ),
                        rx.text(
                            f"{message['parent_user']}: {message.get('parent_text', '')[:50]}...",
                            font_size="0.8em",
                            color=theme["colors"]["text"]["secondary"],
                            font_style="italic",
                            overflow="hidden",
                            text_overflow="ellipsis",
                            white_space="nowrap",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    style=chat_styles["reply_indicator"],
                ),
            ),
            # Contenido principal del mensaje
            rx.hstack(
                rx.avatar(
                    name=message["user"],
                    size="3",
                    bg=theme["colors"]["bg"]["accent"],
                    color="white",
                    font_weight="bold",
                ),
                rx.vstack(
                    rx.text(
                        message["user"],
                        font_weight="600",
                        color=theme["colors"]["text"]["accent"],
                        font_size="0.9em",
                        margin_bottom="0.25rem",
                    ),
                    rx.text(
                        message["text"],
                        color=theme["colors"]["text"]["primary"],
                        font_size="0.95em",
                        line_height="1.4",
                        word_wrap="break-word",
                    ),
                    align_items="flex-start",
                    spacing="1",
                    width="100%",
                    min_width="0",
                ),
                spacing="3",
                width="100%",
                align_items="flex-start",
            ),
            # Botón de responder (mejorado para móviles)
            rx.button(
                rx.hstack(
                    rx.icon("arrow_left", size=14),
                    rx.text("Responder", display=["none", "inline"]),
                    spacing="1",
                ),
                on_click=lambda: State.set_reply_to(message["id"]),
                variant="ghost",
                color=theme["colors"]["text"]["secondary"],
                size="1",
                position="absolute",
                right="0.5rem",
                top="0.5rem",
                opacity="0",
                transition="all 0.2s ease",
                _group_hover={"opacity": "1"},
                _hover={
                    "background": theme["colors"]["bg"]["hover"],
                    "color": theme["colors"]["text"]["accent"],
                },
                # Accessibility improvements
                aria_label=f"Responder al mensaje de {message['user']}",
            ),
            spacing="2",
            position="relative",
            width="100%",
        ),
        style={
            **chat_styles["message_card"],
            "animation": "messageSlide 0.3s ease-out",
        },
        role="article",
        aria_label=f"Mensaje de {message['user']}",
        class_name="group",  # Para el hover del botón
    )


def empty_state() -> rx.Component:
    """Estado vacío mejorado."""
    return rx.vstack(
        rx.icon(
            "message_circle",
            size=48,
            color=theme["colors"]["text"]["secondary"],
        ),
        rx.text(
            "¡Bienvenido al chat!",
            font_size="1.5rem",
            font_weight="600",
            color=theme["colors"]["text"]["primary"],
            text_align="center",
        ),
        rx.text(
            "No hay mensajes aún. Sé el primero en escribir algo.",
            font_size="1rem",
            color=theme["colors"]["text"]["secondary"],
            text_align="center",
            max_width="300px",
        ),
        style=chat_styles["empty_state"],
    )


def reply_banner() -> rx.Component:
    """Banner de respuesta mejorado."""
    return rx.box(
        rx.hstack(
            rx.icon(
                "reply",
                size=18,
                color=theme["colors"]["text"]["accent"],
            ),
            rx.text(
                "Respondiendo a un mensaje",
                color=theme["colors"]["text"]["secondary"],
                font_size="0.9rem",
                font_weight="500",
            ),
            rx.spacer(),
            rx.button(
                rx.icon("x", size=16),
                on_click=State.clear_reply,
                variant="ghost",
                size="1",
                color=theme["colors"]["text"]["secondary"],
                _hover={"color": theme["colors"]["text"]["primary"]},
                aria_label="Cancelar respuesta",
            ),
            spacing="2",
            align_items="center",
            width="100%",
        ),
        style=chat_styles["reply_banner"],
    )


def error_banner() -> rx.Component:
    """Banner de error."""
    return rx.cond(
        State.error_message != "",
        rx.box(
            rx.hstack(
                rx.icon("info", size=18, color=theme["colors"]["text"]["error"]),
                rx.text(
                    State.error_message,
                    color=theme["colors"]["text"]["error"],
                    font_size="0.9rem",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("x", size=16),
                    on_click=State.clear_error,
                    variant="ghost",
                    size="1",
                    color=theme["colors"]["text"]["error"],
                    aria_label="Cerrar error",
                ),
                spacing="2",
                align_items="center",
                width="100%",
            ),
            background=theme["colors"]["text"]["error"],
            color="white",
            padding="0.75rem 1rem",
            border_radius="0.5rem",
            margin_bottom="0.5rem",
        ),
    )


def index() -> rx.Component:
    """Página principal mejorada."""
    return rx.fragment(
        # Estilos globales
        rx.html(
            f"<style>{keyframes_style}</style>",
        ),
        rx.box(
            rx.box(
                # Contenedor principal del chat
                rx.box(
                    # Encabezado
                    rx.box(
                        rx.hstack(
                            rx.hstack(
                                rx.text("💬", font_size="1.5rem"),
                                rx.text(
                                    "Chatroom Global", style=chat_styles["header_title"]
                                ),
                                spacing="2",
                                align_items="center",
                            ),
                            rx.box(
                                rx.text(
                                    State.status,
                                    margin="0",
                                ),
                                style=chat_styles["status_badge"],
                            ),
                            width="100%",
                            justify="between",
                            align_items="center",
                        ),
                        style=chat_styles["header"],
                    ),
                    # Banner de error
                    error_banner(),
                    # Banner de respuesta
                    rx.cond(
                        State.replying_to != "",
                        reply_banner(),
                    ),
                    # Área de mensajes
                    rx.box(
                        rx.cond(
                            State.messages,
                            rx.foreach(
                                State.messages,
                                message_card,
                            ),
                            empty_state(),
                        ),
                        style=chat_styles["messages_area"],
                        role="log",
                        aria_label="Mensajes del chat",
                        aria_live="polite",
                    ),
                    # Área de entrada
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.input(
                                    placeholder="Tu nombre",
                                    value=State.username,
                                    on_change=State.set_username,
                                    style={
                                        **chat_styles["input_style"],
                                        **chat_styles["username_input"],
                                    },
                                    aria_label="Nombre de usuario",
                                    required=True,
                                ),
                                rx.input(
                                    placeholder="Escribe tu mensaje...",
                                    value=State.current_message,
                                    on_change=State.set_current_message,
                                    style={
                                        **chat_styles["input_style"],
                                        **chat_styles["message_input"],
                                    },
                                    aria_label="Mensaje",
                                    required=True,
                                ),
                                style=chat_styles["input_container"],
                            ),
                            rx.button(
                                rx.cond(
                                    State.is_loading,
                                    rx.hstack(
                                        rx.spinner(size="3", color="white"),
                                        rx.text("Enviando..."),
                                        spacing="2",
                                    ),
                                    rx.hstack(
                                        rx.icon("arrow_right", size=18),
                                        rx.text("Enviar Mensaje"),
                                        spacing="2",
                                    ),
                                ),
                                on_click=State.post_message,
                                disabled=State.is_loading,
                                style=chat_styles["button_style"],
                                aria_label="Enviar mensaje",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        style=chat_styles["input_area"],
                    ),
                    style=chat_styles["chat_container"],
                ),
                style=chat_styles["page_container"],
            ),
            style=base_style,
        ),
    )


# Página de health check
def healthz():
    """Health check endpoint."""
    return rx.text("OK")


# Configuración de la app mejorada
app = rx.App(
    style=base_style,
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
    # Mejoras para SEO y accesibilidad
    head_components=[
        rx.html(
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">'
        ),
        rx.html('<meta name="theme-color" content="#00a884">'),
        rx.html(
            '<meta name="description" content="Chat en tiempo real - Conecta con personas de todo el mundo">'
        ),
    ],
)

app.add_page(
    index, on_load=State.on_load, title="Chatroom Global - Chat en Tiempo Real"
)
app.add_page(healthz, route="/healthz")
