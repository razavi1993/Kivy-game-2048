def move_labels(my_list, to_left):
	new_list = []
	mlen = len(my_list)
	for i in range(mlen):
		if my_list[i] != "":
			new_list.append(my_list[i])
	if to_left == True:
		new_list = new_list + (4-mlen)*[""]
	else:
		new_list = (4-mlen)*[""] + new_list
	return new_list
