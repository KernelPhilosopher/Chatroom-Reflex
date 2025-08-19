import reflex as rx
import os

# Determinar el entorno
is_prod = os.getenv("REFLEX_ENV") == "prod"

# Configurar URLs basadas en el entorno
base_url = (
    "https://chatroom-reflex.onrender.com" if is_prod else "http://localhost:3000"
)

config = rx.Config(
    app_name="chatroom_reflex",  # cambiado a minúsculas y underscore
    api_url=base_url,
    deploy_url=base_url,
    frontend_path="frontend",
    backend_port=8000,
    frontend_port=3000,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    db_url="",  # No necesitamos base de datos SQL
    env=rx.Env.PROD if is_prod else rx.Env.DEV,
)
