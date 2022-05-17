from concepts import Context

# table below taken from Noll (2016)

lattice = """
  |G|DE|ME|MP|DP|BZ|DT|
1 |X|X |X |X |X |X |X |
2 |X|X |X |X |X |  |X |
3 |X|X |X |X |  |X |  |
4 |X|X |X |X |X |  |  |
5 |X|X |X |X |  |  |  |
6 |X|X |X |  |X |  |  |
7 |X|X |  |X |X |  |  |
8 |X|X |  |X |  |  |  |
9 |X|X |X |  |  |  |  |
10|X|  |  |  |X |  |  |
11| |X |X |  |  |  |  |
12| |X |  |  |  |  |  |
13|X|  |  |  |  |  |  |
"""

c = Context.fromstring(lattice)
# print(c.intension(["MP", "DT"]))
# print(c.lattice.graphviz(view=True))
