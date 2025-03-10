import pickle
import trajets
import api_links
import matplotlib.pyplot as plt
import networkx as nx 

class StationsGraph:
    def __init__(self,load_graph=True):
        if load_graph :
            with open('__pycache__/graph_backup.pickle','rb') as f:
                loaded_StationsGraph = pickle.load(f)
                self.graph = loaded_StationsGraph.graph
        else : 
            trajets_graph = trajets.TrajetsTGVmax()
            trajets_graph.get([api_links.api_prefix],limit_results=1000)
            self.graph = {}
            for trajet in trajets_graph.liste_trajets :
                if not trajet.depart == trajet.arrivee :
                    if trajet.depart not in self.graph.keys() :
                        self.graph[trajet.depart]={trajet.arrivee : trajet.duration()}
                    else : 
                        if trajet.arrivee not in self.graph[trajet.depart] :
                            self.graph[trajet.depart][trajet.arrivee] = trajet.duration()

    def __repr__(self):
        response = ''
        for key in sorted(self.graph.keys()):
            response += '- ' + key + ' ------------------ \n'
            for dest in self.graph[key]:
                response += "   " + dest + "  " + str(self.graph[key][dest]) + '\n'
        return response    

    def plot(self):
        G = nx.Graph()
        
        for orig in self.graph.keys() :
            for dest,weight in self.graph[orig].items():
                G.add_edge(orig,dest,weight=weight.seconds)
        pos = nx.spring_layout(G,k=10,iterations=3)
        nx.draw_networkx_nodes(G, pos, node_size=100)
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(data=True), width=0.1)
        nx.draw_networkx_labels(G, pos, font_size=2, font_family="sans-serif")
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=1)

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.savefig('plt/img.png',dpi=600)

    def add_station(self, origin:str, destinations:dict, duration):
        pass
    
    def find_paths(self, orig, dest):
        pass

    def quickest_path(self, orig, dest):
        pass

if __name__ == '__main__' : 
    graph = StationsGraph(load_graph=True)

    print(graph)
    graph.plot()

    with open('__pycache__/graph_backup.pickle','wb') as f :
        pickle.dump(graph,f)