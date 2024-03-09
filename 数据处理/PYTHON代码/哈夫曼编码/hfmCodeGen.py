"""
构造哈夫曼树和解码哈夫曼
"""
from dataclasses import dataclass
from typing import Any
import re

@dataclass
class TreeStru:
    wights: int
    left_node: Any=None
    right_node: Any=None

@dataclass
class T:
    left_node: Any=None
    right_node: Any=None

@dataclass
class QueueNodeStru:
    node_content: Any
    wights: int

def treeFlat(hfm_tree:TreeStru):
    hfm_tree_str = str(hfm_tree)
    hfm_tree_str = re.sub("left_node=","",re.sub("right_node=","",re.sub(r"wights=\d+,","",re.sub(r"TreeStru","T",hfm_tree_str))))
    hfm_tree_str = hfm_tree_str.replace("( ","(")
    hfm_tree_str = hfm_tree_str.replace(", ",",")
    return hfm_tree_str+"\n"

def dictFlat(hfm_dict:dict):
    hfm_dict_str = str(hfm_dict)
    hfm_dict_str = hfm_dict_str.replace("', '","','")
    hfm_dict_str = hfm_dict_str.replace("': '","':'")
    return hfm_dict_str+"\n"

def construct_tree(node_arry: list) -> list:
    if len(node_arry) > 1:
        # 队列排序
        node_arry.sort(key=lambda x: (x.wights), reverse=False)
        # 获得队列中最小的两个
        node_min_1 = node_arry[0]
        node_min_2 = node_arry[1]

        # 使用最小的两个节点构建树
        new_wights = node_min_1.wights + node_min_2.wights
        new_tree = TreeStru(
            wights=new_wights,
            left_node=node_min_1.node_content,
            right_node=node_min_2.node_content,
        )
        # 去掉队列中最小的两个节点，并加入新构造的树
        new_node_arry = node_arry[2:]
        new_node_arry.append(QueueNodeStru(node_content=new_tree, wights=new_wights))

        node_arry = construct_tree(new_node_arry)
    return node_arry

def get_hfm_code_dict(node_dict: dict, root_node: Any, path: str) -> dict:
    if getattr(root_node, "left_node", None) is not None:
        left_node_path = path + "0"
        get_hfm_code_dict(node_dict, root_node.left_node, left_node_path)
        right_node_path = path + "1"
        get_hfm_code_dict(node_dict, root_node.right_node, right_node_path)
    else:
        node_dict[root_node] = path
    return node_dict

def dict_tree_hfm(words_str: list):
    pl = {}
    # 计算字符串中每个字符出现的频率
    for i in words_str:
        if i not in pl.keys():
            pl[i] = words_str.count(i)
    # 构建节点队列
    node_arry = [
        QueueNodeStru(node_content=key, wights=value) for key, value in pl.items()
    ]
    # 生成只有一个节点的队列，该节点就是 霍夫曼树
    node_arry = construct_tree(node_arry)
    hfm_tree = node_arry[0].node_content
    node_dict = get_hfm_code_dict({}, hfm_tree, "")
    return (node_dict,eval(treeFlat(hfm_tree)))

def encode_hfm(words_list: list, node_dict: dict):
    code_str = ""
    # 用霍夫曼树压缩字符串，获得编码
    for i in words_list:
        code_str = code_str + node_dict[i]
    return code_str

def decode_hfm(hfm_code_str: str, hfm_tree: TreeStru):
    htm_tree_backup = hfm_tree
    words_str = []
    for i in hfm_code_str:
        if i == "0":
            hfm_tree = hfm_tree.left_node
            if getattr(hfm_tree, "left_node", None) is None:
                words_str.append(hfm_tree)
                hfm_tree = htm_tree_backup

        elif i == "1":
            hfm_tree = hfm_tree.right_node
            # 根据霍夫曼的构成原理，左子树或右子树若存在必定结对存在
            if getattr(hfm_tree, "left_node", None) is None:
                words_str.append(hfm_tree)
                hfm_tree = htm_tree_backup
    return words_str

