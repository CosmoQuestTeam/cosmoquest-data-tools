import click

from datetime import datetime

from pony.orm import db_session

# Most imports are performed within specific commands to avoid importing everything when running individual commands


class CLIError(BaseException):
    pass


@click.command()
@click.option("--application", default="moon_mappers")
@click.option("--name", default=datetime.now().strftime("%Y%m%d%H%M"))
@click.option('--count', default=200)
@db_session
def download_images(application, name, count):
    import cosmoquest_data_tools.models.cosmoquest_legacy as models
    import concurrent.futures
    import os

    application = models.Application.get(name=application)

    if application is None:
        raise CLIError(f"Invalid Application'")

    images = application.images.random(count)[:]
    image_urls = [image.file_location for image in images]

    print(f"Preparing to download {len(image_urls)} images from '{application.name}'...")

    if not os.path.isdir("data/image_sets"):
        os.mkdir("data/image_sets")

    download_path = f"data/image_sets/{name}"
    os.mkdir(download_path)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = list()

        for image_url in image_urls:
            file_name = "_".join(image_url.split("/")[-3:])
            futures.append(executor.submit(_download_image, image_url, download_path, file_name))

        for future in concurrent.futures.as_completed(futures):
            pass


@click.command()
@click.option("--environment", default="development")
def web(environment):
    import time

    if environment not in ["development", "production"]:
        print(f"Invalid environment '{environment}'. Assuming 'development'...")
        environment = "development"

    print(f"Web Application starting with environment '{environment}'...")

    _start_crossbar()
    time.sleep(5)
    _start_api_component()
    _start_frontend(environment)

    print("Started! Press CTRL+C to stop...")

    while True:
        time.sleep(0.1)  # Keep running, don't peg the CPU...


def _download_image(image_url, file_path, file_name):
    import requests

    print(f"Downloading '{image_url}'...")

    with open(f"{file_path}/{file_name}", "wb") as f:
        response = requests.get(image_url)
        f.write(response.content)


def _start_crossbar():
    import subprocess
    import shlex
    import os

    print("Launching Crossbar router...")

    crossbar_command = "crossbar start --config config/crossbar.json"

    # Crossbar seems to catch the CTRL-C WITHOUT signal handling for the subprocess ¯\_(ツ)_/¯
    FNULL = open(os.devnull, "w")
    subprocess.Popen(shlex.split(crossbar_command), stdout=FNULL, stderr=subprocess.STDOUT)
    FNULL.close()


def _start_api_component():
    import subprocess
    import shlex
    import os
    import signal
    import atexit
    import time

    print("Launching API WAMP Component...")

    wamp_component_command = "python -m cosmoquest_data_tools.wamp_components.api_component"

    FNULL = open(os.devnull, "w")
    wamp_component_process = subprocess.Popen(shlex.split(wamp_component_command), shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    FNULL.close()

    def handle_signal(signum=15, frame=None, do_exit=True):
        if wamp_component_process is not None and signum == 15:
            if wamp_component_process.poll() is None:
                wamp_component_process.send_signal(signum)
                time.sleep(1)
                exit()

    signal.signal(signal.SIGTERM, handle_signal)
    atexit.register(handle_signal, 15, None, False)


def _start_frontend(environment):
    import subprocess
    import shlex
    import os
    import signal
    import atexit
    import time

    print("Launching Frontend...")

    if environment == "development":
        npm_script_command = "cd web && npm start"
    elif environment == "production":
        npm_script_command = "cd web && npm start"  # TODO: Serve built app with Python

    FNULL = open(os.devnull, "w")
    npm_script_process = subprocess.Popen(shlex.split(npm_script_command), shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    FNULL.close()

    def handle_signal(signum=15, frame=None, do_exit=True):
        if npm_script_process is not None and signum == 15:
            if npm_script_process.poll() is None:
                npm_script_process.send_signal(signum)
                time.sleep(1)
                exit()

    signal.signal(signal.SIGTERM, handle_signal)
    atexit.register(handle_signal, 15, None, False)


@click.group()
def cli():
    pass


cli.add_command(download_images)
cli.add_command(web)

if __name__ == '__main__':
    cli()
