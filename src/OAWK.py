#!/usr/bin/env python3
import argparse
import os
import pickle
import sys
import warnings

dict_content = {}
list_correctness=[]
list_last_values=[]

def add_to_dict(key, val, dict): #adds element to a dictionary with a certain val; creates element if it doesn't exist

	if key in dict:
		# append the new number to the existing array at this slot
		dict[key] = dict.get(key) + val
	else:
		# create a new array in this slot
		dict[key] = val
		if dict == dict_content:
			list_correctness.append([])
			list_last_values.append([])

def read_file(path):  # read file and add it to a dictionary
	dict_names_internal = {}
	name_tool = ""
	last_line_header = False
	file = open(path, "r")
	count = -1

	for line in file:

		if line[0] != ">":
			if last_line_header == True:
				count += 1
				add_to_dict(count, name_tool, dict_names_internal)
				last_line_header = False

			# print(count)
			add_to_dict(count, line.strip("\n"), dict_content)
		else:
			if last_line_header == False:
				try:
					name_tool = line.split("[")[1].split("]")[0]
				except:
					print(line.split("["))
				last_line_header = True


	file.close()
	return dict_names_internal


def update_correctness(chosen, k): #updates the list of correct values
	count = 0

	for i in list_correctness:
		if len(list_correctness[count]) == k:
			list_correctness[count].pop(0)

		if list_last_values[count][len(list_last_values[count]) -1] == chosen:
			list_correctness[count].append(1)
		else:
			list_correctness[count].append(0)

		count += 1

def performance_calculator(list_corr_tools, beta):

	if beta == None:
		return sum(list_corr_tools)

	else:
		counter = 0
		result = 0

		for i in list_corr_tools:

			max_val = (((1 - beta) / len(list_corr_tools) ) * counter ) + beta
			result += max_val * i
			
			counter += 1


		return result






def get_value_correctness(key, beta):
	correctness_expected = performance_calculator(list_correctness[key], beta)

	return correctness_expected
	


def generate_consensus (output, k):

	count = 0
	finished = 0

	list_bases = "actguACTGU"
	consensus = []
	keys_finished = []

	while finished < len(dict_content):

		dict_bases = {}
		for key in dict_content:
			try:
				base = dict_content.get(key)[count]
			except:
				if key not in keys_finished:
					keys_finished.append(key)
					finished += 1


			if base in list_bases: #check if it is one of the bases
				if base == "a" or base == "A":
					add_to_dict("A", get_value_correctness(key, beta), dict_bases)
					if len(list_last_values[key]) == k:
						list_last_values[key].pop(0)
					list_last_values[key].append("A")

				elif base == "c" or base == "C":
					add_to_dict("C", get_value_correctness(key, beta), dict_bases)
					if len(list_last_values[key]) == k:
						list_last_values[key].pop(0)
					list_last_values[key].append("C")

				elif base == "t" or base == "T":
					add_to_dict("T", get_value_correctness(key, beta), dict_bases)
					if len(list_last_values[key]) == k:
						list_last_values[key].pop(0)
					list_last_values[key].append("T")

				elif base == "g" or base == "G":
					add_to_dict("G", get_value_correctness(key, beta), dict_bases)
					if len(list_last_values[key]) == k:
						list_last_values[key].pop(0)
					list_last_values[key].append("G")

				elif base == "u" or base == "U":
					add_to_dict("U", get_value_correctness(key, beta), dict_bases)
					if len(list_last_values[key]) == k:
						list_last_values[key].pop(0)
					list_last_values[key].append("U")

				elif base == "n" or base == "N":
					if len(list_last_values[key]) == k:
						list_last_values[key].pop(0)
					list_last_values[key].append("N")

			else: #error; not any of the bases
				if len(list_last_values[key]) == k:
					list_last_values[key].pop(0)
				list_last_values[key].append("N")

		try:
			max_val = max(dict_bases.values())
		except:
			max_val = 0
		max_keys = [k for k, v in dict_bases.items() if v == max_val]

		#print("MAX value", max_val , "Max keys " , max_keys)

		if len(max_keys) == 1:
			consensus.append(max_keys[0])
			update_correctness(max_keys[0], k)
		if max_val == 0:
			consensus.append("N")
			update_correctness("N", k)
		if len(max_keys) > 1:
			if "A" in max_keys:
				consensus.append("A")
				update_correctness("A", k)
			elif "T" in max_keys:
				consensus.append("T")
				update_correctness("T", k)
			elif "C" in max_keys:
				consensus.append("C")
				update_correctness("C", k)
			elif "G" in max_keys:
				consensus.append("G")
				update_correctness("G", k)
			elif "U" in max_keys:
				consensus.append("U")
				update_correctness("U", k)
			else:
				consensus.append("N")
				update_correctness("N", k)
		count += 1


	file = open(output, "w")

	consensus[:len(dict_content.get(0))]
	#print("consensus length", len(consensus))
	file.write(">Conse" + virus + "\n" + ''.join(consensus)  + "\n")

	file.close()

def import_model(filename):
	# if pickle file exists read from there as it is faster
	if os.path.exists(filename):
		return pickle.load(open(filename, 'rb'))
	else:
		ans = input("File does not exist. Execute without machine learning model? [Y/n]")

		if ans.lower() == "n":
			sys.exit()


if __name__ == '__main__':

	warnings.filterwarnings("ignore")

	parser = argparse.ArgumentParser(description="Index",
	usage="python3 OAWK.py -i <aligned multi-FASTA> -v <Name virus> -k <values of k> -b <value of b>")

	parser.add_argument("-i", help="Aligned multi-FASTA", type=str, required=True)
	parser.add_argument("-v", help="Name of the virus.", type=str, required=False)
	parser.add_argument("-k", help="Values of k, separated by spaces", nargs="+", type=int, required=True)
	parser.add_argument("-b", help="Value of b.", type=float, required=False)

	args = parser.parse_args()

	beta = None
	if args.b is not None:
		beta = args.b

	virus = None
	if args.v is not None:
		virus = args.v
	else:
		virus = "unknown"

	filename = args.i
	dict_names_internal = read_file(filename)

	count = 0
	for i in args.k:
		generate_consensus("tmp-" + virus + "-" + str(i) + ".fa", i)
		count += 1

	os.system("cat tmp-" + virus + "-*.fa > new.fa")
	os.system('rm tmp-*.fa')
