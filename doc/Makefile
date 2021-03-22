TARGETS = \
	SDU\ IoT\ -\ Group\ 0\ -\ Handin\ 0\ -\ Sampling\ Rate.pdf \

DEPS = \
	figs/hist.pdf \
	figs/heatmap.pdf \
	figs/comparison.pdf \
	figs/thist.pdf \
	figs/timediff.pdf \

#####################################################################
####################################################### major targets

all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm -f ${TARGETS}

mrproper: clean
	touch  d.aux d.log d~ d.nav d.out d.snm d.toc .includes
	rm -Rf *.aux *.log *~ *.nav *.out *.snm *.toc .includes

#####################################################################
############################################# general include targets

.includes:
	rm -Rf .includes
	mkdir .includes

.includes/main.timestamp: .includes *.tex
	cd .. ; bin/generate-tex-includes PDF doc/main.tex doc
	touch .includes/main.timestamp

#####################################################################
############################################ specific include targets

figs/hist.pdf: ../var/adc/hist.pdf
	cp ../var/adc/hist.pdf figs/hist.pdf

../var/adc/hist.pdf:
	cd ../var/adc/ ; make hist.pdf

figs/heatmap.pdf: ../var/adct/heatmap.pdf
	cp ../var/adct/heatmap.pdf figs/heatmap.pdf

../var/adct/heatmap.pdf:
	cd ../var/adct/ ; make heatmap.pdf

figs/comparison.pdf: ../var/adct/comparison.pdf
	cp ../var/adct/comparison.pdf figs/comparison.pdf

../var/adct/comparison.pdf:
	cd ../var/adct/ ; make comparison.pdf

figs/timediff.pdf: ../var/adct/timediff.pdf
	cp ../var/adct/timediff.pdf figs/timediff.pdf

../var/adct/timediff.pdf:
	cd ../var/adct/ ; make timediff.pdf

figs/thist.pdf: ../var/t/thist.pdf
	cp ../var/t/thist.pdf figs/thist.pdf

../var/t/thist.pdf:
	cd ../var/t/ ; make thist.pdf

#####################################################################
####################################################### minor targets

SDU\ IoT\ -\ Group\ 0\ -\ Handin\ 0\ -\ Sampling\ Rate.pdf: *.tex ${DEPS} .includes/main.timestamp
	pdflatex -shell-escape main.tex
	pdflatex -shell-escape main.tex
	mv main.pdf SDU\ IoT\ -\ Group\ 0\ -\ Handin\ 0\ -\ Sampling\ Rate.pdf

