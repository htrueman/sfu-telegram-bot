from typing import List
from aiogram import Bot, Dispatcher
from .config import load_config, Config
from .handlers import routers_list
from .middlewares.config import ConfigMiddleware
from .services import broadcaster


class ZipperBot:
    @staticmethod
    async def __on_startup(bot: Bot, admin_ids: List[int]) -> None:
        await broadcaster.broadcast(bot, admin_ids, "Bot started!")

    @staticmethod
    def __register_global_middlewares(dp: Dispatcher, config: Config) -> None:
        """
        Register global middlewares for the given dispatcher.
        Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

        :param dp: The dispatcher instance.
        :type dp: Dispatcher
        :param config: The configuration object from the loaded configuration.
        :return: None
        """
        middleware_types = [
            ConfigMiddleware(config),
        ]

        for middleware_type in middleware_types:
            dp.message.outer_middleware(middleware_type)
            dp.callback_query.outer_middleware(middleware_type)

    async def start(self) -> None:
        config = load_config()

        bot = Bot(token=config.base_bot.token, parse_mode="HTML")
        dp = Dispatcher()

        dp.include_routers(*routers_list)

        self.__register_global_middlewares(dp, config)

        # await self.__on_startup(bot, config.base_bot.admin_ids)  # Uncomment to enable broadcaster
        await dp.start_polling(bot)
