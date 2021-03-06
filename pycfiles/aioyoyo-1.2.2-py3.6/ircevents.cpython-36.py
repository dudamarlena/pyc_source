# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\aioyoyo\oyoyo\ircevents.py
# Compiled at: 2017-03-02 21:26:43
# Size of source mod 2**32: 6322 bytes
"""Adds names for numeric commands"""
numeric_events = {'001':'welcome', 
 '002':'yourhost', 
 '003':'created', 
 '004':'myinfo', 
 '005':'featurelist', 
 '010':'toomanypeeps', 
 '200':'tracelink', 
 '201':'traceconnecting', 
 '202':'tracehandshake', 
 '203':'traceunknown', 
 '204':'traceoperator', 
 '205':'traceuser', 
 '206':'traceserver', 
 '207':'traceservice', 
 '208':'tracenewtype', 
 '209':'traceclass', 
 '210':'tracereconnect', 
 '211':'statslinkinfo', 
 '212':'statscommands', 
 '213':'statscline', 
 '214':'statsnline', 
 '215':'statsiline', 
 '216':'statskline', 
 '217':'statsqline', 
 '218':'statsyline', 
 '219':'endofstats', 
 '221':'umodeis', 
 '231':'serviceinfo', 
 '232':'endofservices', 
 '233':'service', 
 '234':'servlist', 
 '235':'servlistend', 
 '241':'statslline', 
 '242':'statsuptime', 
 '243':'statsoline', 
 '244':'statshline', 
 '250':'luserconns', 
 '251':'luserclient', 
 '252':'luserop', 
 '253':'luserunknown', 
 '254':'luserchannels', 
 '255':'luserme', 
 '256':'adminme', 
 '257':'adminloc1', 
 '258':'adminloc2', 
 '259':'adminemail', 
 '261':'tracelog', 
 '262':'endoftrace', 
 '263':'tryagain', 
 '265':'n_local', 
 '266':'n_global', 
 '300':'none', 
 '301':'away', 
 '302':'userhost', 
 '303':'ison', 
 '305':'unaway', 
 '306':'nowaway', 
 '311':'whoisuser', 
 '312':'whoisserver', 
 '313':'whoisoperator', 
 '314':'whowasuser', 
 '315':'endofwho', 
 '316':'whoischanop', 
 '317':'whoisidle', 
 '318':'endofwhois', 
 '319':'whoischannels', 
 '321':'liststart', 
 '322':'list', 
 '323':'listend', 
 '324':'channelmodeis', 
 '329':'channelcreate', 
 '331':'notopic', 
 '332':'currenttopic', 
 '333':'topicinfo', 
 '341':'inviting', 
 '342':'summoning', 
 '346':'invitelist', 
 '347':'endofinvitelist', 
 '348':'exceptlist', 
 '349':'endofexceptlist', 
 '351':'version', 
 '352':'whoreply', 
 '353':'namreply', 
 '361':'killdone', 
 '362':'closing', 
 '363':'closeend', 
 '364':'links', 
 '365':'endoflinks', 
 '366':'endofnames', 
 '367':'banlist', 
 '368':'endofbanlist', 
 '369':'endofwhowas', 
 '371':'info', 
 '372':'motd', 
 '373':'infostart', 
 '374':'endofinfo', 
 '375':'motdstart', 
 '376':'endofmotd', 
 '377':'motd2', 
 '381':'youreoper', 
 '382':'rehashing', 
 '384':'myportis', 
 '391':'time', 
 '392':'usersstart', 
 '393':'users', 
 '394':'endofusers', 
 '395':'nousers', 
 '401':'nosuchnick', 
 '402':'nosuchserver', 
 '403':'nosuchchannel', 
 '404':'cannotsendtochan', 
 '405':'toomanychannels', 
 '406':'wasnosuchnick', 
 '407':'toomanytargets', 
 '409':'noorigin', 
 '411':'norecipient', 
 '412':'notexttosend', 
 '413':'notoplevel', 
 '414':'wildtoplevel', 
 '421':'unknowncommand', 
 '422':'nomotd', 
 '423':'noadmininfo', 
 '424':'fileerror', 
 '431':'nonicknamegiven', 
 '432':'erroneusnickname', 
 '433':'nicknameinuse', 
 '436':'nickcollision', 
 '437':'unavailresource', 
 '441':'usernotinchannel', 
 '442':'notonchannel', 
 '443':'useronchannel', 
 '444':'nologin', 
 '445':'summondisabled', 
 '446':'usersdisabled', 
 '451':'notregistered', 
 '461':'needmoreparams', 
 '462':'alreadyregistered', 
 '463':'nopermforhost', 
 '464':'passwdmismatch', 
 '465':'yourebannedcreep', 
 '466':'youwillbebanned', 
 '467':'keyset', 
 '471':'channelisfull', 
 '472':'unknownmode', 
 '473':'inviteonlychan', 
 '474':'bannedfromchan', 
 '475':'badchannelkey', 
 '476':'badchanmask', 
 '477':'nochanmodes', 
 '478':'banlistfull', 
 '481':'noprivileges', 
 '482':'chanoprivsneeded', 
 '483':'cantkillserver', 
 '484':'restricted', 
 '485':'uniqopprivsneeded', 
 '491':'nooperhost', 
 '492':'noservicehost', 
 '501':'umodeunknownflag', 
 '502':'usersdontmatch'}
numeric_events = {bytes(k, 'ascii'):v for k, v in numeric_events.items()}
generated_events = [
 'dcc_connect',
 'dcc_disconnect',
 'dccmsg',
 'disconnect',
 'ctcp',
 'ctcpreply']
protocol_events = [
 'error',
 'join',
 'kick',
 'mode',
 'part',
 'ping',
 'privmsg',
 'privnotice',
 'pubmsg',
 'pubnotice',
 'quit',
 'invite',
 'pong']
all_events = generated_events + protocol_events + list(numeric_events.values())