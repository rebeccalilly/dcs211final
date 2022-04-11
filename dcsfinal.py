from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from progress.bar import Bar


sequence_file = input("Enter the name of your sequence file in FASTA format: ")
sequence_data = open(sequence_file).read()
bar = Bar("Processing sequence data: ")
result_handle = NCBIWWW.qblast("blastn", "nt", sequence_data)
bar.finish()

with open("results.xml","w") as save_file:
    blast_results = result_handle.read()
    save_file.write(blast_results)

results = open("results.xml","r")
records = list(NCBIXML.parse(results)) #parse results (xml file) into a list
one_query = records[0] #from a list to a record class that holds all BLAST output

accession_numbers = [] #create empty list to store the accession_numbers of each organism

for i in range(len(one_query.alignments)): #loop through every query to obtain the accession_number
    one_hit = one_query.alignments[i]
    accession_numbers.append(one_hit.accession)


#parsing GenBank data
from Bio import Entrez
Entrez.email = input("Enter your email address (so that NCBI can contact you if there's a problem):")

for i in accession_numbers:
    handle = Entrez.efetch(db = 'nucleotide', rettype = 'gb', retmode = 'text', id = i)
    record = handle.read()
    info = record.split("\n")
    location_line = [i for i in info if i.startswith('  JOURNAL   Submitted') or i.startswith('FEATURES') or i.startswith('COMMENT')]
    location_line_indices = []
    for j in location_line:
        index_number = info.index(j)
        location_line_indices.append(index_number)

    index_1 = location_line_indices[0]
    index_2 = location_line_indices[-1]

    location_info = info[index_1:index_2]
    first_line = location_info[0]
    first_line_split = first_line.split(") ")
    cleaned_first_line = first_line_split[1]
    location = cleaned_first_line

    for h in location_info[1:]:
        cleaned_line = h.lstrip(" ")
        location += cleaned_line

    if "COMMENT" in location:
        updated_location = location.split("COMMENT")
        location = updated_location[0]

    if "URL" in location:
        updated_location = location.split("URL")
        location = updated_location[0]

    print(f"The location where the journal was published for accession number:{i} is {location}")