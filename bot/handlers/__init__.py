from .start_handler import admin_router, user_router
from .file_handler import file_router
# from .user_start_handler import user_router
from .zip_handler import zip_router
from .echo_handler import echo_router

routers_list = [
    admin_router,
    user_router,
    zip_router,
    file_router,
    echo_router,
]

__all__ = [
    "routers_list",
]
