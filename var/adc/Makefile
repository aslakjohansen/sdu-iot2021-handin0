TARGETS = \
	hist.pdf \



all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch d~
	rm    *~



hist.pdf: adc_diff.log
	./hist.py

adc_diff.log: adc.log
	./convert.py adc.log adc_diff.log

