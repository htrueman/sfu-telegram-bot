import time
from telepot.loop import MessageLoop
from .action_processor import ActionProcessor
from .config import Bot, REQUEST_TIMEOUT


class ZipperBot:
    @staticmethod
    def start() -> None:
        action = ActionProcessor()
        MessageLoop(
            Bot,
            handle={
                "chat": action.on_chat_message,
                "callback_query": action.on_callback_query,
            },
        ).run_as_thread()

        print("Listening ...")
        while True:
            time.sleep(REQUEST_TIMEOUT)
