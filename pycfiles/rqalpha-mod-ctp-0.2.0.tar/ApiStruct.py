# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-ctp/rqalpha_mod_ctp/ctp/pyctp/linux64_27/ApiStruct.py
# Compiled at: 2017-05-25 23:02:29
from __future__ import absolute_import as _init
T = {}
T['TE_RESUME'] = 'int'
TERT_RESTART = 0
TERT_RESUME = 1
TERT_QUICK = 2
T['TraderID'] = 'char[21]'
T['InvestorID'] = 'char[13]'
T['BrokerID'] = 'char[11]'
T['BrokerAbbr'] = 'char[9]'
T['BrokerName'] = 'char[81]'
T['ExchangeInstID'] = 'char[31]'
T['OrderRef'] = 'char[13]'
T['ParticipantID'] = 'char[11]'
T['UserID'] = 'char[16]'
T['Password'] = 'char[41]'
T['ClientID'] = 'char[11]'
T['InstrumentID'] = 'char[31]'
T['MarketID'] = 'char[31]'
T['ProductName'] = 'char[21]'
T['ExchangeID'] = 'char[9]'
T['ExchangeName'] = 'char[61]'
T['ExchangeAbbr'] = 'char[9]'
T['ExchangeFlag'] = 'char[2]'
T['MacAddress'] = 'char[21]'
T['SystemID'] = 'char[21]'
T['ExchangeProperty'] = 'char'
EXP_Normal = '0'
EXP_GenOrderByTrade = '1'
T['Date'] = 'char[9]'
T['Time'] = 'char[9]'
T['LongTime'] = 'char[13]'
T['InstrumentName'] = 'char[21]'
T['SettlementGroupID'] = 'char[9]'
T['OrderSysID'] = 'char[21]'
T['TradeID'] = 'char[21]'
T['CommandType'] = 'char[65]'
T['IPAddress'] = 'char[16]'
T['IPPort'] = 'int'
T['ProductInfo'] = 'char[11]'
T['ProtocolInfo'] = 'char[11]'
T['BusinessUnit'] = 'char[21]'
T['DepositSeqNo'] = 'char[15]'
T['IdentifiedCardNo'] = 'char[51]'
T['IdCardType'] = 'char'
ICT_EID = '0'
ICT_IDCard = '1'
ICT_OfficerIDCard = '2'
ICT_PoliceIDCard = '3'
ICT_SoldierIDCard = '4'
ICT_HouseholdRegister = '5'
ICT_Passport = '6'
ICT_TaiwanCompatriotIDCard = '7'
ICT_HomeComingCard = '8'
ICT_LicenseNo = '9'
ICT_TaxNo = 'A'
ICT_HMMainlandTravelPermit = 'B'
ICT_TwMainlandTravelPermit = 'C'
ICT_DrivingLicense = 'D'
ICT_SocialID = 'F'
ICT_LocalID = 'G'
ICT_BusinessRegistration = 'H'
ICT_HKMCIDCard = 'I'
ICT_AccountsPermits = 'J'
ICT_OtherCard = 'x'
T['OrderLocalID'] = 'char[13]'
T['UserName'] = 'char[81]'
T['PartyName'] = 'char[81]'
T['ErrorMsg'] = 'char[81]'
T['FieldName'] = 'char[2049]'
T['FieldContent'] = 'char[2049]'
T['SystemName'] = 'char[41]'
T['Content'] = 'char[501]'
T['InvestorRange'] = 'char'
IR_All = '1'
IR_Group = '2'
IR_Single = '3'
T['DepartmentRange'] = 'char'
DR_All = '1'
DR_Group = '2'
DR_Single = '3'
T['DataSyncStatus'] = 'char'
DS_Asynchronous = '1'
DS_Synchronizing = '2'
DS_Synchronized = '3'
T['BrokerDataSyncStatus'] = 'char'
BDS_Synchronized = '1'
BDS_Synchronizing = '2'
T['ExchangeConnectStatus'] = 'char'
ECS_NoConnection = '1'
ECS_QryInstrumentSent = '2'
ECS_GotInformation = '9'
T['TraderConnectStatus'] = 'char'
TCS_NotConnected = '1'
TCS_Connected = '2'
TCS_QryInstrumentSent = '3'
TCS_SubPrivateFlow = '4'
T['FunctionCode'] = 'char'
FC_DataAsync = '1'
FC_ForceUserLogout = '2'
FC_UserPasswordUpdate = '3'
FC_BrokerPasswordUpdate = '4'
FC_InvestorPasswordUpdate = '5'
FC_OrderInsert = '6'
FC_OrderAction = '7'
FC_SyncSystemData = '8'
FC_SyncBrokerData = '9'
FC_BachSyncBrokerData = 'A'
FC_SuperQuery = 'B'
FC_ParkedOrderInsert = 'C'
FC_ParkedOrderAction = 'D'
FC_SyncOTP = 'E'
FC_DeleteOrder = 'F'
T['BrokerFunctionCode'] = 'char'
BFC_ForceUserLogout = '1'
BFC_UserPasswordUpdate = '2'
BFC_SyncBrokerData = '3'
BFC_BachSyncBrokerData = '4'
BFC_OrderInsert = '5'
BFC_OrderAction = '6'
BFC_AllQuery = '7'
BFC_log = 'a'
BFC_BaseQry = 'b'
BFC_TradeQry = 'c'
BFC_Trade = 'd'
BFC_Virement = 'e'
BFC_Risk = 'f'
BFC_Session = 'g'
BFC_RiskNoticeCtl = 'h'
BFC_RiskNotice = 'i'
BFC_BrokerDeposit = 'j'
BFC_QueryFund = 'k'
BFC_QueryOrder = 'l'
BFC_QueryTrade = 'm'
BFC_QueryPosition = 'n'
BFC_QueryMarketData = 'o'
BFC_QueryUserEvent = 'p'
BFC_QueryRiskNotify = 'q'
BFC_QueryFundChange = 'r'
BFC_QueryInvestor = 's'
BFC_QueryTradingCode = 't'
BFC_ForceClose = 'u'
BFC_PressTest = 'v'
BFC_RemainCalc = 'w'
BFC_NetPositionInd = 'x'
BFC_RiskPredict = 'y'
BFC_DataExport = 'z'
BFC_RiskTargetSetup = 'A'
BFC_MarketDataWarn = 'B'
BFC_QryBizNotice = 'C'
BFC_CfgBizNotice = 'D'
BFC_SyncOTP = 'E'
BFC_SendBizNotice = 'F'
BFC_CfgRiskLevelStd = 'G'
BFC_TbCommand = 'H'
BFC_DeleteOrder = 'J'
BFC_ParkedOrderInsert = 'K'
BFC_ParkedOrderAction = 'L'
T['OrderActionStatus'] = 'char'
OAS_Submitted = 'a'
OAS_Accepted = 'b'
OAS_Rejected = 'c'
T['OrderStatus'] = 'char'
OST_AllTraded = '0'
OST_PartTradedQueueing = '1'
OST_PartTradedNotQueueing = '2'
OST_NoTradeQueueing = '3'
OST_NoTradeNotQueueing = '4'
OST_Canceled = '5'
OST_Unknown = 'a'
OST_NotTouched = 'b'
OST_Touched = 'c'
T['OrderSubmitStatus'] = 'char'
OSS_InsertSubmitted = '0'
OSS_CancelSubmitted = '1'
OSS_ModifySubmitted = '2'
OSS_Accepted = '3'
OSS_InsertRejected = '4'
OSS_CancelRejected = '5'
OSS_ModifyRejected = '6'
T['PositionDate'] = 'char'
PSD_Today = '1'
PSD_History = '2'
T['PositionDateType'] = 'char'
PDT_UseHistory = '1'
PDT_NoUseHistory = '2'
T['TradingRole'] = 'char'
ER_Broker = '1'
ER_Host = '2'
ER_Maker = '3'
T['ProductClass'] = 'char'
PC_Futures = '1'
PC_Options = '2'
PC_Combination = '3'
PC_Spot = '4'
PC_EFP = '5'
PC_SpotOption = '6'
T['InstLifePhase'] = 'char'
IP_NotStart = '0'
IP_Started = '1'
IP_Pause = '2'
IP_Expired = '3'
T['Direction'] = 'char'
D_Buy = '0'
D_Sell = '1'
T['PositionType'] = 'char'
PT_Net = '1'
PT_Gross = '2'
T['PosiDirection'] = 'char'
PD_Net = '1'
PD_Long = '2'
PD_Short = '3'
T['SysSettlementStatus'] = 'char'
SS_NonActive = '1'
SS_Startup = '2'
SS_Operating = '3'
SS_Settlement = '4'
SS_SettlementFinished = '5'
T['RatioAttr'] = 'char'
RA_Trade = '0'
RA_Settlement = '1'
T['HedgeFlag'] = 'char'
HF_Speculation = '1'
HF_Arbitrage = '2'
HF_Hedge = '3'
T['BillHedgeFlag'] = 'char'
BHF_Speculation = '1'
BHF_Arbitrage = '2'
BHF_Hedge = '3'
T['ClientIDType'] = 'char'
CIDT_Speculation = '1'
CIDT_Arbitrage = '2'
CIDT_Hedge = '3'
T['OrderPriceType'] = 'char'
OPT_AnyPrice = '1'
OPT_LimitPrice = '2'
OPT_BestPrice = '3'
OPT_LastPrice = '4'
OPT_LastPricePlusOneTicks = '5'
OPT_LastPricePlusTwoTicks = '6'
OPT_LastPricePlusThreeTicks = '7'
OPT_AskPrice1 = '8'
OPT_AskPrice1PlusOneTicks = '9'
OPT_AskPrice1PlusTwoTicks = 'A'
OPT_AskPrice1PlusThreeTicks = 'B'
OPT_BidPrice1 = 'C'
OPT_BidPrice1PlusOneTicks = 'D'
OPT_BidPrice1PlusTwoTicks = 'E'
OPT_BidPrice1PlusThreeTicks = 'F'
OPT_FiveLevelPrice = 'G'
T['OffsetFlag'] = 'char'
OF_Open = '0'
OF_Close = '1'
OF_ForceClose = '2'
OF_CloseToday = '3'
OF_CloseYesterday = '4'
OF_ForceOff = '5'
OF_LocalForceClose = '6'
T['ForceCloseReason'] = 'char'
FCC_NotForceClose = '0'
FCC_LackDeposit = '1'
FCC_ClientOverPositionLimit = '2'
FCC_MemberOverPositionLimit = '3'
FCC_NotMultiple = '4'
FCC_Violation = '5'
FCC_Other = '6'
FCC_PersonDeliv = '7'
T['OrderType'] = 'char'
ORDT_Normal = '0'
ORDT_DeriveFromQuote = '1'
ORDT_DeriveFromCombination = '2'
ORDT_Combination = '3'
ORDT_ConditionalOrder = '4'
ORDT_Swap = '5'
T['TimeCondition'] = 'char'
TC_IOC = '1'
TC_GFS = '2'
TC_GFD = '3'
TC_GTD = '4'
TC_GTC = '5'
TC_GFA = '6'
T['VolumeCondition'] = 'char'
VC_AV = '1'
VC_MV = '2'
VC_CV = '3'
T['ContingentCondition'] = 'char'
CC_Immediately = '1'
CC_Touch = '2'
CC_TouchProfit = '3'
CC_ParkedOrder = '4'
CC_LastPriceGreaterThanStopPrice = '5'
CC_LastPriceGreaterEqualStopPrice = '6'
CC_LastPriceLesserThanStopPrice = '7'
CC_LastPriceLesserEqualStopPrice = '8'
CC_AskPriceGreaterThanStopPrice = '9'
CC_AskPriceGreaterEqualStopPrice = 'A'
CC_AskPriceLesserThanStopPrice = 'B'
CC_AskPriceLesserEqualStopPrice = 'C'
CC_BidPriceGreaterThanStopPrice = 'D'
CC_BidPriceGreaterEqualStopPrice = 'E'
CC_BidPriceLesserThanStopPrice = 'F'
CC_BidPriceLesserEqualStopPrice = 'H'
T['ActionFlag'] = 'char'
AF_Delete = '0'
AF_Modify = '3'
T['TradingRight'] = 'char'
TR_Allow = '0'
TR_CloseOnly = '1'
TR_Forbidden = '2'
T['OrderSource'] = 'char'
OSRC_Participant = '0'
OSRC_Administrator = '1'
T['TradeType'] = 'char'
TRDT_SplitCombination = '#'
TRDT_Common = '0'
TRDT_OptionsExecution = '1'
TRDT_OTC = '2'
TRDT_EFPDerived = '3'
TRDT_CombinationDerived = '4'
T['PriceSource'] = 'char'
PSRC_LastPrice = '0'
PSRC_Buy = '1'
PSRC_Sell = '2'
T['InstrumentStatus'] = 'char'
IS_BeforeTrading = '0'
IS_NoTrading = '1'
IS_Continous = '2'
IS_AuctionOrdering = '3'
IS_AuctionBalance = '4'
IS_AuctionMatch = '5'
IS_Closed = '6'
T['InstStatusEnterReason'] = 'char'
IER_Automatic = '1'
IER_Manual = '2'
IER_Fuse = '3'
T['OrderActionRef'] = 'int'
T['InstallCount'] = 'int'
T['InstallID'] = 'int'
T['ErrorID'] = 'int'
T['SettlementID'] = 'int'
T['Volume'] = 'int'
T['FrontID'] = 'int'
T['SessionID'] = 'int'
T['SequenceNo'] = 'int'
T['CommandNo'] = 'int'
T['Millisec'] = 'int'
T['VolumeMultiple'] = 'int'
T['TradingSegmentSN'] = 'int'
T['RequestID'] = 'int'
T['Year'] = 'int'
T['Month'] = 'int'
T['Bool'] = 'int'
T['Price'] = 'double'
T['CombOffsetFlag'] = 'char[5]'
T['CombHedgeFlag'] = 'char[5]'
T['Ratio'] = 'double'
T['Money'] = 'double'
T['LargeVolume'] = 'double'
T['SequenceSeries'] = 'short'
T['CommPhaseNo'] = 'short'
T['SequenceLabel'] = 'char[2]'
T['UnderlyingMultiple'] = 'double'
T['Priority'] = 'int'
T['ContractCode'] = 'char[41]'
T['City'] = 'char[51]'
T['IsStock'] = 'char[11]'
T['Channel'] = 'char[51]'
T['Address'] = 'char[101]'
T['ZipCode'] = 'char[7]'
T['Telephone'] = 'char[41]'
T['Fax'] = 'char[41]'
T['Mobile'] = 'char[41]'
T['EMail'] = 'char[41]'
T['Memo'] = 'char[161]'
T['CompanyCode'] = 'char[51]'
T['Website'] = 'char[51]'
T['TaxNo'] = 'char[31]'
T['BatchStatus'] = 'char'
BS_NoUpload = '1'
BS_Uploaded = '2'
BS_Failed = '3'
T['PropertyID'] = 'char[33]'
T['PropertyName'] = 'char[65]'
T['LicenseNo'] = 'char[51]'
T['AgentID'] = 'char[13]'
T['AgentName'] = 'char[41]'
T['AgentGroupID'] = 'char[13]'
T['AgentGroupName'] = 'char[41]'
T['ReturnStyle'] = 'char'
RS_All = '1'
RS_ByProduct = '2'
T['ReturnPattern'] = 'char'
RP_ByVolume = '1'
RP_ByFeeOnHand = '2'
T['ReturnLevel'] = 'char'
RL_Level1 = '1'
RL_Level2 = '2'
RL_Level3 = '3'
RL_Level4 = '4'
RL_Level5 = '5'
RL_Level6 = '6'
RL_Level7 = '7'
RL_Level8 = '8'
RL_Level9 = '9'
T['ReturnStandard'] = 'char'
RSD_ByPeriod = '1'
RSD_ByStandard = '2'
T['MortgageType'] = 'char'
MT_Out = '0'
MT_In = '1'
T['InvestorSettlementParamID'] = 'char'
ISPI_MortgageRatio = '4'
ISPI_MarginWay = '5'
ISPI_BillDeposit = '9'
T['ExchangeSettlementParamID'] = 'char'
ESPI_MortgageRatio = '1'
ESPI_OtherFundItem = '2'
ESPI_OtherFundImport = '3'
ESPI_CFFEXMinPrepa = '6'
ESPI_CZCESettlementType = '7'
ESPI_ExchDelivFeeMode = '9'
ESPI_DelivFeeMode = '0'
ESPI_CZCEComMarginType = 'A'
ESPI_DceComMarginType = 'B'
ESPI_OptOutDisCountRate = 'a'
ESPI_OptMiniGuarantee = 'b'
T['SystemParamID'] = 'char'
SPI_InvestorIDMinLength = '1'
SPI_AccountIDMinLength = '2'
SPI_UserRightLogon = '3'
SPI_SettlementBillTrade = '4'
SPI_TradingCode = '5'
SPI_CheckFund = '6'
SPI_CommModelRight = '7'
SPI_MarginModelRight = '9'
SPI_IsStandardActive = '8'
SPI_UploadSettlementFile = 'U'
SPI_DownloadCSRCFile = 'D'
SPI_SettlementBillFile = 'S'
SPI_CSRCOthersFile = 'C'
SPI_InvestorPhoto = 'P'
SPI_CSRCData = 'R'
SPI_InvestorPwdModel = 'I'
SPI_CFFEXInvestorSettleFile = 'F'
SPI_InvestorIDType = 'a'
SPI_FreezeMaxReMain = 'r'
SPI_IsSync = 'A'
SPI_RelieveOpenLimit = 'O'
SPI_IsStandardFreeze = 'X'
SPI_CZCENormalProductHedge = 'B'
T['TradeParamID'] = 'char'
TPID_EncryptionStandard = 'E'
TPID_RiskMode = 'R'
TPID_RiskModeGlobal = 'G'
TPID_modeEncode = 'P'
TPID_tickMode = 'T'
TPID_SingleUserSessionMaxNum = 'S'
TPID_LoginFailMaxNum = 'L'
TPID_IsAuthForce = 'A'
T['SettlementParamValue'] = 'char[256]'
T['CounterID'] = 'char[33]'
T['InvestorGroupName'] = 'char[41]'
T['BrandCode'] = 'char[257]'
T['Warehouse'] = 'char[257]'
T['ProductDate'] = 'char[41]'
T['Grade'] = 'char[41]'
T['Classify'] = 'char[41]'
T['Position'] = 'char[41]'
T['Yieldly'] = 'char[41]'
T['Weight'] = 'char[41]'
T['SubEntryFundNo'] = 'int'
T['FileID'] = 'char'
FI_SettlementFund = 'F'
FI_Trade = 'T'
FI_InvestorPosition = 'P'
FI_SubEntryFund = 'O'
FI_CZCECombinationPos = 'C'
FI_CSRCData = 'R'
FI_CZCEClose = 'L'
FI_CZCENoClose = 'N'
FI_PositionDtl = 'D'
FI_OptionStrike = 'S'
FI_SettlementPriceComparison = 'M'
FI_NonTradePosChange = 'B'
T['FileName'] = 'char[257]'
T['FileType'] = 'char'
FUT_Settlement = '0'
FUT_Check = '1'
T['FileFormat'] = 'char'
FFT_Txt = '0'
FFT_Zip = '1'
FFT_DBF = '2'
T['FileUploadStatus'] = 'char'
FUS_SucceedUpload = '1'
FUS_FailedUpload = '2'
FUS_SucceedLoad = '3'
FUS_PartSucceedLoad = '4'
FUS_FailedLoad = '5'
T['TransferDirection'] = 'char'
TD_Out = '0'
TD_In = '1'
T['UploadMode'] = 'char[21]'
T['AccountID'] = 'char[13]'
T['BankFlag'] = 'char[4]'
T['BankAccount'] = 'char[41]'
T['OpenName'] = 'char[61]'
T['OpenBank'] = 'char[101]'
T['BankName'] = 'char[101]'
T['PublishPath'] = 'char[257]'
T['OperatorID'] = 'char[65]'
T['MonthCount'] = 'int'
T['AdvanceMonthArray'] = 'char[13]'
T['DateExpr'] = 'char[1025]'
T['InstrumentIDExpr'] = 'char[41]'
T['InstrumentNameExpr'] = 'char[41]'
T['SpecialCreateRule'] = 'char'
SC_NoSpecialRule = '0'
SC_NoSpringFestival = '1'
T['BasisPriceType'] = 'char'
IPT_LastSettlement = '1'
IPT_LaseClose = '2'
T['ProductLifePhase'] = 'char'
PLP_Active = '1'
PLP_NonActive = '2'
PLP_Canceled = '3'
T['DeliveryMode'] = 'char'
DM_CashDeliv = '1'
DM_CommodityDeliv = '2'
T['LogLevel'] = 'char[33]'
T['ProcessName'] = 'char[257]'
T['OperationMemo'] = 'char[1025]'
T['FundIOType'] = 'char'
FIOT_FundIO = '1'
FIOT_Transfer = '2'
FIOT_SwapCurrency = '3'
T['FundType'] = 'char'
FT_Deposite = '1'
FT_ItemFund = '2'
FT_Company = '3'
FT_InnerTransfer = '4'
T['FundDirection'] = 'char'
FD_In = '1'
FD_Out = '2'
T['FundStatus'] = 'char'
FS_Record = '1'
FS_Check = '2'
FS_Charge = '3'
T['BillNo'] = 'char[15]'
T['BillName'] = 'char[33]'
T['PublishStatus'] = 'char'
PS_None = '1'
PS_Publishing = '2'
PS_Published = '3'
T['EnumValueID'] = 'char[65]'
T['EnumValueType'] = 'char[33]'
T['EnumValueLabel'] = 'char[65]'
T['EnumValueResult'] = 'char[33]'
T['SystemStatus'] = 'char'
ES_NonActive = '1'
ES_Startup = '2'
ES_Initialize = '3'
ES_Initialized = '4'
ES_Close = '5'
ES_Closed = '6'
ES_Settlement = '7'
T['SettlementStatus'] = 'char'
STS_Initialize = '0'
STS_Settlementing = '1'
STS_Settlemented = '2'
STS_Finished = '3'
T['RangeIntType'] = 'char[33]'
T['RangeIntFrom'] = 'char[33]'
T['RangeIntTo'] = 'char[33]'
T['FunctionID'] = 'char[25]'
T['FunctionValueCode'] = 'char[257]'
T['FunctionName'] = 'char[65]'
T['RoleID'] = 'char[11]'
T['RoleName'] = 'char[41]'
T['Description'] = 'char[401]'
T['CombineID'] = 'char[25]'
T['CombineType'] = 'char[25]'
T['InvestorType'] = 'char'
CT_Person = '0'
CT_Company = '1'
CT_Fund = '2'
CT_SpecialOrgan = '3'
CT_Asset = '4'
T['BrokerType'] = 'char'
BT_Trade = '0'
BT_TradeSettle = '1'
T['RiskLevel'] = 'char'
FAS_Low = '1'
FAS_Normal = '2'
FAS_Focus = '3'
FAS_Risk = '4'
T['FeeAcceptStyle'] = 'char'
FAS_ByTrade = '1'
FAS_ByDeliv = '2'
FAS_None = '3'
FAS_FixFee = '4'
T['PasswordType'] = 'char'
PWDT_Trade = '1'
PWDT_Account = '2'
T['Algorithm'] = 'char'
AG_All = '1'
AG_OnlyLost = '2'
AG_OnlyGain = '3'
AG_None = '4'
T['IncludeCloseProfit'] = 'char'
ICP_Include = '0'
ICP_NotInclude = '2'
T['AllWithoutTrade'] = 'char'
AWT_Enable = '0'
AWT_Disable = '2'
AWT_NoHoldEnable = '3'
T['Comment'] = 'char[31]'
T['Version'] = 'char[4]'
T['TradeCode'] = 'char[7]'
T['TradeDate'] = 'char[9]'
T['TradeTime'] = 'char[9]'
T['TradeSerial'] = 'char[9]'
T['TradeSerialNo'] = 'int'
T['FutureID'] = 'char[11]'
T['BankID'] = 'char[4]'
T['BankBrchID'] = 'char[5]'
T['BankBranchID'] = 'char[11]'
T['OperNo'] = 'char[17]'
T['DeviceID'] = 'char[3]'
T['RecordNum'] = 'char[7]'
T['FutureAccount'] = 'char[22]'
T['FuturePwdFlag'] = 'char'
FPWD_UnCheck = '0'
FPWD_Check = '1'
T['TransferType'] = 'char'
TT_BankToFuture = '0'
TT_FutureToBank = '1'
T['FutureAccPwd'] = 'char[17]'
T['CurrencyCode'] = 'char[4]'
T['RetCode'] = 'char[5]'
T['RetInfo'] = 'char[129]'
T['TradeAmt'] = 'char[20]'
T['UseAmt'] = 'char[20]'
T['FetchAmt'] = 'char[20]'
T['TransferValidFlag'] = 'char'
TVF_Invalid = '0'
TVF_Valid = '1'
TVF_Reverse = '2'
T['CertCode'] = 'char[21]'
T['Reason'] = 'char'
RN_CD = '0'
RN_ZT = '1'
RN_QT = '2'
T['FundProjectID'] = 'char[5]'
T['Sex'] = 'char'
SEX_None = '0'
SEX_Man = '1'
SEX_Woman = '2'
T['Profession'] = 'char[101]'
T['National'] = 'char[31]'
T['Province'] = 'char[51]'
T['Region'] = 'char[16]'
T['Country'] = 'char[16]'
T['LicenseNO'] = 'char[33]'
T['CompanyType'] = 'char[16]'
T['BusinessScope'] = 'char[1001]'
T['CapitalCurrency'] = 'char[4]'
T['UserType'] = 'char'
UT_Investor = '0'
UT_Operator = '1'
UT_SuperUser = '2'
T['RateType'] = 'char'
RATETYPE_MarginRate = '2'
T['NoteType'] = 'char'
NOTETYPE_TradeSettleBill = '1'
NOTETYPE_TradeSettleMonth = '2'
NOTETYPE_CallMarginNotes = '3'
NOTETYPE_ForceCloseNotes = '4'
NOTETYPE_TradeNotes = '5'
NOTETYPE_DelivNotes = '6'
T['SettlementStyle'] = 'char'
SBS_Day = '1'
SBS_Volume = '2'
T['BrokerDNS'] = 'char[256]'
T['Sentence'] = 'char[501]'
T['SettlementBillType'] = 'char'
ST_Day = '0'
ST_Month = '1'
T['UserRightType'] = 'char'
URT_Logon = '1'
URT_Transfer = '2'
URT_EMail = '3'
URT_Fax = '4'
URT_ConditionOrder = '5'
T['MarginPriceType'] = 'char'
MPT_PreSettlementPrice = '1'
MPT_SettlementPrice = '2'
MPT_AveragePrice = '3'
MPT_OpenPrice = '4'
T['BillGenStatus'] = 'char'
BGS_None = '0'
BGS_NoGenerated = '1'
BGS_Generated = '2'
T['AlgoType'] = 'char'
AT_HandlePositionAlgo = '1'
AT_FindMarginRateAlgo = '2'
T['HandlePositionAlgoID'] = 'char'
HPA_Base = '1'
HPA_DCE = '2'
HPA_CZCE = '3'
T['FindMarginRateAlgoID'] = 'char'
FMRA_Base = '1'
FMRA_DCE = '2'
FMRA_CZCE = '3'
T['HandleTradingAccountAlgoID'] = 'char'
HTAA_Base = '1'
HTAA_DCE = '2'
HTAA_CZCE = '3'
T['PersonType'] = 'char'
PST_Order = '1'
PST_Open = '2'
PST_Fund = '3'
PST_Settlement = '4'
PST_Company = '5'
PST_Corporation = '6'
PST_LinkMan = '7'
PST_Ledger = '8'
PST_Trustee = '9'
PST_TrusteeCorporation = 'A'
PST_TrusteeOpen = 'B'
PST_TrusteeContact = 'C'
PST_ForeignerRefer = 'D'
PST_CorporationRefer = 'E'
T['QueryInvestorRange'] = 'char'
QIR_All = '1'
QIR_Group = '2'
QIR_Single = '3'
T['InvestorRiskStatus'] = 'char'
IRS_Normal = '1'
IRS_Warn = '2'
IRS_Call = '3'
IRS_Force = '4'
IRS_Exception = '5'
T['LegID'] = 'int'
T['LegMultiple'] = 'int'
T['ImplyLevel'] = 'int'
T['ClearAccount'] = 'char[33]'
T['OrganNO'] = 'char[6]'
T['ClearbarchID'] = 'char[6]'
T['UserEventType'] = 'char'
UET_Login = '1'
UET_Logout = '2'
UET_Trading = '3'
UET_TradingError = '4'
UET_UpdatePassword = '5'
UET_Authenticate = '6'
UET_Other = '9'
T['UserEventInfo'] = 'char[1025]'
T['CloseStyle'] = 'char'
ICS_Close = '0'
ICS_CloseToday = '1'
T['StatMode'] = 'char'
SM_Non = '0'
SM_Instrument = '1'
SM_Product = '2'
SM_Investor = '3'
T['ParkedOrderStatus'] = 'char'
PAOS_NotSend = '1'
PAOS_Send = '2'
PAOS_Deleted = '3'
T['ParkedOrderID'] = 'char[13]'
T['ParkedOrderActionID'] = 'char[13]'
T['VirDealStatus'] = 'char'
VDS_Dealing = '1'
VDS_DeaclSucceed = '2'
T['OrgSystemID'] = 'char'
ORGS_Standard = '0'
ORGS_ESunny = '1'
ORGS_KingStarV6 = '2'
T['VirTradeStatus'] = 'char'
VTS_NaturalDeal = '0'
VTS_SucceedEnd = '1'
VTS_FailedEND = '2'
VTS_Exception = '3'
VTS_ManualDeal = '4'
VTS_MesException = '5'
VTS_SysException = '6'
T['VirBankAccType'] = 'char'
VBAT_BankBook = '1'
VBAT_BankCard = '2'
VBAT_CreditCard = '3'
T['VirementStatus'] = 'char'
VMS_Natural = '0'
VMS_Canceled = '9'
T['VirementAvailAbility'] = 'char'
VAA_NoAvailAbility = '0'
VAA_AvailAbility = '1'
VAA_Repeal = '2'
T['VirementTradeCode'] = 'char[7]'
VTC_BankBankToFuture = '102001'
VTC_BankFutureToBank = '102002'
VTC_FutureBankToFuture = '202001'
VTC_FutureFutureToBank = '202002'
T['PhotoTypeName'] = 'char[41]'
T['PhotoTypeID'] = 'char[5]'
T['PhotoName'] = 'char[161]'
T['TopicID'] = 'int'
T['ReportTypeID'] = 'char[3]'
T['CharacterID'] = 'char[5]'
T['AMLParamID'] = 'char[21]'
T['AMLInvestorType'] = 'char[3]'
T['AMLIdCardType'] = 'char[3]'
T['AMLTradeDirect'] = 'char[3]'
T['AMLTradeModel'] = 'char[3]'
T['AMLParamID'] = 'char[21]'
T['AMLOpParamValue'] = 'double'
T['AMLCustomerCardType'] = 'char[81]'
T['AMLInstitutionName'] = 'char[65]'
T['AMLDistrictID'] = 'char[7]'
T['AMLRelationShip'] = 'char[3]'
T['AMLInstitutionType'] = 'char[3]'
T['AMLInstitutionID'] = 'char[13]'
T['AMLAccountType'] = 'char[5]'
T['AMLTradingType'] = 'char[7]'
T['AMLTransactClass'] = 'char[7]'
T['AMLCapitalIO'] = 'char[3]'
T['AMLSite'] = 'char[10]'
T['AMLCapitalPurpose'] = 'char[129]'
T['AMLReportType'] = 'char[2]'
T['AMLSerialNo'] = 'char[5]'
T['AMLStatus'] = 'char[2]'
T['AMLGenStatus'] = 'char'
GEN_Program = '0'
GEN_HandWork = '1'
T['AMLSeqCode'] = 'char[65]'
T['AMLFileName'] = 'char[257]'
T['AMLMoney'] = 'double'
T['AMLFileAmount'] = 'int'
T['CFMMCKey'] = 'char[21]'
T['CFMMCToken'] = 'char[21]'
T['CFMMCKeyKind'] = 'char'
CFMMCKK_REQUEST = 'R'
CFMMCKK_AUTO = 'A'
CFMMCKK_MANUAL = 'M'
T['AMLReportName'] = 'char[81]'
T['IndividualName'] = 'char[51]'
T['CurrencyID'] = 'char[4]'
T['CustNumber'] = 'char[36]'
T['OrganCode'] = 'char[36]'
T['OrganName'] = 'char[71]'
T['SuperOrganCode'] = 'char[12]'
T['SubBranchID'] = 'char[31]'
T['SubBranchName'] = 'char[71]'
T['BranchNetCode'] = 'char[31]'
T['BranchNetName'] = 'char[71]'
T['OrganFlag'] = 'char[2]'
T['BankCodingForFuture'] = 'char[33]'
T['BankReturnCode'] = 'char[7]'
T['PlateReturnCode'] = 'char[5]'
T['BankSubBranchID'] = 'char[31]'
T['FutureBranchID'] = 'char[31]'
T['ReturnCode'] = 'char[7]'
T['OperatorCode'] = 'char[17]'
T['ClearDepID'] = 'char[6]'
T['ClearBrchID'] = 'char[6]'
T['ClearName'] = 'char[71]'
T['BankAccountName'] = 'char[71]'
T['InvDepID'] = 'char[6]'
T['InvBrchID'] = 'char[6]'
T['MessageFormatVersion'] = 'char[36]'
T['Digest'] = 'char[36]'
T['AuthenticData'] = 'char[129]'
T['PasswordKey'] = 'char[129]'
T['FutureAccountName'] = 'char[129]'
T['MobilePhone'] = 'char[21]'
T['FutureMainKey'] = 'char[129]'
T['FutureWorkKey'] = 'char[129]'
T['FutureTransKey'] = 'char[129]'
T['BankMainKey'] = 'char[129]'
T['BankWorkKey'] = 'char[129]'
T['BankTransKey'] = 'char[129]'
T['BankServerDescription'] = 'char[129]'
T['AddInfo'] = 'char[129]'
T['DescrInfoForReturnCode'] = 'char[129]'
T['CountryCode'] = 'char[21]'
T['Serial'] = 'int'
T['PlateSerial'] = 'int'
T['BankSerial'] = 'char[13]'
T['CorrectSerial'] = 'int'
T['FutureSerial'] = 'int'
T['ApplicationID'] = 'int'
T['BankProxyID'] = 'int'
T['FBTCoreID'] = 'int'
T['ServerPort'] = 'int'
T['RepealedTimes'] = 'int'
T['RepealTimeInterval'] = 'int'
T['TotalTimes'] = 'int'
T['FBTRequestID'] = 'int'
T['TID'] = 'int'
T['TradeAmount'] = 'double'
T['CustFee'] = 'double'
T['FutureFee'] = 'double'
T['SingleMaxAmt'] = 'double'
T['SingleMinAmt'] = 'double'
T['TotalAmt'] = 'double'
T['CertificationType'] = 'char'
CFT_IDCard = '0'
CFT_Passport = '1'
CFT_OfficerIDCard = '2'
CFT_SoldierIDCard = '3'
CFT_HomeComingCard = '4'
CFT_HouseholdRegister = '5'
CFT_LicenseNo = '6'
CFT_InstitutionCodeCard = '7'
CFT_TempLicenseNo = '8'
CFT_NoEnterpriseLicenseNo = '9'
CFT_OtherCard = 'x'
CFT_SuperDepAgree = 'a'
T['FileBusinessCode'] = 'char'
FBC_Others = '0'
FBC_TransferDetails = '1'
FBC_CustAccStatus = '2'
FBC_AccountTradeDetails = '3'
FBC_FutureAccountChangeInfoDetails = '4'
FBC_CustMoneyDetail = '5'
FBC_CustCancelAccountInfo = '6'
FBC_CustMoneyResult = '7'
FBC_OthersExceptionResult = '8'
FBC_CustInterestNetMoneyDetails = '9'
FBC_CustMoneySendAndReceiveDetails = 'a'
FBC_CorporationMoneyTotal = 'b'
FBC_MainbodyMoneyTotal = 'c'
FBC_MainPartMonitorData = 'd'
FBC_PreparationMoney = 'e'
FBC_BankMoneyMonitorData = 'f'
T['CashExchangeCode'] = 'char'
CEC_Exchange = '1'
CEC_Cash = '2'
T['YesNoIndicator'] = 'char'
YNI_Yes = '0'
YNI_No = '1'
T['BanlanceType'] = 'char'
BLT_CurrentMoney = '0'
BLT_UsableMoney = '1'
BLT_FetchableMoney = '2'
BLT_FreezeMoney = '3'
T['Gender'] = 'char'
GD_Unknown = '0'
GD_Male = '1'
GD_Female = '2'
T['FeePayFlag'] = 'char'
FPF_BEN = '0'
FPF_OUR = '1'
FPF_SHA = '2'
T['PassWordKeyType'] = 'char'
PWKT_ExchangeKey = '0'
PWKT_PassWordKey = '1'
PWKT_MACKey = '2'
PWKT_MessageKey = '3'
T['FBTPassWordType'] = 'char'
PWT_Query = '0'
PWT_Fetch = '1'
PWT_Transfer = '2'
PWT_Trade = '3'
T['FBTEncryMode'] = 'char'
EM_NoEncry = '0'
EM_DES = '1'
EM_3DES = '2'
T['BankRepealFlag'] = 'char'
BRF_BankNotNeedRepeal = '0'
BRF_BankWaitingRepeal = '1'
BRF_BankBeenRepealed = '2'
T['BrokerRepealFlag'] = 'char'
BRORF_BrokerNotNeedRepeal = '0'
BRORF_BrokerWaitingRepeal = '1'
BRORF_BrokerBeenRepealed = '2'
T['InstitutionType'] = 'char'
TS_Bank = '0'
TS_Future = '1'
TS_Store = '2'
T['LastFragment'] = 'char'
LF_Yes = '0'
LF_No = '1'
T['BankAccStatus'] = 'char'
BAS_Normal = '0'
BAS_Freeze = '1'
BAS_ReportLoss = '2'
T['MoneyAccountStatus'] = 'char'
MAS_Normal = '0'
MAS_Cancel = '1'
T['ManageStatus'] = 'char'
MSS_Point = '0'
MSS_PrePoint = '1'
MSS_CancelPoint = '2'
T['SystemType'] = 'char'
SYT_FutureBankTransfer = '0'
SYT_StockBankTransfer = '1'
SYT_TheThirdPartStore = '2'
T['TxnEndFlag'] = 'char'
TEF_NormalProcessing = '0'
TEF_Success = '1'
TEF_Failed = '2'
TEF_Abnormal = '3'
TEF_ManualProcessedForException = '4'
TEF_CommuFailedNeedManualProcess = '5'
TEF_SysErrorNeedManualProcess = '6'
T['ProcessStatus'] = 'char'
PSS_NotProcess = '0'
PSS_StartProcess = '1'
PSS_Finished = '2'
T['CustType'] = 'char'
CUSTT_Person = '0'
CUSTT_Institution = '1'
T['FBTTransferDirection'] = 'char'
FBTTD_FromBankToFuture = '1'
FBTTD_FromFutureToBank = '2'
T['OpenOrDestroy'] = 'char'
OOD_Open = '1'
OOD_Destroy = '0'
T['AvailabilityFlag'] = 'char'
AVAF_Invalid = '0'
AVAF_Valid = '1'
AVAF_Repeal = '2'
T['OrganType'] = 'char'
OT_Bank = '1'
OT_Future = '2'
OT_PlateForm = '9'
T['OrganLevel'] = 'char'
OL_HeadQuarters = '1'
OL_Branch = '2'
T['ProtocalID'] = 'char'
PID_FutureProtocal = '0'
PID_ICBCProtocal = '1'
PID_ABCProtocal = '2'
PID_CBCProtocal = '3'
PID_CCBProtocal = '4'
PID_BOCOMProtocal = '5'
PID_FBTPlateFormProtocal = 'X'
T['ConnectMode'] = 'char'
CM_ShortConnect = '0'
CM_LongConnect = '1'
T['SyncMode'] = 'char'
SRM_ASync = '0'
SRM_Sync = '1'
T['BankAccType'] = 'char'
BAT_BankBook = '1'
BAT_SavingCard = '2'
BAT_CreditCard = '3'
T['FutureAccType'] = 'char'
FAT_BankBook = '1'
FAT_SavingCard = '2'
FAT_CreditCard = '3'
T['OrganStatus'] = 'char'
OS_Ready = '0'
OS_CheckIn = '1'
OS_CheckOut = '2'
OS_CheckFileArrived = '3'
OS_CheckDetail = '4'
OS_DayEndClean = '5'
OS_Invalid = '9'
T['CCBFeeMode'] = 'char'
CCBFM_ByAmount = '1'
CCBFM_ByMonth = '2'
T['CommApiType'] = 'char'
CAPIT_Client = '1'
CAPIT_Server = '2'
CAPIT_UserApi = '3'
T['ServiceID'] = 'int'
T['ServiceLineNo'] = 'int'
T['ServiceName'] = 'char[61]'
T['LinkStatus'] = 'char'
LS_Connected = '1'
LS_Disconnected = '2'
T['CommApiPointer'] = 'int'
T['PwdFlag'] = 'char'
BPWDF_NoCheck = '0'
BPWDF_BlankCheck = '1'
BPWDF_EncryptCheck = '2'
T['SecuAccType'] = 'char'
SAT_AccountID = '1'
SAT_CardID = '2'
SAT_SHStockholderID = '3'
SAT_SZStockholderID = '4'
T['TransferStatus'] = 'char'
TRFS_Normal = '0'
TRFS_Repealed = '1'
T['SponsorType'] = 'char'
SPTYPE_Broker = '0'
SPTYPE_Bank = '1'
T['ReqRspType'] = 'char'
REQRSP_Request = '0'
REQRSP_Response = '1'
T['FBTUserEventType'] = 'char'
FBTUET_SignIn = '0'
FBTUET_FromBankToFuture = '1'
FBTUET_FromFutureToBank = '2'
FBTUET_OpenAccount = '3'
FBTUET_CancelAccount = '4'
FBTUET_ChangeAccount = '5'
FBTUET_RepealFromBankToFuture = '6'
FBTUET_RepealFromFutureToBank = '7'
FBTUET_QueryBankAccount = '8'
FBTUET_QueryFutureAccount = '9'
FBTUET_SignOut = 'A'
FBTUET_SyncKey = 'B'
FBTUET_Other = 'Z'
T['BankIDByBank'] = 'char[21]'
T['BankOperNo'] = 'char[4]'
T['BankCustNo'] = 'char[21]'
T['DBOPSeqNo'] = 'int'
T['TableName'] = 'char[61]'
T['PKName'] = 'char[201]'
T['PKValue'] = 'char[501]'
T['DBOperation'] = 'char'
DBOP_Insert = '0'
DBOP_Update = '1'
DBOP_Delete = '2'
T['SyncFlag'] = 'char'
SYNF_Yes = '0'
SYNF_No = '1'
T['TargetID'] = 'char[4]'
T['SyncType'] = 'char'
SYNT_OneOffSync = '0'
SYNT_TimerSync = '1'
SYNT_TimerFullSync = '2'
T['FBETime'] = 'char[7]'
T['FBEBankNo'] = 'char[13]'
T['FBECertNo'] = 'char[13]'
T['ExDirection'] = 'char'
FBEDIR_Settlement = '0'
FBEDIR_Sale = '1'
T['FBEBankAccount'] = 'char[33]'
T['FBEBankAccountName'] = 'char[61]'
T['FBEAmt'] = 'double'
T['FBEBusinessType'] = 'char[3]'
T['FBEPostScript'] = 'char[61]'
T['FBERemark'] = 'char[71]'
T['ExRate'] = 'double'
T['FBEResultFlag'] = 'char'
FBERES_Success = '0'
FBERES_InsufficientBalance = '1'
FBERES_UnknownTrading = '8'
FBERES_Fail = 'x'
T['FBERtnMsg'] = 'char[61]'
T['FBEExtendMsg'] = 'char[61]'
T['FBEBusinessSerial'] = 'char[31]'
T['FBESystemSerial'] = 'char[21]'
T['FBETotalExCnt'] = 'int'
T['FBEExchStatus'] = 'char'
FBEES_Normal = '0'
FBEES_ReExchange = '1'
T['FBEFileFlag'] = 'char'
FBEFG_DataPackage = '0'
FBEFG_File = '1'
T['FBEAlreadyTrade'] = 'char'
FBEAT_NotTrade = '0'
FBEAT_Trade = '1'
T['FBEOpenBank'] = 'char[61]'
T['FBEUserEventType'] = 'char'
FBEUET_SignIn = '0'
FBEUET_Exchange = '1'
FBEUET_ReExchange = '2'
FBEUET_QueryBankAccount = '3'
FBEUET_QueryExchDetial = '4'
FBEUET_QueryExchSummary = '5'
FBEUET_QueryExchRate = '6'
FBEUET_CheckBankAccount = '7'
FBEUET_SignOut = '8'
FBEUET_Other = 'Z'
T['FBEFileName'] = 'char[21]'
T['FBEBatchSerial'] = 'char[21]'
T['FBEReqFlag'] = 'char'
FBERF_UnProcessed = '0'
FBERF_WaitSend = '1'
FBERF_SendSuccess = '2'
FBERF_SendFailed = '3'
FBERF_WaitReSend = '4'
T['NotifyClass'] = 'char'
NC_NOERROR = '0'
NC_Warn = '1'
NC_Call = '2'
NC_Force = '3'
NC_CHUANCANG = '4'
NC_Exception = '5'
T['RiskNofityInfo'] = 'char[257]'
T['ForceCloseSceneId'] = 'char[24]'
T['ForceCloseType'] = 'char'
FCT_Manual = '0'
FCT_Single = '1'
FCT_Group = '2'
T['InstrumentIDs'] = 'char[101]'
T['RiskNotifyMethod'] = 'char'
RNM_System = '0'
RNM_SMS = '1'
RNM_EMail = '2'
RNM_Manual = '3'
T['RiskNotifyStatus'] = 'char'
RNS_NotGen = '0'
RNS_Generated = '1'
RNS_SendError = '2'
RNS_SendOk = '3'
RNS_Received = '4'
RNS_Confirmed = '5'
T['RiskUserEvent'] = 'char'
RUE_ExportData = '0'
T['ParamID'] = 'int'
T['ParamName'] = 'char[41]'
T['ParamValue'] = 'char[41]'
T['ConditionalOrderSortType'] = 'char'
COST_LastPriceAsc = '0'
COST_LastPriceDesc = '1'
COST_AskPriceAsc = '2'
COST_AskPriceDesc = '3'
COST_BidPriceAsc = '4'
COST_BidPriceDesc = '5'
T['SendType'] = 'char'
UOAST_NoSend = '0'
UOAST_Sended = '1'
UOAST_Generated = '2'
UOAST_SendFail = '3'
UOAST_Success = '4'
UOAST_Fail = '5'
UOAST_Cancel = '6'
T['ClientIDStatus'] = 'char'
UOACS_NoApply = '1'
UOACS_Submited = '2'
UOACS_Sended = '3'
UOACS_Success = '4'
UOACS_Refuse = '5'
UOACS_Cancel = '6'
T['IndustryID'] = 'char[17]'
T['QuestionID'] = 'char[5]'
T['QuestionContent'] = 'char[41]'
T['OptionID'] = 'char[13]'
T['OptionContent'] = 'char[61]'
T['QuestionType'] = 'char'
QT_Radio = '1'
QT_Option = '2'
QT_Blank = '3'
T['ProcessID'] = 'char[33]'
T['SeqNo'] = 'int'
T['UOAProcessStatus'] = 'char[3]'
T['ProcessType'] = 'char[3]'
T['BusinessType'] = 'char'
BT_Request = '1'
BT_Response = '2'
BT_Notice = '3'
T['CfmmcReturnCode'] = 'char'
CRC_Success = '0'
CRC_Working = '1'
CRC_InfoFail = '2'
CRC_IDCardFail = '3'
CRC_OtherFail = '4'
T['ExReturnCode'] = 'int'
T['ClientType'] = 'char'
CfMMCCT_All = '0'
CfMMCCT_Person = '1'
CfMMCCT_Company = '2'
CfMMCCT_Other = '3'
CfMMCCT_SpecialOrgan = '4'
CfMMCCT_Asset = '5'
T['ExchangeIDType'] = 'char'
EIDT_SHFE = 'S'
EIDT_CZCE = 'Z'
EIDT_DCE = 'D'
EIDT_CFFEX = 'J'
EIDT_INE = 'N'
T['ExClientIDType'] = 'char'
ECIDT_Hedge = '1'
ECIDT_Arbitrage = '2'
ECIDT_Speculation = '3'
T['ClientClassify'] = 'char[11]'
T['UOAOrganType'] = 'char[11]'
T['UOACountryCode'] = 'char[11]'
T['AreaCode'] = 'char[11]'
T['FuturesID'] = 'char[21]'
T['CffmcDate'] = 'char[11]'
T['CffmcTime'] = 'char[11]'
T['NocID'] = 'char[21]'
T['UpdateFlag'] = 'char'
UF_NoUpdate = '0'
UF_Success = '1'
UF_Fail = '2'
UF_TCSuccess = '3'
UF_TCFail = '4'
UF_Cancel = '5'
T['ApplyOperateID'] = 'char'
AOID_OpenInvestor = '1'
AOID_ModifyIDCard = '2'
AOID_ModifyNoIDCard = '3'
AOID_ApplyTradingCode = '4'
AOID_CancelTradingCode = '5'
AOID_CancelInvestor = '6'
AOID_FreezeAccount = '8'
AOID_ActiveFreezeAccount = '9'
T['ApplyStatusID'] = 'char'
ASID_NoComplete = '1'
ASID_Submited = '2'
ASID_Checked = '3'
ASID_Refused = '4'
ASID_Deleted = '5'
T['SendMethod'] = 'char'
UOASM_ByAPI = '1'
UOASM_ByFile = '2'
T['EventType'] = 'char[33]'
T['EventMode'] = 'char'
EvM_ADD = '1'
EvM_UPDATE = '2'
EvM_DELETE = '3'
EvM_CHECK = '4'
EvM_COPY = '5'
EvM_CANCEL = '6'
EvM_Reverse = '7'
T['UOAAutoSend'] = 'char'
UOAA_ASR = '1'
UOAA_ASNR = '2'
UOAA_NSAR = '3'
UOAA_NSR = '4'
T['QueryDepth'] = 'int'
T['DataCenterID'] = 'int'
T['FlowID'] = 'char'
EvM_InvestorGroupFlow = '1'
EvM_InvestorRate = '2'
EvM_InvestorCommRateModel = '3'
T['CheckLevel'] = 'char'
CL_Zero = '0'
CL_One = '1'
CL_Two = '2'
T['CheckNo'] = 'int'
T['CheckStatus'] = 'char'
CHS_Init = '0'
CHS_Checking = '1'
CHS_Checked = '2'
CHS_Refuse = '3'
CHS_Cancel = '4'
T['UsedStatus'] = 'char'
CHU_Unused = '0'
CHU_Used = '1'
CHU_Fail = '2'
T['RateTemplateName'] = 'char[61]'
T['PropertyString'] = 'char[2049]'
T['BankAcountOrigin'] = 'char'
BAO_ByAccProperty = '0'
BAO_ByFBTransfer = '1'
T['MonthBillTradeSum'] = 'char'
MBTS_ByInstrument = '0'
MBTS_ByDayInsPrc = '1'
MBTS_ByDayIns = '2'
T['FBTTradeCodeEnum'] = 'char[7]'
FTC_BankLaunchBankToBroker = '102001'
FTC_BrokerLaunchBankToBroker = '202001'
FTC_BankLaunchBrokerToBank = '102002'
FTC_BrokerLaunchBrokerToBank = '202002'
T['RateTemplateID'] = 'char[9]'
T['RiskRate'] = 'char[21]'
T['Timestamp'] = 'int'
T['InvestorIDRuleName'] = 'char[61]'
T['InvestorIDRuleExpr'] = 'char[513]'
T['LastDrift'] = 'int'
T['LastSuccess'] = 'int'
T['AuthKey'] = 'char[41]'
T['SerialNumber'] = 'char[17]'
T['OTPType'] = 'char'
OTP_NONE = '0'
OTP_TOTP = '1'
T['OTPVendorsID'] = 'char[2]'
T['OTPVendorsName'] = 'char[61]'
T['OTPStatus'] = 'char'
OTPS_Unused = '0'
OTPS_Used = '1'
OTPS_Disuse = '2'
T['BrokerUserType'] = 'char'
BUT_Investor = '1'
BUT_BrokerUser = '2'
T['FutureType'] = 'char'
FUTT_Commodity = '1'
FUTT_Financial = '2'
T['FundEventType'] = 'char'
FET_Restriction = '0'
FET_TodayRestriction = '1'
FET_Transfer = '2'
FET_Credit = '3'
FET_InvestorWithdrawAlm = '4'
FET_BankRestriction = '5'
FET_Accountregister = '6'
FET_ExchangeFundIO = '7'
FET_InvestorFundIO = '8'
T['AccountSourceType'] = 'char'
AST_FBTransfer = '0'
AST_ManualEntry = '1'
T['CodeSourceType'] = 'char'
CST_UnifyAccount = '0'
CST_ManualEntry = '1'
T['UserRange'] = 'char'
UR_All = '0'
UR_Single = '1'
T['TimeSpan'] = 'char[9]'
T['ImportSequenceID'] = 'char[17]'
T['ByGroup'] = 'char'
BG_Investor = '2'
BG_Group = '1'
T['TradeSumStatMode'] = 'char'
TSSM_Instrument = '1'
TSSM_Product = '2'
TSSM_Exchange = '3'
T['ComType'] = 'int'
T['UserProductID'] = 'char[33]'
T['UserProductName'] = 'char[65]'
T['UserProductMemo'] = 'char[129]'
T['CSRCCancelFlag'] = 'char[2]'
T['CSRCDate'] = 'char[11]'
T['CSRCInvestorName'] = 'char[201]'
T['CSRCOpenInvestorName'] = 'char[101]'
T['CSRCInvestorID'] = 'char[13]'
T['CSRCIdentifiedCardNo'] = 'char[51]'
T['CSRCClientID'] = 'char[11]'
T['CSRCBankFlag'] = 'char[3]'
T['CSRCBankAccount'] = 'char[23]'
T['CSRCOpenName'] = 'char[401]'
T['CSRCMemo'] = 'char[101]'
T['CSRCTime'] = 'char[11]'
T['CSRCTradeID'] = 'char[21]'
T['CSRCExchangeInstID'] = 'char[31]'
T['CSRCMortgageName'] = 'char[7]'
T['CSRCReason'] = 'char[3]'
T['IsSettlement'] = 'char[2]'
T['CSRCMoney'] = 'double'
T['CSRCPrice'] = 'double'
T['CSRCOptionsType'] = 'char[2]'
T['CSRCStrikePrice'] = 'double'
T['CSRCTargetProductID'] = 'char[3]'
T['CSRCTargetInstrID'] = 'char[31]'
T['CommModelName'] = 'char[161]'
T['CommModelMemo'] = 'char[1025]'
T['ExprSetMode'] = 'char'
ESM_Relative = '1'
ESM_Typical = '2'
T['RateInvestorRange'] = 'char'
RIR_All = '1'
RIR_Model = '2'
RIR_Single = '3'
T['AgentBrokerID'] = 'char[13]'
T['DRIdentityID'] = 'int'
T['DRIdentityName'] = 'char[65]'
T['DBLinkID'] = 'char[31]'
T['SyncDataStatus'] = 'char'
SDS_Initialize = '0'
SDS_Settlementing = '1'
SDS_Settlemented = '2'
T['TradeSource'] = 'char'
TSRC_NORMAL = '0'
TSRC_QUERY = '1'
T['FlexStatMode'] = 'char'
FSM_Product = '1'
FSM_Exchange = '2'
FSM_All = '3'
T['ByInvestorRange'] = 'char'
BIR_Property = '1'
BIR_All = '2'
T['SRiskRate'] = 'char[21]'
T['SequenceNo12'] = 'int'
T['PropertyInvestorRange'] = 'char'
PIR_All = '1'
PIR_Property = '2'
PIR_Single = '3'
T['FileStatus'] = 'char'
FIS_NoCreate = '0'
FIS_Created = '1'
FIS_Failed = '2'
T['FileGenStyle'] = 'char'
FGS_FileTransmit = '0'
FGS_FileGen = '1'
T['SysOperMode'] = 'char'
SoM_Add = '1'
SoM_Update = '2'
SoM_Delete = '3'
SoM_Copy = '4'
SoM_AcTive = '5'
SoM_CanCel = '6'
SoM_ReSet = '7'
T['SysOperType'] = 'char'
SoT_UpdatePassword = '0'
SoT_UserDepartment = '1'
SoT_RoleManager = '2'
SoT_RoleFunction = '3'
SoT_BaseParam = '4'
SoT_SetUserID = '5'
SoT_SetUserRole = '6'
SoT_UserIpRestriction = '7'
SoT_DepartmentManager = '8'
SoT_DepartmentCopy = '9'
SoT_Tradingcode = 'A'
SoT_InvestorStatus = 'B'
SoT_InvestorAuthority = 'C'
SoT_PropertySet = 'D'
SoT_ReSetInvestorPasswd = 'E'
SoT_InvestorPersonalityInfo = 'F'
T['CSRCDataQueyType'] = 'char'
CSRCQ_Current = '0'
CSRCQ_History = '1'
T['FreezeStatus'] = 'char'
FRS_Normal = '1'
FRS_Freeze = '0'
T['StandardStatus'] = 'char'
STST_Standard = '0'
STST_NonStandard = '1'
T['CSRCFreezeStatus'] = 'char[2]'
T['RightParamType'] = 'char'
RPT_Freeze = '1'
RPT_FreezeActive = '2'
RPT_OpenLimit = '3'
RPT_RelieveOpenLimit = '4'
T['RightTemplateID'] = 'char[9]'
T['RightTemplateName'] = 'char[61]'
T['DataStatus'] = 'char'
AMLDS_Normal = '0'
AMLDS_Deleted = '1'
T['AMLCheckStatus'] = 'char'
AMLCHS_Init = '0'
AMLCHS_Checking = '1'
AMLCHS_Checked = '2'
AMLCHS_RefuseReport = '3'
T['AmlDateType'] = 'char'
AMLDT_DrawDay = '0'
AMLDT_TouchDay = '1'
T['AmlCheckLevel'] = 'char'
AMLCL_CheckLevel0 = '0'
AMLCL_CheckLevel1 = '1'
AMLCL_CheckLevel2 = '2'
AMLCL_CheckLevel3 = '3'
T['AmlCheckFlow'] = 'char[2]'
T['DataType'] = 'char[129]'
T['ExportFileType'] = 'char'
EFT_CSV = '0'
EFT_EXCEL = '1'
EFT_DBF = '2'
T['SettleManagerType'] = 'char'
SMT_Before = '1'
SMT_Settlement = '2'
SMT_After = '3'
SMT_Settlemented = '4'
T['SettleManagerID'] = 'char[33]'
T['SettleManagerName'] = 'char[129]'
T['SettleManagerLevel'] = 'char'
SML_Must = '1'
SML_Alarm = '2'
SML_Prompt = '3'
SML_Ignore = '4'
T['SettleManagerGroup'] = 'char'
SMG_Exhcange = '1'
SMG_ASP = '2'
SMG_CSRC = '3'
T['CheckResultMemo'] = 'char[1025]'
T['FunctionUrl'] = 'char[1025]'
T['AuthInfo'] = 'char[129]'
T['AuthCode'] = 'char[17]'
T['LimitUseType'] = 'char'
LUT_Repeatable = '1'
LUT_Unrepeatable = '2'
T['DataResource'] = 'char'
DAR_Settle = '1'
DAR_Exchange = '2'
DAR_CSRC = '3'
T['MarginType'] = 'char'
MGT_ExchMarginRate = '0'
MGT_InstrMarginRate = '1'
MGT_InstrMarginRateTrade = '2'
T['ActiveType'] = 'char'
ACT_Intraday = '1'
ACT_Long = '2'
T['MarginRateType'] = 'char'
MRT_Exchange = '1'
MRT_Investor = '2'
MRT_InvestorTrade = '3'
T['BackUpStatus'] = 'char'
BUS_UnBak = '0'
BUS_BakUp = '1'
BUS_BakUped = '2'
BUS_BakFail = '3'
T['InitSettlement'] = 'char'
SIS_UnInitialize = '0'
SIS_Initialize = '1'
SIS_Initialized = '2'
T['ReportStatus'] = 'char'
SRS_NoCreate = '0'
SRS_Create = '1'
SRS_Created = '2'
SRS_CreateFail = '3'
T['SaveStatus'] = 'char'
SSS_UnSaveData = '0'
SSS_SaveDatad = '1'
T['SettArchiveStatus'] = 'char'
SAS_UnArchived = '0'
SAS_Archiving = '1'
SAS_Archived = '2'
SAS_ArchiveFail = '3'
T['CTPType'] = 'char'
CTPT_Unkown = '0'
CTPT_MainCenter = '1'
CTPT_BackUp = '2'
T['ToolID'] = 'char[9]'
T['ToolName'] = 'char[81]'
T['CloseDealType'] = 'char'
CDT_Normal = '0'
CDT_SpecFirst = '1'
T['MortgageFundUseRange'] = 'char'
MFUR_None = '0'
MFUR_Margin = '1'
MFUR_All = '2'
T['CurrencyUnit'] = 'double'
T['ExchangeRate'] = 'double'
T['SpecProductType'] = 'char'
SPT_CzceHedge = '1'
SPT_IneForeignCurrency = '2'
SPT_DceOpenClose = '3'
T['FundMortgageType'] = 'char'
FMT_Mortgage = '1'
FMT_Redemption = '2'
T['AccountSettlementParamID'] = 'char'
ASPI_BaseMargin = '1'
ASPI_LowestInterest = '2'
T['CurrencyName'] = 'char[31]'
T['CurrencySign'] = 'char[4]'
T['FundMortDirection'] = 'char'
FMD_In = '1'
FMD_Out = '2'
T['BusinessClass'] = 'char'
BT_Profit = '0'
BT_Loss = '1'
BT_Other = 'Z'
T['SwapSourceType'] = 'char'
SST_Manual = '0'
SST_Automatic = '1'
T['CurrExDirection'] = 'char'
CED_Settlement = '0'
CED_Sale = '1'
T['CurrencySwapStatus'] = 'char'
CSS_Entry = '1'
CSS_Approve = '2'
CSS_Refuse = '3'
CSS_Revoke = '4'
CSS_Send = '5'
CSS_Success = '6'
CSS_Failure = '7'
T['CurrExchCertNo'] = 'char[13]'
T['BatchSerialNo'] = 'char[21]'
T['ReqFlag'] = 'char'
REQF_NoSend = '0'
REQF_SendSuccess = '1'
REQF_SendFailed = '2'
REQF_WaitReSend = '3'
T['ResFlag'] = 'char'
RESF_Success = '0'
RESF_InsuffiCient = '1'
RESF_UnKnown = '8'
T['PageControl'] = 'char[2]'
T['RecordCount'] = 'int'
T['CurrencySwapMemo'] = 'char[101]'
T['ExStatus'] = 'char'
EXS_Before = '0'
EXS_After = '1'
T['ClientRegion'] = 'char'
CR_Domestic = '1'
CR_GMT = '2'
CR_Foreign = '3'
T['WorkPlace'] = 'char[101]'
T['BusinessPeriod'] = 'char[21]'
T['WebSite'] = 'char[101]'
T['UOAIdCardType'] = 'char[3]'
T['ClientMode'] = 'char[3]'
T['InvestorFullName'] = 'char[101]'
T['UOABrokerID'] = 'char[11]'
T['UOAZipCode'] = 'char[11]'
T['UOAEMail'] = 'char[101]'
T['OldCity'] = 'char[41]'
T['CorporateIdentifiedCardNo'] = 'char[101]'
T['HasBoard'] = 'char'
HB_No = '0'
HB_Yes = '1'
T['StartMode'] = 'char'
SM_Normal = '1'
SM_Emerge = '2'
SM_Restore = '3'
T['TemplateType'] = 'char'
TPT_Full = '1'
TPT_Increment = '2'
TPT_BackUp = '3'
T['LoginMode'] = 'char'
LM_Trade = '0'
LM_Transfer = '1'
T['PromptType'] = 'char'
CPT_Instrument = '1'
CPT_Margin = '2'
T['LedgerManageID'] = 'char[51]'
T['InvestVariety'] = 'char[101]'
T['BankAccountType'] = 'char[2]'
T['LedgerManageBank'] = 'char[101]'
T['CffexDepartmentName'] = 'char[101]'
T['CffexDepartmentCode'] = 'char[9]'
T['HasTrustee'] = 'char'
HT_Yes = '1'
HT_No = '0'
T['CSRCMemo1'] = 'char[41]'
T['AssetmgrCFullName'] = 'char[101]'
T['AssetmgrApprovalNO'] = 'char[51]'
T['AssetmgrMgrName'] = 'char[401]'
T['AmType'] = 'char'
AMT_Bank = '1'
AMT_Securities = '2'
AMT_Fund = '3'
AMT_Insurance = '4'
AMT_Trust = '5'
AMT_Other = '9'
T['CSRCAmType'] = 'char[5]'
T['CSRCFundIOType'] = 'char'
CFIOT_FundIO = '0'
CFIOT_SwapCurrency = '1'
T['CusAccountType'] = 'char'
CAT_Futures = '1'
CAT_AssetmgrFuture = '2'
CAT_AssetmgrTrustee = '3'
CAT_AssetmgrTransfer = '4'
T['CSRCNational'] = 'char[4]'
T['CSRCSecAgentID'] = 'char[11]'
T['LanguageType'] = 'char'
LT_Chinese = '1'
LT_English = '2'
T['AmAccount'] = 'char[23]'
T['AssetmgrClientType'] = 'char'
AMCT_Person = '1'
AMCT_Organ = '2'
AMCT_SpecialOrgan = '4'
T['AssetmgrType'] = 'char'
ASST_Futures = '3'
ASST_SpecialOrgan = '4'
T['UOM'] = 'char[11]'
T['SHFEInstLifePhase'] = 'char[3]'
T['SHFEProductClass'] = 'char[11]'
T['PriceDecimal'] = 'char[2]'
T['InTheMoneyFlag'] = 'char[2]'
T['CheckInstrType'] = 'char'
CIT_HasExch = '0'
CIT_HasATP = '1'
CIT_HasDiff = '2'
T['DeliveryType'] = 'char'
DT_HandDeliv = '1'
DT_PersonDeliv = '2'
T['BigMoney'] = 'double'
T['MaxMarginSideAlgorithm'] = 'char'
MMSA_NO = '0'
MMSA_YES = '1'
T['DAClientType'] = 'char'
CACT_Person = '0'
CACT_Company = '1'
CACT_Other = '2'
T['CombinInstrID'] = 'char[61]'
T['CombinSettlePrice'] = 'char[61]'
T['DCEPriority'] = 'int'
T['TradeGroupID'] = 'int'
T['IsCheckPrepa'] = 'int'
T['UOAAssetmgrType'] = 'char'
UOAAT_Futures = '1'
UOAAT_SpecialOrgan = '2'
T['DirectionEn'] = 'char'
DEN_Buy = '0'
DEN_Sell = '1'
T['OffsetFlagEn'] = 'char'
OFEN_Open = '0'
OFEN_Close = '1'
OFEN_ForceClose = '2'
OFEN_CloseToday = '3'
OFEN_CloseYesterday = '4'
OFEN_ForceOff = '5'
OFEN_LocalForceClose = '6'
T['HedgeFlagEn'] = 'char'
HFEN_Speculation = '1'
HFEN_Arbitrage = '2'
HFEN_Hedge = '3'
T['FundIOTypeEn'] = 'char'
FIOTEN_FundIO = '1'
FIOTEN_Transfer = '2'
FIOTEN_SwapCurrency = '3'
T['FundTypeEn'] = 'char'
FTEN_Deposite = '1'
FTEN_ItemFund = '2'
FTEN_Company = '3'
FTEN_InnerTransfer = '4'
T['FundDirectionEn'] = 'char'
FDEN_In = '1'
FDEN_Out = '2'
T['FundMortDirectionEn'] = 'char'
FMDEN_In = '1'
FMDEN_Out = '2'
T['SwapBusinessType'] = 'char[3]'
T['OptionsType'] = 'char'
CP_CallOptions = '1'
CP_PutOptions = '2'
T['StrikeMode'] = 'char'
STM_Continental = '0'
STM_American = '1'
STM_Bermuda = '2'
T['StrikeType'] = 'char'
STT_Hedge = '0'
STT_Match = '1'
T['ApplyType'] = 'char'
APPT_NotStrikeNum = '4'
T['GiveUpDataSource'] = 'char'
GUDS_Gen = '0'
GUDS_Hand = '1'
T['ExecOrderSysID'] = 'char[21]'
T['ExecResult'] = 'char'
OER_NoExec = 'n'
OER_Canceled = 'c'
OER_OK = '0'
OER_NoPosition = '1'
OER_NoDeposit = '2'
OER_NoParticipant = '3'
OER_NoClient = '4'
OER_NoInstrument = '6'
OER_NoRight = '7'
OER_InvalidVolume = '8'
OER_NoEnoughHistoryTrade = '9'
OER_Unknown = 'a'
T['StrikeSequence'] = 'int'
T['StrikeTime'] = 'char[13]'
T['CombinationType'] = 'char'
COMBT_Future = '0'
COMBT_BUL = '1'
COMBT_BER = '2'
COMBT_STD = '3'
COMBT_STG = '4'
COMBT_PRT = '5'
COMBT_CLD = '6'
T['OptionRoyaltyPriceType'] = 'char'
ORPT_PreSettlementPrice = '1'
ORPT_OpenPrice = '4'
T['BalanceAlgorithm'] = 'char'
BLAG_Default = '1'
BLAG_IncludeOptValLost = '2'
T['ActionType'] = 'char'
ACTP_Exec = '1'
ACTP_Abandon = '2'
T['ForQuoteStatus'] = 'char'
FQST_Submitted = 'a'
FQST_Accepted = 'b'
FQST_Rejected = 'c'
T['ValueMethod'] = 'char'
VM_Absolute = '0'
VM_Ratio = '1'
T['ExecOrderPositionFlag'] = 'char'
EOPF_Reserve = '0'
EOPF_UnReserve = '1'
T['ExecOrderCloseFlag'] = 'char'
EOCF_AutoClose = '0'
EOCF_NotToClose = '1'
T['ProductType'] = 'char'
PTE_Futures = '1'
PTE_Options = '2'
T['CZCEUploadFileName'] = 'char'
CUFN_CUFN_O = 'O'
CUFN_CUFN_T = 'T'
CUFN_CUFN_P = 'P'
CUFN_CUFN_N = 'N'
CUFN_CUFN_L = 'L'
CUFN_CUFN_F = 'F'
CUFN_CUFN_C = 'C'
CUFN_CUFN_M = 'M'
T['DCEUploadFileName'] = 'char'
DUFN_DUFN_O = 'O'
DUFN_DUFN_T = 'T'
DUFN_DUFN_P = 'P'
DUFN_DUFN_F = 'F'
DUFN_DUFN_C = 'C'
DUFN_DUFN_D = 'D'
DUFN_DUFN_M = 'M'
DUFN_DUFN_S = 'S'
T['SHFEUploadFileName'] = 'char'
SUFN_SUFN_O = 'O'
SUFN_SUFN_T = 'T'
SUFN_SUFN_P = 'P'
SUFN_SUFN_F = 'F'
T['CFFEXUploadFileName'] = 'char'
CFUFN_SUFN_T = 'T'
CFUFN_SUFN_P = 'P'
CFUFN_SUFN_F = 'F'
CFUFN_SUFN_S = 'S'
T['CombDirection'] = 'char'
CMDR_Comb = '0'
CMDR_UnComb = '1'

