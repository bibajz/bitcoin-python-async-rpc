all: clean

clean:
	@echo Cleaning crew has arrived!
	@rm -rf .mypy_cache .eggs build dist */*.egg-info
	@rm -f *.py[co] */*.py[co] */*/*.py[co]
	@rm -f *.so */*.so */*/*.so */*/*/*.so
	@rm -f *.c */*.c */*/*.c */*/*/*.c