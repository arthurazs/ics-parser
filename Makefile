.PHONY: r run
run: r
r:
	python3 ics.py

.PHONY: c clean
clean: c
c:
	rm *.ics
