# Install

```shell
docker image build --rm --tag tail_py .
```

# Use

```shell
docker container run --rm -v $(pwd):/opt/project tail_py ./tail.py -n 2 ololo.txt | wc -l
```
