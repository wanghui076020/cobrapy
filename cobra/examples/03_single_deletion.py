#cobra/examples/03_single_deletion.py
#
#This file provides a simple example of how to perform
#a single deletion simulation
from cobra.flux_analysis import single_deletion
from cPickle import load, dump
from time import time
from math import floor
test_directory = 'files/'
from cobra.manipulation import initialize_growth_medium
with open(test_directory + 'salmonella.pickle') as in_file:
    cobra_model = load(in_file)


initialize_growth_medium(cobra_model, 'LB')
#Expected growth rates for the salmonella model with deletions in LB medium
the_names = ['tpiA', 'metN', 'atpA', 'eno']
the_loci =  ['STM4081', 'STM0247', 'STM3867', 'STM2952']
the_genes = tpiA, metN, atpA, eno = map(cobra_model.genes.get_by_id, the_loci)
the_growth_rates = {tpiA:2.41, metN:2.43, atpA:1.87, eno:1.81} #expected growth rates after deletion

#Perform a single gene deletion
the_results = single_deletion(cobra_model, [tpiA])


gene_list = the_growth_rates.keys()
#Perform deletions for all genes in the list
start_time = time()

rates, statuses, problems = single_deletion(cobra_model,
                                            gene_list)
for the_gene, v in statuses.items():
    if v != 'optimal':
        print '\t\tdeletion %s was not optimal'%the_gene
for the_gene, v in rates.items():
    v = floor(100*v)/100
    if v != the_growth_rates[the_gene]:
        print '\t\tFAILED: %s simulation (%1.3f) != expectation (%1.2f)'%(the_gene.name,
                                                                              v,
                                                                              the_growth_rates[the_gene])
    else:
        print '\t\tPASSED: %s simulation (%1.3f) ~= expectation (%1.2f)'%(the_gene.name,
                                                                              v,
                                                                              the_growth_rates[the_gene])


print '\t\tsingle deletion time: %f seconds'%(time() - start_time)

