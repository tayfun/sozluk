all: move-lxml package clean

move-lxml:
	mv lxml-ami-build lxml

package:
	zip -r9 main.zip *.py requests/ lxml/

clean:
	mv lxml lxml-ami-build
	rm main.zip
