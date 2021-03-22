TARGETS = \
	heatmap.pdf \
	comparison.pdf \
	timediff.pdf \



all: ${TARGETS}

clean:
	touch ${TARGETS}
	rm    ${TARGETS}

mrproper: clean
	touch heatmap.json comparison.csv d~
	rm    heatmap.json comparison.csv *~



heatmap.pdf: heatmap.json
	./render-heatmap.py heatmap.json heatmap.pdf


heatmap.json: adct.log
	./make-heatmap.py adct.log heatmap.json

comparison.pdf: comparison.csv
	./render-comparison.py

comparison.csv: adct.log
	./make-comparison.py adct.log comparison.csv 0 500

timediff.pdf: timediff.csv
	./render-timediff.py

timediff.csv: adct.log
	./make-timediff.py adct.log timediff.csv

