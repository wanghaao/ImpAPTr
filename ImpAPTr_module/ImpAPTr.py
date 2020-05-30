<<<<<<< HEAD
import copy

from math import log

import numpy as np


class Node(object):
    def __init__(self):
        self.parent = None
        self.children = []
        self.path = []
        self.pruned = False
        self.base_pruned = False

        self.rightmost = False

        self.fail_number = [0, 0]
        self.request_number = [0, 0]
        self.impact_factor = 0
        self.contribution_power = 0
        self.diversity_power = 0

        self.rank = [0, 0]


def ImpAPTr_main(previous, current, dimension, previous_counter, current_counter):
    return create_pruning_tree(previous, current, dimension, previous_counter, current_counter)


# Impact Analysis based on Pruning Tree search
def create_pruning_tree(previous, current, dimension, previous_counter, current_counter):
    root_node = Node()

    root_node.rightmost = True
    root_node.impact_factor = - 1.0
    root_node.diversity_power = - 1.0
    root_node.request_number = [0, 0]
    root_node.fail_number = [0, 0]

    layer_limit = 2

    shape = np.asarray(previous).shape

    zero_layer_pruned = []
    create_node_next_layer(root_node, dimension, shape, previous, current, previous_counter, current_counter,
                           zero_layer_pruned)

    layer_nodes = []
    for child in root_node.children:
        layer_nodes.append(child)

    results_all_layers = []

    first_layer_pruned = []
    for child in root_node.children:
        if child.base_pruned:
            first_layer_pruned.append(child.path[0])

    bfs_search(layer_nodes, dimension, shape, previous, current, previous_counter,
               current_counter, layer_limit, results_all_layers, first_layer_pruned)

    return results_all_layers


def bfs_search(next_layer, dimension, shape, previous_ndarray, current_ndarray, previous_counter,
               current_counter, layer_limit, results_all_layers, first_layer_pruned):
    if len(next_layer) == 0:
        return
    if layer_limit == 0:
        return
    pruned_nodes_path = []
    not_pruned_nodes = []
    for node in next_layer:
        if node.pruned:
            pruned_nodes_path.append(node.path)
        else:
            not_pruned_nodes.append(node)

    next_layer_nodes = []
    current_layer_nodes = []

    # rightmost
    if len(not_pruned_nodes) > 0:
        not_pruned_nodes[-1].rightmost = True
    redundancy_for_nodes = []
    for not_node in not_pruned_nodes:
        if not_node.path in pruned_nodes_path:
            not_node.pruned = True

        if not_node.path in redundancy_for_nodes:
            not_node.pruned = True
        else:
            redundancy_for_nodes.append(not_node.path)

        if not not_node.pruned:
            current_layer_nodes.append(not_node)
            if layer_limit > 1:
                create_node_next_layer(not_node, dimension, shape, previous_ndarray, current_ndarray,
                                       previous_counter,
                                       current_counter, first_layer_pruned)
        if not_node.rightmost:
            if len(current_layer_nodes) > 0:
                if len(current_layer_nodes[-1].children) > 0:
                    current_layer_nodes[-1].children[-1].rightmost = True

            result_current_layer = result_nodes_for_current_layer(current_layer_nodes)

            results_all_layers.append(result_current_layer)
            current_layer_nodes.clear()
            pruned_nodes_path.clear()

        for ch in not_node.children:
            next_layer_nodes.append(ch)
    # BFS
    bfs_search(next_layer_nodes, dimension, shape, previous_ndarray, current_ndarray, previous_counter,
               current_counter, layer_limit - 1, results_all_layers, first_layer_pruned)


def result_nodes_for_current_layer(current_layer_nodes):
    layer_nodes = []
    for node in current_layer_nodes:
        # filtering
        if node.contribution_power > 0.0001:
            layer_nodes.append(node)
    return layer_nodes


def JS_divergence(p, q):
    # JS_divergence
    if p == 0.0 and q == 0.0:
        return 0.0
    if p == 0.0 and q != 0.0:
        return 0.5 * q
    if p != 0.0 and q == 0.0:
        return 0.5 * p
    divergence = 0.5 * (p * log((2 * p) / (p + q)) + q * log((2 * q) / (p + q)))
    return divergence


