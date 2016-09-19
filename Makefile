all: mv-lxml-for-ami package mv-lxml-for-local

mv-lxml-for-ami:
	mv lxml-ami-build lxml

package:
	zip -r9 main.zip *.py requests/ lxml/ boto3/

mv-lxml-for-local:
	mv lxml lxml-ami-build

clean:
	rm main.zip
