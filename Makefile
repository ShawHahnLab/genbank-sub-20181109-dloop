all: errorsummary.val

### .fsa FASTA input
# Create a single .fsa file with all input sequences.  Correct a few of the
# source modifier entries for Country also.
dloop.fsa:
	sed 's/Republic of Congo/Republic of the Congo/' raw/split/*.fasta \
	| sed 's/Guinea Bissau/Guinea-Bissau/' \
	> $@

### .tbl Features table
# We have a spreadsheet that contains most of the features info already, but
# then also have a custom .tbl chunk for entry SY94.
dloop.tbl: raw/annotations.tsv raw/SY94_custom.tbl
	./convert_tbl.py SY94  < $< > $@ && cat $(word 2,$^) >> $@

### Run tbl2asn
# -t ... will define the template, shared across all entries
#    Created on https://submit.ncbi.nlm.nih.gov/genbank/template/submission/
# -j lets us supply additional source features to apply to everything (in this
#    case, that the sequences came from the mitochondrion.)
# -p . will search for data in the current directory
# -a s will do batch processing, allowing multiple sequences in one input file
# -V vb will both run verification checks and generate GenBank flat files
# -Z ... will create a discrepancy report
#  
#  The .sqn file is what we need to submit to GenBank.  The rest is for our own
#  reference.
errorsummary.val: raw/template.sbt.txt dloop.fsa dloop.tbl
	tbl2asn -t $< \
		-j '[location=mitochondrion]' \
		-p . \
		-a s \
		-V vb -Z discrep_report.txt && \
	grep . *.val

clean:
	rm -f dloop.tbl dloop.fsa  \
		errorsummary.val dloop.val discrep_report.txt make_log.txt \
		dloop.gbf dloop.sqn