class BaseStruct(object):

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, (', ').join('%s=%r' % (k, getattr(self, k)) for k, t in self._fields_))


class Dissemination(BaseStruct):

    def __init__(self, SequenceSeries=0, SequenceNo=0):
        self.SequenceSeries = ''
        self.SequenceNo = ''


class ReqUserLogin(BaseStruct):

    def __init__(self, TradingDay='', BrokerID='', UserID='', Password='', UserProductInfo='', InterfaceProductInfo='', ProtocolInfo='', MacAddress='', OneTimePassword='', ClientIPAddress=''):
        self.TradingDay = 'Date'
        self.BrokerID = ''
        self.UserID = ''
        self.Password = ''
        self.UserProductInfo = 'ProductInfo'
        self.InterfaceProductInfo = 'ProductInfo'
        self.ProtocolInfo = ''
        self.MacAddress = ''
        self.OneTimePassword = 'Password'
        self.ClientIPAddress = 'IPAddress'


class RspUserLogin(BaseStruct):

    def __init__(self, TradingDay='', LoginTime='', BrokerID='', UserID='', SystemName='', FrontID=0, SessionID=0, MaxOrderRef='', SHFETime='', DCETime='', CZCETime='', FFEXTime='', INETime=''):
        self.TradingDay = 'Date'
        self.LoginTime = 'Time'
        self.BrokerID = ''
        self.UserID = ''
        self.SystemName = ''
        self.FrontID = ''
        self.SessionID = ''
        self.MaxOrderRef = 'OrderRef'
        self.SHFETime = 'Time'
        self.DCETime = 'Time'
        self.CZCETime = 'Time'
        self.FFEXTime = 'Time'
        self.INETime = 'Time'


