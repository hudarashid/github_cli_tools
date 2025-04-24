# Test
.PHONY: tests
tests:
	@pytest tests/

# Help
.PHONY:	help
help:
	@python main.py -h

# Help subparser
# make help cmd=list    # Shows help for the list command
# make help cmd=create-branch  # Shows help for the create command
.PHONY:	help-sub
help-sub:
	@python main.py $(args) -h





