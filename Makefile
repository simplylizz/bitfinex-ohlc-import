build:
	docker build -t bitfinex .

build-tests:
	docker build -t bitfinex-tests -f Dockerfile.tests .

test:
	./run_tests.sh
