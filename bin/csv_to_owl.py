#!/usr/bin/env jython

# Python imports.
import csv
import os
import sys
from argparse import ArgumentParser
from ontobuilder import OWLOntologyBuilder


# Define and process the command-line arguments.
argp = ArgumentParser(description='Compiles an OWL ontology from a base \
ontology file and one or more CSV term description tables.')
argp.add_argument('-b', '--base_ontology', type=str, required=True, help='An \
OWL ontology file to use as a base for compiling the final ontology.')
argp.add_argument('-n', '--no_def_expand', action='store_true', help='If this \
flag is given, no attempt will be made to modify definition strings by adding \
the IDs of term labels referenced in the definitions.')
argp.add_argument('-i', '--id', type=str, required=False, default='',
    help='An IRI to use as the ID for the compiled ontology.')
argp.add_argument('-o', '--output', type=str, required=True, help='A path to \
use for the compiled ontology file.')
argp.add_argument('termsfiles', type=str, nargs='*', help='One or more CSV \
files that contain tables defining the new ontology terms.')
args = argp.parse_args()

# Verify that the base ontology file exists.
if not(os.path.isfile(args.base_ontology)):
    raise RuntimeError(
        'The source ontology could not be found: ' + args.base_ontology + '.'
    )

# Verify that the terms CSV files exist.
for termsfile in args.termsfiles:
    if not(os.path.isfile(termsfile)):
        raise RuntimeError(
            'The input CSV file could not be found: ' + termsfile + '.'
        )

ontbuilder = OWLOntologyBuilder(args.base_ontology)

# Process each source CSV file.
for termsfile in args.termsfiles:
    with open(termsfile) as fin:
        reader = csv.DictReader(fin)
        rowcnt = 1
        for csvrow in reader:
            rowcnt += 1
            if not(csvrow['Ignore'].strip().upper().startswith('Y')):
                try:
                    if csvrow['Type'].lower() == 'class':
                        ontbuilder.addClass(csvrow, not(args.no_def_expand))
                    elif csvrow['Type'].lower() == 'objectproperty':
                        exit('Not yet supported.')
                    elif csvrow['Type'].lower() == 'dataproperty':
                        ontbuilder.addDataProperty(csvrow, not(args.no_def_expand))
                    else:
                        raise RuntimeError('The entity type "' + csvrow['Type']
                                + '" is not supported.')
                except RuntimeError as err:
                    print('\nError encountered in term description in row '
                            + str(rowcnt) + ' of "' + termsfile + '":')
                    print err
                    print
                    sys.exit(1)

# Set the ontology ID, if a new ID was provided.
newid = args.id.strip()
if newid != '':
    ontbuilder.getOntology().setOntologyID(newid)

# Write the ontology to the output file.
ontbuilder.getOntology().saveOntology(args.output)

