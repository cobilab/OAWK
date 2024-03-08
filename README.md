# Optimized and Adaptive Weighted-K (OAWK)

Consensus-generating tool from aligned multi-FASTA files.

### REPLICATION ###

To download OAWK in a Linux system, please run:
<pre>
git clone https://github.com/cobilab/OAWK_consensus_generator.git
cd src
chmod +x *.sh
</pre>

To generate a consensus the following command should be executed:
<pre>
python3 OAWK.py -i input.fa -v name_virus -k values_of_k -b value_of_b
</pre>

To evaluate the consensus generated for one file, given a reference, please type:
<pre>
./OAWK_evaluation.sh --reconstructed reconstructed.fa --reference reference.fa --output results 
</pre>

### CITATION ###

On using this software/method please cite:

* pending

### ISSUES ###

For any issue let us know at [issues link](https://github.com/cobilab/OAWK_consensus_generator/issues).

### LICENSE ###

GPL v3.

For more information:
<pre>http://www.gnu.org/licenses/gpl-3.0.html</pre>
