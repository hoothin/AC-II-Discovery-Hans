import csv
import os

'''
获取并解密刺客信条英文文本
author:hoothin
'''
inputFile = ".\\Strings_US.strings"
outputFile = ".\\langText.csv"

huffmanTree = {}
def getHuffmanTree():
    global huffmanTree
    huffmanTemp = []
    def searchLAndR(tree, node):
        left = node[0]
        right = node[1]
        try:
            if left > 0x100:
                treeLeft = {}
                searchLAndR(treeLeft, huffmanTemp[left - 0x100])
                tree["left"] = treeLeft
            elif left != 0:
                tree["left"] = left
            if right > 0x100:
                treeRight = {}
                searchLAndR(treeRight, huffmanTemp[right - 0x100])
                tree["right"] = treeRight
            elif right != 0:
                tree["right"] = right
        except Exception as e:
            print(e)
            pass
    with open(inputFile, "rb") as fp:
        index = 0x18e4
        fp.seek(index)
        while index < 0x1a7b:
            index += 4
            leftValue = int.from_bytes(fp.read(2), byteorder='little')
            rightValue = int.from_bytes(fp.read(2), byteorder='little')
            huffmanTemp.append([leftValue, rightValue])
        searchLAndR(huffmanTree, huffmanTemp[0])
        index = 0x335b
        fp.seek(index)
        curHuffman = b""
        index += 1
        curByte = fp.read(1)
        with open(outputFile, "w+", encoding = "utf-8", newline = '') as csvfile:
            writer = csv.writer(csvfile)
            while curByte:
                if curByte == b"\x00":
                    if curHuffman != b"":
                        writer.writerow([getText(curHuffman), index])
                    curHuffman = b""
                else:
                    curHuffman += curByte
                curByte = fp.read(1)
                index += 1
 
def getText(bytes):
    global huffmanTree
    curNode = huffmanTree
    resultBytes = b""
    endChar = False
    for char in bytes:
        for x in range(8):
            if endChar:
                char = int(char / 2)
                endChar = False
                continue
            if char % 2 == 0:
                if "left" in curNode:
                    curNode = curNode["left"]
                else:
                    break
            else:
                if "right" in curNode:
                    curNode = curNode["right"]
                else:
                    break
            if isinstance(curNode,int):
                resultBytes += curNode.to_bytes(1, byteorder='big')
                curNode = huffmanTree
                endChar = True
            char = int(char / 2)
    return resultBytes.decode("unicode_escape")

if __name__ == '__main__':
    getHuffmanTree()
    #getText()