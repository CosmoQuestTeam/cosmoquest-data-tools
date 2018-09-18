import asyncio

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp import auth

from cosmoquest_data_tools.config import config


class APIComponent:
    @classmethod
    def run(cls):
        print(f"Starting {cls.__name__}...")

        url = f"ws://{config['crossbar']['host']}:{config['crossbar']['port']}"

        runner = ApplicationRunner(url=url, realm=config["crossbar"]["realm"])
        runner.run(APIWAMPComponent)


class APIWAMPComponent(ApplicationSession):
    def __init__(self, c=None):
        super().__init__(c)

    def onConnect(self):
        self.join(config["crossbar"]["realm"], ["wampcra"], config["crossbar"]["auth"]["username"])

    def onDisconnect(self):
        print("Disconnected from Crossbar!")

    def onChallenge(self, challenge):
        secret = config["crossbar"]["auth"]["password"]
        signature = auth.compute_wcs(secret.encode("utf-8"), challenge.extra["challenge"].encode("utf-8"))

        return signature.decode("ascii")

    async def onJoin(self, details):

        def foo():
            return {"foo": "bar"}

        await self.register(foo, f"{config['crossbar']['realm']}.foo", options=RegisterOptions(invoke="roundrobin"))


if __name__ == "__main__":
    APIComponent.run()
