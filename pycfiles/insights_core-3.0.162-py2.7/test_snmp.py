# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_snmp.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.snmp import TcpIpStats
from insights.parsers.snmp import TcpIpStatsIPV6
from insights.tests import context_wrap
PROC_SNMP = ('\nIp: Forwarding DefaultTTL InReceives InHdrErrors InAddrErrors ForwDatagrams InUnknownProtos InDiscards InDelivers OutRequests OutDiscards OutNoRoutes ReasmTimeout ReasmReqds ReasmOKs ReasmFails FragOKs FragFails FragCreates\nIp: 2 64 2628 0 2 0 0 0 2624 1618 0 0 0 0 0 10 0 0 0\nIcmp: InMsgs InErrors InDestUnreachs InTimeExcds InParmProbs InSrcQuenchs InRedirects InEchos InEchoReps InTimestamps InTimestampReps InAddrMasks InAddrMaskReps OutMsgs OutErrors OutDestUnreachs OutTimeExcds OutParmProbs OutSrcQuenchs OutRedirects OutEchos OutEchoReps OutTimestamps OutTimestampReps OutAddrMasks OutAddrMaskReps\nIcmp: 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 2 0 0 0 0 0 0 0 0 0 0\nIcmpMsg: InType3 OutType3\nIcmpMsg: 34 44\nTcp: RtoAlgorithm RtoMin RtoMax MaxConn ActiveOpens PassiveOpens AttemptFails EstabResets CurrEstab InSegs OutSegs RetransSegs InErrs OutRsts\nTcp: 1 200 120000 -1 25 4 0 0 1 2529 1520 1 0 9\nUdp: InDatagrams NoPorts InErrors OutDatagrams RcvbufErrors SndbufErrors\nUdp: 95 0 0 95 1 4\nUdpLite: InDatagrams NoPorts InErrors OutDatagrams RcvbufErrors SndbufErrors\nUdpLite: 0 10 0 0 0 100\n').strip()
PROC_SNMP_NO = ('\n').strip()
PROC_SNMP6 = ('\nIp6InReceives                   \t757\nIp6InHdrErrors                  \t0\nIp6InTooBigErrors               \t0\nIp6InNoRoutes                   \t0\nIp6InAddrErrors                 \t0\nIp6InUnknownProtos              \t0\nIp6InTruncatedPkts              \t0\nIp6InDiscards                   \t0\nIp6InDelivers                   \t748\nIp6OutForwDatagrams             \t0\nIp6OutRequests                  \t713\nIp6OutDiscards                  \t0\nIp6OutNoRoutes                  \t0\nIp6ReasmTimeout                 \t0\nIp6ReasmReqds                   \t0\nIp6ReasmOKs                     \t0\nIp6ReasmFails                   \t0\nIp6FragOKs                      \t0\nIp6FragFails                    \t0\nIp6FragCreates                  \t0\nIp6InMcastPkts                  \t99\nIp6OutMcastPkts                 \t71\nIp6InOctets                     \t579410\nIp6OutOctets                    \t1553244\nIp6InMcastOctets                \t9224\nIp6OutMcastOctets               \t5344\nIp6InBcastOctets                \t0\nIp6OutBcastOctets               \t0\nIp6InNoECTPkts                  \t759\nIp6InECT1Pkts                   \t0\nIp6InECT0Pkts                   \t0\nIp6InCEPkts                     \t0\nIcmp6InMsgs                     \t94\nIcmp6InErrors                   \t0\nIcmp6OutMsgs                    \t41\nIcmp6OutErrors                  \t0\nIcmp6InCsumErrors               \t0\nIcmp6InDestUnreachs             \t0\nIcmp6InPktTooBigs               \t0\nIcmp6InTimeExcds                \t0\nIcmp6InParmProblems             \t0\nIcmp6InEchos                    \t0\nIcmp6InEchoReplies              \t0\nIcmp6InGroupMembQueries         \t28\nIcmp6InGroupMembResponses       \t0\nIcmp6InGroupMembReductions      \t0\nIcmp6InRouterSolicits           \t0\nIcmp6InRouterAdvertisements     \t62\nIcmp6InNeighborSolicits         \t3\nIcmp6InNeighborAdvertisements   \t1\nIcmp6InRedirects                \t0\nIcmp6InMLDv2Reports             \t0\nIcmp6OutDestUnreachs            \t0\nIcmp6OutPktTooBigs              \t0\nIcmp6OutTimeExcds               \t0\nIcmp6OutParmProblems            \t0\nIcmp6OutEchos                   \t0\nIcmp6OutEchoReplies             \t0\nIcmp6OutGroupMembQueries        \t0\nIcmp6OutGroupMembResponses      \t0\nIcmp6OutGroupMembReductions     \t0\nIcmp6OutRouterSolicits          \t1\nIcmp6OutRouterAdvertisements    \t0\nIcmp6OutNeighborSolicits        \t3\nIcmp6OutNeighborAdvertisements  \t3\nIcmp6OutRedirects               \t0\nIcmp6OutMLDv2Reports            \t34\nIcmp6InType130                  \t28\nIcmp6InType134                  \t62\nIcmp6InType135                  \t3\nIcmp6InType136                  \t1\nIcmp6OutType133                 \t1\nIcmp6OutType135                 \t3\nIcmp6OutType136                 \t3\nIcmp6OutType143                 \t34\nUdp6InDatagrams                 \t0\nUdp6NoPorts                     \t0\nUdp6InErrors                    \t0\nUdp6OutDatagrams                \t0\nUdp6RcvbufErrors                \t0\nUdp6SndbufErrors                \t0\nUdp6InCsumErrors                \t0\nUdpLite6InDatagrams             \t0\nUdpLite6NoPorts                 \t0\nUdpLite6InErrors                \t0\nUdpLite6OutDatagrams            \t0\nUdpLite6RcvbufErrors            \t0\nUdpLite6SndbufErrors            \t0\nUdpLite6InCsumErrors            \t0\n').strip()
PROC_SNMP6_ODD = ('\nIp6InReceives                   \t757\nIp6InHdrErrors                  \t0\nIcmp6OutMLDv2Reports            \t0\nIcmp6InType130                  \t28\nIcmp6InType134                  \t62\nIp6InDiscards\n').strip()

