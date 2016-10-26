#
# Provides a class, ImportModuleBuilder, for building import module OWL files
# by extracting terms from an existing ontology.
#

# Python imports.
import csv
import os
from urllib import FancyURLopener
from urllib2 import HTTPError
from progressbar import ProgressBar, Percentage, Bar, ETA
import math
from ontology import Ontology

# Java imports.
from java.util import HashSet
from org.semanticweb.owlapi.model import IRI, OWLClassExpression
from org.semanticweb.owlapi.model import OWLObjectPropertyExpression
from org.semanticweb.owlapi.model import OWLObjectProperty


class URLOpenerWithErrorHandling(FancyURLopener):
    """
    Extends FancyURLopener by adding better error handling for unrecoverable
    HTTP errors (e.g., 404).
    """
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        raise HTTPError(url, errcode, errmsg, headers, fp)


class ImportModuleBuilder:
    """
    Builds import modules using terms from an external ontology.  The argument
    "base_IRI" is the base IRI string to use when generating IRIs for module
    OWL files.
    """
    def __init__(self, base_IRI):
        self.progbar = None
        self.sourceOntologyIRI = ''

        self.base_IRI = base_IRI

        # Define the strings that indicate TRUE in the CSV files.  Note that
        # variants of these strings with different casing will also be
        # recognized.
        self.true_strs = ['t', 'true', 'y', 'yes']

    def _updateDownloadProgress(self, blocks_transferred, blocksize, filesize):
        """
        Instantiates and updates a console-based progress bar to indicate
        ontology download progress.  This method should be passed to the
        retrieve() method of URLOpenerWithErrorHandling.
        """
        #print blocks_transferred, blocksize, filesize
        if blocks_transferred == 0:
            self.progbar = ProgressBar(
                widgets=[Percentage(), '', Bar(marker='-', left='[', right=']'), ' ' , ETA()],
                maxval=int(math.ceil(float(filesize) / blocksize))
            )
            print '\nDownloading ' + self.sourceOntologyIRI
            self.progbar.start()
        else:
            self.progbar.update(blocks_transferred)
            if blocks_transferred == self.progbar.maxval:
                self.progbar.finish()
                print

    def _getOutputFileName(self, ontologyIRI, outputsuffix):
        """
        Constructs the file name for the output import module file.
        """
        # Extract the name of the source ontology file from the IRI.
        ontfile = os.path.basename(ontologyIRI)

        # Generate the file name for the ouput ontology OWL file.
        outputfile = os.path.splitext(ontfile)[0] + outputsuffix

        return outputfile

    def isBuildNeeded(self, ontologyIRI, termsfile_path, outputsuffix):
        """
        Tests whether an import module actually needs to be built.  If the file
        located at termsfile_path has 
        """
        outputfile = self._getOutputFileName(ontologyIRI, outputsuffix)
    
        # If the output file already exists and the terms file was not
        # modified/created more recently, there is nothing to do.
        if os.path.isfile(outputfile):
            if os.path.getmtime(outputfile) > os.path.getmtime(termsfile_path):
                return False

        return True
        
    def buildModule(self, ontologyIRI, termsfile_path, outputsuffix):
        """
        Builds an import module from a single external ontology and a CSV file
        containing a set of terms to import.  The import module will be saved
        as an OWL file with a name generated by appending outputsuffix to the
        base of the source ontology file name.

          ontologyIRI: The IRI of the source ontology.
          termsfile_path: The CSV file containing the terms to import.
          outputsuffix: A string to use when generating file names for the
                        import module OWL files.
        """
        # Verify that the terms file exists.
        if not(os.path.isfile(termsfile_path)):
            raise RuntimeError('Could not find the terms CSV file "'
                    + termsfile_path + '".')

        # Extract the name of the source ontology file from the IRI.
        ontfile = os.path.basename(ontologyIRI)

        # Generate the file name and IRI for the ouput ontology OWL file.
        outputfile = self._getOutputFileName(ontologyIRI, outputsuffix)
        ont_IRI = IRI.create(self.base_IRI + outputfile)

        # Verify that the source ontology file exists; if not, download it.
        if not(os.path.isfile(ontfile)):
            opener = URLOpenerWithErrorHandling()
            try:
                self.sourceOntologyIRI = ontologyIRI
                opener.retrieve(ontologyIRI, ontfile, self._updateDownloadProgress)
            except HTTPError as err:
                raise RuntimeError('Unable to download the external ontology at "'
                        + ontologyIRI + '": ' + str(err))

        sourceont = Ontology(ontfile)
        signature = HashSet()
        reasoner = None
        excluded_ents = []
        with open(termsfile_path) as filein:
            reader = csv.DictReader(filein)
        
            # Read the terms to import from the CSV file, add each term to the
            # signature set for module extraction, and add the descendents of
            # each term, if desired.
            for row in reader:
                owlent = sourceont.getEntityByID(row['ID'])
                if owlent == None:
                    raise RuntimeError(row['ID'] + ' could not be found in the source ontology')

                if row['Exclude'].strip().lower() in self.true_strs:
                    excluded_ents.append(owlent)
                else:
                    signature.add(owlent)
    
                    if row['Seed descendants'].strip().lower() in self.true_strs:
                        if reasoner == None:
                            reasoner = sourceont.getHermitReasoner()
    
                        # Get the entity's subclasses or subproperties.
                        if isinstance(owlent, OWLClassExpression):
                            signature.addAll(reasoner.getSubClasses(owlent, False).getFlattened())
                        elif isinstance(owlent, OWLObjectPropertyExpression):
                            propset = reasoner.getSubObjectProperties(owlent, False).getFlattened()
                            # Note that getSubObjectProperties() can return both
                            # named properties and ObjectInverseOf (i.e., unnamed)
                            # properties, so we need to check the type of each
                            # property before adding it to the module signature.
                            for prop in propset:
                                if isinstance(prop, OWLObjectProperty):
                                    signature.add(prop)

        if signature.size() == 0:
            raise RuntimeError('No terms to import were found in the terms file.')
        
        if reasoner != None:
            reasoner.dispose()

        module = sourceont.extractModule(signature, ont_IRI)

        # Remove any entities that should be excluded from the final module.
        for ent in excluded_ents:
            module.removeEntity(ent)

        module.saveOntology(outputfile)