class UserLogout(BaseStruct):

    def __init__(self, BrokerID='', UserID=''):
        self.BrokerID = ''
        self.UserID = ''


class ForceUserLogout(BaseStruct):

    def __init__(self, BrokerID='', UserID=''):
        self.BrokerID = ''
        self.UserID = ''


class ReqAuthenticate(BaseStruct):

    def __init__(self, BrokerID='', UserID='', UserProductInfo='', AuthCode=''):
        self.BrokerID = ''
        self.UserID = ''
        self.UserProductInfo = 'ProductInfo'
        self.AuthCode = ''


class RspAuthenticate(BaseStruct):

    def __init__(self, BrokerID='', UserID='', UserProductInfo=''):
        self.BrokerID = ''
        self.UserID = ''
        self.UserProductInfo = 'ProductInfo'


class AuthenticationInfo(BaseStruct):

    def __init__(self, BrokerID='', UserID='', UserProductInfo='', AuthInfo='', IsResult=0):
        self.BrokerID = ''
        self.UserID = ''
        self.UserProductInfo = 'ProductInfo'
        self.AuthInfo = ''
        self.IsResult = 'Bool'


class TransferHeader(BaseStruct):

    def __init__(self, Version='', TradeCode='', TradeDate='', TradeTime='', TradeSerial='', FutureID='', BankID='', BankBrchID='', OperNo='', DeviceID='', RecordNum='', SessionID=0, RequestID=0):
        self.Version = ''
        self.TradeCode = ''
        self.TradeDate = ''
        self.TradeTime = ''
        self.TradeSerial = ''
        self.FutureID = ''
        self.BankID = ''
        self.BankBrchID = ''
        self.OperNo = ''
        self.DeviceID = ''
        self.RecordNum = ''
        self.SessionID = ''
        self.RequestID = ''


class TransferBankToFutureReq(BaseStruct):

    def __init__(self, FutureAccount='', FuturePwdFlag=FPWD_UnCheck, FutureAccPwd='', TradeAmt=0.0, CustFee=0.0, CurrencyCode=''):
        self.FutureAccount = 'AccountID'
        self.FuturePwdFlag = ''
        self.FutureAccPwd = ''
        self.TradeAmt = 'Money'
        self.CustFee = 'Money'
        self.CurrencyCode = ''


class TransferBankToFutureRsp(BaseStruct):

    def __init__(self, RetCode='', RetInfo='', FutureAccount='', TradeAmt=0.0, CustFee=0.0, CurrencyCode=''):
        self.RetCode = ''
        self.RetInfo = ''
        self.FutureAccount = 'AccountID'
        self.TradeAmt = 'Money'
        self.CustFee = 'Money'
        self.CurrencyCode = ''


class TransferFutureToBankReq(BaseStruct):

    def __init__(self, FutureAccount='', FuturePwdFlag=FPWD_UnCheck, FutureAccPwd='', TradeAmt=0.0, CustFee=0.0, CurrencyCode=''):
        self.FutureAccount = 'AccountID'
        self.FuturePwdFlag = ''
        self.FutureAccPwd = ''
        self.TradeAmt = 'Money'
        self.CustFee = 'Money'
        self.CurrencyCode = ''


class TransferFutureToBankRsp(BaseStruct):

    def __init__(self, RetCode='', RetInfo='', FutureAccount='', TradeAmt=0.0, CustFee=0.0, CurrencyCode=''):
        self.RetCode = ''
        self.RetInfo = ''
        self.FutureAccount = 'AccountID'
        self.TradeAmt = 'Money'
        self.CustFee = 'Money'
        self.CurrencyCode = ''


class TransferQryBankReq(BaseStruct):

    def __init__(self, FutureAccount='', FuturePwdFlag=FPWD_UnCheck, FutureAccPwd='', CurrencyCode=''):
        self.FutureAccount = 'AccountID'
        self.FuturePwdFlag = ''
        self.FutureAccPwd = ''
        self.CurrencyCode = ''


class TransferQryBankRsp(BaseStruct):

    def __init__(self, RetCode='', RetInfo='', FutureAccount='', TradeAmt=0.0, UseAmt=0.0, FetchAmt=0.0, CurrencyCode=''):
        self.RetCode = ''
        self.RetInfo = ''
        self.FutureAccount = 'AccountID'
        self.TradeAmt = 'Money'
        self.UseAmt = 'Money'
        self.FetchAmt = 'Money'
        self.CurrencyCode = ''


class TransferQryDetailReq(BaseStruct):

    def __init__(self, FutureAccount=''):
        self.FutureAccount = 'AccountID'


class TransferQryDetailRsp(BaseStruct):

    def __init__(self, TradeDate='', TradeTime='', TradeCode='', FutureSerial=0, FutureID='', FutureAccount='', BankSerial=0, BankID='', BankBrchID='', BankAccount='', CertCode='', CurrencyCode='', TxAmount=0.0, Flag=TVF_Invalid):
        self.TradeDate = 'Date'
        self.TradeTime = ''
        self.TradeCode = ''
        self.FutureSerial = 'TradeSerialNo'
        self.FutureID = ''
        self.FutureAccount = ''
        self.BankSerial = 'TradeSerialNo'
        self.BankID = ''
        self.BankBrchID = ''
        self.BankAccount = ''
        self.CertCode = ''
        self.CurrencyCode = ''
        self.TxAmount = 'Money'
        self.Flag = 'TransferValidFlag'


class RspInfo(BaseStruct):

    def __init__(self, ErrorID=0, ErrorMsg=''):
        self.ErrorID = ''
        self.ErrorMsg = ''


class Exchange(BaseStruct):

    def __init__(self, ExchangeID='', ExchangeName='', ExchangeProperty=EXP_Normal):
        self.ExchangeID = ''
        self.ExchangeName = ''
        self.ExchangeProperty = ''


class Product(BaseStruct):

    def __init__(self, ProductID='', ProductName='', ExchangeID='', ProductClass=PC_Futures, VolumeMultiple=0, PriceTick=0.0, MaxMarketOrderVolume=0, MinMarketOrderVolume=0, MaxLimitOrderVolume=0, MinLimitOrderVolume=0, PositionType=PT_Net, PositionDateType=PDT_UseHistory, CloseDealType=CDT_Normal, TradeCurrencyID='', MortgageFundUseRange=MFUR_None, ExchangeProductID='', UnderlyingMultiple=0.0):
        self.ProductID = 'InstrumentID'
        self.ProductName = ''
        self.ExchangeID = ''
        self.ProductClass = ''
        self.VolumeMultiple = ''
        self.PriceTick = 'Price'
        self.MaxMarketOrderVolume = 'Volume'
        self.MinMarketOrderVolume = 'Volume'
        self.MaxLimitOrderVolume = 'Volume'
        self.MinLimitOrderVolume = 'Volume'
        self.PositionType = ''
        self.PositionDateType = ''
        self.CloseDealType = ''
        self.TradeCurrencyID = 'CurrencyID'
        self.MortgageFundUseRange = ''
        self.ExchangeProductID = 'InstrumentID'
        self.UnderlyingMultiple = ''


class Instrument(BaseStruct):

    def __init__(self, InstrumentID='', ExchangeID='', InstrumentName='', ExchangeInstID='', ProductID='', ProductClass=PC_Futures, DeliveryYear=0, DeliveryMonth=0, MaxMarketOrderVolume=0, MinMarketOrderVolume=0, MaxLimitOrderVolume=0, MinLimitOrderVolume=0, VolumeMultiple=0, PriceTick=0.0, CreateDate='', OpenDate='', ExpireDate='', StartDelivDate='', EndDelivDate='', InstLifePhase=IP_NotStart, IsTrading=0, PositionType=PT_Net, PositionDateType=PDT_UseHistory, LongMarginRatio=0.0, ShortMarginRatio=0.0, MaxMarginSideAlgorithm=MMSA_NO, UnderlyingInstrID='', StrikePrice=0.0, OptionsType=CP_CallOptions, UnderlyingMultiple=0.0, CombinationType=COMBT_Future):
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.InstrumentName = ''
        self.ExchangeInstID = ''
        self.ProductID = 'InstrumentID'
        self.ProductClass = ''
        self.DeliveryYear = 'Year'
        self.DeliveryMonth = 'Month'
        self.MaxMarketOrderVolume = 'Volume'
        self.MinMarketOrderVolume = 'Volume'
        self.MaxLimitOrderVolume = 'Volume'
        self.MinLimitOrderVolume = 'Volume'
        self.VolumeMultiple = ''
        self.PriceTick = 'Price'
        self.CreateDate = 'Date'
        self.OpenDate = 'Date'
        self.ExpireDate = 'Date'
        self.StartDelivDate = 'Date'
        self.EndDelivDate = 'Date'
        self.InstLifePhase = ''
        self.IsTrading = 'Bool'
        self.PositionType = ''
        self.PositionDateType = ''
        self.LongMarginRatio = 'Ratio'
        self.ShortMarginRatio = 'Ratio'
        self.MaxMarginSideAlgorithm = ''
        self.UnderlyingInstrID = 'InstrumentID'
        self.StrikePrice = 'Price'
        self.OptionsType = ''
        self.UnderlyingMultiple = ''
        self.CombinationType = ''


class Broker(BaseStruct):

    def __init__(self, BrokerID='', BrokerAbbr='', BrokerName='', IsActive=0):
        self.BrokerID = ''
        self.BrokerAbbr = ''
        self.BrokerName = ''
        self.IsActive = 'Bool'


class Trader(BaseStruct):

    def __init__(self, ExchangeID='', TraderID='', ParticipantID='', Password='', InstallCount=0, BrokerID=''):
        self.ExchangeID = ''
        self.TraderID = ''
        self.ParticipantID = ''
        self.Password = ''
        self.InstallCount = ''
        self.BrokerID = ''


class Investor(BaseStruct):

    def __init__(self, InvestorID='', BrokerID='', InvestorGroupID='', InvestorName='', IdentifiedCardType=ICT_EID, IdentifiedCardNo='', IsActive=0, Telephone='', Address='', OpenDate='', Mobile='', CommModelID='', MarginModelID=''):
        self.InvestorID = ''
        self.BrokerID = ''
        self.InvestorGroupID = 'InvestorID'
        self.InvestorName = 'PartyName'
        self.IdentifiedCardType = 'IdCardType'
        self.IdentifiedCardNo = ''
        self.IsActive = 'Bool'
        self.Telephone = ''
        self.Address = ''
        self.OpenDate = 'Date'
        self.Mobile = ''
        self.CommModelID = 'InvestorID'
        self.MarginModelID = 'InvestorID'


class TradingCode(BaseStruct):

    def __init__(self, InvestorID='', BrokerID='', ExchangeID='', ClientID='', IsActive=0, ClientIDType=CIDT_Speculation):
        self.InvestorID = ''
        self.BrokerID = ''
        self.ExchangeID = ''
        self.ClientID = ''
        self.IsActive = 'Bool'
        self.ClientIDType = ''


class PartBroker(BaseStruct):

    def __init__(self, BrokerID='', ExchangeID='', ParticipantID='', IsActive=0):
        self.BrokerID = ''
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.IsActive = 'Bool'


class SuperUser(BaseStruct):

    def __init__(self, UserID='', UserName='', Password='', IsActive=0):
        self.UserID = ''
        self.UserName = ''
        self.Password = ''
        self.IsActive = 'Bool'


class SuperUserFunction(BaseStruct):

    def __init__(self, UserID='', FunctionCode=FC_DataAsync):
        self.UserID = ''
        self.FunctionCode = ''


class InvestorGroup(BaseStruct):

    def __init__(self, BrokerID='', InvestorGroupID='', InvestorGroupName=''):
        self.BrokerID = ''
        self.InvestorGroupID = 'InvestorID'
        self.InvestorGroupName = ''


