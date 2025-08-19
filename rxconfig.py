import reflex as rx
import os

# Configuración básica
config = rx.Config(
    app_name="Chatroom_Reflex",
    env=rx.Env.DEV,  # Configuración por defecto para desarrollo
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    db_url="",  # No necesitamos base de datos SQL
)
