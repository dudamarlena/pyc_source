# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Python27\Lib\site-packages\comdet\community.py
# Compiled at: 2014-08-01 01:39:06
import os, wrapper, traceback

class KeyError(Exception):

    def __init__(self, arg):
        self.msg = arg


class modularity:
    c_inner = 0.0
    inci_c = 0.0
    inci_i = 0.0
    i_inci_c = 0.0
    total = 0.0

    def display(self):
        print 'c_inner   %f' % self.c_inner
        print 'inci_c    %f' % self.inci_c
        print 'inci_i    %f' % self.inci_i
        print 'i_inci_c  %f' % self.i_inci_c
        print 'total     %f' % self.total

    def calculate(self):
        try:
            tmp1 = (self.c_inner + self.i_inci_c + self.i_inci_c) / (self.total + self.total)
            tmp1 = tmp1 - (self.inci_c + self.inci_i) / (self.total + self.total) * ((self.inci_c + self.inci_i) / (self.total + self.total))
            tmp2 = self.c_inner / (self.total + self.total)
            tmp2 = tmp2 - self.inci_c / (self.total + self.total) * (self.inci_c / (self.total + self.total))
            tmp2 = tmp2 - self.inci_i / (self.total + self.total) * (self.inci_i / (self.total + self.total))
            tmp1 = tmp1 - tmp2
            return tmp1
        except ZeroDivisionError:
            return 0


