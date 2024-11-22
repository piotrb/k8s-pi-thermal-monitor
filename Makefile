build:
	docker build . -t k8s-pi-thermal-monitor

build-builder:
	docker build . --target builder -t k8s-pi-thermal-monitor:builder

run-builder:
	docker run -it --rm \
		--entrypoint /bin/bash \
		k8s-pi-thermal-monitor:builder
		# -v `pwd`:/app \

volume:
	docker volume create k8s-pi-thermal-monitor
	docker run -it --user root --rm -v k8s-pi-thermal-monitor:/data --entrypoint /bin/bash k8s-pi-thermal-monitor

shell: build
	docker run -it --rm --entrypoint /bin/bash k8s-pi-thermal-monitor

run: build
	docker run -it --rm -v `pwd`:/data -e THERMAL_ZONE=/data/temp k8s-pi-thermal-monitor
