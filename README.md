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



## Podman commands

### Linux Vitual Machine
* Create podman machine `podman machine init`
* Start machine `podman machine start`

### Images & Container commands
* List all images - `podman images`

* Start a container from image - `Podman run -p <localport>:<imageport> <imagename>`


* Run in detached mode with `-d` flag. 
`podman run -d -p 5000:5000 docker.io/digvijaytaunk/simple_flask`

* It is a good practice to remove the container once it is not running. `--rm` — Removes the container once stopped.
`podman run --rm -d -p 5000:5000 <image-name>`

* Remove container `podman rm <ContainerName>`
* Remove image `podman rmi <imageName>`

## Podman build image
* Run podman build command to build image - `podman build --tag <image-name> .`

`--tag` - give name to image.

`.` - use root directory to pick the dockerfile.

# TODO - how to debug python code running in docker