class TradingAccount(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', PreMortgage=0.0, PreCredit=0.0, PreDeposit=0.0, PreBalance=0.0, PreMargin=0.0, InterestBase=0.0, Interest=0.0, Deposit=0.0, Withdraw=0.0, FrozenMargin=0.0, FrozenCash=0.0, FrozenCommission=0.0, CurrMargin=0.0, CashIn=0.0, Commission=0.0, CloseProfit=0.0, PositionProfit=0.0, Balance=0.0, Available=0.0, WithdrawQuota=0.0, Reserve=0.0, TradingDay='', SettlementID=0, Credit=0.0, Mortgage=0.0, ExchangeMargin=0.0, DeliveryMargin=0.0, ExchangeDeliveryMargin=0.0, ReserveBalance=0.0, CurrencyID='', PreFundMortgageIn=0.0, PreFundMortgageOut=0.0, FundMortgageIn=0.0, FundMortgageOut=0.0, FundMortgageAvailable=0.0, MortgageableFund=0.0, SpecProductMargin=0.0, SpecProductFrozenMargin=0.0, SpecProductCommission=0.0, SpecProductFrozenCommission=0.0, SpecProductPositionProfit=0.0, SpecProductCloseProfit=0.0, SpecProductPositionProfitByAlg=0.0, SpecProductExchangeMargin=0.0):
        self.BrokerID = ''
        self.AccountID = ''
        self.PreMortgage = 'Money'
        self.PreCredit = 'Money'
        self.PreDeposit = 'Money'
        self.PreBalance = 'Money'
        self.PreMargin = 'Money'
        self.InterestBase = 'Money'
        self.Interest = 'Money'
        self.Deposit = 'Money'
        self.Withdraw = 'Money'
        self.FrozenMargin = 'Money'
        self.FrozenCash = 'Money'
        self.FrozenCommission = 'Money'
        self.CurrMargin = 'Money'
        self.CashIn = 'Money'
        self.Commission = 'Money'
        self.CloseProfit = 'Money'
        self.PositionProfit = 'Money'
        self.Balance = 'Money'
        self.Available = 'Money'
        self.WithdrawQuota = 'Money'
        self.Reserve = 'Money'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.Credit = 'Money'
        self.Mortgage = 'Money'
        self.ExchangeMargin = 'Money'
        self.DeliveryMargin = 'Money'
        self.ExchangeDeliveryMargin = 'Money'
        self.ReserveBalance = 'Money'
        self.CurrencyID = ''
        self.PreFundMortgageIn = 'Money'
        self.PreFundMortgageOut = 'Money'
        self.FundMortgageIn = 'Money'
        self.FundMortgageOut = 'Money'
        self.FundMortgageAvailable = 'Money'
        self.MortgageableFund = 'Money'
        self.SpecProductMargin = 'Money'
        self.SpecProductFrozenMargin = 'Money'
        self.SpecProductCommission = 'Money'
        self.SpecProductFrozenCommission = 'Money'
        self.SpecProductPositionProfit = 'Money'
        self.SpecProductCloseProfit = 'Money'
        self.SpecProductPositionProfitByAlg = 'Money'
        self.SpecProductExchangeMargin = 'Money'


class InvestorPosition(BaseStruct):

    def __init__(self, InstrumentID='', BrokerID='', InvestorID='', PosiDirection=PD_Net, HedgeFlag=HF_Speculation, PositionDate=PSD_Today, YdPosition=0, Position=0, LongFrozen=0, ShortFrozen=0, LongFrozenAmount=0.0, ShortFrozenAmount=0.0, OpenVolume=0, CloseVolume=0, OpenAmount=0.0, CloseAmount=0.0, PositionCost=0.0, PreMargin=0.0, UseMargin=0.0, FrozenMargin=0.0, FrozenCash=0.0, FrozenCommission=0.0, CashIn=0.0, Commission=0.0, CloseProfit=0.0, PositionProfit=0.0, PreSettlementPrice=0.0, SettlementPrice=0.0, TradingDay='', SettlementID=0, OpenCost=0.0, ExchangeMargin=0.0, CombPosition=0, CombLongFrozen=0, CombShortFrozen=0, CloseProfitByDate=0.0, CloseProfitByTrade=0.0, TodayPosition=0, MarginRateByMoney=0.0, MarginRateByVolume=0.0, StrikeFrozen=0, StrikeFrozenAmount=0.0, AbandonFrozen=0):
        self.InstrumentID = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.PosiDirection = ''
        self.HedgeFlag = ''
        self.PositionDate = ''
        self.YdPosition = 'Volume'
        self.Position = 'Volume'
        self.LongFrozen = 'Volume'
        self.ShortFrozen = 'Volume'
        self.LongFrozenAmount = 'Money'
        self.ShortFrozenAmount = 'Money'
        self.OpenVolume = 'Volume'
        self.CloseVolume = 'Volume'
        self.OpenAmount = 'Money'
        self.CloseAmount = 'Money'
        self.PositionCost = 'Money'
        self.PreMargin = 'Money'
        self.UseMargin = 'Money'
        self.FrozenMargin = 'Money'
        self.FrozenCash = 'Money'
        self.FrozenCommission = 'Money'
        self.CashIn = 'Money'
        self.Commission = 'Money'
        self.CloseProfit = 'Money'
        self.PositionProfit = 'Money'
        self.PreSettlementPrice = 'Price'
        self.SettlementPrice = 'Price'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.OpenCost = 'Money'
        self.ExchangeMargin = 'Money'
        self.CombPosition = 'Volume'
        self.CombLongFrozen = 'Volume'
        self.CombShortFrozen = 'Volume'
        self.CloseProfitByDate = 'Money'
        self.CloseProfitByTrade = 'Money'
        self.TodayPosition = 'Volume'
        self.MarginRateByMoney = 'Ratio'
        self.MarginRateByVolume = 'Ratio'
        self.StrikeFrozen = 'Volume'
        self.StrikeFrozenAmount = 'Money'
        self.AbandonFrozen = 'Volume'


class InstrumentMarginRate(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', HedgeFlag=HF_Speculation, LongMarginRatioByMoney=0.0, LongMarginRatioByVolume=0.0, ShortMarginRatioByMoney=0.0, ShortMarginRatioByVolume=0.0, IsRelative=0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.HedgeFlag = ''
        self.LongMarginRatioByMoney = 'Ratio'
        self.LongMarginRatioByVolume = 'Money'
        self.ShortMarginRatioByMoney = 'Ratio'
        self.ShortMarginRatioByVolume = 'Money'
        self.IsRelative = 'Bool'


class InstrumentCommissionRate(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', OpenRatioByMoney=0.0, OpenRatioByVolume=0.0, CloseRatioByMoney=0.0, CloseRatioByVolume=0.0, CloseTodayRatioByMoney=0.0, CloseTodayRatioByVolume=0.0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.OpenRatioByMoney = 'Ratio'
        self.OpenRatioByVolume = 'Ratio'
        self.CloseRatioByMoney = 'Ratio'
        self.CloseRatioByVolume = 'Ratio'
        self.CloseTodayRatioByMoney = 'Ratio'
        self.CloseTodayRatioByVolume = 'Ratio'


class DepthMarketData(BaseStruct):

    def __init__(self, TradingDay='', InstrumentID='', ExchangeID='', ExchangeInstID='', LastPrice=0.0, PreSettlementPrice=0.0, PreClosePrice=0.0, PreOpenInterest=0.0, OpenPrice=0.0, HighestPrice=0.0, LowestPrice=0.0, Volume=0, Turnover=0.0, OpenInterest=0.0, ClosePrice=0.0, SettlementPrice=0.0, UpperLimitPrice=0.0, LowerLimitPrice=0.0, PreDelta=0.0, CurrDelta=0.0, UpdateTime='', UpdateMillisec=0, BidPrice1=0.0, BidVolume1=0, AskPrice1=0.0, AskVolume1=0, BidPrice2=0.0, BidVolume2=0, AskPrice2=0.0, AskVolume2=0, BidPrice3=0.0, BidVolume3=0, AskPrice3=0.0, AskVolume3=0, BidPrice4=0.0, BidVolume4=0, AskPrice4=0.0, AskVolume4=0, BidPrice5=0.0, BidVolume5=0, AskPrice5=0.0, AskVolume5=0, AveragePrice=0.0, ActionDay=''):
        self.TradingDay = 'Date'
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.ExchangeInstID = ''
        self.LastPrice = 'Price'
        self.PreSettlementPrice = 'Price'
        self.PreClosePrice = 'Price'
        self.PreOpenInterest = 'LargeVolume'
        self.OpenPrice = 'Price'
        self.HighestPrice = 'Price'
        self.LowestPrice = 'Price'
        self.Volume = ''
        self.Turnover = 'Money'
        self.OpenInterest = 'LargeVolume'
        self.ClosePrice = 'Price'
        self.SettlementPrice = 'Price'
        self.UpperLimitPrice = 'Price'
        self.LowerLimitPrice = 'Price'
        self.PreDelta = 'Ratio'
        self.CurrDelta = 'Ratio'
        self.UpdateTime = 'Time'
        self.UpdateMillisec = 'Millisec'
        self.BidPrice1 = 'Price'
        self.BidVolume1 = 'Volume'
        self.AskPrice1 = 'Price'
        self.AskVolume1 = 'Volume'
        self.BidPrice2 = 'Price'
        self.BidVolume2 = 'Volume'
        self.AskPrice2 = 'Price'
        self.AskVolume2 = 'Volume'
        self.BidPrice3 = 'Price'
        self.BidVolume3 = 'Volume'
        self.AskPrice3 = 'Price'
        self.AskVolume3 = 'Volume'
        self.BidPrice4 = 'Price'
        self.BidVolume4 = 'Volume'
        self.AskPrice4 = 'Price'
        self.AskVolume4 = 'Volume'
        self.BidPrice5 = 'Price'
        self.BidVolume5 = 'Volume'
        self.AskPrice5 = 'Price'
        self.AskVolume5 = 'Volume'
        self.AveragePrice = 'Price'
        self.ActionDay = 'Date'


class InstrumentTradingRight(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', TradingRight=TR_Allow):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.TradingRight = ''


class BrokerUser(BaseStruct):

    def __init__(self, BrokerID='', UserID='', UserName='', UserType=UT_Investor, IsActive=0, IsUsingOTP=0):
        self.BrokerID = ''
        self.UserID = ''
        self.UserName = ''
        self.UserType = ''
        self.IsActive = 'Bool'
        self.IsUsingOTP = 'Bool'


class BrokerUserPassword(BaseStruct):

    def __init__(self, BrokerID='', UserID='', Password=''):
        self.BrokerID = ''
        self.UserID = ''
        self.Password = ''


class BrokerUserFunction(BaseStruct):

    def __init__(self, BrokerID='', UserID='', BrokerFunctionCode=BFC_ForceUserLogout):
        self.BrokerID = ''
        self.UserID = ''
        self.BrokerFunctionCode = ''


class TraderOffer(BaseStruct):

    def __init__(self, ExchangeID='', TraderID='', ParticipantID='', Password='', InstallID=0, OrderLocalID='', TraderConnectStatus=TCS_NotConnected, ConnectRequestDate='', ConnectRequestTime='', LastReportDate='', LastReportTime='', ConnectDate='', ConnectTime='', StartDate='', StartTime='', TradingDay='', BrokerID='', MaxTradeID='', MaxOrderMessageReference=''):
        self.ExchangeID = ''
        self.TraderID = ''
        self.ParticipantID = ''
        self.Password = ''
        self.InstallID = ''
        self.OrderLocalID = ''
        self.TraderConnectStatus = ''
        self.ConnectRequestDate = 'Date'
        self.ConnectRequestTime = 'Time'
        self.LastReportDate = 'Date'
        self.LastReportTime = 'Time'
        self.ConnectDate = 'Date'
        self.ConnectTime = 'Time'
        self.StartDate = 'Date'
        self.StartTime = 'Time'
        self.TradingDay = 'Date'
        self.BrokerID = ''
        self.MaxTradeID = 'TradeID'
        self.MaxOrderMessageReference = 'ReturnCode'


class SettlementInfo(BaseStruct):

    def __init__(self, TradingDay='', SettlementID=0, BrokerID='', InvestorID='', SequenceNo=0, Content=''):
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.SequenceNo = ''
        self.Content = ''


class InstrumentMarginRateAdjust(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', HedgeFlag=HF_Speculation, LongMarginRatioByMoney=0.0, LongMarginRatioByVolume=0.0, ShortMarginRatioByMoney=0.0, ShortMarginRatioByVolume=0.0, IsRelative=0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.HedgeFlag = ''
        self.LongMarginRatioByMoney = 'Ratio'
        self.LongMarginRatioByVolume = 'Money'
        self.ShortMarginRatioByMoney = 'Ratio'
        self.ShortMarginRatioByVolume = 'Money'
        self.IsRelative = 'Bool'


class ExchangeMarginRate(BaseStruct):

    def __init__(self, BrokerID='', InstrumentID='', HedgeFlag=HF_Speculation, LongMarginRatioByMoney=0.0, LongMarginRatioByVolume=0.0, ShortMarginRatioByMoney=0.0, ShortMarginRatioByVolume=0.0):
        self.BrokerID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''
        self.LongMarginRatioByMoney = 'Ratio'
        self.LongMarginRatioByVolume = 'Money'
        self.ShortMarginRatioByMoney = 'Ratio'
        self.ShortMarginRatioByVolume = 'Money'


class ExchangeMarginRateAdjust(BaseStruct):

    def __init__(self, BrokerID='', InstrumentID='', HedgeFlag=HF_Speculation, LongMarginRatioByMoney=0.0, LongMarginRatioByVolume=0.0, ShortMarginRatioByMoney=0.0, ShortMarginRatioByVolume=0.0, ExchLongMarginRatioByMoney=0.0, ExchLongMarginRatioByVolume=0.0, ExchShortMarginRatioByMoney=0.0, ExchShortMarginRatioByVolume=0.0, NoLongMarginRatioByMoney=0.0, NoLongMarginRatioByVolume=0.0, NoShortMarginRatioByMoney=0.0, NoShortMarginRatioByVolume=0.0):
        self.BrokerID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''
        self.LongMarginRatioByMoney = 'Ratio'
        self.LongMarginRatioByVolume = 'Money'
        self.ShortMarginRatioByMoney = 'Ratio'
        self.ShortMarginRatioByVolume = 'Money'
        self.ExchLongMarginRatioByMoney = 'Ratio'
        self.ExchLongMarginRatioByVolume = 'Money'
        self.ExchShortMarginRatioByMoney = 'Ratio'
        self.ExchShortMarginRatioByVolume = 'Money'
        self.NoLongMarginRatioByMoney = 'Ratio'
        self.NoLongMarginRatioByVolume = 'Money'
        self.NoShortMarginRatioByMoney = 'Ratio'
        self.NoShortMarginRatioByVolume = 'Money'


class ExchangeRate(BaseStruct):

    def __init__(self, BrokerID='', FromCurrencyID='', FromCurrencyUnit=0.0, ToCurrencyID='', ExchangeRate=0.0):
        self.BrokerID = ''
        self.FromCurrencyID = 'CurrencyID'
        self.FromCurrencyUnit = 'CurrencyUnit'
        self.ToCurrencyID = 'CurrencyID'
        self.ExchangeRate = ''


class SettlementRef(BaseStruct):

    def __init__(self, TradingDay='', SettlementID=0):
        self.TradingDay = 'Date'
        self.SettlementID = ''


class CurrentTime(BaseStruct):

    def __init__(self, CurrDate='', CurrTime='', CurrMillisec=0, ActionDay=''):
        self.CurrDate = 'Date'
        self.CurrTime = 'Time'
        self.CurrMillisec = 'Millisec'
        self.ActionDay = 'Date'


class CommPhase(BaseStruct):

    def __init__(self, TradingDay='', CommPhaseNo=0, SystemID=''):
        self.TradingDay = 'Date'
        self.CommPhaseNo = ''
        self.SystemID = ''


class LoginInfo(BaseStruct):

    def __init__(self, FrontID=0, SessionID=0, BrokerID='', UserID='', LoginDate='', LoginTime='', IPAddress='', UserProductInfo='', InterfaceProductInfo='', ProtocolInfo='', SystemName='', Password='', MaxOrderRef='', SHFETime='', DCETime='', CZCETime='', FFEXTime='', MacAddress='', OneTimePassword='', INETime=''):
        self.FrontID = ''
        self.SessionID = ''
        self.BrokerID = ''
        self.UserID = ''
        self.LoginDate = 'Date'
        self.LoginTime = 'Time'
        self.IPAddress = ''
        self.UserProductInfo = 'ProductInfo'
        self.InterfaceProductInfo = 'ProductInfo'
        self.ProtocolInfo = ''
        self.SystemName = ''
        self.Password = ''
        self.MaxOrderRef = 'OrderRef'
        self.SHFETime = 'Time'
        self.DCETime = 'Time'
        self.CZCETime = 'Time'
        self.FFEXTime = 'Time'
        self.MacAddress = ''
        self.OneTimePassword = 'Password'
        self.INETime = 'Time'


class LogoutAll(BaseStruct):

    def __init__(self, FrontID=0, SessionID=0, SystemName=''):
        self.FrontID = ''
        self.SessionID = ''
        self.SystemName = ''


class FrontStatus(BaseStruct):

    def __init__(self, FrontID=0, LastReportDate='', LastReportTime='', IsActive=0):
        self.FrontID = ''
        self.LastReportDate = 'Date'
        self.LastReportTime = 'Time'
        self.IsActive = 'Bool'


class UserPasswordUpdate(BaseStruct):

    def __init__(self, BrokerID='', UserID='', OldPassword='', NewPassword=''):
        self.BrokerID = ''
        self.UserID = ''
        self.OldPassword = 'Password'
        self.NewPassword = 'Password'


class InputOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', OrderRef='', UserID='', OrderPriceType=OPT_AnyPrice, Direction=D_Buy, CombOffsetFlag='', CombHedgeFlag='', LimitPrice=0.0, VolumeTotalOriginal=0, TimeCondition=TC_IOC, GTDDate='', VolumeCondition=VC_AV, MinVolume=0, ContingentCondition=CC_Immediately, StopPrice=0.0, ForceCloseReason=FCC_NotForceClose, IsAutoSuspend=0, BusinessUnit='', RequestID=0, UserForceClose=0, IsSwapOrder=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.OrderRef = ''
        self.UserID = ''
        self.OrderPriceType = ''
        self.Direction = ''
        self.CombOffsetFlag = ''
        self.CombHedgeFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeTotalOriginal = 'Volume'
        self.TimeCondition = ''
        self.GTDDate = 'Date'
        self.VolumeCondition = ''
        self.MinVolume = 'Volume'
        self.ContingentCondition = ''
        self.StopPrice = 'Price'
        self.ForceCloseReason = ''
        self.IsAutoSuspend = 'Bool'
        self.BusinessUnit = ''
        self.RequestID = ''
        self.UserForceClose = 'Bool'
        self.IsSwapOrder = 'Bool'


class Order(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', OrderRef='', UserID='', OrderPriceType=OPT_AnyPrice, Direction=D_Buy, CombOffsetFlag='', CombHedgeFlag='', LimitPrice=0.0, VolumeTotalOriginal=0, TimeCondition=TC_IOC, GTDDate='', VolumeCondition=VC_AV, MinVolume=0, ContingentCondition=CC_Immediately, StopPrice=0.0, ForceCloseReason=FCC_NotForceClose, IsAutoSuspend=0, BusinessUnit='', RequestID=0, OrderLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, OrderSubmitStatus=OSS_InsertSubmitted, NotifySequence=0, TradingDay='', SettlementID=0, OrderSysID='', OrderSource=OSRC_Participant, OrderStatus=OST_AllTraded, OrderType=ORDT_Normal, VolumeTraded=0, VolumeTotal=0, InsertDate='', InsertTime='', ActiveTime='', SuspendTime='', UpdateTime='', CancelTime='', ActiveTraderID='', ClearingPartID='', SequenceNo=0, FrontID=0, SessionID=0, UserProductInfo='', StatusMsg='', UserForceClose=0, ActiveUserID='', BrokerOrderSeq=0, RelativeOrderSysID='', ZCETotalTradedVolume=0, IsSwapOrder=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.OrderRef = ''
        self.UserID = ''
        self.OrderPriceType = ''
        self.Direction = ''
        self.CombOffsetFlag = ''
        self.CombHedgeFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeTotalOriginal = 'Volume'
        self.TimeCondition = ''
        self.GTDDate = 'Date'
        self.VolumeCondition = ''
        self.MinVolume = 'Volume'
        self.ContingentCondition = ''
        self.StopPrice = 'Price'
        self.ForceCloseReason = ''
        self.IsAutoSuspend = 'Bool'
        self.BusinessUnit = ''
        self.RequestID = ''
        self.OrderLocalID = ''
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.OrderSubmitStatus = ''
        self.NotifySequence = 'SequenceNo'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.OrderSysID = ''
        self.OrderSource = ''
        self.OrderStatus = ''
        self.OrderType = ''
        self.VolumeTraded = 'Volume'
        self.VolumeTotal = 'Volume'
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.ActiveTime = 'Time'
        self.SuspendTime = 'Time'
        self.UpdateTime = 'Time'
        self.CancelTime = 'Time'
        self.ActiveTraderID = 'TraderID'
        self.ClearingPartID = 'ParticipantID'
        self.SequenceNo = ''
        self.FrontID = ''
        self.SessionID = ''
        self.UserProductInfo = 'ProductInfo'
        self.StatusMsg = 'ErrorMsg'
        self.UserForceClose = 'Bool'
        self.ActiveUserID = 'UserID'
        self.BrokerOrderSeq = 'SequenceNo'
        self.RelativeOrderSysID = 'OrderSysID'
        self.ZCETotalTradedVolume = 'Volume'
        self.IsSwapOrder = 'Bool'


class ExchangeOrder(BaseStruct):

    def __init__(self, OrderPriceType=OPT_AnyPrice, Direction=D_Buy, CombOffsetFlag='', CombHedgeFlag='', LimitPrice=0.0, VolumeTotalOriginal=0, TimeCondition=TC_IOC, GTDDate='', VolumeCondition=VC_AV, MinVolume=0, ContingentCondition=CC_Immediately, StopPrice=0.0, ForceCloseReason=FCC_NotForceClose, IsAutoSuspend=0, BusinessUnit='', RequestID=0, OrderLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, OrderSubmitStatus=OSS_InsertSubmitted, NotifySequence=0, TradingDay='', SettlementID=0, OrderSysID='', OrderSource=OSRC_Participant, OrderStatus=OST_AllTraded, OrderType=ORDT_Normal, VolumeTraded=0, VolumeTotal=0, InsertDate='', InsertTime='', ActiveTime='', SuspendTime='', UpdateTime='', CancelTime='', ActiveTraderID='', ClearingPartID='', SequenceNo=0):
        self.OrderPriceType = ''
        self.Direction = ''
        self.CombOffsetFlag = ''
        self.CombHedgeFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeTotalOriginal = 'Volume'
        self.TimeCondition = ''
        self.GTDDate = 'Date'
        self.VolumeCondition = ''
        self.MinVolume = 'Volume'
        self.ContingentCondition = ''
        self.StopPrice = 'Price'
        self.ForceCloseReason = ''
        self.IsAutoSuspend = 'Bool'
        self.BusinessUnit = ''
        self.RequestID = ''
        self.OrderLocalID = ''
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.OrderSubmitStatus = ''
        self.NotifySequence = 'SequenceNo'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.OrderSysID = ''
        self.OrderSource = ''
        self.OrderStatus = ''
        self.OrderType = ''
        self.VolumeTraded = 'Volume'
        self.VolumeTotal = 'Volume'
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.ActiveTime = 'Time'
        self.SuspendTime = 'Time'
        self.UpdateTime = 'Time'
        self.CancelTime = 'Time'
        self.ActiveTraderID = 'TraderID'
        self.ClearingPartID = 'ParticipantID'
        self.SequenceNo = ''


class ExchangeOrderInsertError(BaseStruct):

    def __init__(self, ExchangeID='', ParticipantID='', TraderID='', InstallID=0, OrderLocalID='', ErrorID=0, ErrorMsg=''):
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.OrderLocalID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class InputOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', OrderActionRef=0, OrderRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', OrderSysID='', ActionFlag=AF_Delete, LimitPrice=0.0, VolumeChange=0, UserID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.OrderActionRef = ''
        self.OrderRef = ''
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.ActionFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeChange = 'Volume'
        self.UserID = ''
        self.InstrumentID = ''


class OrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', OrderActionRef=0, OrderRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', OrderSysID='', ActionFlag=AF_Delete, LimitPrice=0.0, VolumeChange=0, ActionDate='', ActionTime='', TraderID='', InstallID=0, OrderLocalID='', ActionLocalID='', ParticipantID='', ClientID='', BusinessUnit='', OrderActionStatus=OAS_Submitted, UserID='', StatusMsg='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.OrderActionRef = ''
        self.OrderRef = ''
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.ActionFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeChange = 'Volume'
        self.ActionDate = 'Date'
        self.ActionTime = 'Time'
        self.TraderID = ''
        self.InstallID = ''
        self.OrderLocalID = ''
        self.ActionLocalID = 'OrderLocalID'
        self.ParticipantID = ''
        self.ClientID = ''
        self.BusinessUnit = ''
        self.OrderActionStatus = ''
        self.UserID = ''
        self.StatusMsg = 'ErrorMsg'
        self.InstrumentID = ''


class ExchangeOrderAction(BaseStruct):

    def __init__(self, ExchangeID='', OrderSysID='', ActionFlag=AF_Delete, LimitPrice=0.0, VolumeChange=0, ActionDate='', ActionTime='', TraderID='', InstallID=0, OrderLocalID='', ActionLocalID='', ParticipantID='', ClientID='', BusinessUnit='', OrderActionStatus=OAS_Submitted, UserID=''):
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.ActionFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeChange = 'Volume'
        self.ActionDate = 'Date'
        self.ActionTime = 'Time'
        self.TraderID = ''
        self.InstallID = ''
        self.OrderLocalID = ''
        self.ActionLocalID = 'OrderLocalID'
        self.ParticipantID = ''
        self.ClientID = ''
        self.BusinessUnit = ''
        self.OrderActionStatus = ''
        self.UserID = ''


class ExchangeOrderActionError(BaseStruct):

    def __init__(self, ExchangeID='', OrderSysID='', TraderID='', InstallID=0, OrderLocalID='', ActionLocalID='', ErrorID=0, ErrorMsg=''):
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.OrderLocalID = ''
        self.ActionLocalID = 'OrderLocalID'
        self.ErrorID = ''
        self.ErrorMsg = ''


class ExchangeTrade(BaseStruct):

    def __init__(self, ExchangeID='', TradeID='', Direction=D_Buy, OrderSysID='', ParticipantID='', ClientID='', TradingRole=ER_Broker, ExchangeInstID='', OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, Price=0.0, Volume=0, TradeDate='', TradeTime='', TradeType=TRDT_SplitCombination, PriceSource=PSRC_LastPrice, TraderID='', OrderLocalID='', ClearingPartID='', BusinessUnit='', SequenceNo=0, TradeSource=TSRC_NORMAL):
        self.ExchangeID = ''
        self.TradeID = ''
        self.Direction = ''
        self.OrderSysID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.TradingRole = ''
        self.ExchangeInstID = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.Price = ''
        self.Volume = ''
        self.TradeDate = 'Date'
        self.TradeTime = 'Time'
        self.TradeType = ''
        self.PriceSource = ''
        self.TraderID = ''
        self.OrderLocalID = ''
        self.ClearingPartID = 'ParticipantID'
        self.BusinessUnit = ''
        self.SequenceNo = ''
        self.TradeSource = ''


class Trade(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', OrderRef='', UserID='', ExchangeID='', TradeID='', Direction=D_Buy, OrderSysID='', ParticipantID='', ClientID='', TradingRole=ER_Broker, ExchangeInstID='', OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, Price=0.0, Volume=0, TradeDate='', TradeTime='', TradeType=TRDT_SplitCombination, PriceSource=PSRC_LastPrice, TraderID='', OrderLocalID='', ClearingPartID='', BusinessUnit='', SequenceNo=0, TradingDay='', SettlementID=0, BrokerOrderSeq=0, TradeSource=TSRC_NORMAL):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.OrderRef = ''
        self.UserID = ''
        self.ExchangeID = ''
        self.TradeID = ''
        self.Direction = ''
        self.OrderSysID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.TradingRole = ''
        self.ExchangeInstID = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.Price = ''
        self.Volume = ''
        self.TradeDate = 'Date'
        self.TradeTime = 'Time'
        self.TradeType = ''
        self.PriceSource = ''
        self.TraderID = ''
        self.OrderLocalID = ''
        self.ClearingPartID = 'ParticipantID'
        self.BusinessUnit = ''
        self.SequenceNo = ''
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.BrokerOrderSeq = 'SequenceNo'
        self.TradeSource = ''


class UserSession(BaseStruct):

    def __init__(self, FrontID=0, SessionID=0, BrokerID='', UserID='', LoginDate='', LoginTime='', IPAddress='', UserProductInfo='', InterfaceProductInfo='', ProtocolInfo='', MacAddress=''):
        self.FrontID = ''
        self.SessionID = ''
        self.BrokerID = ''
        self.UserID = ''
        self.LoginDate = 'Date'
        self.LoginTime = 'Time'
        self.IPAddress = ''
        self.UserProductInfo = 'ProductInfo'
        self.InterfaceProductInfo = 'ProductInfo'
        self.ProtocolInfo = ''
        self.MacAddress = ''


class QueryMaxOrderVolume(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', Direction=D_Buy, OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, MaxVolume=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.Direction = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.MaxVolume = 'Volume'


class SettlementInfoConfirm(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ConfirmDate='', ConfirmTime=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ConfirmDate = 'Date'
        self.ConfirmTime = 'Time'


class SyncDeposit(BaseStruct):

    def __init__(self, DepositSeqNo='', BrokerID='', InvestorID='', Deposit=0.0, IsForce=0, CurrencyID=''):
        self.DepositSeqNo = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.Deposit = 'Money'
        self.IsForce = 'Bool'
        self.CurrencyID = ''


class SyncFundMortgage(BaseStruct):

    def __init__(self, MortgageSeqNo='', BrokerID='', InvestorID='', FromCurrencyID='', MortgageAmount=0.0, ToCurrencyID=''):
        self.MortgageSeqNo = 'DepositSeqNo'
        self.BrokerID = ''
        self.InvestorID = ''
        self.FromCurrencyID = 'CurrencyID'
        self.MortgageAmount = 'Money'
        self.ToCurrencyID = 'CurrencyID'


class BrokerSync(BaseStruct):

    def __init__(self, BrokerID=''):
        self.BrokerID = ''


class SyncingInvestor(BaseStruct):

    def __init__(self, InvestorID='', BrokerID='', InvestorGroupID='', InvestorName='', IdentifiedCardType=ICT_EID, IdentifiedCardNo='', IsActive=0, Telephone='', Address='', OpenDate='', Mobile='', CommModelID='', MarginModelID=''):
        self.InvestorID = ''
        self.BrokerID = ''
        self.InvestorGroupID = 'InvestorID'
        self.InvestorName = 'PartyName'
        self.IdentifiedCardType = 'IdCardType'
        self.IdentifiedCardNo = ''
        self.IsActive = 'Bool'
        self.Telephone = ''
        self.Address = ''
        self.OpenDate = 'Date'
        self.Mobile = ''
        self.CommModelID = 'InvestorID'
        self.MarginModelID = 'InvestorID'


class SyncingTradingCode(BaseStruct):

    def __init__(self, InvestorID='', BrokerID='', ExchangeID='', ClientID='', IsActive=0, ClientIDType=CIDT_Speculation):
        self.InvestorID = ''
        self.BrokerID = ''
        self.ExchangeID = ''
        self.ClientID = ''
        self.IsActive = 'Bool'
        self.ClientIDType = ''


class SyncingInvestorGroup(BaseStruct):

    def __init__(self, BrokerID='', InvestorGroupID='', InvestorGroupName=''):
        self.BrokerID = ''
        self.InvestorGroupID = 'InvestorID'
        self.InvestorGroupName = ''


class SyncingTradingAccount(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', PreMortgage=0.0, PreCredit=0.0, PreDeposit=0.0, PreBalance=0.0, PreMargin=0.0, InterestBase=0.0, Interest=0.0, Deposit=0.0, Withdraw=0.0, FrozenMargin=0.0, FrozenCash=0.0, FrozenCommission=0.0, CurrMargin=0.0, CashIn=0.0, Commission=0.0, CloseProfit=0.0, PositionProfit=0.0, Balance=0.0, Available=0.0, WithdrawQuota=0.0, Reserve=0.0, TradingDay='', SettlementID=0, Credit=0.0, Mortgage=0.0, ExchangeMargin=0.0, DeliveryMargin=0.0, ExchangeDeliveryMargin=0.0, ReserveBalance=0.0, CurrencyID='', PreFundMortgageIn=0.0, PreFundMortgageOut=0.0, FundMortgageIn=0.0, FundMortgageOut=0.0, FundMortgageAvailable=0.0, MortgageableFund=0.0, SpecProductMargin=0.0, SpecProductFrozenMargin=0.0, SpecProductCommission=0.0, SpecProductFrozenCommission=0.0, SpecProductPositionProfit=0.0, SpecProductCloseProfit=0.0, SpecProductPositionProfitByAlg=0.0, SpecProductExchangeMargin=0.0):
        self.BrokerID = ''
        self.AccountID = ''
        self.PreMortgage = 'Money'
        self.PreCredit = 'Money'
        self.PreDeposit = 'Money'
        self.PreBalance = 'Money'
        self.PreMargin = 'Money'
        self.InterestBase = 'Money'
        self.Interest = 'Money'
        self.Deposit = 'Money'
        self.Withdraw = 'Money'
        self.FrozenMargin = 'Money'
        self.FrozenCash = 'Money'
        self.FrozenCommission = 'Money'
        self.CurrMargin = 'Money'
        self.CashIn = 'Money'
        self.Commission = 'Money'
        self.CloseProfit = 'Money'
        self.PositionProfit = 'Money'
        self.Balance = 'Money'
        self.Available = 'Money'
        self.WithdrawQuota = 'Money'
        self.Reserve = 'Money'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.Credit = 'Money'
        self.Mortgage = 'Money'
        self.ExchangeMargin = 'Money'
        self.DeliveryMargin = 'Money'
        self.ExchangeDeliveryMargin = 'Money'
        self.ReserveBalance = 'Money'
        self.CurrencyID = ''
        self.PreFundMortgageIn = 'Money'
        self.PreFundMortgageOut = 'Money'
        self.FundMortgageIn = 'Money'
        self.FundMortgageOut = 'Money'
        self.FundMortgageAvailable = 'Money'
        self.MortgageableFund = 'Money'
        self.SpecProductMargin = 'Money'
        self.SpecProductFrozenMargin = 'Money'
        self.SpecProductCommission = 'Money'
        self.SpecProductFrozenCommission = 'Money'
        self.SpecProductPositionProfit = 'Money'
        self.SpecProductCloseProfit = 'Money'
        self.SpecProductPositionProfitByAlg = 'Money'
        self.SpecProductExchangeMargin = 'Money'


class SyncingInvestorPosition(BaseStruct):

    def __init__(self, InstrumentID='', BrokerID='', InvestorID='', PosiDirection=PD_Net, HedgeFlag=HF_Speculation, PositionDate=PSD_Today, YdPosition=0, Position=0, LongFrozen=0, ShortFrozen=0, LongFrozenAmount=0.0, ShortFrozenAmount=0.0, OpenVolume=0, CloseVolume=0, OpenAmount=0.0, CloseAmount=0.0, PositionCost=0.0, PreMargin=0.0, UseMargin=0.0, FrozenMargin=0.0, FrozenCash=0.0, FrozenCommission=0.0, CashIn=0.0, Commission=0.0, CloseProfit=0.0, PositionProfit=0.0, PreSettlementPrice=0.0, SettlementPrice=0.0, TradingDay='', SettlementID=0, OpenCost=0.0, ExchangeMargin=0.0, CombPosition=0, CombLongFrozen=0, CombShortFrozen=0, CloseProfitByDate=0.0, CloseProfitByTrade=0.0, TodayPosition=0, MarginRateByMoney=0.0, MarginRateByVolume=0.0, StrikeFrozen=0, StrikeFrozenAmount=0.0, AbandonFrozen=0):
        self.InstrumentID = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.PosiDirection = ''
        self.HedgeFlag = ''
        self.PositionDate = ''
        self.YdPosition = 'Volume'
        self.Position = 'Volume'
        self.LongFrozen = 'Volume'
        self.ShortFrozen = 'Volume'
        self.LongFrozenAmount = 'Money'
        self.ShortFrozenAmount = 'Money'
        self.OpenVolume = 'Volume'
        self.CloseVolume = 'Volume'
        self.OpenAmount = 'Money'
        self.CloseAmount = 'Money'
        self.PositionCost = 'Money'
        self.PreMargin = 'Money'
        self.UseMargin = 'Money'
        self.FrozenMargin = 'Money'
        self.FrozenCash = 'Money'
        self.FrozenCommission = 'Money'
        self.CashIn = 'Money'
        self.Commission = 'Money'
        self.CloseProfit = 'Money'
        self.PositionProfit = 'Money'
        self.PreSettlementPrice = 'Price'
        self.SettlementPrice = 'Price'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.OpenCost = 'Money'
        self.ExchangeMargin = 'Money'
        self.CombPosition = 'Volume'
        self.CombLongFrozen = 'Volume'
        self.CombShortFrozen = 'Volume'
        self.CloseProfitByDate = 'Money'
        self.CloseProfitByTrade = 'Money'
        self.TodayPosition = 'Volume'
        self.MarginRateByMoney = 'Ratio'
        self.MarginRateByVolume = 'Ratio'
        self.StrikeFrozen = 'Volume'
        self.StrikeFrozenAmount = 'Money'
        self.AbandonFrozen = 'Volume'


class SyncingInstrumentMarginRate(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', HedgeFlag=HF_Speculation, LongMarginRatioByMoney=0.0, LongMarginRatioByVolume=0.0, ShortMarginRatioByMoney=0.0, ShortMarginRatioByVolume=0.0, IsRelative=0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.HedgeFlag = ''
        self.LongMarginRatioByMoney = 'Ratio'
        self.LongMarginRatioByVolume = 'Money'
        self.ShortMarginRatioByMoney = 'Ratio'
        self.ShortMarginRatioByVolume = 'Money'
        self.IsRelative = 'Bool'


class SyncingInstrumentCommissionRate(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', OpenRatioByMoney=0.0, OpenRatioByVolume=0.0, CloseRatioByMoney=0.0, CloseRatioByVolume=0.0, CloseTodayRatioByMoney=0.0, CloseTodayRatioByVolume=0.0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.OpenRatioByMoney = 'Ratio'
        self.OpenRatioByVolume = 'Ratio'
        self.CloseRatioByMoney = 'Ratio'
        self.CloseRatioByVolume = 'Ratio'
        self.CloseTodayRatioByMoney = 'Ratio'
        self.CloseTodayRatioByVolume = 'Ratio'


class SyncingInstrumentTradingRight(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', TradingRight=TR_Allow):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.TradingRight = ''


class QryOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID='', OrderSysID='', InsertTimeStart='', InsertTimeEnd=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.InsertTimeStart = 'Time'
        self.InsertTimeEnd = 'Time'


class QryTrade(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID='', TradeID='', TradeTimeStart='', TradeTimeEnd=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.TradeID = ''
        self.TradeTimeStart = 'Time'
        self.TradeTimeEnd = 'Time'


class QryInvestorPosition(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''


class QryTradingAccount(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', CurrencyID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.CurrencyID = ''


class QryInvestor(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class QryTradingCode(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExchangeID='', ClientID='', ClientIDType=CIDT_Speculation):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExchangeID = ''
        self.ClientID = ''
        self.ClientIDType = ''


class QryInvestorGroup(BaseStruct):

    def __init__(self, BrokerID=''):
        self.BrokerID = ''


class QryInstrumentMarginRate(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', HedgeFlag=HF_Speculation):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''


class QryInstrumentCommissionRate(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''


class QryInstrumentTradingRight(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''


class QryBroker(BaseStruct):

    def __init__(self, BrokerID=''):
        self.BrokerID = ''


class QryTrader(BaseStruct):

    def __init__(self, ExchangeID='', ParticipantID='', TraderID=''):
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.TraderID = ''


class QrySuperUserFunction(BaseStruct):

    def __init__(self, UserID=''):
        self.UserID = ''


class QryUserSession(BaseStruct):

    def __init__(self, FrontID=0, SessionID=0, BrokerID='', UserID=''):
        self.FrontID = ''
        self.SessionID = ''
        self.BrokerID = ''
        self.UserID = ''


class QryPartBroker(BaseStruct):

    def __init__(self, ExchangeID='', BrokerID='', ParticipantID=''):
        self.ExchangeID = ''
        self.BrokerID = ''
        self.ParticipantID = ''


class QryFrontStatus(BaseStruct):

    def __init__(self, FrontID=0):
        self.FrontID = ''


class QryExchangeOrder(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeInstID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class QryOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExchangeID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExchangeID = ''


class QryExchangeOrderAction(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class QrySuperUser(BaseStruct):

    def __init__(self, UserID=''):
        self.UserID = ''


class QryExchange(BaseStruct):

    def __init__(self, ExchangeID=''):
        self.ExchangeID = ''


class QryProduct(BaseStruct):

    def __init__(self, ProductID='', ProductClass=PC_Futures):
        self.ProductID = 'InstrumentID'
        self.ProductClass = ''


class QryInstrument(BaseStruct):

    def __init__(self, InstrumentID='', ExchangeID='', ExchangeInstID='', ProductID=''):
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.ExchangeInstID = ''
        self.ProductID = 'InstrumentID'


class QryDepthMarketData(BaseStruct):

    def __init__(self, InstrumentID=''):
        self.InstrumentID = ''


class QryBrokerUser(BaseStruct):

    def __init__(self, BrokerID='', UserID=''):
        self.BrokerID = ''
        self.UserID = ''


class QryBrokerUserFunction(BaseStruct):

    def __init__(self, BrokerID='', UserID=''):
        self.BrokerID = ''
        self.UserID = ''


class QryTraderOffer(BaseStruct):

    def __init__(self, ExchangeID='', ParticipantID='', TraderID=''):
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.TraderID = ''


class QrySyncDeposit(BaseStruct):

    def __init__(self, BrokerID='', DepositSeqNo=''):
        self.BrokerID = ''
        self.DepositSeqNo = ''


class QrySettlementInfo(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', TradingDay=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.TradingDay = 'Date'


class QryExchangeMarginRate(BaseStruct):

    def __init__(self, BrokerID='', InstrumentID='', HedgeFlag=HF_Speculation):
        self.BrokerID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''


class QryExchangeMarginRateAdjust(BaseStruct):

    def __init__(self, BrokerID='', InstrumentID='', HedgeFlag=HF_Speculation):
        self.BrokerID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''


class QryExchangeRate(BaseStruct):

    def __init__(self, BrokerID='', FromCurrencyID='', ToCurrencyID=''):
        self.BrokerID = ''
        self.FromCurrencyID = 'CurrencyID'
        self.ToCurrencyID = 'CurrencyID'


class QrySyncFundMortgage(BaseStruct):

    def __init__(self, BrokerID='', MortgageSeqNo=''):
        self.BrokerID = ''
        self.MortgageSeqNo = 'DepositSeqNo'


class QryHisOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID='', OrderSysID='', InsertTimeStart='', InsertTimeEnd='', TradingDay='', SettlementID=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.InsertTimeStart = 'Time'
        self.InsertTimeEnd = 'Time'
        self.TradingDay = 'Date'
        self.SettlementID = ''


class OptionInstrMiniMargin(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', MinMargin=0.0, ValueMethod=VM_Absolute, IsRelative=0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.MinMargin = 'Money'
        self.ValueMethod = ''
        self.IsRelative = 'Bool'


class OptionInstrMarginAdjust(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', SShortMarginRatioByMoney=0.0, SShortMarginRatioByVolume=0.0, HShortMarginRatioByMoney=0.0, HShortMarginRatioByVolume=0.0, AShortMarginRatioByMoney=0.0, AShortMarginRatioByVolume=0.0, IsRelative=0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.SShortMarginRatioByMoney = 'Ratio'
        self.SShortMarginRatioByVolume = 'Money'
        self.HShortMarginRatioByMoney = 'Ratio'
        self.HShortMarginRatioByVolume = 'Money'
        self.AShortMarginRatioByMoney = 'Ratio'
        self.AShortMarginRatioByVolume = 'Money'
        self.IsRelative = 'Bool'


class OptionInstrCommRate(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', OpenRatioByMoney=0.0, OpenRatioByVolume=0.0, CloseRatioByMoney=0.0, CloseRatioByVolume=0.0, CloseTodayRatioByMoney=0.0, CloseTodayRatioByVolume=0.0, StrikeRatioByMoney=0.0, StrikeRatioByVolume=0.0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.OpenRatioByMoney = 'Ratio'
        self.OpenRatioByVolume = 'Ratio'
        self.CloseRatioByMoney = 'Ratio'
        self.CloseRatioByVolume = 'Ratio'
        self.CloseTodayRatioByMoney = 'Ratio'
        self.CloseTodayRatioByVolume = 'Ratio'
        self.StrikeRatioByMoney = 'Ratio'
        self.StrikeRatioByVolume = 'Ratio'


class OptionInstrTradeCost(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', HedgeFlag=HF_Speculation, FixedMargin=0.0, MiniMargin=0.0, Royalty=0.0, ExchFixedMargin=0.0, ExchMiniMargin=0.0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''
        self.FixedMargin = 'Money'
        self.MiniMargin = 'Money'
        self.Royalty = 'Money'
        self.ExchFixedMargin = 'Money'
        self.ExchMiniMargin = 'Money'


class QryOptionInstrTradeCost(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', HedgeFlag=HF_Speculation, InputPrice=0.0, UnderlyingPrice=0.0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''
        self.InputPrice = 'Price'
        self.UnderlyingPrice = 'Price'


class QryOptionInstrCommRate(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''


class IndexPrice(BaseStruct):

    def __init__(self, BrokerID='', InstrumentID='', ClosePrice=0.0):
        self.BrokerID = ''
        self.InstrumentID = ''
        self.ClosePrice = 'Price'


class InputExecOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExecOrderRef='', UserID='', Volume=0, RequestID=0, BusinessUnit='', OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, ActionType=ACTP_Exec, PosiDirection=PD_Net, ReservePositionFlag=EOPF_Reserve, CloseFlag=EOCF_AutoClose):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExecOrderRef = 'OrderRef'
        self.UserID = ''
        self.Volume = ''
        self.RequestID = ''
        self.BusinessUnit = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.ActionType = ''
        self.PosiDirection = ''
        self.ReservePositionFlag = 'ExecOrderPositionFlag'
        self.CloseFlag = 'ExecOrderCloseFlag'


class InputExecOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExecOrderActionRef=0, ExecOrderRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', ExecOrderSysID='', ActionFlag=AF_Delete, UserID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExecOrderActionRef = 'OrderActionRef'
        self.ExecOrderRef = 'OrderRef'
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.ExecOrderSysID = ''
        self.ActionFlag = ''
        self.UserID = ''
        self.InstrumentID = ''


class ExecOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExecOrderRef='', UserID='', Volume=0, RequestID=0, BusinessUnit='', OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, ActionType=ACTP_Exec, PosiDirection=PD_Net, ReservePositionFlag=EOPF_Reserve, CloseFlag=EOCF_AutoClose, ExecOrderLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, OrderSubmitStatus=OSS_InsertSubmitted, NotifySequence=0, TradingDay='', SettlementID=0, ExecOrderSysID='', InsertDate='', InsertTime='', CancelTime='', ExecResult=OER_NoExec, ClearingPartID='', SequenceNo=0, FrontID=0, SessionID=0, UserProductInfo='', StatusMsg='', ActiveUserID='', BrokerExecOrderSeq=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExecOrderRef = 'OrderRef'
        self.UserID = ''
        self.Volume = ''
        self.RequestID = ''
        self.BusinessUnit = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.ActionType = ''
        self.PosiDirection = ''
        self.ReservePositionFlag = 'ExecOrderPositionFlag'
        self.CloseFlag = 'ExecOrderCloseFlag'
        self.ExecOrderLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.OrderSubmitStatus = ''
        self.NotifySequence = 'SequenceNo'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.ExecOrderSysID = ''
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.CancelTime = 'Time'
        self.ExecResult = ''
        self.ClearingPartID = 'ParticipantID'
        self.SequenceNo = ''
        self.FrontID = ''
        self.SessionID = ''
        self.UserProductInfo = 'ProductInfo'
        self.StatusMsg = 'ErrorMsg'
        self.ActiveUserID = 'UserID'
        self.BrokerExecOrderSeq = 'SequenceNo'


class ExecOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExecOrderActionRef=0, ExecOrderRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', ExecOrderSysID='', ActionFlag=AF_Delete, ActionDate='', ActionTime='', TraderID='', InstallID=0, ExecOrderLocalID='', ActionLocalID='', ParticipantID='', ClientID='', BusinessUnit='', OrderActionStatus=OAS_Submitted, UserID='', ActionType=ACTP_Exec, StatusMsg='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExecOrderActionRef = 'OrderActionRef'
        self.ExecOrderRef = 'OrderRef'
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.ExecOrderSysID = ''
        self.ActionFlag = ''
        self.ActionDate = 'Date'
        self.ActionTime = 'Time'
        self.TraderID = ''
        self.InstallID = ''
        self.ExecOrderLocalID = 'OrderLocalID'
        self.ActionLocalID = 'OrderLocalID'
        self.ParticipantID = ''
        self.ClientID = ''
        self.BusinessUnit = ''
        self.OrderActionStatus = ''
        self.UserID = ''
        self.ActionType = ''
        self.StatusMsg = 'ErrorMsg'
        self.InstrumentID = ''


class QryExecOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID='', ExecOrderSysID='', InsertTimeStart='', InsertTimeEnd=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.ExecOrderSysID = ''
        self.InsertTimeStart = 'Time'
        self.InsertTimeEnd = 'Time'


class ExchangeExecOrder(BaseStruct):

    def __init__(self, Volume=0, RequestID=0, BusinessUnit='', OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, ActionType=ACTP_Exec, PosiDirection=PD_Net, ReservePositionFlag=EOPF_Reserve, CloseFlag=EOCF_AutoClose, ExecOrderLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, OrderSubmitStatus=OSS_InsertSubmitted, NotifySequence=0, TradingDay='', SettlementID=0, ExecOrderSysID='', InsertDate='', InsertTime='', CancelTime='', ExecResult=OER_NoExec, ClearingPartID='', SequenceNo=0):
        self.Volume = ''
        self.RequestID = ''
        self.BusinessUnit = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.ActionType = ''
        self.PosiDirection = ''
        self.ReservePositionFlag = 'ExecOrderPositionFlag'
        self.CloseFlag = 'ExecOrderCloseFlag'
        self.ExecOrderLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.OrderSubmitStatus = ''
        self.NotifySequence = 'SequenceNo'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.ExecOrderSysID = ''
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.CancelTime = 'Time'
        self.ExecResult = ''
        self.ClearingPartID = 'ParticipantID'
        self.SequenceNo = ''


class QryExchangeExecOrder(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeInstID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class QryExecOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExchangeID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExchangeID = ''


class ExchangeExecOrderAction(BaseStruct):

    def __init__(self, ExchangeID='', ExecOrderSysID='', ActionFlag=AF_Delete, ActionDate='', ActionTime='', TraderID='', InstallID=0, ExecOrderLocalID='', ActionLocalID='', ParticipantID='', ClientID='', BusinessUnit='', OrderActionStatus=OAS_Submitted, UserID='', ActionType=ACTP_Exec):
        self.ExchangeID = ''
        self.ExecOrderSysID = ''
        self.ActionFlag = ''
        self.ActionDate = 'Date'
        self.ActionTime = 'Time'
        self.TraderID = ''
        self.InstallID = ''
        self.ExecOrderLocalID = 'OrderLocalID'
        self.ActionLocalID = 'OrderLocalID'
        self.ParticipantID = ''
        self.ClientID = ''
        self.BusinessUnit = ''
        self.OrderActionStatus = ''
        self.UserID = ''
        self.ActionType = ''


class QryExchangeExecOrderAction(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class ErrExecOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExecOrderRef='', UserID='', Volume=0, RequestID=0, BusinessUnit='', OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, ActionType=ACTP_Exec, PosiDirection=PD_Net, ReservePositionFlag=EOPF_Reserve, CloseFlag=EOCF_AutoClose, ErrorID=0, ErrorMsg=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExecOrderRef = 'OrderRef'
        self.UserID = ''
        self.Volume = ''
        self.RequestID = ''
        self.BusinessUnit = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.ActionType = ''
        self.PosiDirection = ''
        self.ReservePositionFlag = 'ExecOrderPositionFlag'
        self.CloseFlag = 'ExecOrderCloseFlag'
        self.ErrorID = ''
        self.ErrorMsg = ''


class QryErrExecOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class ErrExecOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExecOrderActionRef=0, ExecOrderRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', ExecOrderSysID='', ActionFlag=AF_Delete, UserID='', InstrumentID='', ErrorID=0, ErrorMsg=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExecOrderActionRef = 'OrderActionRef'
        self.ExecOrderRef = 'OrderRef'
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.ExecOrderSysID = ''
        self.ActionFlag = ''
        self.UserID = ''
        self.InstrumentID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class QryErrExecOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class OptionInstrTradingRight(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', Direction=D_Buy, TradingRight=TR_Allow):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.Direction = ''
        self.TradingRight = ''


class QryOptionInstrTradingRight(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', Direction=D_Buy):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.Direction = ''


class InputForQuote(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ForQuoteRef='', UserID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ForQuoteRef = 'OrderRef'
        self.UserID = ''


class ForQuote(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ForQuoteRef='', UserID='', ForQuoteLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, InsertDate='', InsertTime='', ForQuoteStatus=FQST_Submitted, FrontID=0, SessionID=0, StatusMsg='', ActiveUserID='', BrokerForQutoSeq=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ForQuoteRef = 'OrderRef'
        self.UserID = ''
        self.ForQuoteLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.ForQuoteStatus = ''
        self.FrontID = ''
        self.SessionID = ''
        self.StatusMsg = 'ErrorMsg'
        self.ActiveUserID = 'UserID'
        self.BrokerForQutoSeq = 'SequenceNo'


class QryForQuote(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID='', InsertTimeStart='', InsertTimeEnd=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.InsertTimeStart = 'Time'
        self.InsertTimeEnd = 'Time'


class ExchangeForQuote(BaseStruct):

    def __init__(self, ForQuoteLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, InsertDate='', InsertTime='', ForQuoteStatus=FQST_Submitted):
        self.ForQuoteLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.ForQuoteStatus = ''


class QryExchangeForQuote(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeInstID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class InputQuote(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', QuoteRef='', UserID='', AskPrice=0.0, BidPrice=0.0, AskVolume=0, BidVolume=0, RequestID=0, BusinessUnit='', AskOffsetFlag=OF_Open, BidOffsetFlag=OF_Open, AskHedgeFlag=HF_Speculation, BidHedgeFlag=HF_Speculation, AskOrderRef='', BidOrderRef='', ForQuoteSysID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.QuoteRef = 'OrderRef'
        self.UserID = ''
        self.AskPrice = 'Price'
        self.BidPrice = 'Price'
        self.AskVolume = 'Volume'
        self.BidVolume = 'Volume'
        self.RequestID = ''
        self.BusinessUnit = ''
        self.AskOffsetFlag = 'OffsetFlag'
        self.BidOffsetFlag = 'OffsetFlag'
        self.AskHedgeFlag = 'HedgeFlag'
        self.BidHedgeFlag = 'HedgeFlag'
        self.AskOrderRef = 'OrderRef'
        self.BidOrderRef = 'OrderRef'
        self.ForQuoteSysID = 'OrderSysID'


class InputQuoteAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', QuoteActionRef=0, QuoteRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', QuoteSysID='', ActionFlag=AF_Delete, UserID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.QuoteActionRef = 'OrderActionRef'
        self.QuoteRef = 'OrderRef'
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.QuoteSysID = 'OrderSysID'
        self.ActionFlag = ''
        self.UserID = ''
        self.InstrumentID = ''


class Quote(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', QuoteRef='', UserID='', AskPrice=0.0, BidPrice=0.0, AskVolume=0, BidVolume=0, RequestID=0, BusinessUnit='', AskOffsetFlag=OF_Open, BidOffsetFlag=OF_Open, AskHedgeFlag=HF_Speculation, BidHedgeFlag=HF_Speculation, QuoteLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, NotifySequence=0, OrderSubmitStatus=OSS_InsertSubmitted, TradingDay='', SettlementID=0, QuoteSysID='', InsertDate='', InsertTime='', CancelTime='', QuoteStatus=OST_AllTraded, ClearingPartID='', SequenceNo=0, AskOrderSysID='', BidOrderSysID='', FrontID=0, SessionID=0, UserProductInfo='', StatusMsg='', ActiveUserID='', BrokerQuoteSeq=0, AskOrderRef='', BidOrderRef='', ForQuoteSysID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.QuoteRef = 'OrderRef'
        self.UserID = ''
        self.AskPrice = 'Price'
        self.BidPrice = 'Price'
        self.AskVolume = 'Volume'
        self.BidVolume = 'Volume'
        self.RequestID = ''
        self.BusinessUnit = ''
        self.AskOffsetFlag = 'OffsetFlag'
        self.BidOffsetFlag = 'OffsetFlag'
        self.AskHedgeFlag = 'HedgeFlag'
        self.BidHedgeFlag = 'HedgeFlag'
        self.QuoteLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.NotifySequence = 'SequenceNo'
        self.OrderSubmitStatus = ''
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.QuoteSysID = 'OrderSysID'
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.CancelTime = 'Time'
        self.QuoteStatus = 'OrderStatus'
        self.ClearingPartID = 'ParticipantID'
        self.SequenceNo = ''
        self.AskOrderSysID = 'OrderSysID'
        self.BidOrderSysID = 'OrderSysID'
        self.FrontID = ''
        self.SessionID = ''
        self.UserProductInfo = 'ProductInfo'
        self.StatusMsg = 'ErrorMsg'
        self.ActiveUserID = 'UserID'
        self.BrokerQuoteSeq = 'SequenceNo'
        self.AskOrderRef = 'OrderRef'
        self.BidOrderRef = 'OrderRef'
        self.ForQuoteSysID = 'OrderSysID'


class QuoteAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', QuoteActionRef=0, QuoteRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', QuoteSysID='', ActionFlag=AF_Delete, ActionDate='', ActionTime='', TraderID='', InstallID=0, QuoteLocalID='', ActionLocalID='', ParticipantID='', ClientID='', BusinessUnit='', OrderActionStatus=OAS_Submitted, UserID='', StatusMsg='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.QuoteActionRef = 'OrderActionRef'
        self.QuoteRef = 'OrderRef'
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.QuoteSysID = 'OrderSysID'
        self.ActionFlag = ''
        self.ActionDate = 'Date'
        self.ActionTime = 'Time'
        self.TraderID = ''
        self.InstallID = ''
        self.QuoteLocalID = 'OrderLocalID'
        self.ActionLocalID = 'OrderLocalID'
        self.ParticipantID = ''
        self.ClientID = ''
        self.BusinessUnit = ''
        self.OrderActionStatus = ''
        self.UserID = ''
        self.StatusMsg = 'ErrorMsg'
        self.InstrumentID = ''


class QryQuote(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID='', QuoteSysID='', InsertTimeStart='', InsertTimeEnd=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.QuoteSysID = 'OrderSysID'
        self.InsertTimeStart = 'Time'
        self.InsertTimeEnd = 'Time'


class ExchangeQuote(BaseStruct):

    def __init__(self, AskPrice=0.0, BidPrice=0.0, AskVolume=0, BidVolume=0, RequestID=0, BusinessUnit='', AskOffsetFlag=OF_Open, BidOffsetFlag=OF_Open, AskHedgeFlag=HF_Speculation, BidHedgeFlag=HF_Speculation, QuoteLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, NotifySequence=0, OrderSubmitStatus=OSS_InsertSubmitted, TradingDay='', SettlementID=0, QuoteSysID='', InsertDate='', InsertTime='', CancelTime='', QuoteStatus=OST_AllTraded, ClearingPartID='', SequenceNo=0, AskOrderSysID='', BidOrderSysID='', ForQuoteSysID=''):
        self.AskPrice = 'Price'
        self.BidPrice = 'Price'
        self.AskVolume = 'Volume'
        self.BidVolume = 'Volume'
        self.RequestID = ''
        self.BusinessUnit = ''
        self.AskOffsetFlag = 'OffsetFlag'
        self.BidOffsetFlag = 'OffsetFlag'
        self.AskHedgeFlag = 'HedgeFlag'
        self.BidHedgeFlag = 'HedgeFlag'
        self.QuoteLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.NotifySequence = 'SequenceNo'
        self.OrderSubmitStatus = ''
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.QuoteSysID = 'OrderSysID'
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.CancelTime = 'Time'
        self.QuoteStatus = 'OrderStatus'
        self.ClearingPartID = 'ParticipantID'
        self.SequenceNo = ''
        self.AskOrderSysID = 'OrderSysID'
        self.BidOrderSysID = 'OrderSysID'
        self.ForQuoteSysID = 'OrderSysID'


class QryExchangeQuote(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeInstID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class QryQuoteAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExchangeID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExchangeID = ''


class ExchangeQuoteAction(BaseStruct):

    def __init__(self, ExchangeID='', QuoteSysID='', ActionFlag=AF_Delete, ActionDate='', ActionTime='', TraderID='', InstallID=0, QuoteLocalID='', ActionLocalID='', ParticipantID='', ClientID='', BusinessUnit='', OrderActionStatus=OAS_Submitted, UserID=''):
        self.ExchangeID = ''
        self.QuoteSysID = 'OrderSysID'
        self.ActionFlag = ''
        self.ActionDate = 'Date'
        self.ActionTime = 'Time'
        self.TraderID = ''
        self.InstallID = ''
        self.QuoteLocalID = 'OrderLocalID'
        self.ActionLocalID = 'OrderLocalID'
        self.ParticipantID = ''
        self.ClientID = ''
        self.BusinessUnit = ''
        self.OrderActionStatus = ''
        self.UserID = ''


class QryExchangeQuoteAction(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class OptionInstrDelta(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', Delta=0.0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.Delta = 'Ratio'


class ForQuoteRsp(BaseStruct):

    def __init__(self, TradingDay='', InstrumentID='', ForQuoteSysID='', ForQuoteTime='', ActionDay='', ExchangeID=''):
        self.TradingDay = 'Date'
        self.InstrumentID = ''
        self.ForQuoteSysID = 'OrderSysID'
        self.ForQuoteTime = 'Time'
        self.ActionDay = 'Date'
        self.ExchangeID = ''


class StrikeOffset(BaseStruct):

    def __init__(self, InstrumentID='', InvestorRange=IR_All, BrokerID='', InvestorID='', Offset=0.0):
        self.InstrumentID = ''
        self.InvestorRange = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.Offset = 'Money'


class QryStrikeOffset(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''


class CombInstrumentGuard(BaseStruct):

    def __init__(self, BrokerID='', InstrumentID='', GuarantRatio=0.0):
        self.BrokerID = ''
        self.InstrumentID = ''
        self.GuarantRatio = 'Ratio'


class QryCombInstrumentGuard(BaseStruct):

    def __init__(self, BrokerID='', InstrumentID=''):
        self.BrokerID = ''
        self.InstrumentID = ''


class InputCombAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', CombActionRef='', UserID='', Direction=D_Buy, Volume=0, CombDirection=CMDR_Comb, HedgeFlag=HF_Speculation):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.CombActionRef = 'OrderRef'
        self.UserID = ''
        self.Direction = ''
        self.Volume = ''
        self.CombDirection = ''
        self.HedgeFlag = ''


class CombAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', CombActionRef='', UserID='', Direction=D_Buy, Volume=0, CombDirection=CMDR_Comb, HedgeFlag=HF_Speculation, ActionLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, ActionStatus=OAS_Submitted, NotifySequence=0, TradingDay='', SettlementID=0, SequenceNo=0, FrontID=0, SessionID=0, UserProductInfo='', StatusMsg=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.CombActionRef = 'OrderRef'
        self.UserID = ''
        self.Direction = ''
        self.Volume = ''
        self.CombDirection = ''
        self.HedgeFlag = ''
        self.ActionLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.ActionStatus = 'OrderActionStatus'
        self.NotifySequence = 'SequenceNo'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.SequenceNo = ''
        self.FrontID = ''
        self.SessionID = ''
        self.UserProductInfo = 'ProductInfo'
        self.StatusMsg = 'ErrorMsg'


class QryCombAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''


class ExchangeCombAction(BaseStruct):

    def __init__(self, Direction=D_Buy, Volume=0, CombDirection=CMDR_Comb, HedgeFlag=HF_Speculation, ActionLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, ActionStatus=OAS_Submitted, NotifySequence=0, TradingDay='', SettlementID=0, SequenceNo=0):
        self.Direction = ''
        self.Volume = ''
        self.CombDirection = ''
        self.HedgeFlag = ''
        self.ActionLocalID = 'OrderLocalID'
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.ActionStatus = 'OrderActionStatus'
        self.NotifySequence = 'SequenceNo'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.SequenceNo = ''


class QryExchangeCombAction(BaseStruct):

    def __init__(self, ParticipantID='', ClientID='', ExchangeInstID='', ExchangeID='', TraderID=''):
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.ExchangeID = ''
        self.TraderID = ''


class ProductExchRate(BaseStruct):

    def __init__(self, ProductID='', QuoteCurrencyID='', ExchangeRate=0.0):
        self.ProductID = 'InstrumentID'
        self.QuoteCurrencyID = 'CurrencyID'
        self.ExchangeRate = ''


class QryProductExchRate(BaseStruct):

    def __init__(self, ProductID=''):
        self.ProductID = 'InstrumentID'


class MarketData(BaseStruct):

    def __init__(self, TradingDay='', InstrumentID='', ExchangeID='', ExchangeInstID='', LastPrice=0.0, PreSettlementPrice=0.0, PreClosePrice=0.0, PreOpenInterest=0.0, OpenPrice=0.0, HighestPrice=0.0, LowestPrice=0.0, Volume=0, Turnover=0.0, OpenInterest=0.0, ClosePrice=0.0, SettlementPrice=0.0, UpperLimitPrice=0.0, LowerLimitPrice=0.0, PreDelta=0.0, CurrDelta=0.0, UpdateTime='', UpdateMillisec=0, ActionDay=''):
        self.TradingDay = 'Date'
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.ExchangeInstID = ''
        self.LastPrice = 'Price'
        self.PreSettlementPrice = 'Price'
        self.PreClosePrice = 'Price'
        self.PreOpenInterest = 'LargeVolume'
        self.OpenPrice = 'Price'
        self.HighestPrice = 'Price'
        self.LowestPrice = 'Price'
        self.Volume = ''
        self.Turnover = 'Money'
        self.OpenInterest = 'LargeVolume'
        self.ClosePrice = 'Price'
        self.SettlementPrice = 'Price'
        self.UpperLimitPrice = 'Price'
        self.LowerLimitPrice = 'Price'
        self.PreDelta = 'Ratio'
        self.CurrDelta = 'Ratio'
        self.UpdateTime = 'Time'
        self.UpdateMillisec = 'Millisec'
        self.ActionDay = 'Date'


class MarketDataBase(BaseStruct):

    def __init__(self, TradingDay='', PreSettlementPrice=0.0, PreClosePrice=0.0, PreOpenInterest=0.0, PreDelta=0.0):
        self.TradingDay = 'Date'
        self.PreSettlementPrice = 'Price'
        self.PreClosePrice = 'Price'
        self.PreOpenInterest = 'LargeVolume'
        self.PreDelta = 'Ratio'


class MarketDataStatic(BaseStruct):

    def __init__(self, OpenPrice=0.0, HighestPrice=0.0, LowestPrice=0.0, ClosePrice=0.0, UpperLimitPrice=0.0, LowerLimitPrice=0.0, SettlementPrice=0.0, CurrDelta=0.0):
        self.OpenPrice = 'Price'
        self.HighestPrice = 'Price'
        self.LowestPrice = 'Price'
        self.ClosePrice = 'Price'
        self.UpperLimitPrice = 'Price'
        self.LowerLimitPrice = 'Price'
        self.SettlementPrice = 'Price'
        self.CurrDelta = 'Ratio'


class MarketDataLastMatch(BaseStruct):

    def __init__(self, LastPrice=0.0, Volume=0, Turnover=0.0, OpenInterest=0.0):
        self.LastPrice = 'Price'
        self.Volume = ''
        self.Turnover = 'Money'
        self.OpenInterest = 'LargeVolume'


class MarketDataBestPrice(BaseStruct):

    def __init__(self, BidPrice1=0.0, BidVolume1=0, AskPrice1=0.0, AskVolume1=0):
        self.BidPrice1 = 'Price'
        self.BidVolume1 = 'Volume'
        self.AskPrice1 = 'Price'
        self.AskVolume1 = 'Volume'


class MarketDataBid23(BaseStruct):

    def __init__(self, BidPrice2=0.0, BidVolume2=0, BidPrice3=0.0, BidVolume3=0):
        self.BidPrice2 = 'Price'
        self.BidVolume2 = 'Volume'
        self.BidPrice3 = 'Price'
        self.BidVolume3 = 'Volume'


class MarketDataAsk23(BaseStruct):

    def __init__(self, AskPrice2=0.0, AskVolume2=0, AskPrice3=0.0, AskVolume3=0):
        self.AskPrice2 = 'Price'
        self.AskVolume2 = 'Volume'
        self.AskPrice3 = 'Price'
        self.AskVolume3 = 'Volume'


class MarketDataBid45(BaseStruct):

    def __init__(self, BidPrice4=0.0, BidVolume4=0, BidPrice5=0.0, BidVolume5=0):
        self.BidPrice4 = 'Price'
        self.BidVolume4 = 'Volume'
        self.BidPrice5 = 'Price'
        self.BidVolume5 = 'Volume'


class MarketDataAsk45(BaseStruct):

    def __init__(self, AskPrice4=0.0, AskVolume4=0, AskPrice5=0.0, AskVolume5=0):
        self.AskPrice4 = 'Price'
        self.AskVolume4 = 'Volume'
        self.AskPrice5 = 'Price'
        self.AskVolume5 = 'Volume'


class MarketDataUpdateTime(BaseStruct):

    def __init__(self, InstrumentID='', UpdateTime='', UpdateMillisec=0, ActionDay=''):
        self.InstrumentID = ''
        self.UpdateTime = 'Time'
        self.UpdateMillisec = 'Millisec'
        self.ActionDay = 'Date'


class MarketDataExchange(BaseStruct):

    def __init__(self, ExchangeID=''):
        self.ExchangeID = ''


class SpecificInstrument(BaseStruct):

    def __init__(self, InstrumentID=''):
        self.InstrumentID = ''


class InstrumentStatus(BaseStruct):

    def __init__(self, ExchangeID='', ExchangeInstID='', SettlementGroupID='', InstrumentID='', InstrumentStatus=IS_BeforeTrading, TradingSegmentSN=0, EnterTime='', EnterReason=IER_Automatic):
        self.ExchangeID = ''
        self.ExchangeInstID = ''
        self.SettlementGroupID = ''
        self.InstrumentID = ''
        self.InstrumentStatus = ''
        self.TradingSegmentSN = ''
        self.EnterTime = 'Time'
        self.EnterReason = 'InstStatusEnterReason'


class QryInstrumentStatus(BaseStruct):

    def __init__(self, ExchangeID='', ExchangeInstID=''):
        self.ExchangeID = ''
        self.ExchangeInstID = ''


class InvestorAccount(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', AccountID='', CurrencyID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.AccountID = ''
        self.CurrencyID = ''


class PositionProfitAlgorithm(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', Algorithm=AG_All, Memo='', CurrencyID=''):
        self.BrokerID = ''
        self.AccountID = ''
        self.Algorithm = ''
        self.Memo = ''
        self.CurrencyID = ''


class Discount(BaseStruct):

    def __init__(self, BrokerID='', InvestorRange=IR_All, InvestorID='', Discount=0.0):
        self.BrokerID = ''
        self.InvestorRange = ''
        self.InvestorID = ''
        self.Discount = 'Ratio'


class QryTransferBank(BaseStruct):

    def __init__(self, BankID='', BankBrchID=''):
        self.BankID = ''
        self.BankBrchID = ''


class TransferBank(BaseStruct):

    def __init__(self, BankID='', BankBrchID='', BankName='', IsActive=0):
        self.BankID = ''
        self.BankBrchID = ''
        self.BankName = ''
        self.IsActive = 'Bool'


class QryInvestorPositionDetail(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''


class InvestorPositionDetail(BaseStruct):

    def __init__(self, InstrumentID='', BrokerID='', InvestorID='', HedgeFlag=HF_Speculation, Direction=D_Buy, OpenDate='', TradeID='', Volume=0, OpenPrice=0.0, TradingDay='', SettlementID=0, TradeType=TRDT_SplitCombination, CombInstrumentID='', ExchangeID='', CloseProfitByDate=0.0, CloseProfitByTrade=0.0, PositionProfitByDate=0.0, PositionProfitByTrade=0.0, Margin=0.0, ExchMargin=0.0, MarginRateByMoney=0.0, MarginRateByVolume=0.0, LastSettlementPrice=0.0, SettlementPrice=0.0, CloseVolume=0, CloseAmount=0.0):
        self.InstrumentID = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.HedgeFlag = ''
        self.Direction = ''
        self.OpenDate = 'Date'
        self.TradeID = ''
        self.Volume = ''
        self.OpenPrice = 'Price'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.TradeType = ''
        self.CombInstrumentID = 'InstrumentID'
        self.ExchangeID = ''
        self.CloseProfitByDate = 'Money'
        self.CloseProfitByTrade = 'Money'
        self.PositionProfitByDate = 'Money'
        self.PositionProfitByTrade = 'Money'
        self.Margin = 'Money'
        self.ExchMargin = 'Money'
        self.MarginRateByMoney = 'Ratio'
        self.MarginRateByVolume = 'Ratio'
        self.LastSettlementPrice = 'Price'
        self.SettlementPrice = 'Price'
        self.CloseVolume = 'Volume'
        self.CloseAmount = 'Money'


class TradingAccountPassword(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', Password='', CurrencyID=''):
        self.BrokerID = ''
        self.AccountID = ''
        self.Password = ''
        self.CurrencyID = ''


class MDTraderOffer(BaseStruct):

    def __init__(self, ExchangeID='', TraderID='', ParticipantID='', Password='', InstallID=0, OrderLocalID='', TraderConnectStatus=TCS_NotConnected, ConnectRequestDate='', ConnectRequestTime='', LastReportDate='', LastReportTime='', ConnectDate='', ConnectTime='', StartDate='', StartTime='', TradingDay='', BrokerID='', MaxTradeID='', MaxOrderMessageReference=''):
        self.ExchangeID = ''
        self.TraderID = ''
        self.ParticipantID = ''
        self.Password = ''
        self.InstallID = ''
        self.OrderLocalID = ''
        self.TraderConnectStatus = ''
        self.ConnectRequestDate = 'Date'
        self.ConnectRequestTime = 'Time'
        self.LastReportDate = 'Date'
        self.LastReportTime = 'Time'
        self.ConnectDate = 'Date'
        self.ConnectTime = 'Time'
        self.StartDate = 'Date'
        self.StartTime = 'Time'
        self.TradingDay = 'Date'
        self.BrokerID = ''
        self.MaxTradeID = 'TradeID'
        self.MaxOrderMessageReference = 'ReturnCode'


class QryMDTraderOffer(BaseStruct):

    def __init__(self, ExchangeID='', ParticipantID='', TraderID=''):
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.TraderID = ''


class QryNotice(BaseStruct):

    def __init__(self, BrokerID=''):
        self.BrokerID = ''


class Notice(BaseStruct):

    def __init__(self, BrokerID='', Content='', SequenceLabel=''):
        self.BrokerID = ''
        self.Content = ''
        self.SequenceLabel = ''


class UserRight(BaseStruct):

    def __init__(self, BrokerID='', UserID='', UserRightType=URT_Logon, IsForbidden=0):
        self.BrokerID = ''
        self.UserID = ''
        self.UserRightType = ''
        self.IsForbidden = 'Bool'


class QrySettlementInfoConfirm(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class LoadSettlementInfo(BaseStruct):

    def __init__(self, BrokerID=''):
        self.BrokerID = ''


class BrokerWithdrawAlgorithm(BaseStruct):

    def __init__(self, BrokerID='', WithdrawAlgorithm=AG_All, UsingRatio=0.0, IncludeCloseProfit=ICP_Include, AllWithoutTrade=AWT_Enable, AvailIncludeCloseProfit=ICP_Include, IsBrokerUserEvent=0, CurrencyID='', FundMortgageRatio=0.0, BalanceAlgorithm=BLAG_Default):
        self.BrokerID = ''
        self.WithdrawAlgorithm = 'Algorithm'
        self.UsingRatio = 'Ratio'
        self.IncludeCloseProfit = ''
        self.AllWithoutTrade = ''
        self.AvailIncludeCloseProfit = 'IncludeCloseProfit'
        self.IsBrokerUserEvent = 'Bool'
        self.CurrencyID = ''
        self.FundMortgageRatio = 'Ratio'
        self.BalanceAlgorithm = ''


class TradingAccountPasswordUpdateV1(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', OldPassword='', NewPassword=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.OldPassword = 'Password'
        self.NewPassword = 'Password'


class TradingAccountPasswordUpdate(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', OldPassword='', NewPassword='', CurrencyID=''):
        self.BrokerID = ''
        self.AccountID = ''
        self.OldPassword = 'Password'
        self.NewPassword = 'Password'
        self.CurrencyID = ''


class QryCombinationLeg(BaseStruct):

    def __init__(self, CombInstrumentID='', LegID=0, LegInstrumentID=''):
        self.CombInstrumentID = 'InstrumentID'
        self.LegID = ''
        self.LegInstrumentID = 'InstrumentID'


class QrySyncStatus(BaseStruct):

    def __init__(self, TradingDay=''):
        self.TradingDay = 'Date'


class CombinationLeg(BaseStruct):

    def __init__(self, CombInstrumentID='', LegID=0, LegInstrumentID='', Direction=D_Buy, LegMultiple=0, ImplyLevel=0):
        self.CombInstrumentID = 'InstrumentID'
        self.LegID = ''
        self.LegInstrumentID = 'InstrumentID'
        self.Direction = ''
        self.LegMultiple = ''
        self.ImplyLevel = ''


class SyncStatus(BaseStruct):

    def __init__(self, TradingDay='', DataSyncStatus=DS_Asynchronous):
        self.TradingDay = 'Date'
        self.DataSyncStatus = ''


class QryLinkMan(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class LinkMan(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', PersonType=PST_Order, IdentifiedCardType=ICT_EID, IdentifiedCardNo='', PersonName='', Telephone='', Address='', ZipCode='', Priority=0, UOAZipCode='', PersonFullName=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.PersonType = ''
        self.IdentifiedCardType = 'IdCardType'
        self.IdentifiedCardNo = ''
        self.PersonName = 'PartyName'
        self.Telephone = ''
        self.Address = ''
        self.ZipCode = ''
        self.Priority = ''
        self.UOAZipCode = ''
        self.PersonFullName = 'InvestorFullName'


class QryBrokerUserEvent(BaseStruct):

    def __init__(self, BrokerID='', UserID='', UserEventType=UET_Login):
        self.BrokerID = ''
        self.UserID = ''
        self.UserEventType = ''


class BrokerUserEvent(BaseStruct):

    def __init__(self, BrokerID='', UserID='', UserEventType=UET_Login, EventSequenceNo=0, EventDate='', EventTime='', UserEventInfo='', InvestorID='', InstrumentID=''):
        self.BrokerID = ''
        self.UserID = ''
        self.UserEventType = ''
        self.EventSequenceNo = 'SequenceNo'
        self.EventDate = 'Date'
        self.EventTime = 'Time'
        self.UserEventInfo = ''
        self.InvestorID = ''
        self.InstrumentID = ''


class QryContractBank(BaseStruct):

    def __init__(self, BrokerID='', BankID='', BankBrchID=''):
        self.BrokerID = ''
        self.BankID = ''
        self.BankBrchID = ''


class ContractBank(BaseStruct):

    def __init__(self, BrokerID='', BankID='', BankBrchID='', BankName=''):
        self.BrokerID = ''
        self.BankID = ''
        self.BankBrchID = ''
        self.BankName = ''


class InvestorPositionCombineDetail(BaseStruct):

    def __init__(self, TradingDay='', OpenDate='', ExchangeID='', SettlementID=0, BrokerID='', InvestorID='', ComTradeID='', TradeID='', InstrumentID='', HedgeFlag=HF_Speculation, Direction=D_Buy, TotalAmt=0, Margin=0.0, ExchMargin=0.0, MarginRateByMoney=0.0, MarginRateByVolume=0.0, LegID=0, LegMultiple=0, CombInstrumentID='', TradeGroupID=0):
        self.TradingDay = 'Date'
        self.OpenDate = 'Date'
        self.ExchangeID = ''
        self.SettlementID = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.ComTradeID = 'TradeID'
        self.TradeID = ''
        self.InstrumentID = ''
        self.HedgeFlag = ''
        self.Direction = ''
        self.TotalAmt = 'Volume'
        self.Margin = 'Money'
        self.ExchMargin = 'Money'
        self.MarginRateByMoney = 'Ratio'
        self.MarginRateByVolume = 'Ratio'
        self.LegID = ''
        self.LegMultiple = ''
        self.CombInstrumentID = 'InstrumentID'
        self.TradeGroupID = ''


class ParkedOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', OrderRef='', UserID='', OrderPriceType=OPT_AnyPrice, Direction=D_Buy, CombOffsetFlag='', CombHedgeFlag='', LimitPrice=0.0, VolumeTotalOriginal=0, TimeCondition=TC_IOC, GTDDate='', VolumeCondition=VC_AV, MinVolume=0, ContingentCondition=CC_Immediately, StopPrice=0.0, ForceCloseReason=FCC_NotForceClose, IsAutoSuspend=0, BusinessUnit='', RequestID=0, UserForceClose=0, ExchangeID='', ParkedOrderID='', UserType=UT_Investor, Status=PAOS_NotSend, ErrorID=0, ErrorMsg='', IsSwapOrder=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.OrderRef = ''
        self.UserID = ''
        self.OrderPriceType = ''
        self.Direction = ''
        self.CombOffsetFlag = ''
        self.CombHedgeFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeTotalOriginal = 'Volume'
        self.TimeCondition = ''
        self.GTDDate = 'Date'
        self.VolumeCondition = ''
        self.MinVolume = 'Volume'
        self.ContingentCondition = ''
        self.StopPrice = 'Price'
        self.ForceCloseReason = ''
        self.IsAutoSuspend = 'Bool'
        self.BusinessUnit = ''
        self.RequestID = ''
        self.UserForceClose = 'Bool'
        self.ExchangeID = ''
        self.ParkedOrderID = ''
        self.UserType = ''
        self.Status = 'ParkedOrderStatus'
        self.ErrorID = ''
        self.ErrorMsg = ''
        self.IsSwapOrder = 'Bool'


class ParkedOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', OrderActionRef=0, OrderRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', OrderSysID='', ActionFlag=AF_Delete, LimitPrice=0.0, VolumeChange=0, UserID='', InstrumentID='', ParkedOrderActionID='', UserType=UT_Investor, Status=PAOS_NotSend, ErrorID=0, ErrorMsg=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.OrderActionRef = ''
        self.OrderRef = ''
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.ActionFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeChange = 'Volume'
        self.UserID = ''
        self.InstrumentID = ''
        self.ParkedOrderActionID = ''
        self.UserType = ''
        self.Status = 'ParkedOrderStatus'
        self.ErrorID = ''
        self.ErrorMsg = ''


class QryParkedOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''


class QryParkedOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', ExchangeID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''


class RemoveParkedOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ParkedOrderID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ParkedOrderID = ''


class RemoveParkedOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ParkedOrderActionID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ParkedOrderActionID = ''


class InvestorWithdrawAlgorithm(BaseStruct):

    def __init__(self, BrokerID='', InvestorRange=IR_All, InvestorID='', UsingRatio=0.0, CurrencyID='', FundMortgageRatio=0.0):
        self.BrokerID = ''
        self.InvestorRange = ''
        self.InvestorID = ''
        self.UsingRatio = 'Ratio'
        self.CurrencyID = ''
        self.FundMortgageRatio = 'Ratio'


class QryInvestorPositionCombineDetail(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', CombInstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.CombInstrumentID = 'InstrumentID'


class MarketDataAveragePrice(BaseStruct):

    def __init__(self, AveragePrice=0.0):
        self.AveragePrice = 'Price'


class VerifyInvestorPassword(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', Password=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.Password = ''


class UserIP(BaseStruct):

    def __init__(self, BrokerID='', UserID='', IPAddress='', IPMask='', MacAddress=''):
        self.BrokerID = ''
        self.UserID = ''
        self.IPAddress = ''
        self.IPMask = 'IPAddress'
        self.MacAddress = ''


class TradingNoticeInfo(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', SendTime='', FieldContent='', SequenceSeries=0, SequenceNo=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.SendTime = 'Time'
        self.FieldContent = 'Content'
        self.SequenceSeries = ''
        self.SequenceNo = ''


class TradingNotice(BaseStruct):

    def __init__(self, BrokerID='', InvestorRange=IR_All, InvestorID='', SequenceSeries=0, UserID='', SendTime='', SequenceNo=0, FieldContent=''):
        self.BrokerID = ''
        self.InvestorRange = ''
        self.InvestorID = ''
        self.SequenceSeries = ''
        self.UserID = ''
        self.SendTime = 'Time'
        self.SequenceNo = ''
        self.FieldContent = 'Content'


class QryTradingNotice(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class QryErrOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class ErrOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', OrderRef='', UserID='', OrderPriceType=OPT_AnyPrice, Direction=D_Buy, CombOffsetFlag='', CombHedgeFlag='', LimitPrice=0.0, VolumeTotalOriginal=0, TimeCondition=TC_IOC, GTDDate='', VolumeCondition=VC_AV, MinVolume=0, ContingentCondition=CC_Immediately, StopPrice=0.0, ForceCloseReason=FCC_NotForceClose, IsAutoSuspend=0, BusinessUnit='', RequestID=0, UserForceClose=0, ErrorID=0, ErrorMsg='', IsSwapOrder=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.OrderRef = ''
        self.UserID = ''
        self.OrderPriceType = ''
        self.Direction = ''
        self.CombOffsetFlag = ''
        self.CombHedgeFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeTotalOriginal = 'Volume'
        self.TimeCondition = ''
        self.GTDDate = 'Date'
        self.VolumeCondition = ''
        self.MinVolume = 'Volume'
        self.ContingentCondition = ''
        self.StopPrice = 'Price'
        self.ForceCloseReason = ''
        self.IsAutoSuspend = 'Bool'
        self.BusinessUnit = ''
        self.RequestID = ''
        self.UserForceClose = 'Bool'
        self.ErrorID = ''
        self.ErrorMsg = ''
        self.IsSwapOrder = 'Bool'


class ErrorConditionalOrder(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', OrderRef='', UserID='', OrderPriceType=OPT_AnyPrice, Direction=D_Buy, CombOffsetFlag='', CombHedgeFlag='', LimitPrice=0.0, VolumeTotalOriginal=0, TimeCondition=TC_IOC, GTDDate='', VolumeCondition=VC_AV, MinVolume=0, ContingentCondition=CC_Immediately, StopPrice=0.0, ForceCloseReason=FCC_NotForceClose, IsAutoSuspend=0, BusinessUnit='', RequestID=0, OrderLocalID='', ExchangeID='', ParticipantID='', ClientID='', ExchangeInstID='', TraderID='', InstallID=0, OrderSubmitStatus=OSS_InsertSubmitted, NotifySequence=0, TradingDay='', SettlementID=0, OrderSysID='', OrderSource=OSRC_Participant, OrderStatus=OST_AllTraded, OrderType=ORDT_Normal, VolumeTraded=0, VolumeTotal=0, InsertDate='', InsertTime='', ActiveTime='', SuspendTime='', UpdateTime='', CancelTime='', ActiveTraderID='', ClearingPartID='', SequenceNo=0, FrontID=0, SessionID=0, UserProductInfo='', StatusMsg='', UserForceClose=0, ActiveUserID='', BrokerOrderSeq=0, RelativeOrderSysID='', ZCETotalTradedVolume=0, ErrorID=0, ErrorMsg='', IsSwapOrder=0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.OrderRef = ''
        self.UserID = ''
        self.OrderPriceType = ''
        self.Direction = ''
        self.CombOffsetFlag = ''
        self.CombHedgeFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeTotalOriginal = 'Volume'
        self.TimeCondition = ''
        self.GTDDate = 'Date'
        self.VolumeCondition = ''
        self.MinVolume = 'Volume'
        self.ContingentCondition = ''
        self.StopPrice = 'Price'
        self.ForceCloseReason = ''
        self.IsAutoSuspend = 'Bool'
        self.BusinessUnit = ''
        self.RequestID = ''
        self.OrderLocalID = ''
        self.ExchangeID = ''
        self.ParticipantID = ''
        self.ClientID = ''
        self.ExchangeInstID = ''
        self.TraderID = ''
        self.InstallID = ''
        self.OrderSubmitStatus = ''
        self.NotifySequence = 'SequenceNo'
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.OrderSysID = ''
        self.OrderSource = ''
        self.OrderStatus = ''
        self.OrderType = ''
        self.VolumeTraded = 'Volume'
        self.VolumeTotal = 'Volume'
        self.InsertDate = 'Date'
        self.InsertTime = 'Time'
        self.ActiveTime = 'Time'
        self.SuspendTime = 'Time'
        self.UpdateTime = 'Time'
        self.CancelTime = 'Time'
        self.ActiveTraderID = 'TraderID'
        self.ClearingPartID = 'ParticipantID'
        self.SequenceNo = ''
        self.FrontID = ''
        self.SessionID = ''
        self.UserProductInfo = 'ProductInfo'
        self.StatusMsg = 'ErrorMsg'
        self.UserForceClose = 'Bool'
        self.ActiveUserID = 'UserID'
        self.BrokerOrderSeq = 'SequenceNo'
        self.RelativeOrderSysID = 'OrderSysID'
        self.ZCETotalTradedVolume = 'Volume'
        self.ErrorID = ''
        self.ErrorMsg = ''
        self.IsSwapOrder = 'Bool'


class QryErrOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class ErrOrderAction(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', OrderActionRef=0, OrderRef='', RequestID=0, FrontID=0, SessionID=0, ExchangeID='', OrderSysID='', ActionFlag=AF_Delete, LimitPrice=0.0, VolumeChange=0, ActionDate='', ActionTime='', TraderID='', InstallID=0, OrderLocalID='', ActionLocalID='', ParticipantID='', ClientID='', BusinessUnit='', OrderActionStatus=OAS_Submitted, UserID='', StatusMsg='', InstrumentID='', ErrorID=0, ErrorMsg=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.OrderActionRef = ''
        self.OrderRef = ''
        self.RequestID = ''
        self.FrontID = ''
        self.SessionID = ''
        self.ExchangeID = ''
        self.OrderSysID = ''
        self.ActionFlag = ''
        self.LimitPrice = 'Price'
        self.VolumeChange = 'Volume'
        self.ActionDate = 'Date'
        self.ActionTime = 'Time'
        self.TraderID = ''
        self.InstallID = ''
        self.OrderLocalID = ''
        self.ActionLocalID = 'OrderLocalID'
        self.ParticipantID = ''
        self.ClientID = ''
        self.BusinessUnit = ''
        self.OrderActionStatus = ''
        self.UserID = ''
        self.StatusMsg = 'ErrorMsg'
        self.InstrumentID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class QryExchangeSequence(BaseStruct):

    def __init__(self, ExchangeID=''):
        self.ExchangeID = ''


class ExchangeSequence(BaseStruct):

    def __init__(self, ExchangeID='', SequenceNo=0, MarketStatus=IS_BeforeTrading):
        self.ExchangeID = ''
        self.SequenceNo = ''
        self.MarketStatus = 'InstrumentStatus'


class QueryMaxOrderVolumeWithPrice(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', InstrumentID='', Direction=D_Buy, OffsetFlag=OF_Open, HedgeFlag=HF_Speculation, MaxVolume=0, Price=0.0):
        self.BrokerID = ''
        self.InvestorID = ''
        self.InstrumentID = ''
        self.Direction = ''
        self.OffsetFlag = ''
        self.HedgeFlag = ''
        self.MaxVolume = 'Volume'
        self.Price = ''


class QryBrokerTradingParams(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', CurrencyID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.CurrencyID = ''


class BrokerTradingParams(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', MarginPriceType=MPT_PreSettlementPrice, Algorithm=AG_All, AvailIncludeCloseProfit=ICP_Include, CurrencyID='', OptionRoyaltyPriceType=ORPT_PreSettlementPrice):
        self.BrokerID = ''
        self.InvestorID = ''
        self.MarginPriceType = ''
        self.Algorithm = ''
        self.AvailIncludeCloseProfit = 'IncludeCloseProfit'
        self.CurrencyID = ''
        self.OptionRoyaltyPriceType = ''


class QryBrokerTradingAlgos(BaseStruct):

    def __init__(self, BrokerID='', ExchangeID='', InstrumentID=''):
        self.BrokerID = ''
        self.ExchangeID = ''
        self.InstrumentID = ''


class BrokerTradingAlgos(BaseStruct):

    def __init__(self, BrokerID='', ExchangeID='', InstrumentID='', HandlePositionAlgoID=HPA_Base, FindMarginRateAlgoID=FMRA_Base, HandleTradingAccountAlgoID=HTAA_Base):
        self.BrokerID = ''
        self.ExchangeID = ''
        self.InstrumentID = ''
        self.HandlePositionAlgoID = ''
        self.FindMarginRateAlgoID = ''
        self.HandleTradingAccountAlgoID = ''


class QueryBrokerDeposit(BaseStruct):

    def __init__(self, BrokerID='', ExchangeID=''):
        self.BrokerID = ''
        self.ExchangeID = ''


class BrokerDeposit(BaseStruct):

    def __init__(self, TradingDay='', BrokerID='', ParticipantID='', ExchangeID='', PreBalance=0.0, CurrMargin=0.0, CloseProfit=0.0, Balance=0.0, Deposit=0.0, Withdraw=0.0, Available=0.0, Reserve=0.0, FrozenMargin=0.0):
        self.TradingDay = 'TradeDate'
        self.BrokerID = ''
        self.ParticipantID = ''
        self.ExchangeID = ''
        self.PreBalance = 'Money'
        self.CurrMargin = 'Money'
        self.CloseProfit = 'Money'
        self.Balance = 'Money'
        self.Deposit = 'Money'
        self.Withdraw = 'Money'
        self.Available = 'Money'
        self.Reserve = 'Money'
        self.FrozenMargin = 'Money'


class QryCFMMCBrokerKey(BaseStruct):

    def __init__(self, BrokerID=''):
        self.BrokerID = ''


class CFMMCBrokerKey(BaseStruct):

    def __init__(self, BrokerID='', ParticipantID='', CreateDate='', CreateTime='', KeyID=0, CurrentKey='', KeyKind=CFMMCKK_REQUEST):
        self.BrokerID = ''
        self.ParticipantID = ''
        self.CreateDate = 'Date'
        self.CreateTime = 'Time'
        self.KeyID = 'SequenceNo'
        self.CurrentKey = 'CFMMCKey'
        self.KeyKind = 'CFMMCKeyKind'


class CFMMCTradingAccountKey(BaseStruct):

    def __init__(self, BrokerID='', ParticipantID='', AccountID='', KeyID=0, CurrentKey=''):
        self.BrokerID = ''
        self.ParticipantID = ''
        self.AccountID = ''
        self.KeyID = 'SequenceNo'
        self.CurrentKey = 'CFMMCKey'


class QryCFMMCTradingAccountKey(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class BrokerUserOTPParam(BaseStruct):

    def __init__(self, BrokerID='', UserID='', OTPVendorsID='', SerialNumber='', AuthKey='', LastDrift=0, LastSuccess=0, OTPType=OTP_NONE):
        self.BrokerID = ''
        self.UserID = ''
        self.OTPVendorsID = ''
        self.SerialNumber = ''
        self.AuthKey = ''
        self.LastDrift = ''
        self.LastSuccess = ''
        self.OTPType = ''


class ManualSyncBrokerUserOTP(BaseStruct):

    def __init__(self, BrokerID='', UserID='', OTPType=OTP_NONE, FirstOTP='', SecondOTP=''):
        self.BrokerID = ''
        self.UserID = ''
        self.OTPType = ''
        self.FirstOTP = 'Password'
        self.SecondOTP = 'Password'


class CommRateModel(BaseStruct):

    def __init__(self, BrokerID='', CommModelID='', CommModelName=''):
        self.BrokerID = ''
        self.CommModelID = 'InvestorID'
        self.CommModelName = ''


class QryCommRateModel(BaseStruct):

    def __init__(self, BrokerID='', CommModelID=''):
        self.BrokerID = ''
        self.CommModelID = 'InvestorID'


class MarginModel(BaseStruct):

    def __init__(self, BrokerID='', MarginModelID='', MarginModelName=''):
        self.BrokerID = ''
        self.MarginModelID = 'InvestorID'
        self.MarginModelName = 'CommModelName'


class QryMarginModel(BaseStruct):

    def __init__(self, BrokerID='', MarginModelID=''):
        self.BrokerID = ''
        self.MarginModelID = 'InvestorID'


class EWarrantOffset(BaseStruct):

    def __init__(self, TradingDay='', BrokerID='', InvestorID='', ExchangeID='', InstrumentID='', Direction=D_Buy, HedgeFlag=HF_Speculation, Volume=0):
        self.TradingDay = 'TradeDate'
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExchangeID = ''
        self.InstrumentID = ''
        self.Direction = ''
        self.HedgeFlag = ''
        self.Volume = ''


class QryEWarrantOffset(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ExchangeID='', InstrumentID=''):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ExchangeID = ''
        self.InstrumentID = ''


class QryInvestorProductGroupMargin(BaseStruct):

    def __init__(self, BrokerID='', InvestorID='', ProductGroupID='', HedgeFlag=HF_Speculation):
        self.BrokerID = ''
        self.InvestorID = ''
        self.ProductGroupID = 'InstrumentID'
        self.HedgeFlag = ''


class InvestorProductGroupMargin(BaseStruct):

    def __init__(self, ProductGroupID='', BrokerID='', InvestorID='', TradingDay='', SettlementID=0, FrozenMargin=0.0, LongFrozenMargin=0.0, ShortFrozenMargin=0.0, UseMargin=0.0, LongUseMargin=0.0, ShortUseMargin=0.0, ExchMargin=0.0, LongExchMargin=0.0, ShortExchMargin=0.0, CloseProfit=0.0, FrozenCommission=0.0, Commission=0.0, FrozenCash=0.0, CashIn=0.0, PositionProfit=0.0, OffsetAmount=0.0, LongOffsetAmount=0.0, ShortOffsetAmount=0.0, ExchOffsetAmount=0.0, LongExchOffsetAmount=0.0, ShortExchOffsetAmount=0.0, HedgeFlag=HF_Speculation):
        self.ProductGroupID = 'InstrumentID'
        self.BrokerID = ''
        self.InvestorID = ''
        self.TradingDay = 'Date'
        self.SettlementID = ''
        self.FrozenMargin = 'Money'
        self.LongFrozenMargin = 'Money'
        self.ShortFrozenMargin = 'Money'
        self.UseMargin = 'Money'
        self.LongUseMargin = 'Money'
        self.ShortUseMargin = 'Money'
        self.ExchMargin = 'Money'
        self.LongExchMargin = 'Money'
        self.ShortExchMargin = 'Money'
        self.CloseProfit = 'Money'
        self.FrozenCommission = 'Money'
        self.Commission = 'Money'
        self.FrozenCash = 'Money'
        self.CashIn = 'Money'
        self.PositionProfit = 'Money'
        self.OffsetAmount = 'Money'
        self.LongOffsetAmount = 'Money'
        self.ShortOffsetAmount = 'Money'
        self.ExchOffsetAmount = 'Money'
        self.LongExchOffsetAmount = 'Money'
        self.ShortExchOffsetAmount = 'Money'
        self.HedgeFlag = ''


class QueryCFMMCTradingAccountToken(BaseStruct):

    def __init__(self, BrokerID='', InvestorID=''):
        self.BrokerID = ''
        self.InvestorID = ''


class CFMMCTradingAccountToken(BaseStruct):

    def __init__(self, BrokerID='', ParticipantID='', AccountID='', KeyID=0, Token=''):
        self.BrokerID = ''
        self.ParticipantID = ''
        self.AccountID = ''
        self.KeyID = 'SequenceNo'
        self.Token = 'CFMMCToken'


class ReqOpenAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', Gender=GD_Unknown, CountryCode='', CustType=CUSTT_Person, Address='', ZipCode='', Telephone='', MobilePhone='', Fax='', EMail='', MoneyAccountStatus=MAS_Normal, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, VerifyCertNoFlag=YNI_Yes, CurrencyID='', CashExchangeCode=CEC_Exchange, Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', TID=0, UserID=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.Gender = ''
        self.CountryCode = ''
        self.CustType = ''
        self.Address = ''
        self.ZipCode = ''
        self.Telephone = ''
        self.MobilePhone = ''
        self.Fax = ''
        self.EMail = ''
        self.MoneyAccountStatus = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.CashExchangeCode = ''
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.TID = ''
        self.UserID = ''


class ReqCancelAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', Gender=GD_Unknown, CountryCode='', CustType=CUSTT_Person, Address='', ZipCode='', Telephone='', MobilePhone='', Fax='', EMail='', MoneyAccountStatus=MAS_Normal, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, VerifyCertNoFlag=YNI_Yes, CurrencyID='', CashExchangeCode=CEC_Exchange, Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', TID=0, UserID=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.Gender = ''
        self.CountryCode = ''
        self.CustType = ''
        self.Address = ''
        self.ZipCode = ''
        self.Telephone = ''
        self.MobilePhone = ''
        self.Fax = ''
        self.EMail = ''
        self.MoneyAccountStatus = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.CashExchangeCode = ''
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.TID = ''
        self.UserID = ''


class ReqChangeAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', Gender=GD_Unknown, CountryCode='', CustType=CUSTT_Person, Address='', ZipCode='', Telephone='', MobilePhone='', Fax='', EMail='', MoneyAccountStatus=MAS_Normal, BankAccount='', BankPassWord='', NewBankAccount='', NewBankPassWord='', AccountID='', Password='', BankAccType=BAT_BankBook, InstallID=0, VerifyCertNoFlag=YNI_Yes, CurrencyID='', BrokerIDByBank='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, TID=0, Digest=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.Gender = ''
        self.CountryCode = ''
        self.CustType = ''
        self.Address = ''
        self.ZipCode = ''
        self.Telephone = ''
        self.MobilePhone = ''
        self.Fax = ''
        self.EMail = ''
        self.MoneyAccountStatus = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.NewBankAccount = 'BankAccount'
        self.NewBankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.BankAccType = ''
        self.InstallID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.TID = ''
        self.Digest = ''


class ReqTransfer(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, FutureSerial=0, UserID='', VerifyCertNoFlag=YNI_Yes, CurrencyID='', TradeAmount=0.0, FutureFetchAmount=0.0, FeePayFlag=FPF_BEN, CustFee=0.0, BrokerFee=0.0, Message='', Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', RequestID=0, TID=0, TransferStatus=TRFS_Normal):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.FutureSerial = ''
        self.UserID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.TradeAmount = ''
        self.FutureFetchAmount = 'TradeAmount'
        self.FeePayFlag = ''
        self.CustFee = ''
        self.BrokerFee = 'FutureFee'
        self.Message = 'AddInfo'
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.TransferStatus = ''


class RspTransfer(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, FutureSerial=0, UserID='', VerifyCertNoFlag=YNI_Yes, CurrencyID='', TradeAmount=0.0, FutureFetchAmount=0.0, FeePayFlag=FPF_BEN, CustFee=0.0, BrokerFee=0.0, Message='', Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', RequestID=0, TID=0, TransferStatus=TRFS_Normal, ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.FutureSerial = ''
        self.UserID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.TradeAmount = ''
        self.FutureFetchAmount = 'TradeAmount'
        self.FeePayFlag = ''
        self.CustFee = ''
        self.BrokerFee = 'FutureFee'
        self.Message = 'AddInfo'
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.TransferStatus = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class ReqRepeal(BaseStruct):

    def __init__(self, RepealTimeInterval=0, RepealedTimes=0, BankRepealFlag=BRF_BankNotNeedRepeal, BrokerRepealFlag=BRORF_BrokerNotNeedRepeal, PlateRepealSerial=0, BankRepealSerial='', FutureRepealSerial=0, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, FutureSerial=0, UserID='', VerifyCertNoFlag=YNI_Yes, CurrencyID='', TradeAmount=0.0, FutureFetchAmount=0.0, FeePayFlag=FPF_BEN, CustFee=0.0, BrokerFee=0.0, Message='', Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', RequestID=0, TID=0, TransferStatus=TRFS_Normal):
        self.RepealTimeInterval = ''
        self.RepealedTimes = ''
        self.BankRepealFlag = ''
        self.BrokerRepealFlag = ''
        self.PlateRepealSerial = 'PlateSerial'
        self.BankRepealSerial = 'BankSerial'
        self.FutureRepealSerial = 'FutureSerial'
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.FutureSerial = ''
        self.UserID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.TradeAmount = ''
        self.FutureFetchAmount = 'TradeAmount'
        self.FeePayFlag = ''
        self.CustFee = ''
        self.BrokerFee = 'FutureFee'
        self.Message = 'AddInfo'
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.TransferStatus = ''


class RspRepeal(BaseStruct):

    def __init__(self, RepealTimeInterval=0, RepealedTimes=0, BankRepealFlag=BRF_BankNotNeedRepeal, BrokerRepealFlag=BRORF_BrokerNotNeedRepeal, PlateRepealSerial=0, BankRepealSerial='', FutureRepealSerial=0, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, FutureSerial=0, UserID='', VerifyCertNoFlag=YNI_Yes, CurrencyID='', TradeAmount=0.0, FutureFetchAmount=0.0, FeePayFlag=FPF_BEN, CustFee=0.0, BrokerFee=0.0, Message='', Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', RequestID=0, TID=0, TransferStatus=TRFS_Normal, ErrorID=0, ErrorMsg=''):
        self.RepealTimeInterval = ''
        self.RepealedTimes = ''
        self.BankRepealFlag = ''
        self.BrokerRepealFlag = ''
        self.PlateRepealSerial = 'PlateSerial'
        self.BankRepealSerial = 'BankSerial'
        self.FutureRepealSerial = 'FutureSerial'
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.FutureSerial = ''
        self.UserID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.TradeAmount = ''
        self.FutureFetchAmount = 'TradeAmount'
        self.FeePayFlag = ''
        self.CustFee = ''
        self.BrokerFee = 'FutureFee'
        self.Message = 'AddInfo'
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.TransferStatus = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class ReqQueryAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', FutureSerial=0, InstallID=0, UserID='', VerifyCertNoFlag=YNI_Yes, CurrencyID='', Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', RequestID=0, TID=0):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.FutureSerial = ''
        self.InstallID = ''
        self.UserID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''


class RspQueryAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', FutureSerial=0, InstallID=0, UserID='', VerifyCertNoFlag=YNI_Yes, CurrencyID='', Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', RequestID=0, TID=0, BankUseAmount=0.0, BankFetchAmount=0.0):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.FutureSerial = ''
        self.InstallID = ''
        self.UserID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.BankUseAmount = 'TradeAmount'
        self.BankFetchAmount = 'TradeAmount'


class FutureSignIO(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Digest='', CurrencyID='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Digest = ''
        self.CurrencyID = ''
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''


class RspFutureSignIn(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Digest='', CurrencyID='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0, ErrorID=0, ErrorMsg='', PinKey='', MacKey=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Digest = ''
        self.CurrencyID = ''
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''
        self.PinKey = 'PasswordKey'
        self.MacKey = 'PasswordKey'


class ReqFutureSignOut(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Digest='', CurrencyID='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Digest = ''
        self.CurrencyID = ''
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''


class RspFutureSignOut(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Digest='', CurrencyID='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0, ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Digest = ''
        self.CurrencyID = ''
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class ReqQueryTradeResultBySerial(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, Reference=0, RefrenceIssureType=TS_Bank, RefrenceIssure='', CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', CurrencyID='', TradeAmount=0.0, Digest=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.Reference = 'Serial'
        self.RefrenceIssureType = 'InstitutionType'
        self.RefrenceIssure = 'OrganCode'
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.CurrencyID = ''
        self.TradeAmount = ''
        self.Digest = ''


class RspQueryTradeResultBySerial(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, ErrorID=0, ErrorMsg='', Reference=0, RefrenceIssureType=TS_Bank, RefrenceIssure='', OriginReturnCode='', OriginDescrInfoForReturnCode='', BankAccount='', BankPassWord='', AccountID='', Password='', CurrencyID='', TradeAmount=0.0, Digest=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''
        self.Reference = 'Serial'
        self.RefrenceIssureType = 'InstitutionType'
        self.RefrenceIssure = 'OrganCode'
        self.OriginReturnCode = 'ReturnCode'
        self.OriginDescrInfoForReturnCode = 'DescrInfoForReturnCode'
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.CurrencyID = ''
        self.TradeAmount = ''
        self.Digest = ''


class ReqDayEndFileReady(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, FileBusinessCode=FBC_Others, Digest=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.FileBusinessCode = ''
        self.Digest = ''


class ReturnResult(BaseStruct):

    def __init__(self, ReturnCode='', DescrInfoForReturnCode=''):
        self.ReturnCode = ''
        self.DescrInfoForReturnCode = ''


class VerifyFuturePassword(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, AccountID='', Password='', BankAccount='', BankPassWord='', InstallID=0, TID=0, CurrencyID=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.AccountID = ''
        self.Password = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.InstallID = ''
        self.TID = ''
        self.CurrencyID = ''


class VerifyCustInfo(BaseStruct):

    def __init__(self, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person):
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''


class VerifyFuturePasswordAndCustInfo(BaseStruct):

    def __init__(self, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, AccountID='', Password='', CurrencyID=''):
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.AccountID = ''
        self.Password = ''
        self.CurrencyID = ''


class DepositResultInform(BaseStruct):

    def __init__(self, DepositSeqNo='', BrokerID='', InvestorID='', Deposit=0.0, RequestID=0, ReturnCode='', DescrInfoForReturnCode=''):
        self.DepositSeqNo = ''
        self.BrokerID = ''
        self.InvestorID = ''
        self.Deposit = 'Money'
        self.RequestID = ''
        self.ReturnCode = ''
        self.DescrInfoForReturnCode = ''


class ReqSyncKey(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Message='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Message = 'AddInfo'
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''


class RspSyncKey(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Message='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0, ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Message = 'AddInfo'
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class NotifyQueryAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', CustType=CUSTT_Person, BankAccount='', BankPassWord='', AccountID='', Password='', FutureSerial=0, InstallID=0, UserID='', VerifyCertNoFlag=YNI_Yes, CurrencyID='', Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', RequestID=0, TID=0, BankUseAmount=0.0, BankFetchAmount=0.0, ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustType = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.FutureSerial = ''
        self.InstallID = ''
        self.UserID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.BankUseAmount = 'TradeAmount'
        self.BankFetchAmount = 'TradeAmount'
        self.ErrorID = ''
        self.ErrorMsg = ''


class TransferSerial(BaseStruct):

    def __init__(self, PlateSerial=0, TradeDate='', TradingDay='', TradeTime='', TradeCode='', SessionID=0, BankID='', BankBranchID='', BankAccType=BAT_BankBook, BankAccount='', BankSerial='', BrokerID='', BrokerBranchID='', FutureAccType=FAT_BankBook, AccountID='', InvestorID='', FutureSerial=0, IdCardType=ICT_EID, IdentifiedCardNo='', CurrencyID='', TradeAmount=0.0, CustFee=0.0, BrokerFee=0.0, AvailabilityFlag=AVAF_Invalid, OperatorCode='', BankNewAccount='', ErrorID=0, ErrorMsg=''):
        self.PlateSerial = ''
        self.TradeDate = ''
        self.TradingDay = 'Date'
        self.TradeTime = ''
        self.TradeCode = ''
        self.SessionID = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BankAccType = ''
        self.BankAccount = ''
        self.BankSerial = ''
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.FutureAccType = ''
        self.AccountID = ''
        self.InvestorID = ''
        self.FutureSerial = ''
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CurrencyID = ''
        self.TradeAmount = ''
        self.CustFee = ''
        self.BrokerFee = 'FutureFee'
        self.AvailabilityFlag = ''
        self.OperatorCode = ''
        self.BankNewAccount = 'BankAccount'
        self.ErrorID = ''
        self.ErrorMsg = ''


class QryTransferSerial(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', BankID='', CurrencyID=''):
        self.BrokerID = ''
        self.AccountID = ''
        self.BankID = ''
        self.CurrencyID = ''


class NotifyFutureSignIn(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Digest='', CurrencyID='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0, ErrorID=0, ErrorMsg='', PinKey='', MacKey=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Digest = ''
        self.CurrencyID = ''
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''
        self.PinKey = 'PasswordKey'
        self.MacKey = 'PasswordKey'


class NotifyFutureSignOut(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Digest='', CurrencyID='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0, ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Digest = ''
        self.CurrencyID = ''
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class NotifySyncKey(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, InstallID=0, UserID='', Message='', DeviceID='', BrokerIDByBank='', OperNo='', RequestID=0, TID=0, ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.InstallID = ''
        self.UserID = ''
        self.Message = 'AddInfo'
        self.DeviceID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.OperNo = ''
        self.RequestID = ''
        self.TID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class QryAccountregister(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', BankID='', BankBranchID='', CurrencyID=''):
        self.BrokerID = ''
        self.AccountID = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.CurrencyID = ''


class Accountregister(BaseStruct):

    def __init__(self, TradeDay='', BankID='', BankBranchID='', BankAccount='', BrokerID='', BrokerBranchID='', AccountID='', IdCardType=ICT_EID, IdentifiedCardNo='', CustomerName='', CurrencyID='', OpenOrDestroy=OOD_Open, RegDate='', OutDate='', TID=0, CustType=CUSTT_Person, BankAccType=BAT_BankBook):
        self.TradeDay = 'TradeDate'
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BankAccount = ''
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.AccountID = ''
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.CustomerName = 'IndividualName'
        self.CurrencyID = ''
        self.OpenOrDestroy = ''
        self.RegDate = 'TradeDate'
        self.OutDate = 'TradeDate'
        self.TID = ''
        self.CustType = ''
        self.BankAccType = ''


class OpenAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', Gender=GD_Unknown, CountryCode='', CustType=CUSTT_Person, Address='', ZipCode='', Telephone='', MobilePhone='', Fax='', EMail='', MoneyAccountStatus=MAS_Normal, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, VerifyCertNoFlag=YNI_Yes, CurrencyID='', CashExchangeCode=CEC_Exchange, Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', TID=0, UserID='', ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.Gender = ''
        self.CountryCode = ''
        self.CustType = ''
        self.Address = ''
        self.ZipCode = ''
        self.Telephone = ''
        self.MobilePhone = ''
        self.Fax = ''
        self.EMail = ''
        self.MoneyAccountStatus = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.CashExchangeCode = ''
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.TID = ''
        self.UserID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class CancelAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', Gender=GD_Unknown, CountryCode='', CustType=CUSTT_Person, Address='', ZipCode='', Telephone='', MobilePhone='', Fax='', EMail='', MoneyAccountStatus=MAS_Normal, BankAccount='', BankPassWord='', AccountID='', Password='', InstallID=0, VerifyCertNoFlag=YNI_Yes, CurrencyID='', CashExchangeCode=CEC_Exchange, Digest='', BankAccType=BAT_BankBook, DeviceID='', BankSecuAccType=BAT_BankBook, BrokerIDByBank='', BankSecuAcc='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, OperNo='', TID=0, UserID='', ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.Gender = ''
        self.CountryCode = ''
        self.CustType = ''
        self.Address = ''
        self.ZipCode = ''
        self.Telephone = ''
        self.MobilePhone = ''
        self.Fax = ''
        self.EMail = ''
        self.MoneyAccountStatus = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.InstallID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.CashExchangeCode = ''
        self.Digest = ''
        self.BankAccType = ''
        self.DeviceID = ''
        self.BankSecuAccType = 'BankAccType'
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankSecuAcc = 'BankAccount'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.OperNo = ''
        self.TID = ''
        self.UserID = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class ChangeAccount(BaseStruct):

    def __init__(self, TradeCode='', BankID='', BankBranchID='', BrokerID='', BrokerBranchID='', TradeDate='', TradeTime='', BankSerial='', TradingDay='', PlateSerial=0, LastFragment=LF_Yes, SessionID=0, CustomerName='', IdCardType=ICT_EID, IdentifiedCardNo='', Gender=GD_Unknown, CountryCode='', CustType=CUSTT_Person, Address='', ZipCode='', Telephone='', MobilePhone='', Fax='', EMail='', MoneyAccountStatus=MAS_Normal, BankAccount='', BankPassWord='', NewBankAccount='', NewBankPassWord='', AccountID='', Password='', BankAccType=BAT_BankBook, InstallID=0, VerifyCertNoFlag=YNI_Yes, CurrencyID='', BrokerIDByBank='', BankPwdFlag=BPWDF_NoCheck, SecuPwdFlag=BPWDF_NoCheck, TID=0, Digest='', ErrorID=0, ErrorMsg=''):
        self.TradeCode = ''
        self.BankID = ''
        self.BankBranchID = 'BankBrchID'
        self.BrokerID = ''
        self.BrokerBranchID = 'FutureBranchID'
        self.TradeDate = ''
        self.TradeTime = ''
        self.BankSerial = ''
        self.TradingDay = 'TradeDate'
        self.PlateSerial = 'Serial'
        self.LastFragment = ''
        self.SessionID = ''
        self.CustomerName = 'IndividualName'
        self.IdCardType = ''
        self.IdentifiedCardNo = ''
        self.Gender = ''
        self.CountryCode = ''
        self.CustType = ''
        self.Address = ''
        self.ZipCode = ''
        self.Telephone = ''
        self.MobilePhone = ''
        self.Fax = ''
        self.EMail = ''
        self.MoneyAccountStatus = ''
        self.BankAccount = ''
        self.BankPassWord = 'Password'
        self.NewBankAccount = 'BankAccount'
        self.NewBankPassWord = 'Password'
        self.AccountID = ''
        self.Password = ''
        self.BankAccType = ''
        self.InstallID = ''
        self.VerifyCertNoFlag = 'YesNoIndicator'
        self.CurrencyID = ''
        self.BrokerIDByBank = 'BankCodingForFuture'
        self.BankPwdFlag = 'PwdFlag'
        self.SecuPwdFlag = 'PwdFlag'
        self.TID = ''
        self.Digest = ''
        self.ErrorID = ''
        self.ErrorMsg = ''


class SecAgentACIDMap(BaseStruct):

    def __init__(self, BrokerID='', UserID='', AccountID='', CurrencyID='', BrokerSecAgentID=''):
        self.BrokerID = ''
        self.UserID = ''
        self.AccountID = ''
        self.CurrencyID = ''
        self.BrokerSecAgentID = 'AccountID'


class QrySecAgentACIDMap(BaseStruct):

    def __init__(self, BrokerID='', UserID='', AccountID='', CurrencyID=''):
        self.BrokerID = ''
        self.UserID = ''
        self.AccountID = ''
        self.CurrencyID = ''


class UserRightsAssign(BaseStruct):

    def __init__(self, BrokerID='', UserID='', DRIdentityID=0):
        self.BrokerID = ''
        self.UserID = ''
        self.DRIdentityID = ''


class BrokerUserRightAssign(BaseStruct):

    def __init__(self, BrokerID='', DRIdentityID=0, Tradeable=0):
        self.BrokerID = ''
        self.DRIdentityID = ''
        self.Tradeable = 'Bool'


class DRTransfer(BaseStruct):

    def __init__(self, OrigDRIdentityID=0, DestDRIdentityID=0, OrigBrokerID='', DestBrokerID=''):
        self.OrigDRIdentityID = 'DRIdentityID'
        self.DestDRIdentityID = 'DRIdentityID'
        self.OrigBrokerID = 'BrokerID'
        self.DestBrokerID = 'BrokerID'


class FensUserInfo(BaseStruct):

    def __init__(self, BrokerID='', UserID='', LoginMode=LM_Trade):
        self.BrokerID = ''
        self.UserID = ''
        self.LoginMode = ''


class CurrTransferIdentity(BaseStruct):

    def __init__(self, IdentityID=0):
        self.IdentityID = 'DRIdentityID'


class LoginForbiddenUser(BaseStruct):

    def __init__(self, BrokerID='', UserID=''):
        self.BrokerID = ''
        self.UserID = ''


class QryLoginForbiddenUser(BaseStruct):

    def __init__(self, BrokerID='', UserID=''):
        self.BrokerID = ''
        self.UserID = ''


class MulticastGroupInfo(BaseStruct):

    def __init__(self, GroupIP='', GroupPort=0, SourceIP=''):
        self.GroupIP = 'IPAddress'
        self.GroupPort = 'IPPort'
        self.SourceIP = 'IPAddress'


class TradingAccountReserve(BaseStruct):

    def __init__(self, BrokerID='', AccountID='', Reserve=0.0, CurrencyID=''):
        self.BrokerID = ''
        self.AccountID = ''
        self.Reserve = 'Money'
        self.CurrencyID = ''


error = {'NONE': 0, 0: 'CTP:正确', 'INVALID_DATA_SYNC_STATUS': 1, 1: 'CTP:不在已同步状态', 'INCONSISTENT_INFORMATION': 2, 2: 'CTP:会话信息不一致', 'INVALID_LOGIN': 3, 3: 'CTP:不合法的登录', 'USER_NOT_ACTIVE': 4, 4: 'CTP:用户不活跃', 'DUPLICATE_LOGIN': 5, 5: 'CTP:重复的登录', 'NOT_LOGIN_YET': 6, 6: 'CTP:还没有登录', 'NOT_INITED': 7, 7: 'CTP:还没有初始化', 'FRONT_NOT_ACTIVE': 8, 8: 'CTP:前置不活跃', 'NO_PRIVILEGE': 9, 9: 'CTP:无此权限', 'CHANGE_OTHER_PASSWORD': 10, 10: 'CTP:修改别人的口令', 'USER_NOT_FOUND': 11, 11: 'CTP:找不到该用户', 'BROKER_NOT_FOUND': 12, 12: 'CTP:找不到该经纪公司', 'INVESTOR_NOT_FOUND': 13, 13: 'CTP:找不到投资者', 'OLD_PASSWORD_MISMATCH': 14, 14: 'CTP:原口令不匹配', 'BAD_FIELD': 15, 15: 'CTP:报单字段有误', 'INSTRUMENT_NOT_FOUND': 16, 16: 'CTP:找不到合约', 'INSTRUMENT_NOT_TRADING': 17, 17: 'CTP:合约不能交易', 'NOT_EXCHANGE_PARTICIPANT': 18, 18: 'CTP:经纪公司不是交易所的会员', 'INVESTOR_NOT_ACTIVE': 19, 19: 'CTP:投资者不活跃', 'NOT_EXCHANGE_CLIENT': 20, 20: 'CTP:投资者未在交易所开户', 'NO_VALID_TRADER_AVAILABLE': 21, 21: 'CTP:该交易席位未连接到交易所', 'DUPLICATE_ORDER_REF': 22, 22: 'CTP:报单错误：不允许重复报单', 'BAD_ORDER_ACTION_FIELD': 23, 23: 'CTP:错误的报单操作字段', 'DUPLICATE_ORDER_ACTION_REF': 24, 24: 'CTP:撤单已报送，不允许重复撤单', 'ORDER_NOT_FOUND': 25, 25: 'CTP:撤单找不到相应报单', 'INSUITABLE_ORDER_STATUS': 26, 26: 'CTP:报单已全成交或已撤销，不能再撤', 'UNSUPPORTED_FUNCTION': 27, 27: 'CTP:不支持的功能', 'NO_TRADING_RIGHT': 28, 28: 'CTP:没有报单交易权限', 'CLOSE_ONLY': 29, 29: 'CTP:只能平仓', 'OVER_CLOSE_POSITION': 30, 30: 'CTP:平仓量超过持仓量', 'INSUFFICIENT_MONEY': 31, 31: 'CTP:资金不足', 'DUPLICATE_PK': 32, 32: 'CTP:主键重复', 'CANNOT_FIND_PK': 33, 33: 'CTP:找不到主键', 'CAN_NOT_INACTIVE_BROKER': 34, 34: 'CTP:设置经纪公司不活跃状态失败', 'BROKER_SYNCHRONIZING': 35, 35: 'CTP:经纪公司正在同步', 'BROKER_SYNCHRONIZED': 36, 36: 'CTP:经纪公司已同步', 'SHORT_SELL': 37, 37: 'CTP:现货交易不能卖空', 'INVALID_SETTLEMENT_REF': 38, 38: 'CTP:不合法的结算引用', 'CFFEX_NETWORK_ERROR': 39, 39: 'CTP:交易所网络连接失败', 'CFFEX_OVER_REQUEST': 40, 40: 'CTP:交易所未处理请求超过许可数', 'CFFEX_OVER_REQUEST_PER_SECOND': 41, 41: 'CTP:交易所每秒发送请求数超过许可数', 'SETTLEMENT_INFO_NOT_CONFIRMED': 42, 42: 'CTP:结算结果未确认', 'DEPOSIT_NOT_FOUND': 43, 43: 'CTP:没有对应的入金记录', 'EXCHANG_TRADING': 44, 44: 'CTP:交易所已经进入连续交易状态', 'PARKEDORDER_NOT_FOUND': 45, 45: 'CTP:找不到预埋（撤单）单', 'PARKEDORDER_HASSENDED': 46, 46: 'CTP:预埋（撤单）单已经发送', 'PARKEDORDER_HASDELETE': 47, 47: 'CTP:预埋（撤单）单已经删除', 'INVALID_INVESTORIDORPASSWORD': 48, 48: 'CTP:无效的投资者或者密码', 'INVALID_LOGIN_IPADDRESS': 49, 49: 'CTP:不合法的登录IP地址', 'OVER_CLOSETODAY_POSITION': 50, 50: 'CTP:平今仓位不足', 'OVER_CLOSEYESTERDAY_POSITION': 51, 51: 'CTP:平昨仓位不足', 'BROKER_NOT_ENOUGH_CONDORDER': 52, 52: 'CTP:经纪公司没有足够可用的条件单数量', 'INVESTOR_NOT_ENOUGH_CONDORDER': 53, 53: 'CTP:投资者没有足够可用的条件单数量', 'BROKER_NOT_SUPPORT_CONDORDER': 54, 54: 'CTP:经纪公司不支持条件单', 'RESEND_ORDER_BROKERINVESTOR_NOTMATCH': 55, 55: 'CTP:重发未知单经济公司/投资者不匹配', 'SYC_OTP_FAILED': 56, 56: 'CTP:同步动态令牌失败', 'OTP_MISMATCH': 57, 57: 'CTP:动态令牌校验错误', 'OTPPARAM_NOT_FOUND': 58, 58: 'CTP:找不到动态令牌配置信息', 'UNSUPPORTED_OTPTYPE': 59, 59: 'CTP:不支持的动态令牌类型', 'SINGLEUSERSESSION_EXCEED_LIMIT': 60, 60: 'CTP:用户在线会话超出上限', 'EXCHANGE_UNSUPPORTED_ARBITRAGE': 61, 61: 'CTP:该交易所不支持套利类型报单', 'NO_CONDITIONAL_ORDER_RIGHT': 62, 62: 'CTP:没有条件单交易权限', 'AUTH_FAILED': 63, 63: 'CTP:客户端认证失败', 'NOT_AUTHENT': 64, 64: 'CTP:客户端未认证', 'SWAPORDER_UNSUPPORTED': 65, 65: 'CTP:该合约不支持互换类型报单', 'OPTIONS_ONLY_SUPPORT_SPEC': 66, 66: 'CTP:该期权合约只支持投机类型报单', 'DUPLICATE_EXECORDER_REF': 67, 67: 'CTP:执行宣告错误，不允许重复执行', 'RESEND_EXECORDER_BROKERINVESTOR_NOTMATCH': 68, 68: 'CTP:重发未知执行宣告经纪公司/投资者不匹配', 'EXECORDER_NOTOPTIONS': 69, 69: 'CTP:只有期权合约可执行', 'OPTIONS_NOT_SUPPORT_EXEC': 70, 70: 'CTP:该期权合约不支持执行', 'BAD_EXECORDER_ACTION_FIELD': 71, 71: 'CTP:执行宣告字段有误', 'DUPLICATE_EXECORDER_ACTION_REF': 72, 72: 'CTP:执行宣告撤单已报送，不允许重复撤单', 'EXECORDER_NOT_FOUND': 73, 73: 'CTP:执行宣告撤单找不到相应执行宣告', 'OVER_EXECUTE_POSITION': 74, 74: 'CTP:执行仓位不足', 'LOGIN_FORBIDDEN': 75, 75: 'CTP:连续登录失败次数超限，登录被禁止', 'INVALID_TRANSFER_AGENT': 76, 76: 'CTP:非法银期代理关系', 'NO_FOUND_FUNCTION': 77, 77: 'CTP:无此功能', 'SEND_EXCHANGEORDER_FAILED': 78, 78: 'CTP:发送报单失败', 'SEND_EXCHANGEORDERACTION_FAILED': 79, 79: 'CTP:发送报单操作失败', 'PRICETYPE_NOTSUPPORT_BYEXCHANGE': 80, 80: 'CTP:交易所不支持的价格类型', 'BAD_EXECUTE_TYPE': 81, 81: 'CTP:错误的执行类型', 'BAD_OPTION_INSTR': 82, 82: 'CTP:无效的组合合约', 'INSTR_NOTSUPPORT_FORQUOTE': 83, 83: 'CTP:该合约不支持询价', 'RESEND_QUOTE_BROKERINVESTOR_NOTMATCH': 84, 84: 'CTP:重发未知报价经纪公司/投资者不匹配', 'INSTR_NOTSUPPORT_QUOTE': 85, 85: 'CTP:该合约不支持报价', 'QUOTE_NOT_FOUND': 86, 86: 'CTP:报价撤单找不到相应报价', 'OPTIONS_NOT_SUPPORT_ABANDON': 87, 87: 'CTP:该期权合约不支持放弃执行', 'COMBOPTIONS_SUPPORT_IOC_ONLY': 88, 88: 'CTP:该组合期权合约只支持IOC', 'OPEN_FILE_FAILED': 89, 89: 'CTP:打开文件失败', 'NEED_RETRY': 90, 90: 'CTP：查询未就绪，请稍后重试', 'EXCHANGE_RTNERROR': 91, 91: 'CTP：交易所返回的错误', 'QUOTE_DERIVEDORDER_ACTIONERROR': 92, 92: 'CTP:报价衍生单要等待交易所返回才能撤单', 'INSTRUMENTMAP_NOT_FOUND': 93, 93: 'CTP:找不到组合合约映射', 'NO_TRADING_RIGHT_IN_SEPC_DR': 101, 101: 'CTP:用户在本系统没有报单权限', 'NO_DR_NO': 102, 102: 'CTP:系统缺少灾备标示号', 'SEND_INSTITUTION_CODE_ERROR': 1000, 1000: 'CTP:银期转账：发送机构代码错误', 'NO_GET_PLATFORM_SN': 1001, 1001: 'CTP:银期转账：取平台流水号错误', 'ILLEGAL_TRANSFER_BANK': 1002, 1002: 'CTP:银期转账：不合法的转账银行', 'ALREADY_OPEN_ACCOUNT': 1003, 1003: 'CTP:银期转账：已经开户', 'NOT_OPEN_ACCOUNT': 1004, 1004: 'CTP:银期转账：未开户', 'PROCESSING': 1005, 1005: 'CTP:银期转账：处理中', 'OVERTIME': 1006, 1006: 'CTP:银期转账：交易超时', 'RECORD_NOT_FOUND': 1007, 1007: 'CTP:银期转账：找不到记录', 'NO_FOUND_REVERSAL_ORIGINAL_TRANSACTION': 1008, 1008: 'CTP:银期转账：找不到被冲正的原始交易', 'CONNECT_HOST_FAILED': 1009, 1009: 'CTP:银期转账：连接主机失败', 'SEND_FAILED': 1010, 1010: 'CTP:银期转账：发送失败', 'LATE_RESPONSE': 1011, 1011: 'CTP:银期转账：迟到应答', 'REVERSAL_BANKID_NOT_MATCH': 1012, 1012: 'CTP:银期转账：冲正交易银行代码错误', 'REVERSAL_BANKACCOUNT_NOT_MATCH': 1013, 1013: 'CTP:银期转账：冲正交易银行账户错误', 'REVERSAL_BROKERID_NOT_MATCH': 1014, 1014: 'CTP:银期转账：冲正交易经纪公司代码错误', 'REVERSAL_ACCOUNTID_NOT_MATCH': 1015, 1015: 'CTP:银期转账：冲正交易资金账户错误', 'REVERSAL_AMOUNT_NOT_MATCH': 1016, 1016: 'CTP:银期转账：冲正交易交易金额错误', 'DB_OPERATION_FAILED': 1017, 1017: 'CTP:银期转账：数据库操作错误', 'SEND_ASP_FAILURE': 1018, 1018: 'CTP:银期转账：发送到交易系统失败', 'NOT_SIGNIN': 1019, 1019: 'CTP:银期转账：没有签到', 'ALREADY_SIGNIN': 1020, 1020: 'CTP:银期转账：已经签到', 'AMOUNT_OR_TIMES_OVER': 1021, 1021: 'CTP:银期转账：金额或次数超限', 'NOT_IN_TRANSFER_TIME': 1022, 1022: 'CTP:银期转账：这一时间段不能转账', 'BANK_SERVER_ERROR': 1023, 1023: '银行主机错', 'BANK_SERIAL_IS_REPEALED': 1024, 1024: 'CTP:银期转账：银行已经冲正', 'BANK_SERIAL_NOT_EXIST': 1025, 1025: 'CTP:银期转账：银行流水不存在', 'NOT_ORGAN_MAP': 1026, 1026: 'CTP:银期转账：机构没有签约', 'EXIST_TRANSFER': 1027, 1027: 'CTP:银期转账：存在转账，不能销户', 'BANK_FORBID_REVERSAL': 1028, 1028: 'CTP:银期转账：银行不支持冲正', 'DUP_BANK_SERIAL': 1029, 1029: 'CTP:银期转账：重复的银行流水', 'FBT_SYSTEM_BUSY': 1030, 1030: 'CTP:银期转账：转账系统忙，稍后再试', 'MACKEY_SYNCING': 1031, 1031: 'CTP:银期转账：MAC密钥正在同步', 'ACCOUNTID_ALREADY_REGISTER': 1032, 1032: 'CTP:银期转账：资金账户已经登记', 'BANKACCOUNT_ALREADY_REGISTER': 1033, 1033: 'CTP:银期转账：银行账户已经登记', 'DUP_BANK_SERIAL_REDO_OK': 1034, 1034: 'CTP:银期转账：重复的银行流水,重发成功', 'CURRENCYID_NOT_SUPPORTED': 1035, 1035: 'CTP:银期转账：该币种代码不支持', 'INVALID_MAC': 1036, 1036: 'CTP:银期转账：MAC值验证失败', 'NOT_SUPPORT_SECAGENT_BY_BANK': 1037, 1037: 'CTP:银期转账：不支持银行端发起的二级代理商转账和查询', 'PINKEY_SYNCING': 1038, 1038: 'CTP:银期转账：PIN密钥正在同步', 'SECAGENT_QUERY_BY_CCB': 1039, 1039: 'CTP:银期转账：建行发起的二级代理商查询', 'NO_VALID_BANKOFFER_AVAILABLE': 2000, 2000: 'CTP:该报盘未连接到银行', 'PASSWORD_MISMATCH': 2001, 2001: 'CTP:资金密码错误', 'DUPLATION_BANK_SERIAL': 2004, 2004: 'CTP:银行流水号重复', 'DUPLATION_OFFER_SERIAL': 2005, 2005: 'CTP:报盘流水号重复', 'SERIAL_NOT_EXSIT': 2006, 2006: 'CTP:被冲正流水不存在(冲正交易)', 'SERIAL_IS_REPEALED': 2007, 2007: 'CTP:原流水已冲正(冲正交易)', 'SERIAL_MISMATCH': 2008, 2008: 'CTP:与原流水信息不符(冲正交易)', 'IdentifiedCardNo_MISMATCH': 2009, 2009: 'CTP:证件号码或类型错误', 'ACCOUNT_NOT_FUND': 2011, 2011: 'CTP:资金账户不存在', 'ACCOUNT_NOT_ACTIVE': 2012, 2012: 'CTP:资金账户已经销户', 'NOT_ALLOW_REPEAL_BYMANUAL': 2013, 2013: 'CTP:该交易不能执行手工冲正', 'AMOUNT_OUTOFTHEWAY': 2014, 2014: 'CTP:转帐金额错误', 'EXCHANGERATE_NOT_FOUND': 2015, 2015: 'CTP:找不到汇率', 'WAITING_OFFER_RSP': 999999, 999999: 'CTP:等待银期报盘处理结果', 'FBE_NO_GET_PLATFORM_SN': 3001, 3001: 'CTP:银期换汇：取平台流水号错误', 'FBE_ILLEGAL_TRANSFER_BANK': 3002, 3002: 'CTP:银期换汇：不合法的转账银行', 'FBE_PROCESSING': 3005, 3005: 'CTP:银期换汇：处理中', 'FBE_OVERTIME': 3006, 3006: 'CTP:银期换汇：交易超时', 'FBE_RECORD_NOT_FOUND': 3007, 3007: 'CTP:银期换汇：找不到记录', 'FBE_CONNECT_HOST_FAILED': 3009, 3009: 'CTP:银期换汇：连接主机失败', 'FBE_SEND_FAILED': 3010, 3010: 'CTP:银期换汇：发送失败', 'FBE_LATE_RESPONSE': 3011, 3011: 'CTP:银期换汇：迟到应答', 'FBE_DB_OPERATION_FAILED': 3017, 3017: 'CTP:银期换汇：数据库操作错误', 'FBE_NOT_SIGNIN': 3019, 3019: 'CTP:银期换汇：没有签到', 'FBE_ALREADY_SIGNIN': 3020, 3020: 'CTP:银期换汇：已经签到', 'FBE_AMOUNT_OR_TIMES_OVER': 3021, 3021: 'CTP:银期换汇：金额或次数超限', 'FBE_NOT_IN_TRANSFER_TIME': 3022, 3022: 'CTP:银期换汇：这一时间段不能换汇', 'FBE_BANK_SERVER_ERROR': 3023, 3023: 'CTP:银期换汇：银行主机错', 'FBE_NOT_ORGAN_MAP': 3026, 3026: 'CTP:银期换汇：机构没有签约', 'FBE_SYSTEM_BUSY': 3030, 3030: 'CTP:银期换汇：换汇系统忙，稍后再试', 'FBE_CURRENCYID_NOT_SUPPORTED': 3035, 3035: 'CTP:银期换汇：该币种代码不支持', 'FBE_WRONG_BANK_ACCOUNT': 3036, 3036: 'CTP:银期换汇：银行帐号不正确', 'FBE_BANK_ACCOUNT_NO_FUNDS': 3037, 3037: 'CTP:银期换汇：银行帐户余额不足', 'FBE_DUP_CERT_NO': 3038, 3038: 'CTP:银期换汇：凭证号重复'}

def _init():
    import re, sys
    from ctypes import c_char, c_short, c_int, c_double, Structure
    G = globals()
    del G['_init']
    T = G.pop('T')
    Base = G.pop('BaseStruct')
    match = re.compile('(\\w+)\\[(\\d+)\\]').match
    D = {'char': c_char, 'short': c_short, 'int': c_int, 'double': c_double}
    for k, v in T.items():
        if v not in D:
            m = match(v).groups()
            D[v] = D[m[0]] * int(m[1])
        T[k] = D[v]

    if sys.version_info[0] >= 3:
        for k, v in G.items():
            if isinstance(v, str) and k[1:-1].count('_') == 1:
                G[k] = v.encode('latin-1')

    else:
        for k in error:
            if not isinstance(k, str):
                error[k] = error[k].decode('utf-8')

        edvs = {'ContingentCondition': CC_Immediately, 'MortgageFundUseRange': MFUR_None, 'AllWithoutTrade': AWT_Enable, 'PositionDateType': PDT_UseHistory, 'TradingRight': TR_Allow, 'UserRightType': URT_Logon, 'InstitutionType': TS_Bank, 'ValueMethod': VM_Absolute, 'HedgeFlag': HF_Speculation, 'TraderConnectStatus': TCS_NotConnected, 'ExecResult': OER_NoExec, 'TradeType': TRDT_SplitCombination, 'PositionType': PT_Net, 'ProductClass': PC_Futures, 'ClientIDType': CIDT_Speculation, 'CombDirection': CMDR_Comb, 'OrderPriceType': OPT_AnyPrice, 'ParkedOrderStatus': PAOS_NotSend, 'YesNoIndicator': YNI_Yes, 'CustType': CUSTT_Person, 'HandlePositionAlgoID': HPA_Base, 'Direction': D_Buy, 'OffsetFlag': OF_Open, 'PosiDirection': PD_Net, 'PwdFlag': BPWDF_NoCheck, 'OptionRoyaltyPriceType': ORPT_PreSettlementPrice, 'CloseDealType': CDT_Normal, 'BalanceAlgorithm': BLAG_Default, 'PersonType': PST_Order, 'ExchangeProperty': EXP_Normal, 'UserType': UT_Investor, 'TimeCondition': TC_IOC, 'ActionType': ACTP_Exec, 'OrderStatus': OST_AllTraded, 'MaxMarginSideAlgorithm': MMSA_NO, 'OrderSubmitStatus': OSS_InsertSubmitted, 'DataSyncStatus': DS_Asynchronous, 'TransferValidFlag': TVF_Invalid, 'AvailabilityFlag': AVAF_Invalid, 'InstStatusEnterReason': IER_Automatic, 'PositionDate': PSD_Today, 'ExecOrderCloseFlag': EOCF_AutoClose, 'ActionFlag': AF_Delete, 'Algorithm': AG_All, 'ForceCloseReason': FCC_NotForceClose, 'OrderType': ORDT_Normal, 'FeePayFlag': FPF_BEN, 'HandleTradingAccountAlgoID': HTAA_Base, 'FuturePwdFlag': FPWD_UnCheck, 'OptionsType': CP_CallOptions, 'Gender': GD_Unknown, 'FunctionCode': FC_DataAsync, 'OrderSource': OSRC_Participant, 'CashExchangeCode': CEC_Exchange, 'BrokerRepealFlag': BRORF_BrokerNotNeedRepeal, 'InstrumentStatus': IS_BeforeTrading, 'OpenOrDestroy': OOD_Open, 'BankRepealFlag': BRF_BankNotNeedRepeal, 'CombinationType': COMBT_Future, 'IdCardType': ICT_EID, 'MarginPriceType': MPT_PreSettlementPrice, 'FileBusinessCode': FBC_Others, 'IncludeCloseProfit': ICP_Include, 'CFMMCKeyKind': CFMMCKK_REQUEST, 'BankAccType': BAT_BankBook, 'ExecOrderPositionFlag': EOPF_Reserve, 'LastFragment': LF_Yes, 'InstLifePhase': IP_NotStart, 'FutureAccType': FAT_BankBook, 'LoginMode': LM_Trade, 'VolumeCondition': VC_AV, 'MoneyAccountStatus': MAS_Normal, 'OTPType': OTP_NONE, 'UserEventType': UET_Login, 'InvestorRange': IR_All, 'ForQuoteStatus': FQST_Submitted, 'FindMarginRateAlgoID': FMRA_Base, 'TransferStatus': TRFS_Normal, 'TradeSource': TSRC_NORMAL, 'PriceSource': PSRC_LastPrice, 'TradingRole': ER_Broker, 'BrokerFunctionCode': BFC_ForceUserLogout, 'OrderActionStatus': OAS_Submitted}
        Structs = [ v for v in G.values() if isinstance(v, type) and issubclass(v, Base) ]
        Base = G['BaseStruct'] = type('BaseStruct', (Structure,), dict((k, v) for k, v in Base.__dict__.items() if k in ('__doc__',
                                                                                                                         '__repr__',
                                                                                                                         '__str__') or not (k.startswith('__') and k.endswith('__'))))

        class builder(object):

            def __setattr__(self, fn, ft):
                ft = ft or fn
                if ft in edvs:
                    self.enums.append((len(self.fields), fn, edvs[ft]))
                self.fields.append((fn, T[ft]))

            def build(self, cls):
                self.__dict__['enums'] = []
                self.__dict__['fields'] = []
                cls.__dict__['__init__'](self)
                d = {'_fields_': tuple(self.fields)}
                if self.enums:
                    enums = tuple(self.enums)

                    def __init__(self, *args, **kwargs):
                        c = len(args)
                        setdefault = kwargs.setdefault
                        for i, n, d in enums:
                            if i >= c:
                                setdefault(n, d)

                        Base.__init__(self, *args, **kwargs)

                    d['__init__'] = __init__
                G[cls.__name__] = type(cls.__name__, (Base,), d)

        builder = builder()
        for cls in Structs:
            builder.build(cls)


_init()