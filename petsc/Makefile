include ${PETSC_DIR}/lib/petsc/conf/variables
include ${PETSC_DIR}/lib/petsc/conf/rules

all: demo1 demo2

demo1: demo1.o
	$(CLINKER) -o demo1 ${PETSC_LIB} $*.o

demo2: demo2.o
	$(CLINKER) -o demo2 ${PETSC_LIB} demo2.o
