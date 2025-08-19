import reflex as rx
import os

config = rx.Config(
    app_name="Chatroom_Reflex",
    env=rx.Env.PROD,  # Cambiamos a producción
    backend_port=8000,
    frontend_port=3000,
    api_url="/",
    db_url="",  # No necesitamos base de datos SQL
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
