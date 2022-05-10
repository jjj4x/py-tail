# Install

```shell
docker image build --rm --tag tail_py .
```

# Use

```shell
docker container run --rm -v $(pwd):/opt/project tail_py ./tail.py -n 2 ololo.txt | wc -l
```

# Use with never-ending file

```shell
docker container run --rm -it tail_py bash

while true; do echo 1 >> file.txt; sleep 1; done &

./tail.py -n 2 file.txt | wc -l
```
