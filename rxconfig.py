import reflex as rx

config = rx.Config(
    app_name="Chatroom_Reflex",
    api_url="https://chatroom-reflex.onrender.com",
    deploy_url="https://chatroom-reflex.onrender.com",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
