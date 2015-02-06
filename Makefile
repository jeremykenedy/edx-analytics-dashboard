.PHONY: requirements

ROOT = $(shell echo "$$PWD")
COVERAGE = $(ROOT)/build/coverage
PACKAGES = analytics_dashboard courses django_rjs help
NUM_PROCESSES = 2
NODE_BIN=./node_modules/.bin

DJANGO_SETTINGS_MODULE := "analytics_dashboard.settings.local"

.PHONY: requirements clean static

requirements: requirements.js
	pip install -q -r requirements/base.txt --exists-action w

requirements.js:
	npm install
	$(NODE_BIN)/bower install

test.requirements: requirements
	pip install -q -r requirements/test.txt --exists-action w

develop: test.requirements
	pip install -q -r requirements/local.txt --exists-action w

test.acceptance: develop
	git clone https://github.com/edx/edx-analytics-data-api.git
	pip install -q -r edx-analytics-data-api/requirements/base.txt

migrate:
	./manage.py migrate

clean:
	find . -name '*.pyc' -delete
	coverage erase

test_python: clean
	./manage.py test --settings=analytics_dashboard.settings.test --with-ignore-docstrings \
		--exclude-dir=analytics_dashboard/settings --exclude-dir=analytics_dashboard/migrations --with-coverage \
		--cover-inclusive --cover-branches --cover-html --cover-html-dir=$(COVERAGE)/html/ \
		--cover-xml --cover-xml-file=$(COVERAGE)/coverage.xml \
		$(foreach package,$(PACKAGES),--cover-package=$(package)) \
		$(PACKAGES)

accept:
	nosetests -v acceptance_tests --processes=$(NUM_PROCESSES) --process-timeout=120 --exclude-dir=acceptance_tests/course_validation

course_validation:
	python -m acceptance_tests.course_validation.generate_report

quality:
	pep8 --config=.pep8 $(PACKAGES)
	pylint $(PACKAGES)

	# Ignore module level docstrings and all test files
	#pep257 --ignore=D100,D203 --match='(?!test).*py' $(PACKAGES)

validate_python: test.requirements test_python quality

validate_js: requirements.js
	$(NODE_BIN)/gulp test
	$(NODE_BIN)/gulp lint
	$(NODE_BIN)/gulp jscs

validate: validate_python validate_js

demo:
	./manage.py switch show_engagement_forum_activity on --create
	./manage.py switch display_verified_enrollment on --create

compile_translations:
	i18n_tool generate -v

extract_translations:
	DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE} PYTHONPATH=".:$PYTHONPATH" i18n_tool extract -v

dummy_translations:
	i18n_tool dummy -v

generate_fake_translations: extract_translations dummy_translations compile_translations

pull_translations:
	tx pull -a

update_translations: pull_translations generate_fake_translations

static:
	$(NODE_BIN)/r.js -o build.js
	./manage.py collectstatic --noinput
	./manage.py compress
