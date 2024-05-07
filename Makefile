build:
	docker build . -t k8s-pi-thermal-monitor

volume:
	docker volume create k8s-pi-thermal-monitor
	docker run -it --user root --rm -v k8s-pi-thermal-monitor:/data --entrypoint /bin/bash k8s-pi-thermal-monitor

run: build
	docker run -it --rm -v k8s-pi-thermal-monitor:/data -e THERMAL_ZONE=/data/temp k8s-pi-thermal-monitor
