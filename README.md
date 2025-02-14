# Demo to show how to use Podman

## Pull docker image from docker hub

### Which image to choose 

 
* `python:<version>` - This is the defacto image. If you are unsure about what your needs are, you probably want to use this one. It is designed to be used both as a throw away container (mount your source code and start the container to start your app), as well as the base to build other images off of.

* `python:<version>-slim` - This image does not contain the common Debian packages contained in the default tag and only contains the minimal Debian packages needed to run python. Unless you are working in an environment where only the python image will be deployed and you have space constraints, we highly recommend using the default image of this repository.


* `python:<version>-alpine` - This image is based on the popular Alpine Linux project⁠, available in the alpine official image. Alpine Linux is much smaller than most distribution base images (~5MB), and thus leads to much slimmer images in general.

* `python:<version>-windowsservercore` - This image is based on Windows Server Core (microsoft/windowsservercore). As such, it only works in places which that image does, such as Windows 10 Professional/Enterprise (Anniversary Edition) or Windows Server 2016.

Choose appropriate docker iamge. Generally use slim image. 
`https://hub.docker.com/_/python/`


### Dockerfile
```
FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```



## Basic Commands - Docker vs Podman:
Operation | Docker Commands | Podman Command
|--------| --------| --------|
List of all running containers |	docker ps |		podman ps
List of all containers	 |	docker ps -a	 |	podman ps -a
Run a container	| docker run -it ubuntu bash |	podman run -it ubuntu bash
Stop a container |		docker stop <container_id>	 |	podman stop <container_id>
Remove an image	 |	docker rmi <image_name> |		podman rmi <image_name>
Remove a container	 |	docker rm <container_id> |		podman rm <container_id>
Pull an image |	docker pull <image_name> |		podman pull <image_name>
List images |		docker images	 |	podman images
Tag an image	 |	docker tag <source_image> <target_image> |		podman tag <source_image> <target_image>
Push an image	 |	docker push <image_name>	 |	podman push <image_name>
View logs	 |	docker logs <container_id>	 |	podman logs <container_id>
Execute command inside container	 |	docker exec -it <container_id> bash	 |	podman exec -it <container_id> bash
Inspect a container |		docker inspect <container_id>	 |	podman inspect <container_id>
Version check	 |	docker --version |		podman --version

### Linux Vitual Machine
* Create podman machine `podman machine init`
* Start machine `podman machine start`


Create a container from docker image -
`podman run -d -p 5000:5000 docker.io/digvijaytaunk/simple_flask`

* It is a good practice to remove the container once it is not running. `--rm` — Removes the container once stopped.
`podman run --rm -d -p 5000:5000 <image-name>`

* Remove container `podman rm <ContainerName>`


`podman run --rm --name demo-container -p 5000:5000 -v "${PWD}:/code" -w /code localhost/my-app`

### Podman build command
Run podman build command to build image - `podman build --tag <image-name> .`

`--tag` or `-t` - give name to image.

`.` - use root directory to pick the dockerfile.


## Debug the local code with break point
To enable debugging with breakpoint Install `debugpy` using `pip install debugpy`

To Enable remote debugging on port 5678 (waits for debugger to attach), add this line in `app.py` file.
```
app = Flask(__name__)

# Only enable debugpy in the MAIN process, not in the auto-reloader
if os.environ.get("FLASK_RUN_FROM_CLI") == "true" and not os.environ.get("WERKZEUG_RUN_MAIN"):
    debugpy.listen(("0.0.0.0", 5670))
    print("⚡ Debugger is listening on port 5670. Attach from VS Code!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

* To debug from local machine and auto reload with breakpoint to debug, run the container using below command.
`podman run --rm --name demo-container -p 5000:5000 -p 5670:5670 -v "${PWD}:/code" -w /code -e FLASK_ENV=development -e FLASK_APP=src/app.py localhost/my-app`

#### Flags Explained
* `podman run` - start container
* `--rm` remove container when stopped to clear disk space
* `--name <container_name>` Name of the container to create. It is not advisable to use this flag and let the podman generate the new name to avoid name conflict.
* `-d` Run in detached mode with `-d` flag. Means it will give you the terminal back and the process running in background.
* `-p 5000:5000` port mapping - <External_port>:<internal_port>
* `-v "${PWD}:/code"` used for volume mapping (bind mounting), allowing you to share files between your local machine and the container. `${PWD}` → Expands to the current directory on your host system (windows). Directory mapping between `<source_path>:<destination_path>` or `<local_path>:<container_path>[:options]`. `[options]` → Optional settings like ro (read-only), rw (read-write).
* `-w` sets `/code` as the working directory inside the container.
It means that when the container starts, it will execute commands from /code instead of the default directory (/). This is useful when running commands that rely on relative paths. 
* `-e` used to set environment variables inside the container. Equivalent to: Running `export FLASK_ENV=development` in Linux or `set FLASK_ENV=development` in Windows.
* `localhost/my-app` Image name to use to start container.

#### Configure VS Code Debegger
Add this to "Preference: Open User setting (JSON)" 
```
{
    "dev.containers.dockerPath": "podman",
}
```

Install Dev Container Extension in VS Code. crtl + sft + P to open command pallet and select "Dev Container: Attach to running container".

Open VS Code and go to .vscode/launch.json (or create it).
```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Attach to Podman Flask App",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/code"
                }
            ],
            "justMyCode": false
        }
    ]
}

```
* Run the Flask app in the Podman container (Step 3).
* Go to VS Code → Run & Debug → Select "Attach to Podman Flask App".
* Click "Start Debugging" (F5).
* Add breakpoints in app.py.


## Other useful commands

Get Linux os version `cat /etc/os-release`