class community:
    nop = -1
    debug = False
    iter_t = -1
    phase = -1

    def error_process(self, flg, msg):
        print 'Error %s' % msg

    def debugger(self, msg):
        if self.debug:
            print '#Pass %d# Phase %d# %s' % (self.iter_t, self.phase, msg)

    def getint(self, string):
        return int(string.strip())

    def format(self, var):
        var = str(var)
        var = var.strip() + '\n'
        return var

    def getcommunity(self, iter_t, prevnodeindex=0):
        try:
            if iter_t <= 0:
                return
            else:
                communityFile = 'PASS%d' % iter_t
                lines = open(communityFile, 'r').readlines()
                noc = self.getint(lines[0])
                line_pos = 1
                result = []
                nodeindex = 0
                for cn in range(noc):
                    non = self.getint(lines[line_pos])
                    line_pos += 1
                    for j in range(non):
                        node_name = lines[line_pos].strip()
                        line_pos += 1
                        if cn == prevnodeindex and iter_t == 1:
                            result.append(node_name)
                        elif cn == prevnodeindex:
                            out = self.getcommunity(iter_t - 1, nodeindex)
                            if not out:
                                continue
                            result.append(out)
                        nodeindex += 1

                return result

        except Exception:
            self.error_process('normal', traceback.format_exc())

    def find_modularity(self, communityFile, nodei, iter_t):
        mod = modularity()
        lines_read = open(communityFile, 'r').readlines()
        total = self.getint(lines_read[0])
        nodes_communityi = set()
        rp = 1
        flg_break = False
        for i in range(total):
            comm_total = self.getint(lines_read[rp])
            rp += 1
            rp_back = rp
            for j in range(comm_total):
                node = lines_read[rp].strip()
                rp += 1
                if nodei == node:
                    rp = rp_back
                    for k in range(comm_total):
                        node = lines_read[rp].strip()
                        rp += 1
                        nodes_communityi.add(node)

                    flg_break = True
                    break

            if flg_break:
                break

        nodes_communityi = list(nodes_communityi)
        rp = 1
        for i in range(total):
            comm_total = self.getint(lines_read[rp])
            rp += 1
            for j in range(comm_total):
                node = lines_read[rp].strip()
                rp += 1
                nodefile = 'PASS%d_%s' % (iter_t, node)
                links = open(nodefile).readlines()
                for link in links:
                    link = link.strip()
                    if nodei == node and link in nodes_communityi:
                        mod.i_inci_c += 1
                        mod.c_inner += 1
                    elif link in nodes_communityi:
                        if node in nodes_communityi:
                            mod.c_inner += 1
                        else:
                            mod.inci_c += 1
                    if link == nodei:
                        mod.inci_i += 1
                    mod.total += 1

        return mod.calculate()

    def create_tmp_community(self, communityFile, nodei, nodej):
        self.debugger('migrating %s -> %s' % (nodei, nodej))
        communityFile_tmp = communityFile + '_tmp'
        lines_read = open(communityFile, 'r').readlines()
        ftc = open(communityFile_tmp, 'w')
        total = lines_read[0]
        lines_write = []
        lines_write.append(total)
        total = self.getint(total)
        rp = 1
        wp = 1
        for i in range(total):
            comm_total = self.getint(lines_read[rp])
            rp += 1
            flag = 0
            buffer = []
            for j in range(comm_total):
                node = lines_read[rp].strip()
                rp += 1
                buffer.append(node)
                if nodei == node:
                    flag = flag + 1
                elif nodej == node:
                    flag = flag + 2

            if flag == 1:
                comm_total -= 1
                if comm_total == 0:
                    lines_write[0] = total - 1
                    continue
                lines_write.append(comm_total)
                wp += 1
                for node in buffer:
                    node = node.strip()
                    if node == nodei:
                        continue
                    lines_write.append(node)
                    wp += 1

            elif flag == 2:
                comm_total += 1
                lines_write.append(comm_total)
                wp += 1
                for node in buffer:
                    lines_write.append(node)
                    wp += 1

                lines_write.append(nodei)
                wp += 1
            else:
                if flag == 3:
                    ftc.close()
                    return False
                lines_write.append(comm_total)
                wp += 1
                for node in buffer:
                    lines_write.append(node)
                    wp += 1

        for line in lines_write:
            ftc.write(self.format(line))

        ftc.close()
        return True

    def migrate_node(self, communityFile, nodei, iter_t):
        communityFile_tmp = '%s_tmp' % communityFile
        nodei_file = 'PASS%d_%s' % (iter_t, nodei)
        neighbours_nodei = open(nodei_file).readlines()
        max_modularity = 0.0
        node_max = ''
        for nodej in neighbours_nodei:
            nodej = nodej.strip()
            if not self.create_tmp_community(communityFile, nodei, nodej):
                continue
            modularity1 = self.find_modularity(communityFile, nodei, iter_t)
            modularity2 = self.find_modularity(communityFile_tmp, nodei, iter_t)
            modularity = modularity2 - modularity1
            self.debugger('\tChange Modularity %f' % modularity)
            if modularity > max_modularity:
                max_modularity = modularity
                node_max = nodej

        self.debugger('\tmax : %f' % max_modularity)
        if max_modularity < 1e-07:
            return False
        self.debugger('\tFinal Migration: %s -> %s' % (nodei, node_max))
        self.create_tmp_community(communityFile, nodei, node_max)
        print communityFile_tmp, communityFile
        os.remove(communityFile)
        os.rename(communityFile_tmp, communityFile)
        return True

    def createpassfile(self, pool1, iter_t):
        nec = pool1.no_of_nodes()
        communityFile = 'PASS%d' % iter_t
        fw = open(communityFile, 'w')
        fw.write('%d\n' % nec)
        for key in pool1.nodes.keys():
            node = pool1.nodes[key]
            fw.write('1\n')
            fw.write('%s\n' % node.node_name)

        fw.close()

    def initial_onetimepass(self, pool1):
        nec = pool1.no_of_nodes()
        communityFile = 'PASS1'
        fw = open(communityFile, 'w')
        fw.write('%d\n' % nec)
        for key in pool1.nodes.keys():
            node = pool1.nodes[key]
            fw.write('1\n')
            fw.write('%s\n' % node.node_name)
            fn = open('PASS1_%s' % node.node_name, 'w')
            for elem in node.elems:
                fn.write('%s\n' % elem)

            fn.close()

        fw.close()
        self.phase1(iter_t=1, nep=-1)

    def getposition(self, communityno):
        communityFile = 'PASS%d' % self.iter_t
        lines = open(communityFile, 'r').readlines()
        noc = self.getint(lines[0])
        line_pos = 1
        for i in range(noc):
            if i == communityno:
                return line_pos
            non = self.getint(lines[line_pos])
            line_pos += 1
            for j in range(non):
                node_name = lines[line_pos].strip()
                line_pos += 1

    def phase1(self, iter_t, nep):
        self.iter_t = iter_t
        self.phase = 1
        if self.nop > 0 and self.nop == iter_t - 1:
            self.getcommunity(self.nop)
            return
        communityFile = 'PASS%d' % iter_t
        lines = open(communityFile, 'r').readlines()
        nec = self.getint(lines[0])
        if nep > 0 and nec == nep:
            self.getcommunity(iter_t - 1)
            return
        flag = 1
        while flag:
            flag = 0
            noc = self.getint(lines[0])
            line_pos = 1
            cuts = 0
            for i in range(noc):
                non = self.getint(lines[line_pos])
                line_pos += 1
                for j in range(non):
                    node_name = lines[line_pos].strip()
                    line_pos += 1
                    if self.migrate_node(communityFile, node_name, iter_t):
                        lines = open(communityFile, 'r').readlines()
                        noc = self.getint(lines[0])
                        line_pos = self.getposition(i - cuts)
                        cuts += 1
                        flag = 1
                        break

        self.phase2(iter_t, nec)

    def phase2(self, iter_t, nec):
        self.phase = 2
        pool2 = wrapper.Pool()
        communityFile = 'PASS%d' % iter_t
        lines_read = open(communityFile, 'r').readlines()
        total = self.getint(lines_read[0])
        rp = 1
        local = 0
        dict_node2community = {}
        for i in range(total):
            comm_total = self.getint(lines_read[rp])
            rp += 1
            name_node = 'node%d' % local
            local += 1
            pool2.add_node(name_node)
            for j in range(comm_total):
                node = lines_read[rp].strip()
                rp += 1
                dict_node2community[node] = name_node

        if not len(dict_node2community.keys()):
            return
        for key in dict_node2community:
            nodefile = 'PASS%d_%s' % (iter_t + 1, dict_node2community[key])
            fnp2 = open(nodefile, 'a')
            key = 'PASS%d_%s' % (iter_t, key)
            if os.path.exists(key):
                for line in open(key, 'r').readlines():
                    line = line.strip()
                    if line not in dict_node2community:
                        continue
                    newlink = dict_node2community[line]
                    self.debugger('writing %s' % newlink)
                    if not newlink:
                        raise KeyError('%s not found in dict_node2community file for Phase2 iter_t %d' % (newlink, iter_t))
                    fnp2.write('%s\n' % newlink)

            fnp2.close()

        iter_t = iter_t + 1
        self.createpassfile(pool2, iter_t)
        self.phase1(iter_t, nec)

    def start(self, pool1, nop, debug):
        self.nop = nop
        self.debug = debug
        self.debugger('No of Passes %d' % self.nop)
        self.initial_onetimepass(pool1)
        return self.getcommunity(self.iter_t)