import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def random_graph_matrix(k):

	'''
	adjacency matrix without diagonal (unnecessary) -> k x (k-1)
	'''
	return np.random.randint(2,size =(k,k-1))

def create_full_graph_matrix(adj_matrix_raw):
	'''
	adj_matrix_raw w/o diagonal -> real adjacency matrix
	'''

	return np.hstack((np.tril(adj_matrix_raw,-1),np.zeros((len(adj_matrix_raw),1),dtype = np.int)))+\
			np.hstack((np.zeros((len(adj_matrix_raw),1),dtype = np.int),np.triu(adj_matrix_raw)))



def create_data(n,k):

	'''
	create n test matrices of size k x (k-1)
	'''

	return [random_graph_matrix(k) for _ in range(n)]

def create_labeled_data(n,k):

	'''
	create n test matrices of size k x (k-1) and labels
	'''

	data = create_data(n,k)
	return {'matrices':data, 'labels':[check_hamiltonian_cycle(adj_matrix_raw) for adj_matrix_raw in data]}

def print_Graph(adj_matrix_raw):

	'''
	print graph
	'''

	print create_full_graph_matrix(adj_matrix_raw)
	graph = nx.DiGraph(create_full_graph_matrix(adj_matrix_raw))
	nx.draw_networkx(graph)
	plt.show()

def check_hamiltonian_cycle(adj_matrix_raw):
	'''
	return true if raw adjacency matrix (k x (k-1)) contains hamiltonian cycle
	'''

	n = len(adj_matrix_raw)

	'''look for path of certain length containing each node only once'''
	def distinct_path(length,start,path):
		#if length is zero, there is a path of this length starting in start
		if not length: 
			# if there is an edge start -> 0, then path -> 0 is a hamiltonian cycle
			if adj_matrix_raw[start,0]:
				new_path = list(path)
				new_path.append(0)
				return new_path

		for head_raw in range(n-1):
			#go through adjacency list
			if adj_matrix_raw[start,head_raw]:
				head = head_raw+(head_raw>=start) 	#because adj_matrix_raw does not contain diagonal elements -> if head_raw >= start, it's actually the next node
				
				'''if head is not already contained in path, add it and look for path of length - 1 from new starting node "head"
				'''

				if not(head in path):	
					new_path = list(path)
					new_path.append(head)
					return distinct_path(length-1,head,new_path)	#find path starting in head with length - 1

		return False

	return distinct_path(n-1,0,[0])


labeled_data = create_labeled_data(25,5)

print labeled_data