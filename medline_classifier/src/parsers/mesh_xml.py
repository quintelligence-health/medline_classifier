import sys, traceback
import sets
from lxml import etree


top_map = {
    'A': 'Anatomy',
    'B': 'Organisms',
    'C': 'Diseases',
    'D': 'Chemicals and Drugs',
    'E': 'Analytical, Diagnostic and Therapeutic Techniques and Equipment',
    'F': 'Psychiatry and Psychology',
    'G': 'Phenomena and Processes',
    'H': 'Disciplines and Occupations',
    'I': 'Anthropology, Education, Sociology and Social Phenomena',
    'J': 'Technology, Industry, Agriculture',
    'K': 'Humanities',
    'L': 'Information Science',
    'M': 'Named Groups',
    'N': 'Health Care',
    'V': 'Publication Characteristics',
    'Z': 'Geographicals'
}

class MeshNode:

    def __init__(self, tree, descriptor_ui, name, tree_number):
        self._tree = tree
        self.descriptor_ui = descriptor_ui
        self.name = name
        self.tree_number = tree_number
        self._child_map = {}
        self._parent = None

    def getCategoryPaths(self):
        if self._getTreeNumberLength(self.descriptor_ui) == 1:
            return [[self.name]]
        duplicates = self._tree.getNodesByDescriptor(self.descriptor_ui)

        result = []
        paths = [[self.name]]
        for node in duplicates:
            parent = node._parent
            if parent is not None:
                parent_paths = parent.getCategoryPaths()
                for path1 in parent_paths:
                    for path2 in paths:
                        result.append(path1 + path2)
        return result

    def addChild(self, child):
        child._parent = self

        if len(self.tree_number) == 0:
            # we are dealing with the artificial root category
            if len(child.tree_number) != 1:
                raise ValueError('Tried to add invalid child to root: ' + child.tree_number + '!')
            self._child_map[child.tree_number] = child
        elif len(self.tree_number) == 1:
            # we are dealing with one of the top categories
            if len(child.tree_number) == 1 or child.tree_number.count('.') > 0:
                raise ValueError('Tried to add invalid child to top category: ' + child.tree_number + '!')
            self._child_map[child.tree_number[1:]] = child
        else:
            # we are dealing with a regular category
            tree_list = self.tree_number.split('.')
            child_tree_list = child.tree_number.split('.')
            if len(child_tree_list) != len(tree_list) + 1:
                raise ValueError('Invalid length of child tree list: ' + child.tree_number)
            self._child_map[child_tree_list[-1]] = child

    def canInsert(self, tree_number):
        if self._getTreeNumberLength(tree_number) == self._getTreeNumberLength(self.tree_number) + 1:
            return True
        elif self._getTreeNumberLength(tree_number) > self._getTreeNumberLength(self.tree_number) + 1:
            child_id = self._getChildIdFromTn(tree_number)
            if child_id not in self._child_map:
                return False
            return self._child_map[child_id].canInsert(tree_number)
        else:
            return False


    def insert(self, node):
        child_id = self._getChildId(node)
        if child_id in self._child_map:
            self._child_map[child_id].insert(node)
        else:
            self.addChild(node)

    def _getChildId(self, node):
        return self._getChildIdFromTn(node.tree_number)

    def _getChildIdFromTn(self, tree_number):
        if len(self.tree_number) == 0:
            return tree_number[0]
        elif len(self.tree_number) == 1:
            dot_idx = tree_number.find('.')
            if dot_idx == -1:
                dot_idx = len(tree_number)
            return tree_number[1:dot_idx]
        else:
            subtree_number = tree_number[len(self.tree_number)+1:]
            dot_idx = subtree_number.find('.')
            if dot_idx == -1:
                dot_idx = len(subtree_number)
            return subtree_number[:dot_idx]

    def _getTreeNumberLength(self, tn):
        if len(tn) == 0:
            return 0
        elif len(tn) == 1:
            return 1
        else:
            return tn.count('.') + 2


class MeshParser:

    def __init__(self):
        self._root = MeshNode(self, '', 'Top', '')
        self._node_map = {'': [self._root]}

        for code, name in top_map.iteritems():
            node = MeshNode(self, code, name, code)
            self._root.insert(node)

    def getNodesByDescriptor(self, descriptor_ui):
        return self._node_map[descriptor_ui]

    def getCategoryPaths(self, descriptor_ui):
        paths = self._node_map[descriptor_ui][0].getCategoryPaths()
        path_set = sets.Set(['/'.join(path) for path in paths])
        result = [path for path in path_set]
        return result

    def parse(self, fname):
        tree = etree.parse(fname)
        descriptors = tree.findall('DescriptorRecord')

        print 'parsed ' + str(len(descriptors)) + ' descriptors'

        non_tree_uis = []
        pending_nodes = []
        for descriptorN, descriptor in enumerate(descriptors):
            if descriptorN % 10000 == 0:
                print 'parsing descriptor ' + str(descriptorN)

            id = None
            try:
                id_el = descriptor.find('DescriptorUI')
                id = id_el.text

                if id is None or id == '':
                    raise ValueError('Could not find the DescriptorUI!')

                name_el = descriptor.find('DescriptorName/String')
                name = name_el.text

                if name is None or name == '':
                    raise ValueError('Could not find name of descriptor: ' + id)

                tree_numbers_el = descriptor.find('TreeNumberList')
                if tree_numbers_el is None:
                    print 'DescriptorUI ' + id + ' does not have a tree number!'
                    non_tree_uis.append(id)
                    continue

                tree_number_els = tree_numbers_el.findall('TreeNumber')
                for tree_number_el in tree_number_els:
                    tree_number = tree_number_el.text
                    if tree_number is None or tree_number == '':
                        raise ValueError('Could not find tree number of DescriptorUI: ' + id + '!')

                    node = MeshNode(self, id, name, tree_number)

                    if self._canInsert(node):
                        self._insert(node)
                    else:
                        pending_nodes.append(node)
            except:
                print 'exception while processing descriptor number ' + str(descriptorN) + ', DescriptorUI: ' + str(id)
                traceback.print_exc(file=sys.stdout)
                exit(1)
        # cleanup the pending nodes
        print 'finished reading descriptors, ' + str(len(pending_nodes)) + ' nodes still pending'
        iterN = 0
        while len(pending_nodes) > 0:
            print 'iteration ' + str(iterN)
            curr_len = len(pending_nodes)

            nodeN = 0
            while nodeN < len(pending_nodes):
                node = pending_nodes[nodeN]
                if self._canInsert(node):
                    self._insert(node)
                    pending_nodes.pop(nodeN)
                else:
                    nodeN += 1

            if len(pending_nodes) == curr_len:
                raise ValueError('Failed to make progress clearing pending nodes!')
            iterN += 1
        # done
        print 'done'
        print str(len(non_tree_uis)) + ' records do not have a tree number'

    def _canInsert(self, node):
        tree_number = node.tree_number
        return self._root.canInsert(tree_number)

    def _insert(self, node):
        self._root.insert(node)
        # the same descriptor_ui can point to different nodes
        # because a single record in MESH can have multiple tree numbers
        if node.descriptor_ui not in self._node_map:
            self._node_map[node.descriptor_ui] = []
        self._node_map[node.descriptor_ui].append(node)
