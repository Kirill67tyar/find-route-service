from trains.models import Train


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


def get_graph2(qs) -> dict:
    graph = {}
    for train in qs:
        graph.setdefault(train.from_city_id, set())
        graph[train.from_city_id].add(train.to_city_id)
    return graph


# для Train.objects.values()
def get_graph(qs) -> dict:
    graph = {}
    for train in qs:
        graph.setdefault(train['from_city_id'], set())
        graph[train['from_city_id']].add(train['to_city_id'])
    return graph


def get_routes(request, form) -> dict:
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    traveling_time = data['traveling_time']
    cities = data['cities']
    qs = Train.objects.values()

    # # не мой вариант
    # qs2 = Train.objects.all()
    # graph2 = get_graph(qs=qs2)

    # мой вариант
    graph = get_graph(qs=qs)

    all_ways = list(dfs_paths(
        graph=graph, start=from_city.pk, goal=to_city.pk
    ))
    if not len(all_ways):
        raise ValueError('Маршрут не найден')

    if cities:
        _cities = {city.pk for city in cities}
        right_ways = []
        for route in all_ways:
            # мой вариант
            # if set(route).issuperset(_cities):
            if all(city in route for city in _cities):
                right_ways.append(route)
        if not right_ways:
            raise ValueError('Маршрут через эти города не возможен')
    else:
        right_ways = all_ways

    # поиск маршрутов, которые подходят по времени
    routes_with_right_time = []
    all_trains = {}
    for train in qs:
        all_trains.setdefault((train['from_city_id'], train['to_city_id'],), [])
        all_trains[(train['from_city_id'], train['to_city_id'],)].append(train)
    for route in right_ways:
        tmp = {
            'trains': [],
        }
        total_time = 0
        for i in range(len(route) - 1):
            train = all_trains[(route[i], route[i + 1])][0]
            total_time += train['travel_time']
            tmp['trains'].append(train)
        tmp['total_time'] = total_time
        if total_time <= traveling_time:
            routes_with_right_time.append(tmp)
    if not routes_with_right_time:
        raise ValueError('Нет маршрутов с подходящим временем')

    # сортировка маршрутов по времени
    sorted_routes = []
    if len(routes_with_right_time) == 1:
        sorted_routes = routes_with_right_time
    else:
        sorted_times = list(set([r['total_time'] for r in routes_with_right_time]))
        sorted_times.sort()
        for time in sorted_times:
            for route in routes_with_right_time:
                if route['total_time'] == time:
                    sorted_routes.append(route)

    context = {
        'form': form,
        'right_ways': right_ways,
        'sorted_routes': sorted_routes,
        'cities': {
            'from_city': from_city,
            'to_city': to_city,
        },
    }
    return context
