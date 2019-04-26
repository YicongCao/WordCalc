ver=v10
img=ailab-embedding

build:
	docker build -t $(img):$(ver) .
	docker image ls | grep $(img)

export:
	docker save -o ../$(img)$(ver).tar $(img):$(ver)

run:
	docker run -it --rm $(img):$(ver) -p 5010:5000