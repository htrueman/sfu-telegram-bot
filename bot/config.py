import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv, find_dotenv


@dataclass
class BaseBot:
    """
    Creates the BaseBot object from environment variables.
    """

    token: str
    admin_ids: list[int]

    @staticmethod
    def from_env():
        """
        Creates the BaseBot object from environment variables.
        """
        load_dotenv(find_dotenv())
        token = os.getenv("BOT_TOKEN")
        admin_ids = eval(os.getenv("ADMINS"))
        return BaseBot(token=token, admin_ids=admin_ids)


@dataclass
class Miscellaneous:
    """
    Miscellaneous configuration class.

    This class holds settings for various other parameters.
    It merely serves as a placeholder for settings that are not part of other categories.

    Attributes
    ----------
    other_params : str, optional
        A string used to hold other various parameters as required (default is None).
    """

    other_params: Optional[str] = None


@dataclass
class Config:
    """
    The main configuration class that integrates all the other configuration classes.

    This class holds the other configuration classes, providing a centralized point of access for all settings.

    Attributes
    ----------
    base_bot : BaseBot
        Holds the settings related to the Telegram Bot.
    misc : Miscellaneous
        Holds the values for miscellaneous settings.
    """

    base_bot: BaseBot
    misc: Miscellaneous


def load_config() -> Config:
    """
    It reads environment variables from a .env file if provided, else from the process environment.
    :return: Config object with attributes set as per environment variables.
    """

    return Config(
        base_bot=BaseBot.from_env(),
        misc=Miscellaneous(),
    )
