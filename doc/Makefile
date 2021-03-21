TARGETS = \
	SDU\ IoT\ -\ Group\ 0\ -\ Handin\ 0\ -\ Sampling\ Rate.pdf \



all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm -f ${TARGETS}

mrproper: clean
	touch d.aux d.log d~ d.nav d.out d.snm d.toc .includes
	rm -f *.aux *.log *~ *.nav *.out *.snm *.toc .includes



.includes:
	rm -Rf .includes
	mkdir .includes

.includes/main.timestamp: .includes *.tex
	cd .. ; bin/generate-tex-includes PDF doc/main.tex doc
	touch .includes/main.timestamp



SDU\ IoT\ -\ Group\ 0\ -\ Handin\ 0\ -\ Sampling\ Rate.pdf: *.tex .includes/main.timestamp
	pdflatex -shell-escape main.tex
	pdflatex -shell-escape main.tex
	mv main.pdf SDU\ IoT\ -\ Group\ 0\ -\ Handin\ 0\ -\ Sampling\ Rate.pdf

