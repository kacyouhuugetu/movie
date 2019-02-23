
def list_to_tree(data, id_col, parentid_col, children_col, show_cols):

	search_id_fun = lambda id_, data:True if data.get(id_col)==id else False

	def list_to_tree_add_node(id_, tree, parentid_map, item_map):
		def list_to_tree_get_path(id_, parentid_map):
			path = []
			while True:
				path.append(id_)
				if not parentid_map.get(id_):
					break

				id_ = parentid_map[id_]

			path.reverse()
			return path

		def list_to_tree_search_item(s, l):
			for item in l:
				if item[id_col] == s:
					return item
			else:
				return None


		path = list_to_tree_get_path(id_, parentid_map)

		cur_node = tree
		for index, id_ in enumerate(path):

			item = item_map[id_]
			res = list_to_tree_search_item(id_, cur_node)

			# 未找到，添加节点
			if res is None:
				cur_node.append(item)

				if index < len(path)-1:
					item[children_col] = []
					cur_node = item[children_col]

			else:
				if index < len(path)-1:
					if children_col not in res:
						res[children_col] = []

					cur_node = res[children_col]


	tree = []
	parentid_map = {}
	item_map = {}
	ids = []

	for item in data:
		if not id_col in item:
			raise TypeError('data的每一项都需包含键%s'%(str(id_col)))

		if item.get(parentid_col):
			parentid_map[item.get(id_col)] = item.get(parentid_col)

		item = dict((key, item.get(key)) for key in item if key in show_cols)
		item_map[item[id_col]] = item

		ids.append(item[id_col])

	if show_cols is None:
		show_cols = [id_col]
	if not id_col in show_cols:
		show_cols.append(id_col)

	for id_ in ids:

		list_to_tree_add_node(id_, tree, parentid_map, item_map)

	return tree