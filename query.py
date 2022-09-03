import rdflib
from rdflib import Graph, Namespace
from rdflib import RDF, RDFS, XSD

# SPASQL Query
# https://rdflib.readthedocs.io/en/stable/intro_to_sparql.html

ns = Namespace('http://example.org/')
g = Graph()
g.parse('./1.ttl', format = 'ttl')
g.bind('ns', ns)

# 查询中国的所有属性
# spa = '''
# SELECT DISTINCT ?alabel ?plabel
# WHERE {
#     ns:China ?p ?o .
#     ?p rdfs:label ?plabel .
#     ?o rdfs:label ?olabel .
# }
# '''
# res = g.query(spa)
# print('China:')
# for row in res:
#     print(f'{row.plabel}:\t{row.olabel}')
# print()


# 查询所有出生年份为1974年的演员
# spa = '''
# SELECT DISTINCT ?alabel
# WHERE {
#     ?a rdf:type ns:Actor .
#     ?a ns:birthYear "1974" .
#     ?a rdfs:label ?alabel
# }
# '''
# print('Actors born in 1974:')
# res = g.query(spa)
# for row in res:
#     print(f'{row.alabel}')
# print()


# 查询所有时区为China Standard Time的地方并按字符排序
# spa = '''
# SELECT DISTINCT ?alabel
# WHERE {
#     ?a ns:timeZone ?t .
#     ?a rdfs:label ?alabel .
#     FILTER (REGEX(str(?t), "China", "i"))
# }
# ORDER BY ?alabel
# '''
# res = g.query(spa)
# print('Timezone in China Standard Time:')
# for row in res:
#     print(f'{row.alabel}')
# print()




# 查询所有国家的数量
spa = '''
SELECT DISTINCT ?alabel
WHERE {
    ?a ns:profession ns:Lawyer .
    ?a ns:profession ns:Lawyer .
    ?a ns:birthPlace ns:Scotland .
    ?a rdfs:label ?alabel .
    SELECT DISTINCT ?alabel
    WHERE {
        ?a ns:birthPlace ?b .
        ?a ns:birthPlace ?b .
    }
}
'''
res = g.query(spa)
print('JS:')
for row in res:
    print(f'{row.alabel}')
print()


# spa = '''
# SELECT DISTINCT ?a
# WHERE {
#     ?a rdf:type ns:Actor .
#     ?a ns:education ns:Yale\ University .
# }
# '''
# res = g.query(spa)
# for row in res:
#     print(f'{row.a}')

# 查询所有演员
# spa = '''
# SELECT DISTINCT ?place
# WHERE {
#     ?a rdf:type ns:Actor .
#     ?a ns:birthPlace ?place .
#     ?place ns:country ns:China .
# }
# '''
# res = g.query(spa)
# for row in res:
#     print(f'{row.place}')

# spa = '''
# SELECT ?p
# WHERE {
#     ?p a rdf:Property .
# }
# '''
