# Docker instruction 

specify MOUNT_DIR where output will be stored 

```
docker build . -t hw2
docker run -v $MOUNT_DIR:/root/artifacts:rw hw2
```