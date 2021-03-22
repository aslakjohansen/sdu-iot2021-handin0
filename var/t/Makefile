TARGETS = \
	thist.pdf \



all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch d~
	rm    *~



thist.pdf: t_processed.log
	./hist.py

t_processed.log: t.log
	./convert.py t.log t_processed.log

