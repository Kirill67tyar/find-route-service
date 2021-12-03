"""

----------------------------------------- ForeignKey ---------------------------------------
аттрибу on_delete для ForeignKey

on_delete=CASCADE - говорит о том, что все записи будут удаляться каскадом,
т.е. если из главной таблицы удалить запись, то все записи, которые на нее ссылаются будут удалены

on_delete=PROTECT - говорит о том, что запись не может быть удалена, если на нее ссылается хоть одна запись
в другой таблице

on_delete=SET_DEFAULT - даёт возможность задать запись по умолчанию

on_delete=SET_NULL - задаёт NULL для всех дочерних записей, при удалении родительских
но чтобы задать SET_NULL нужно в определении этого поля задать также blank=True, null=True

    blank=True - говорит, что это поле можно не заполнять, когда мы создаём какую-то строчку
    null=True - говорит о том, что это поле может быть пустым, там может быть ничего



"""


graph1 = {
    'A': {'B', 'S'},
    'B': {'A'},
    'C': {'D', 'E', 'F', 'S'},
    'D': {'C'},
    'E': {'C', 'H'},
    'F': {'C', 'G'},
    'G': {'F', 'S'},
    'H': {'E', 'G'},
    'S': {'A', 'C', 'G'}
}


def dfs_paths(graph, start, goal):
    stack = [(start, [start, ])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_, ]))


f = dfs_paths(graph1, 'A', 'F')
print(f.__next__())                             # ['A', 'S', 'C', 'F']
print(dfs_paths(graph1, 'A', 'F').__next__())   # ['A', 'S', 'C', 'F']
print(list(dfs_paths(graph1, 'A', 'F')))        # [['A', 'S', 'C', 'F'], ['A', 'S', 'C', 'E', 'H', 'G', 'F'], ['A', 'S', 'G', 'F']]
print(f)                                        # <generator object dfs_path at 0x7f92a5d6bf90>

print(range(1,4), type(range(1,4)))             # range(1, 4) <class 'range'>
print(list(range(1,4)))                         # [1, 2, 3]
