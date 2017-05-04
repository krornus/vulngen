import os
data_dir = './raw_input/'
output_dir = './input'
for in_file, out_file in [[os.path.join(data_dir, f), os.path.join(output_dir, f)]
	 for f in os.listdir(data_dir)]:
	print('File: {}'.format(in_file))
	os.system("pcg proj.pt < {} > {}".format(in_file, out_file))