def test_snmp():
    stats = TcpIpStats(context_wrap(PROC_SNMP))
    snmp_stats = stats.get('Ip')
    assert snmp_stats
    assert snmp_stats['DefaultTTL'] == 64
    assert snmp_stats['InReceives'] == 2628
    assert snmp_stats['InHdrErrors'] == 0
    assert snmp_stats['InAddrErrors'] == 2
    assert snmp_stats['InDiscards'] == 0
    assert snmp_stats['InDelivers'] == 2624
    assert snmp_stats['ReasmFails'] == 10
    assert snmp_stats['OutRequests'] == 1618
    snmp_stats = stats.get('Tcp')
    assert snmp_stats['RtoMax'] == 120000
    assert snmp_stats['MaxConn'] == -1
    assert snmp_stats['OutSegs'] == 1520
    assert snmp_stats['ActiveOpens'] == 25
    snmp_stats = stats.get('IcmpMsg')
    assert snmp_stats['OutType3'] == 44
    snmp_stats = stats.get('Udp')
    assert snmp_stats['OutDatagrams'] == 95
    assert snmp_stats['RcvbufErrors'] == 1
    assert snmp_stats['NoPorts'] == 0
    stats = TcpIpStats(context_wrap(PROC_SNMP_NO))
    snmp_stats = stats.get('Ip')
    assert snmp_stats is None
    return


def test_snmp6():
    stats = TcpIpStatsIPV6(context_wrap(PROC_SNMP6))
    snmp6_stats_RX = stats.get('Ip6InReceives')
    snmp6_stats_MLD = stats.get('Icmp6OutMLDv2Reports')
    assert snmp6_stats_RX == 757
    assert snmp6_stats_MLD == 34
    stats = TcpIpStatsIPV6(context_wrap(PROC_SNMP6_ODD))
    snmp6_stats_disx = stats.get('Ip6InDiscards')
    snmp6_stats_odd = stats.get('some_unknown')
    assert snmp6_stats_disx is None
    assert snmp6_stats_odd is None
    return