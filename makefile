FILES :=                       \
    model.html                 \
    IDB2.log                   \
    models.py                  \
    tests.py                   \
    UML.pdf                    \
    apiary.apib                \

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -f  .coverage
	rm -f  *.pyc
	rm -f  TestModels.tmp
	rm -rf __pycache__

config:
	git config -l

scrub:
	make clean
	rm -f  model.html
	rm -f  IDB1.log

status:
	make clean
	@echo
	git branch
	git remote -v
	git status

test: TestModels.tmp

idb.html: models.py
	pydoc3 -w models

idb.log:
	git log > IDB2.log

TestModels.tmp: tests.py
	coverage3 run --omit=app.py,*flask*,*sqlalchemy*,*dist-packages* --branch tests.py >  TestModels.tmp 2>&1
	coverage3 report -m              >> TestModels.tmp
	cat TestModels.tmp