def create_node_next_layer(current_node, dimension, shape, previous_ndarray, current_ndarray, previous_counter,
                           current_counter, first_layer_pruned):
    current_path = current_node.path
    selectable_elements = selectable_element_path(current_path, dimension, shape, first_layer_pruned)
    children_number = len(selectable_elements)

    for i in range(children_number):
        child = Node()
        path = []
        for el in current_path:
            path.append(el)
        path.append(selectable_elements[i])
        path.sort(key=lambda ele: ele[0])
        child.path = path
        child.parent = current_node
        child.pruned = False

        fail_number, request_number, contribution_power, impact_factor = aggregate_data_element(
            child.path, previous_ndarray,
            current_ndarray,
            previous_counter,
            current_counter)

        child.fail_number = fail_number
        child.request_number = request_number
        child.impact_factor = impact_factor
        child.contribution_power = - contribution_power
        if request_number[0] == 0 or request_number[1] == 0:
            diversity_power = 0.0
        else:
            diversity_power = JS_divergence((request_number[0] - fail_number[0]) / request_number[0],
                                            (request_number[1] - fail_number[1]) / request_number[1])
        child.diversity_power = diversity_power

        pruned_tag, base_pruned = whether_pruned(current_node, child, current_counter)
        child.base_pruned = base_pruned
        if pruned_tag:
            child.pruned = True
        current_node.children.append(child)

    if current_node.rightmost:
        if len(current_node.children) == 0:
            node = search_exists_child(current_node)
            if node is not None:
                node.rightmost = True
        else:
            current_node.children[-1].rightmost = True


def selectable_element_path(current_path, dimension, shape, first_layer_pruned):
    if len(current_path) == 0:
        selected_dimension = []
    else:
        selected_dimension = np.asarray(current_path)[:, 0]
    selectable_dimension = []

    for axis in range(dimension):
        if axis not in selected_dimension:
            selectable_dimension.append(axis)

    selectable_elements = []
    for axis in selectable_dimension:
        for index in range(np.asarray(shape)[axis]):
            el = [axis, index]
            if el not in first_layer_pruned:
                selectable_elements.append(el)
    return selectable_elements


def whether_pruned(parent, child, current_counter):
    if parent.parent is not None:
        if abs(child.request_number[1] - parent.request_number[1]) / parent.request_number[1] < 0.05:
            if abs(child.impact_factor - parent.impact_factor) / abs(parent.impact_factor) < 0.05:
                return True, False

    if child.request_number[1] < sum(current_counter) * 0.0005:
        return True, True

    if child.impact_factor >= 0:
        return True, False

    return False, False


def search_exists_child(child):
    parent = child.parent
    children = copy.deepcopy(parent.children)
    children.reverse()
    for ch in children:
        if len(ch.children) != 0:
            ch.rightmost = True
            return ch


