import rdflib
from rdflib import Graph, Namespace, Literal, BNode, URIRef
from rdflib import RDF, RDFS, XSD
from rdflib.namespace import SKOS, FOAF, RDF

g = Graph()
uri = 'http://example.org/'
ns = Namespace('http://example.org/')
owl = Namespace('http://www.w3.org/2002/07/owl#')

def clean_uri(label):
    return label.replace(' ', '').replace('\'', '').replace('\"', '').replace('\‘', '').replace('\’', '').replace('\“', '').replace('\”', '').replace('\\', '').replace('(', '').replace(')', '').replace('.', '').replace('+', '').replace('%', '').replace('&', '').replace('@', '').replace('$', '').replace('!', '').replace('?', '').replace(',', '')
    #return ''.join([i for i in label if (i >= 'a' and i <= 'a') or (i >= 'A' and i <= 'Z') or (i >= '0' and i <= '9')])

with open('Data/en_instance.txt', 'r') as f: # 54093
    ins_dict_en = {}
    for label in f.readlines():
        label = label.strip()
        node = URIRef(uri + clean_uri(label))
        g.add((node, RDFS.label, Literal(label)))
        ins_dict_en[label] = node

with open('Data/fr_instance.txt', 'r') as f: # 38962
    ins_dict_fr = {}
    for label in f.readlines():
        label = label.strip()
        node = URIRef(uri + clean_uri(label))
        g.add((node, RDFS.label, Literal(label)))
        ins_dict_fr[label] = node

with open('Data/class_list.txt', 'r') as f: # 761
    class_dict = {}
    for label in f.readlines():
        label = label.strip()
        node = URIRef(uri + clean_uri(label))
        g.add((node, RDF.type, RDFS.Class))
        g.add((node, RDFS.label, Literal(label)))
        class_dict[label] = node

with open('Data/property_list.txt', 'r') as f: # 2865
    prop_dict = {}
    for label in f.readlines():
        label = label.strip()
        node = URIRef(uri + clean_uri(label))
        g.add((node, RDF.type, RDF.Property))
        g.add((node, RDFS.label, Literal(label)))
        prop_dict[label] = node
        
with open('Data/CL_link.txt', 'r') as f:
    for line in f.readlines():
        ins_label_en, ins_label_fr = line.strip().split('\t\t')
        g.add((ins_dict_en[ins_label_en], owl.sameAs, ins_dict_fr[ins_label_fr]))
    
with open('Data/subClassOf.txt', 'r') as f:
    for line in f.readlines():
        class_label, class_super_label = line.strip().split('\t\t')
        g.add((class_dict[class_label], RDFS.subClassOf, class_dict[class_super_label]))
    
with open('Data/domain.txt', 'r') as f:
    for line in f.readlines():
        prop_label, class_label = line.strip().split('\t\t')
        g.add((prop_dict[prop_label], RDFS.domain, class_dict[class_label]))
    
with open('Data/range.txt', 'r') as f:
    for line in f.readlines():
        prop_label, range_label = line.strip().split('\t\t')
        if range_label[:4] == 'xsd:':
            g.add((prop_dict[prop_label], RDFS.range, getattr(XSD, range_label[4:])))
        elif range_label[:4] == 'rdf:':
            g.add((prop_dict[prop_label], RDFS.range, getattr(RDF, range_label[4:])))
        elif range_label[:5] == 'skos:':
            g.add((prop_dict[prop_label], RDFS.range, getattr(SKOS, range_label[5:])))
        else:
            # 自定义的 Datatype 在定义 class 的时候已经定义
            g.add((prop_dict[prop_label], RDFS.range, class_dict[class_label]))
    
with open('Data/en_instanceOf.txt', 'r') as f:
    for line in f.readlines():
        ins_label, class_label = line.strip().split('\t\t')
        g.add((ins_dict_en[ins_label], RDF.type, class_dict[class_label]))
    
with open('Data/fr_instanceOf.txt', 'r') as f:
    for line in f.readlines():
        ins_label, class_label = line.strip().split('\t\t')
        g.add((ins_dict_fr[ins_label], RDF.type, class_dict[class_label]))
    
with open('Data/en_object_triples.txt', 'r') as f:
    for line in f.readlines():
        ins_label, prop_label, ins2_label = line.strip().split('\t\t')
        g.add((ins_dict_en[ins_label], prop_dict[prop_label], ins_dict_en[ins2_label]))
    
with open('Data/fr_object_triples.txt', 'r') as f:
    for line in f.readlines():
        ins_label, prop_label, ins2_label = line.strip().split('\t\t')
        g.add((ins_dict_fr[ins_label], prop_dict[prop_label], ins_dict_fr[ins2_label]))
    
with open('Data/en_datatype_triples.txt', 'r') as f:
    for line in f.readlines():
        ins_label, prop_label, value = line.strip().split('\t\t')
        g.add((ins_dict_en[ins_label], prop_dict[prop_label], Literal(value)))
    
with open('Data/fr_datatype_triples.txt', 'r') as f:
    for line in f.readlines():
        ins_label, prop_label, value = line.strip().split('\t\t')
        g.add((ins_dict_fr[ins_label], prop_dict[prop_label], Literal(value)))
    
g.bind('ns', ns)
g.serialize('result.ttl', format='ttl')

