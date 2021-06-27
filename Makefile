.PHONY: venv
venv:
	@ [ -d venv ] || { \
		python -m venv venv > /dev/null \
		&& echo source venv/bin/activate > venv/env.sh; \
	}
	@ echo source venv/env.sh


################################################################################
# pip
################################################################################
.PHONY: pip/install/ipdb
pip/install/ipdb:
	@ pip install -U pip
	@ pip install -U wheel
	@ pip install -U ipdb
	@ pip install -U ipython
	@ pip install -U pytest

.PHONY: pip/install/plotly
pip/install/plotly:
	@ pip install -U plotly
	@ pip install -U dash
	@ pip install -U pandas


################################################################################
# samples
################################################################################
PLOTLY_SAMPLES := \
	renderers scatter scatter3d volume bricks

PLOTLY_TARGETS := \
	$(foreach name,$(PLOTLY_SAMPLES),$(patsubst %,samples/plotly/%,$(name)))
.PHONY: $(PLOTLY_TARGETS)
$(PLOTLY_TARGETS):
	@ python $@.py


################################################################################
# tetris3d
################################################################################
.PHONY: tetris3d/install
tetris3d/install:
	@ cd tetris3d && rm -rf dist && python setup.py sdist
	@ pip install --upgrade --force-reinstall \
		./tetris3d/dist/tetris3d-*.tar.gz

.PHONY: tetris3d/install/editable
tetris3d/install/editable:
	@ pip install -e tetris3d


################################################################################
# scripts
################################################################################
SCRIPTS := \
	profile_solver \
	solve_problem \
	draw_problem \
	draw_brick

SCRIPTS_TARGETS := \
	$(foreach name,$(SCRIPTS),$(patsubst %,scripts/%,$(name)))
.PHONY: $(SCRIPTS_TARGETS)
$(SCRIPTS_TARGETS):
	@ python -O $@.py

PROBLEMS := 101 102 103 104 105 106 107 108
SOLVER_TARGETS := \
	$(foreach id,$(PROBLEMS),$(patsubst %,scripts/solve_problem/%,$(id)))
.PHONY: $(SOLVER_TARGETS)
$(SOLVER_TARGETS):
	@ python -O scripts/solve_problem.py $(lastword $(subst /, ,$@))


################################################################################
# tests
################################################################################
# -include mks/.tests.mk
.PHONY: tests/verbose
tests/verbose:
	@ cd tests && pytest -s -v