def aggregate_data_element(element_path, previous, current, previous_counter, current_counter):
    previous_ndarray = np.asarray(previous)
    current_ndarray = np.asarray(current)
    gap_dimension = 0
    sub_previous_ndarray = previous_ndarray[:]
    sub_current_ndarray = current_ndarray[:]

    cp_element_path = copy.deepcopy(element_path)
    cp_element_path.sort(key=lambda element: element[0])
    start = 0
    end = cp_element_path[-1][0] + 1
    for axis_index in cp_element_path:
        for sub_dim in range(start, end, 1):
            if axis_index[0] == sub_dim:
                if gap_dimension == 0:
                    sub_previous_ndarray = sub_previous_ndarray[axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[axis_index[1]]

                elif gap_dimension == 1:
                    sub_previous_ndarray = sub_previous_ndarray[:, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, axis_index[1]]

                elif gap_dimension == 2:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, axis_index[1]]

                elif gap_dimension == 3:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, axis_index[1]]

                elif gap_dimension == 4:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, axis_index[1]]

                elif gap_dimension == 5:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, :, axis_index[1]]
                elif gap_dimension == 6:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, :, :, axis_index[1]]
                elif gap_dimension == 7:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, :, :, :, axis_index[1]]
                start = sub_dim + 1

            elif axis_index[0] > sub_dim:
                gap_dimension += 1

            else:
                break

    sub_current_ndarray = np.asarray(sub_current_ndarray)
    sub_previous_ndarray = np.asarray(sub_previous_ndarray)
    dim = sub_previous_ndarray.ndim

    if dim == 1:
        fail_previous = sub_previous_ndarray[0]
        fail_actual = sub_current_ndarray[0]
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 2:
        fail_previous = np.sum(sub_previous_ndarray[:, 0])
        fail_actual = np.sum(sub_current_ndarray[:, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 3:
        fail_previous = np.sum(sub_previous_ndarray[:, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 4:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 5:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 6:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 7:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, :, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, :, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)

    fail_number = [fail_previous, fail_actual]
    request_number = [request_previous, request_actual]

    if request_actual == 0 or sum(current_counter) == request_actual:  # 1.不存在请求  2.该维度只有该值有请求
        current_impact_factor = 0
    else:
        current_impact_factor = (current_counter[1]) / sum(current_counter) - (
                current_counter[1] - (request_actual - fail_actual)) / (sum(current_counter) - request_actual)

    if request_previous == 0 or sum(previous_counter) == request_previous:
        previous_impact_factor = 0
    else:
        previous_impact_factor = (previous_counter[1]) / sum(previous_counter) - (
                previous_counter[1] - (request_previous - fail_previous)) / (
                                         sum(previous_counter) - request_previous)

    contribution_power = current_impact_factor - previous_impact_factor
    return fail_number, request_number, contribution_power, current_impact_factor
=======
import copy

from math import log

import numpy as np


class Node(object):
    def __init__(self):
        self.parent = None
        self.children = []
        self.path = []
        self.pruned = False
        self.base_pruned = False

        self.rightmost = False

        self.fail_number = [0, 0]
        self.request_number = [0, 0]
        self.impact_factor = 0
        self.contribution_power = 0
        self.diversity_power = 0

        self.rank = [0, 0]


def ImpAPTr_main(previous, current, dimension, previous_counter, current_counter):
    return create_pruning_tree(previous, current, dimension, previous_counter, current_counter)


# Impact Analysis based on Pruning Tree search
def create_pruning_tree(previous, current, dimension, previous_counter, current_counter):
    root_node = Node()

    root_node.rightmost = True
    root_node.impact_factor = - 1.0
    root_node.diversity_power = - 1.0
    root_node.request_number = [0, 0]
    root_node.fail_number = [0, 0]

    layer_limit = 2

    shape = np.asarray(previous).shape

    zero_layer_pruned = []
    create_node_next_layer(root_node, dimension, shape, previous, current, previous_counter, current_counter,
                           zero_layer_pruned)

    layer_nodes = []
    for child in root_node.children:
        layer_nodes.append(child)

    results_all_layers = []

    first_layer_pruned = []
    for child in root_node.children:
        if child.base_pruned:
            first_layer_pruned.append(child.path[0])

    bfs_search(layer_nodes, dimension, shape, previous, current, previous_counter,
               current_counter, layer_limit, results_all_layers, first_layer_pruned)

    return results_all_layers


def bfs_search(next_layer, dimension, shape, previous_ndarray, current_ndarray, previous_counter,
               current_counter, layer_limit, results_all_layers, first_layer_pruned):
    if len(next_layer) == 0:
        return
    if layer_limit == 0:
        return
    pruned_nodes_path = []
    not_pruned_nodes = []
    for node in next_layer:
        if node.pruned:
            pruned_nodes_path.append(node.path)
        else:
            not_pruned_nodes.append(node)

    next_layer_nodes = []
    current_layer_nodes = []

    # rightmost
    if len(not_pruned_nodes) > 0:
        not_pruned_nodes[-1].rightmost = True
    redundancy_for_nodes = []
    for not_node in not_pruned_nodes:
        if not_node.path in pruned_nodes_path:
            not_node.pruned = True

        if not_node.path in redundancy_for_nodes:
            not_node.pruned = True
        else:
            redundancy_for_nodes.append(not_node.path)

        if not not_node.pruned:
            current_layer_nodes.append(not_node)
            if layer_limit > 1:
                create_node_next_layer(not_node, dimension, shape, previous_ndarray, current_ndarray,
                                       previous_counter,
                                       current_counter, first_layer_pruned)
        if not_node.rightmost:
            if len(current_layer_nodes) > 0:
                if len(current_layer_nodes[-1].children) > 0:
                    current_layer_nodes[-1].children[-1].rightmost = True

            result_current_layer = result_nodes_for_current_layer(current_layer_nodes)

            results_all_layers.append(result_current_layer)
            current_layer_nodes.clear()
            pruned_nodes_path.clear()

        for ch in not_node.children:
            next_layer_nodes.append(ch)
    # BFS
    bfs_search(next_layer_nodes, dimension, shape, previous_ndarray, current_ndarray, previous_counter,
               current_counter, layer_limit - 1, results_all_layers, first_layer_pruned)


def result_nodes_for_current_layer(current_layer_nodes):
    layer_nodes = []
    for node in current_layer_nodes:
        # filtering
        if node.contribution_power > 0.0001:
            layer_nodes.append(node)
    return layer_nodes


def JS_divergence(p, q):
    # JS_divergence
    if p == 0.0 and q == 0.0:
        return 0.0
    if p == 0.0 and q != 0.0:
        return 0.5 * q
    if p != 0.0 and q == 0.0:
        return 0.5 * p
    divergence = 0.5 * (p * log((2 * p) / (p + q)) + q * log((2 * q) / (p + q)))
    return divergence


def create_node_next_layer(current_node, dimension, shape, previous_ndarray, current_ndarray, previous_counter,
                           current_counter, first_layer_pruned):
    current_path = current_node.path
    selectable_elements = selectable_element_path(current_path, dimension, shape, first_layer_pruned)
    children_number = len(selectable_elements)

    for i in range(children_number):
        child = Node()
        path = []
        for el in current_path:
            path.append(el)
        path.append(selectable_elements[i])
        path.sort(key=lambda ele: ele[0])
        child.path = path
        child.parent = current_node
        child.pruned = False

        fail_number, request_number, contribution_power, impact_factor = aggregate_data_element(
            child.path, previous_ndarray,
            current_ndarray,
            previous_counter,
            current_counter)

        child.fail_number = fail_number
        child.request_number = request_number
        child.impact_factor = impact_factor
        child.contribution_power = - contribution_power
        if request_number[0] == 0 or request_number[1] == 0:
            diversity_power = 0.0
        else:
            diversity_power = JS_divergence((request_number[0] - fail_number[0]) / request_number[0],
                                            (request_number[1] - fail_number[1]) / request_number[1])
        child.diversity_power = diversity_power

        pruned_tag, base_pruned = whether_pruned(current_node, child, current_counter)
        child.base_pruned = base_pruned
        if pruned_tag:
            child.pruned = True
        current_node.children.append(child)

    if current_node.rightmost:
        if len(current_node.children) == 0:
            node = search_exists_child(current_node)
            if node is not None:
                node.rightmost = True
        else:
            current_node.children[-1].rightmost = True


def selectable_element_path(current_path, dimension, shape, first_layer_pruned):
    if len(current_path) == 0:
        selected_dimension = []
    else:
        selected_dimension = np.asarray(current_path)[:, 0]
    selectable_dimension = []

    for axis in range(dimension):
        if axis not in selected_dimension:
            selectable_dimension.append(axis)

    selectable_elements = []
    for axis in selectable_dimension:
        for index in range(np.asarray(shape)[axis]):
            el = [axis, index]
            if el not in first_layer_pruned:
                selectable_elements.append(el)
    return selectable_elements


def whether_pruned(parent, child, current_counter):
    if parent.parent is not None:
        if abs(child.request_number[1] - parent.request_number[1]) / parent.request_number[1] < 0.05:
            if abs(child.impact_factor - parent.impact_factor) / abs(parent.impact_factor) < 0.05:
                return True, False

    if child.request_number[1] < sum(current_counter) * 0.0005:
        return True, True

    if child.impact_factor >= 0:
        return True, False

    return False, False


def search_exists_child(child):
    parent = child.parent
    children = copy.deepcopy(parent.children)
    children.reverse()
    for ch in children:
        if len(ch.children) != 0:
            ch.rightmost = True
            return ch


def aggregate_data_element(element_path, previous, current, previous_counter, current_counter):
    previous_ndarray = np.asarray(previous)
    current_ndarray = np.asarray(current)
    gap_dimension = 0
    sub_previous_ndarray = previous_ndarray[:]
    sub_current_ndarray = current_ndarray[:]

    cp_element_path = copy.deepcopy(element_path)
    cp_element_path.sort(key=lambda element: element[0])
    start = 0
    end = cp_element_path[-1][0] + 1
    for axis_index in cp_element_path:
        for sub_dim in range(start, end, 1):
            if axis_index[0] == sub_dim:
                if gap_dimension == 0:
                    sub_previous_ndarray = sub_previous_ndarray[axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[axis_index[1]]

                elif gap_dimension == 1:
                    sub_previous_ndarray = sub_previous_ndarray[:, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, axis_index[1]]

                elif gap_dimension == 2:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, axis_index[1]]

                elif gap_dimension == 3:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, axis_index[1]]

                elif gap_dimension == 4:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, axis_index[1]]

                elif gap_dimension == 5:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, :, axis_index[1]]
                elif gap_dimension == 6:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, :, :, axis_index[1]]
                elif gap_dimension == 7:
                    sub_previous_ndarray = sub_previous_ndarray[:, :, :, :, :, :, :, axis_index[1]]
                    sub_current_ndarray = sub_current_ndarray[:, :, :, :, :, :, :, axis_index[1]]
                start = sub_dim + 1

            elif axis_index[0] > sub_dim:
                gap_dimension += 1

            else:
                break

    sub_current_ndarray = np.asarray(sub_current_ndarray)
    sub_previous_ndarray = np.asarray(sub_previous_ndarray)
    dim = sub_previous_ndarray.ndim

    if dim == 1:
        fail_previous = sub_previous_ndarray[0]
        fail_actual = sub_current_ndarray[0]
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 2:
        fail_previous = np.sum(sub_previous_ndarray[:, 0])
        fail_actual = np.sum(sub_current_ndarray[:, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 3:
        fail_previous = np.sum(sub_previous_ndarray[:, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 4:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 5:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 6:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)
    elif dim == 7:
        fail_previous = np.sum(sub_previous_ndarray[:, :, :, :, :, :, 0])
        fail_actual = np.sum(sub_current_ndarray[:, :, :, :, :, :, 0])
        request_previous = np.sum(sub_previous_ndarray)
        request_actual = np.sum(sub_current_ndarray)

    fail_number = [fail_previous, fail_actual]
    request_number = [request_previous, request_actual]

    if request_actual == 0 or sum(current_counter) == request_actual:  # 1.不存在请求  2.该维度只有该值有请求
        current_impact_factor = 0
    else:
        current_impact_factor = (current_counter[1]) / sum(current_counter) - (
                current_counter[1] - (request_actual - fail_actual)) / (sum(current_counter) - request_actual)

    if request_previous == 0 or sum(previous_counter) == request_previous:
        previous_impact_factor = 0
    else:
        previous_impact_factor = (previous_counter[1]) / sum(previous_counter) - (
                previous_counter[1] - (request_previous - fail_previous)) / (
                                         sum(previous_counter) - request_previous)

    contribution_power = current_impact_factor - previous_impact_factor
    return fail_number, request_number, contribution_power, current_impact_factor
>>>>>>> 59b5fb7231d56e643921b16307d067d95b2c5b41
