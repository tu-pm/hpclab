## Container
*   List all running containers

        docker container ls         

*   List all containers, even those not running

        docker container ls -a           

*   Gracefully stop the specified container

        docker container stop <hash>     

*   Force shutdown of the specified container    

        docker container kill <hash>     

*   Remove specified container from this machine  

        docker container rm <hash>     

        docker container rm $(docker container ls -a -q)

*   Inspect task or container      

        docker inspect <task or container>                 

*   List container IDs

        docker container ls -q                                   

## Image

*   Create image using this directory's Dockerfile

        docker build -t friendlyhello .

*   Run "friendlyname" mapping port 4000 to 80

        docker run -p 4000:80 friendlyhello
        docker run -d -p 4000:80 friendlyhello       # Same thing, but in detached mode

*   List all images on this machine

        docker image ls -a                      

*   Remove specified image from this machine     

        docker image rm <image id>         

*   Remove all images from this machine

        docker image rm $(docker image ls -a -q) 

## Using Registries

*   Log in this CLI session using your Docker credentials

        docker login           

*   Tag <image> for upload to registry
    
        docker tag <image> username/repository:tag

*   Upload tagged image to registry

        docker push username/repository:tag          

*   Run image from a registry

        docker run username/repository:tag                 

## Docker Machine

*   Create a VM

        docker-machine create --driver virtualbox myvm1  

*   View basic information about your node

        docker-machine env myvm1             

*   List the nodes in your swarm

        docker-machine ssh myvm1 "docker node ls" 

*   Inspect a node

        docker-machine ssh myvm1 "docker node inspect <node ID>"      

*   View join token
        
        docker-machine ssh myvm1 "docker swarm join-token -q worker" 

*   Open an SSH session with the VM; type "exit" to end

        docker-machine ssh myvm1 

*   View nodes in swarm (while logged on to manager)

        docker node ls             

*   Make the worker leave the
 
        docker-machine ssh myvm2 "docker swarm leave" swarm

*   Make master leave, kill swarm

        docker-machine ssh myvm1 "docker swarm leave -f" 

*   List VMs, asterisk shows which VM this shell is talking to

        docker-machine ls 

*   Start a VM that is currently not running

        docker-machine start myvm1          

*   Show environment variables and command for myvm1

        docker-machine env myvm1    

*   Connect shell to myvm1

        eval $(docker-machine env myvm1)       

*   Copy file to node's home dir

        
        docker-machine scp docker-compose.yml myvm1:~

*   Deploy an app using ssh (you must have first copied the Compose file to myvm1)

        docker-machine ssh myvm1 "docker stack deploy -c <file> <app>"

*   Disconnect shell from VMs, use native docker
 
        eval $(docker-machine env -u)   

*   Stop all running VMs

        docker-machine stop $(docker-machine ls -q)

*   Delete all VMs and their disk images           

        docker-machine rm $(docker-machine ls -q) # 

## Service

*   List running services associated with an app

        docker service ls               

*   List tasks associated with an app

        docker service ps <service>                

## Swarm

*   Initialize a swarm

        docker swarm init

*   Join to another swam

        docker swarm join --token <token> <ip:port>

*   Take down a single node swarm from the manager

        docker swarm leave --force    

## Stack

*   List stacks or apps

        docker stack ls                                          

*   Run the specified Compose file

        docker stack deploy -c <composefile> <appname>

*   Tear down an application

        docker stack rm <appname>                           

*   Deploy an app; command shell must be set to talk to manager (myvm1), uses local Compose file

        docker stack deploy -c <file> <app>










