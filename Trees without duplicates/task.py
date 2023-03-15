import sys
from functools import total_ordering

all_names = dict()
duplicates = []


def create_node(name, parent, implicit, depth):
    node = Node(name, parent, implicit, depth)
    # if node.type == 'f':
    #     if node.name in all_names:
    #         duplicates.append(node)
    #     else:
    #         all_names[node.name] = True
    return node


@total_ordering
class Node:
    def __init__(self, full_name, parent, implicit: bool, depth):  # (f)nesto.txt
        if implicit:
            self.type = 'd'
            self.name = full_name
        else:
            self.type = full_name[1]
            self.name = full_name[3:]

        if self.type == 'd':
            self.child_list = []
            self.child_map = dict()
        self.parent = parent
        self.ls = False
        self.depth = depth

    def add_child(self, child):
        if child.make_full_name() in self.child_map:
            return
        self.child_map[child.make_full_name()] = child
        self.child_list.append(child)

    def has_child(self, child_name):
        return child_name in self.child_map

    def get_child(self, child_name):
        return self.child_map[child_name]

    def add_ls_children(self, s):
        arr = s.split()
        if self.ls:
            return

        self.ls = True
        for a in arr:
            if self.has_child(a):
                continue
            new_node = create_node(a, self, False, self.depth + 1)
            self.add_child(new_node)

    def make_full_name(self):
        return "(" + self.type + ")" + self.name

    def __eq__(self, obj):
        return self.type == obj.type and self.name == obj.name

    def __lt__(self, obj):
        if self.type == 'd' and obj.type == 'f':
            return True
        if self.type == 'f' and obj.type == 'd':
            return False
        return self.name < obj.name


fileCount = 0
dirCount = 0
tree = ""


def dfs(node: Node, depth_string):
    global fileCount, dirCount, tree
    if node.type == 'f':
        # print('f '+node.name)

        if node.name in all_names:
            duplicates.append(node)
        else:
            all_names[node.name] = True

        tree += depth_string + node.name + "\n"
        fileCount += 1
    else:
        if depth_string == "":
            tree += "/\n"
        else:
            tree += depth_string + node.name + "/\n"
        dirCount += 1

        node.child_list = sorted(node.child_list)
        for child in node.child_list:
            dfs(child, depth_string + "|-")
        if not node.ls:
            tree += depth_string + "|-?\n"


def delete_duplicates(node):
    for dupl in duplicates:
        brisi_cmd = '$ rm ' + dupl.name
        cmd = [brisi_cmd]

        dupl = dupl.parent
        keep_dupl = dupl
        depth1 = node.depth
        depth2 = dupl.depth
        cnt = 0
        total_num = 0
        while depth1 != depth2:
            if depth1 < depth2:
                depth2 -= 1
                cmd.append('$ cd ' + dupl.name)
                dupl = dupl.parent
            else:
                cnt += 1
                node = node.parent
                depth1 -= 1
            total_num += 1

        while node != dupl:
            cmd.append('$ cd ' + dupl.name)
            dupl = dupl.parent
            cnt += 1
            node = node.parent
            total_num += 2

        if keep_dupl.depth + 1 >= total_num:
            for i in range(cnt):
                print("$ cd ..")
            for i in range(len(cmd)):
                print(cmd[len(cmd)-i-1])
        else:
            cmd = [brisi_cmd]
            dupl = keep_dupl
            while dupl.depth != 0:
                cmd.append('$ cd ' + dupl.name)
                dupl = dupl.parent
            cmd.append('$ cd /')
            for i in range(len(cmd)):
                print(cmd[len(cmd)-i-1])
        node = keep_dupl


if __name__ == '__main__':
    i = 0
    last_command = ""
    root = Node("(d)root", None, False, 0)
    curr_prefix = ""
    curr_depth = 0
    curr_node: Node = root
    for line in sys.stdin:
        # if len(line) == 0:
        #     for i in range
        line = line.strip()
        #print("prefix: " + curr_prefix)
        if line == "exit":
            break
        i += 1
        if i == 1:
            continue
        if len(line) > 0 and line[0] == '$':
            command = line[2:4]
            if command == "ls":
                continue
            arg = line[5:]
            if arg == "/":   # cd /
                curr_prefix = ""
                curr_depth = 0
                curr_node = root
            elif arg == "..": # cd ..
                curr_prefix = curr_prefix[:curr_prefix.rindex("/")]
                curr_depth -= 1
                curr_node = curr_node.parent
            else:   # cd dir
                if not curr_node.has_child("(d)" + arg):
                    new_node = create_node(arg, curr_node, True, curr_depth+1)
                    curr_node.add_child(new_node)
                curr_prefix += "/" + arg
                curr_depth += 1
                curr_node = curr_node.get_child("(d)" + arg)
        else:  # result from ls
            curr_node.add_ls_children(line)

    dfs(root, "")
    print(dirCount-1)
    print(fileCount)
    print(tree[:-1])
    if len(duplicates) > 0:
        print("$ cd /")
        delete_duplicates(root)
