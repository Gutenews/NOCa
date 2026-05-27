LIB = ./geometry3D.py ./geometrie.py
PRG = $(wildcard ./*.py)
SRC = $(filter-out $(LIB),$(PRG))

figure: $(SRC)
	for src in $(SRC); do\
		python $$src;\
	done