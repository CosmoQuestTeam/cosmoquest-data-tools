import asyncio

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp import auth

from cosmoquest_data_tools.config import config

from cosmoquest_data_tools.annotation_library import AnnotationLibrary


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

        def list_annotation_libraries():
            annotation_libraries = AnnotationLibrary.discover("data")
            return {"annotation_libraries": [al.as_json_minimal() for al in annotation_libraries]}

        await self.register(list_annotation_libraries, f"{config['crossbar']['realm']}.list_annotation_libraries", options=RegisterOptions(invoke="roundrobin"))


if __name__ == "__main__":
    APIComponent.run()
