# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:30:25 2020

                            +-----------------------+
                            |       SQL语句         |
                            +-----------+-----------+
                                        |
                            +-----------+-----------+
        +------------------->      DB取数据          |
+-------+--------+          +-----------+-----------+
|    下一个DB     |                      |
+-------^--------+                      |
        |                   +-----------v-----------+
        +---------N---------+        是否全部DB取完  |
                            +-----------+-----------+
                                        |
                            +-----------v------------+
                            |         合并数据集      |
                            +------------------------+
                                        |
                                 +--------------+
                                 | 保存为Excel  |
                                 +--------------+



@author: Weirroswei
"""

import time,datetime

dtt=str(datetime.date.today())
dss=str(datetime.date.today()-datetime.timedelta(days=30)) #日期减天数
dsm=str(datetime.date.today().replace(day=1)) #本月1号

#定义开始日期和结束日期；dtt是当前日期；dss是当前日期-30天

# print(f'{dtt},{dss},{dsm}')


#定义取数SQL；


SQL_A042 =  f'''
SELECT 
        (SELECT a0.PrintHeadr
   FROM OADM a0)     AS '公司',
        t0.DocNum AS '订单号',
       t4.U_NAME AS '制单人',
       t0.Comments AS '单据注释',
       打印状态 =
          CASE WHEN t0.Printed = 'Y' THEN '已打印' ELSE '未打印' END,
       单据状态 =
          CASE WHEN t0.DocStatus = 'C' THEN '已结算' ELSE '未清' END,
       单据行状态 =
          CASE
             WHEN t1.LineStatus = 'C' THEN '行已结算'
             ELSE '行未清'
          END,
       是否手工关闭 = t0.DocManClsd,
       是否取消 = t0.CANCELED,
       发货状态 =
          CASE
             WHEN (t1.Quantity - isnull (t2.Quantity, 0.0)) = 0.0
             THEN
                '完全收货'
             WHEN (t1.Quantity - isnull (t2.Quantity, 0.0)) = t1.Quantity
             THEN
                '未收货'
             ELSE
                '部分收货'
          END,
       t0.DocDate AS '订单日期',
       t0.CardCode AS '供方代码',
       t0.CardName AS '供方名称',
       t0.NumAtCard AS '供方参考编号',
       t1.LineNum + 1 AS '单据行号',
       t1.OcrCode AS '品类',
       t1.OcrCode2 AS '品牌',
       t1.OcrCode4 AS '地区',
       t1.OcrCode5 AS '部门',
       t9.WhsName AS '仓库',
       t1.ItemCode AS 'SAP货号',
       t5.U_OldItemNo AS '原来货号',
       CASE WHEN t5.U_Category = N'FG' THEN '商品' ELSE '物料' END
          AS '商品OR物料',
       t1.Dscription AS '品名',
       t1.Quantity AS '订单数量',
       isnull (t1.U_OriPrice, t7.Price) * t1.Quantity AS '采购额',
       t1.PriceAfVAT * t1.Quantity AS '采购折扣额(含税)',
       isnull (t2.Quantity, 0) AS '实收数量',
       isnull (t2.Quantity, 0) * isnull (t1.U_OriPrice, t7.Price)
          AS '实收额',
       isnull (t2.Quantity, 0) * t1.PriceAfVAT AS '实收折扣额(含税)',
       t1.Quantity - isnull (t2.Quantity, 0) AS '未收数量',
         (t1.Quantity - isnull (t2.Quantity, 0))
       * isnull (t1.U_OriPrice, t7.Price)
          AS '未收额',
       (t1.Quantity - isnull (t2.Quantity, 0)) * t1.PriceAfVAT
          AS '未收折扣额(含税)',
       isnull (t3.Quantity, 0) AS '采购退货数量',
       isnull (t3.Quantity, 0) * isnull (t1.U_OriPrice, t7.Price)
          AS '采购退货额',
       isnull (t3.Quantity, 0) * t1.PriceAfVAT AS '采购退货折扣额(含税)'
  FROM [dbo].[OPOR] t0
       INNER JOIN [dbo].[POR1] t1 ON t1.DocEntry = t0.DocEntry
       LEFT JOIN
       (SELECT a1.BaseLine,
               a1.BaseEntry,
               a1.ItemCode,
               sum (a1.Quantity) AS Quantity
          FROM [dbo].[OPDN] a0
               INNER JOIN [dbo].[PDN1] a1 ON a1.DocEntry = a0.DocEntry
        GROUP BY a1.BaseLine, a1.BaseEntry, a1.ItemCode) t2
          ON     t2.BaseEntry = t1.DocEntry
             AND t2.ItemCode = t1.ItemCode
             AND t2.BaseLine = t1.LineNum
       LEFT JOIN
       (SELECT a1.BaseLine,
               a1.BaseEntry,
               a1.ItemCode,
               sum (a2.Quantity) AS Quantity
          FROM [dbo].[OPDN] a0
               INNER JOIN [dbo].[PDN1] a1 ON a1.DocEntry = a0.DocEntry
               INNER JOIN
               (SELECT b1.ItemCode,
                       b1.BaseEntry,
                       b1.BaseLine,
                       sum (b1.Quantity) AS Quantity
                  FROM [dbo].[ORPD] b0
                       INNER JOIN [dbo].[RPD1] b1
                          ON b1.DocEntry = b0.DocEntry
                GROUP BY b1.ItemCode, b1.BaseEntry, b1.BaseLine) a2
                  ON     a2.ItemCode = a1.ItemCode
                     AND a2.BaseEntry = a1.DocEntry
                     AND a2.BaseLine = a1.LineNum
        GROUP BY a1.BaseLine, a1.BaseEntry, a1.ItemCode) t3
          ON     t3.BaseEntry = t1.DocEntry
             AND t3.ItemCode = t1.ItemCode
             AND t3.BaseLine = t1.LineNum
       INNER JOIN [dbo].[OUSR] t4 ON t4.[internal_k] = t0.[UserSign]
       INNER JOIN [dbo].[OITM] t5 ON t5.ItemCode = t1.ItemCode
       INNER JOIN [dbo].[ITM1] t7
          ON t7.ItemCode = t1.ItemCode AND t7.PriceList = (SELECT a0.U_Value
                                   FROM [dbo].[@ADDON_CFG] a0
                                  WHERE a0.Code = 'RPT_001')
       INNER JOIN [dbo].[OWHS] t9 ON t9.WhsCode = t1.WhsCode
 WHERE t0.DocDate >= getdate()-90 --AND t0.DocDate <= '20200430'
ORDER BY t0.DocNum, t1.LineNum


'''


SQL_A031 =  f'''

	
With	T1 AS (
							SELECT
								V0.ItemCode,
								V0.WhsCode,
								SUM( V0.Quantity ) AS 'WarehouseLockedQuantity' 
							FROM
								ETL_VI_WAREHOUSELOCKEDDETAIL V0 
							GROUP BY
								V0.ItemCode,
								V0.WhsCode 
								),							
								
			T0 as (select OITW.OnOrder,OITW.OnHand,OITW.ItemCode,OITW.WhsCode FROM 	OITW  LEFT JOIN  T1 ON OITW.ItemCode = T1.ItemCode AND OITW.WhsCode = T1.WhsCode 						
							WHERE  ISNULL( OITW.OnHand, 0 ) > 0 	OR ISNULL( OITW.OnOrder, 0 ) <> 0	OR ISNULL( T1.WarehouseLockedQuantity, 0 ) > 0
							),
			N as ( SELECT dbo.ETL_FN_GetAddonConfig('RPT_001') as a1, dbo.ETL_FN_GetAddonConfig('RPT_002') as a2),
			ttt2 as (select  U_ProductType,U_Brand,U_Category,U_Subcategory,U_LineMF,ItemCode,U_OldItemNo,CodeBars,ItemName from OITM WHERE ItemCode in (SELECT distinct ItemCode from T0)),
			tttlt as (select Price,itemcode,pricelist from 	ITM1 WHERE ItemCode in (SELECT distinct ItemCode from T0)),
			ttt5 as (select Price,itemcode from tttlt WHERE	 pricelist = (select top 1 a1 from N)),
			ttt6 as (select Price,itemcode from 	ITM1 WHERE	pricelist = (select top 1 a2 from N))

SELECT
	 (SELECT top 1 PrintHeadr FROM OADM)	AS '公司',
	ttt2.U_ProductType AS '品类代码',
	ttt2.U_Brand AS '品牌代码',
	ttt7.U_BrandChiName AS '品牌名称',
	ttt8.U_Agent AS '品牌状态',
	ttt2.U_Category AS '类别',
	ttt2.U_Subcategory AS '子类别',
	ttt2.U_LineMF AS 'POS中类',
	ttt2.ItemCode AS 'SAP货号',
	ttt2.U_OldItemNo AS '原来货号',
	ttt2.CodeBars AS '条码',
	ttt2.ItemName AS '产品描述',
	ttt5.Price AS '中国零售价',
	ttt6.Price AS 'POSM价格',
	ttt3.Street AS '仓储名称',
	ttt9.Location AS '库区名称',
	ttt3.WhsCode AS '仓库代码',
	ttt3.WhsName AS '仓库名称',
	ttt3.[U_AreaCode] AS '归属地区',
	ISNULL( T0.OnHand, 0 ) AS '存货量',
	ISNULL( T1.WarehouseLockedQuantity, 0 ) AS '锁定库存量',
	T0.OnOrder AS '已订购',
	ISNULL( T0.OnHand, 0 ) - ISNULL( T1.WarehouseLockedQuantity, 0 ) AS '可用量' 
FROM
	T0
	LEFT JOIN  T1 ON T0.ItemCode = T1.ItemCode 		AND T0.WhsCode = T1.WhsCode	
	LEFT JOIN  ttt2 ON ttt2.ItemCode = T0.ItemCode
	LEFT JOIN [dbo].[OWHS] ttt3 ON ttt3.WhsCode = T0.WhsCode
	LEFT JOIN  ttt5 ON ttt5.itemcode = ttt2.itemcode
	LEFT JOIN  ttt6 ON ttt6.itemcode = ttt2.itemcode
	LEFT JOIN [dbo].[@BRANDCODE] ttt7 ON ttt7.Code = ttt2.U_Brand
	LEFT JOIN [dbo].[@BRANDPRICE] ttt8 ON ttt8.U_BPType = ttt2.U_ProductType AND ttt8.U_BPBrand = ttt2.U_Brand
	LEFT JOIN [dbo].[OLCT] ttt9 ON ttt9.Code = ttt3.Location
WHERE
	isnull( ttt3.U_AreaCode, '' ) <> '其他'



'''



SQL_A081 =  f'''

DECLARE @FromDate DATETIME
SELECT @FromDate = '{dsm}'
-- '2020-05-01'

DECLARE @ToDate DATETIME
SELECT @ToDate = '{dtt}'

DECLARE @GroupName NVARCHAR(20)
SELECT @GroupName = N''

-----------

SELECT
  (SELECT a0.PrintHeadr
   FROM OADM a0)                                                                                AS '公司',
  tt0.[单据类型],
  S1.Name                                                                                       AS '销售类型',
  tt0.DocNum                                                                                    AS '单号',
  tt0.NumAtCard                                                                                 AS '客户参考编号',
  tt0.DocDate                                                                                   AS '单据日期',
  tt0.Comments                                                                                  AS '备注',
  tt16.FAX                                                                                      AS '渠道类型',
  tt16.U_REGION                                                                                 AS '大区',
  tt16.U_AREA                                                                                   AS '区域',
  tt16.U_PLACE                                                                                  AS '省&直辖市',
  tt17.SlpName                                                                                  AS '销售员',
  tt18.GroupName                                                                                AS '客户组',
  tt0.CardCode                                                                                  AS '客户代码',
  tt9.OcrName                                                                                   AS '客户名称',
  tt0.ShipToCode                                                                                AS 'KA门店名称',
  CASE tt12.U_CounterType
  WHEN '1' THEN '常规柜台'
  WHEN '2' THEN '临时柜台'
  WHEN '3' THEN '特卖柜台'
  WHEN '4' THEN '大型推广'
  WHEN '5' THEN '中型推广'
  WHEN '6' THEN '小型推广'
  ELSE '无' END                                                                                  AS '柜台类型',
  tt0.U_COUNTER                                                                                 AS '柜台号',
  tt12.U_Description                                                                            AS '柜台名称',
  tt8.U_NAME                                                                                    AS '制单人',
  tt3.U_ChiName                                                                                    '品类',
  tt1.U_Subcategory                                                                                '子分类',
  CASE WHEN tt4.U_BrandChiName IS NULL THEN tt4.[Name]
  ELSE tt4.U_BrandChiName END                                                                   AS '品牌',
  CASE WHEN tt4.U_BrandChiName IS NULL THEN tt4.[Name]
  ELSE tt4.U_BrandChiName END + tt3.U_ChiName + CASE WHEN tt1.U_SkincareCat = 'SALON' THEN '-院装'
                                                WHEN tt1.U_SkincareCat = 'RETAIL' THEN '-客装'
                                                ELSE '' END                                     AS '核算项目',
  tt5.OcrName                                                                                   AS '地区',
  tt15.OcrName                                                                                  AS '销售方式',
  tt11.WhsName                                                                                  AS '仓库名称',
  tt1.U_Category                                                                                AS '类别代码',
  tt1.U_LineMF                                                                                  AS '产品中类',
  tt1.ItemCode                                                                                  AS 'SAP货号',
  tt1.U_OldItemNo                                                                               AS '原来货号',
  CASE WHEN isnull(tt0.ItemName,'') = '' THEN tt1.ItemName
  ELSE tt0.ItemName END                                                                         AS '产品名称',
  isnull(tt0.Qty,0.0)                                                                           AS '数量',
  CASE WHEN isnull(tt0.Qty,0.0) * isnull(tt0.U_OriPrice,tt7.Price) = 0.0 THEN 1.0
  ELSE 1 - (tt0.GTotal / (isnull(tt0.Qty,0.0) * isnull(tt0.U_OriPrice,tt7.Price))) END          AS '折扣',
  isnull(tt0.U_OriPrice,tt7.Price)                                                              AS '零售单价',
  isnull(tt0.Qty,0.0) * isnull(tt0.U_OriPrice,tt7.Price)                                        AS '零售金额',
  tt0.GTotal                                                                                    AS '结算金额',
  
	
	dbo.ETL_FN_GetCounterDiscount(tt0.U_COUNTER,tt0.DocDate)                             AS '柜台商场折扣',
  tt0.GTotal * (1 - ISNULL(dbo.ETL_FN_GetCounterDiscount(tt0.U_COUNTER,tt0.DocDate) ,0)) AS '应开票金额',
  tt0.SalesType                                                                        AS '销售备注'
FROM [dbo].[A081](@FromDate,@ToDate) tt0 
LEFT JOIN [dbo].[OITM] tt1 ON tt1.ItemCode = tt0.ItemCode
LEFT JOIN [dbo].[ITM1] tt7 ON tt7.ItemCode = tt0.ItemCode AND tt7.PriceList = (SELECT a0.U_Value
                                                                               FROM [dbo].[@ADDON_CFG] a0
                                                                               WHERE a0.Code = 'RPT_001')
LEFT JOIN [dbo].[ITM1] tt13 ON tt13.ItemCode = tt0.ItemCode AND tt13.PriceList = (SELECT a0.U_Value
                                                                                  FROM [dbo].[@ADDON_CFG] a0
                                                                                  WHERE a0.Code = 'RPT_003')
LEFT JOIN [dbo].[@PRODUCTTYPE] tt3 ON tt3.Code = tt1.U_ProductType
LEFT JOIN [dbo].[@BRANDCODE] tt4 ON tt4.Code = tt1.U_Brand
LEFT JOIN [dbo].[@SALESCAT] s1 ON S1.Code = tt0.U_SalesCat
LEFT JOIN [dbo].[OOCR] tt5 ON tt5.OcrCode = tt0.OcrCode4
LEFT JOIN [dbo].[OOCR] tt6 ON tt6.OcrCode = tt0.OcrCode5
LEFT JOIN [dbo].[OUSR] tt8 ON tt8.[internal_k] = tt0.[UserSign]
LEFT JOIN [dbo].[OOCR] tt9 ON tt9.OcrCode = tt0.OcrCode3
LEFT JOIN [dbo].[CRD1] tt10 ON tt10.CardCode = tt0.CardCode AND tt10.Address = tt0.ShipToCode AND tt10.AdresType = 'S'
LEFT JOIN OWHS tt11 ON tt11.WhsCode = tt0.WhsCode
LEFT JOIN [@COUNTER] tt12 ON tt0.U_COUNTER  =tt12.Code
LEFT JOIN [dbo].[OOCR] tt15 ON tt15.OcrCode = tt0.OcrCode5
LEFT JOIN [dbo].[OCRD] tt16 ON tt16.CardCode = tt0.CardCode
LEFT JOIN [dbo].[OSLP] tt17 ON tt17.slpcode = tt0.slpcode
LEFT JOIN [dbo].[OCRG] tt18 ON tt18.GroupCode = tt16.GroupCode
WHERE (tt18.GroupName = @GroupName OR @GroupName = '') AND (CASE WHEN tt1.U_ProductType = 'OP' AND tt1.U_Category IN (N'FG',N'SE',N'AC') THEN 1
                                                            WHEN tt1.U_ProductType <> 'OP' AND tt1.U_Category IN (N'FG',N'SE') THEN 1
                                                            ELSE 2 END) = 1


'''



SQL_A091 =  f'''
DECLARE @FromDate DATETIME
SELECT @FromDate = '{dsm}'
-- '2020-05-01'

DECLARE @ToDate DATETIME
SELECT @ToDate = '{dtt}'


SELECT
(SELECT a0.PrintHeadr
   FROM OADM a0)      AS '公司',
  tt0.[单据类型],
  tt0.[SalesType]     AS '销售方式',
  tt0.DocDate         AS '单据日期',
  tt0.DocNum          AS '单据编号',
  tt0.CardCode        AS '客户代码',
  tt0.CardName        AS '客户名称',
  tt0.U_COUNTER       AS '柜台号',
  tt12.U_Description  AS '柜台名称',
  tt0.NumAtCard       AS '参考编号',
  tt0.Comments        AS '单据注释',
  tt2.U_NAME          AS '制单人',
  tt3.OcrName         AS '部门',
  tt1.U_ProductType   AS '品类代码',
  tt1.U_Brand         AS '品牌代码',
  tt5.WhsName         AS '仓库名称',
  tt0.ItemCode        AS 'SAP货号',
  tt1.U_OldItemNo     AS '原来货号',
  tt1.ItemName        AS 'SAP名称',tt0.ChinaRetailPrice AS '中国零售价',
  tt4.Price           AS 'POSM价格',
  tt0.Qty             AS '数量',
  tt0.GTotal          AS '行总计(含税)',
  tt4.Price * tt0.Qty AS '合计金额'
FROM [dbo].[A081](@FromDate,@ToDate) tt0
INNER JOIN OITM tt1 ON tt1.ItemCode = tt0.ItemCode
LEFT JOIN OUSR tt2 ON tt2.INTERNAL_K = tt0.UserSign
LEFT JOIN OOCR tt3 ON tt3.OcrCode = tt0.OcrCode4
INNER JOIN ITM1 tt4 ON tt4.ItemCode = tt0.ItemCode AND tt4.PriceList = (SELECT a0.U_Value
                                                                        FROM [dbo].[@ADDON_CFG] a0
                                                                        WHERE a0.Code = 'RPT_002')
LEFT JOIN OWHS tt5 ON tt5.WhsCode = tt0.WhsCode
LEFT JOIN [dbo].[@COUNTER] tt12 ON tt12.[Name] = tt0.U_COUNTER
WHERE tt1.U_Category NOT IN (N'FG',N'SE')

'''

SQL_A034 =  f'''
DECLARE @FromDate DATETIME
SELECT @FromDate = '{dsm}'
-- '2020-05-01'

DECLARE @ToDate DATETIME
SELECT @ToDate = '{dtt}'

SELECT (SELECT a0.PrintHeadr FROM OADM a0) AS '公司',
       tt0.LocCode AS '仓库代码',
       tt2.WhsName AS '仓库名称',
       tt1.U_ProductType AS '品类代码',
       tt1.U_Brand AS '品牌代码',
       dbo.ETL_FN_GetAccountingProject(tt0.ItemCode) AS '核算项目',
       tt1.U_Category AS '类别代码',
       tt0.ItemCode AS 'SAP货号',
       tt1.U_OldItemNo AS '原来货号',
       tt1.ItemName AS '产品描述',
       tt3.Avgprice AS "成本价",
       tt4.Price AS '中国零售价',
       tt5.Price AS 'POSM价格',
       tt0.BGQty AS '期初数量',
       tt0.BGQty * (CASE WHEN tt1.U_Category = 'FG' THEN tt4.Price ELSE tt5.Price END) AS '期初金额',
       tt0.[采购收货],
       tt0.[采购退货],
       tt0.[销售交货],
       tt0.[销售退货],
       tt0.[库存收货],
       tt0.[库存发货],
       tt0.[库存调拨],
       tt0.ENDQty AS '期末数量',
       tt0.ENDQty * (CASE WHEN tt1.U_Category = 'FG' THEN tt4.Price ELSE tt5.Price END) AS '期末金额',
       isnull(tt6.LockQty, 0.0) AS '期末锁定量',
       isnull(tt7.Quantity, 0.0) AS '期末在途量',
       tt0.ENDQty - isnull(tt6.LockQty, 0.0) AS '期末锁定可用量',
       (tt0.ENDQty - isnull(tt6.LockQty, 0.0)) *
       (CASE WHEN tt1.U_Category = 'FG' THEN tt4.Price ELSE tt5.Price END) AS '期末锁定可用金额',
       tt0.ENDQty - isnull(tt6.LockQty, 0.0) + isnull(tt7.Quantity, 0.0) AS '期末锁定可用量(含在途)',
       (tt0.ENDQty - isnull(tt6.LockQty, 0.0) + isnull(tt7.Quantity, 0.0)) *
       isnull(tt4.Price, tt5.Price) AS '期末锁定可用金额(含在途)'
FROM (SELECT t0.ItemCode,
             t0.LocCode,
             sum(CASE WHEN t0.DocDate < @FromDate THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS BGQty,
             sum(CASE WHEN t0.DocDate >= @FromDate AND t0.DocDate <= @ToDate AND t0.TransType = '15'
                           THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS '销售交货',
             sum(CASE WHEN t0.DocDate >= @FromDate AND t0.DocDate <= @ToDate AND t0.TransType = '16'
                           THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS '销售退货',
             sum(CASE WHEN t0.DocDate >= @FromDate AND t0.DocDate <= @ToDate AND t0.TransType = '20'
                           THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS '采购收货',
             sum(CASE WHEN t0.DocDate >= @FromDate AND t0.DocDate <= @ToDate AND t0.TransType = '21'
                           THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS '采购退货',
             sum(CASE WHEN t0.DocDate >= @FromDate AND t0.DocDate <= @ToDate AND t0.TransType = '59'
                           THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS '库存收货',
             sum(CASE WHEN t0.DocDate >= @FromDate AND t0.DocDate <= @ToDate AND t0.TransType = '60'
                           THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS '库存发货',
             sum(CASE WHEN t0.DocDate >= @FromDate AND t0.DocDate <= @ToDate AND t0.TransType = '67'
                           THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS '库存调拨',
             sum(CASE WHEN t0.DocDate <= @ToDate THEN t0.InQty - t0.OutQty ELSE 0.0 END) AS ENDQty
      FROM [dbo].[OIVL] t0
      WHERE t0.InQty - t0.OutQty <> 0
      GROUP BY t0.ItemCode, t0.LocCode) tt0
INNER JOIN [dbo].[OITM] tt1 ON tt1.ItemCode = tt0.ItemCode
INNER JOIN [dbo].[OWHS] tt2 ON tt2.WhsCode = tt0.LocCode
INNER JOIN [dbo].[OITW] tt3 ON tt3.WhsCode = tt0.LocCode AND tt3.ItemCode = tt0.ItemCode
LEFT JOIN [dbo].[ITM1] tt4 ON tt4.ItemCode = tt0.ItemCode AND  tt4.PriceList = (SELECT a0.U_Value FROM [dbo].[@ADDON_CFG] a0 WHERE a0.Code = 'RPT_001')
LEFT JOIN [dbo].[ITM1] tt5 ON tt5.ItemCode = tt0.ItemCode AND  tt5.PriceList = (SELECT a0.U_Value FROM [dbo].[@ADDON_CFG] a0 WHERE a0.Code = 'RPT_002')
LEFT JOIN (SELECT tt0.ItemCode,
                  tt1.WhsCode,
                  sum(isnull(tt0.Qty1, 0.0) + isnull(tt0.Qty2, 0.0) + isnull(tt0.Qty3, 0.0) + isnull(tt0.Qty4, 0.0) +                      isnull(tt0.Qty5, 0.0) + isnull(tt0.Qty6, 0.0)) AS LockQty
           FROM (                                           --草稿单据（已审批通过+已发送审批）
                SELECT t1.ItemCode,
                       t1.WhsCode,
                       t1.Quantity AS Qty1,
                       NULL AS Qty2,
                       NULL AS Qty3,
                       NULL AS Qty4,
                       NULL AS Qty5,
                       NULL AS Qty6
                FROM ODRF t0
                INNER JOIN [dbo].[DRF1] t1 ON t1.DocEntry = t0.DocEntry
                INNER JOIN [dbo].[OWDD] t2 ON t2.DocEntry = t0.DocEntry
                WHERE t2.IsDraft = 'Y' AND t0.WddStatus NOT IN('N', 'C') AND t0.ObjType = '17' AND t0.DocDate <= @ToDate
                UNION ALL --正式销售单据
                SELECT t1.ItemCode,
                       t1.WhsCode,
                       NULL AS Qty1,
                       t1.OpenQty AS Qty2,
                       NULL AS Qty3,
                       NULL AS Qty4,
                       NULL AS Qty5,
                       NULL AS Qty6
                FROM [dbo].[ORDR] t0
                INNER JOIN [dbo].[RDR1] t1 ON t1.DocEntry = t0.DocEntry
                WHERE t1.LineStatus = 'O' AND t0.DocDate <= @ToDate
                UNION ALL --采购退货草稿
                SELECT t1.ItemCode,
                       t1.WhsCode,
                       NULL AS Qty1,
                       NULL AS Qty2,
                       t1.Quantity AS Qty3,
                       NULL AS Qty4,
                       NULL AS Qty5,
                       NULL AS Qty6
                FROM [dbo].[ODRF] t0
                INNER JOIN [dbo].[DRF1] t1 ON t1.DocEntry = t0.DocEntry
                WHERE t0.ObjType = '21' AND t0.DocStatus = 'O' AND t0.DocDate <= @ToDate
                UNION ALL --库存发货草稿
                SELECT t1.ItemCode,
                       t1.WhsCode,
                       NULL AS Qty1,
                       NULL AS Qty2,
                       NULL AS Qty3,
                       t1.Quantity AS Qty4,
                       NULL AS Qty5,
                       NULL AS Qty6
                FROM [dbo].[ODRF] t0
                INNER JOIN [dbo].[DRF1] t1 ON t1.DocEntry = t0.DocEntry
                WHERE t0.ObjType = '60' AND t0.DocStatus = 'O' AND t0.DocDate <= @ToDate
                UNION ALL --库存转储申请正式单据
                SELECT t1.ItemCode,
                       t0.Filler AS WhsCode,
                       NULL AS Qty1,
                       NULL AS Qty2,
                       NULL AS Qty3,
                       NULL AS Qty4,
                       t1.Quantity - isnull(t2.Quantity, 0.0) AS Qty5,
                       NULL AS Qty6
                FROM [dbo].[OWTQ] t0
                INNER JOIN [dbo].[WTQ1] t1 ON t1.DocEntry = t0.DocEntry
                LEFT JOIN (SELECT a1.ItemCode,
                                  a1.BaseEntry,
                                  a1.BaseLine,
                                  sum(a1.Quantity) AS Quantity
                           FROM [dbo].[owtr] a0
                           INNER JOIN [dbo].[WTR1] a1 ON a1.DocEntry = a0.DocEntry
                           GROUP BY a1.ItemCode, a1.BaseEntry, a1.BaseLine) t2                         ON t2.ItemCode = t1.ItemCode AND t2.BaseEntry = t1.DocEntry AND t2.BaseLine = t1.LineNum
                WHERE t0.DocStatus = 'O' AND t0.DocDate <= @ToDate
                UNION ALL --生产订单-标准
                SELECT t1.ItemCode,
                       t1.U_ActWHCode AS WhsCode,
                       NULL AS Qty1,
                       NULL AS Qty2,
                       NULL AS Qty3,
                       NULL AS Qty4,
                       NULL AS Qty5,
                       CASE WHEN t1.PlannedQty - t1.IssuedQty < 0.0 THEN 0.0 ELSE t1.PlannedQty - t1.IssuedQty                           END AS Qty6
                FROM [dbo].[OWOR] t0
                INNER JOIN [dbo].[WOR1] t1 ON t1.DocEntry = t0.DocEntry
                WHERE t0.Status = 'R' AND t0.[Type] = N'S' AND t0.PostDate <= @ToDate
                UNION ALL --生产订单-拆分
                SELECT t0.ItemCode,
                       t0.Warehouse AS WhsCode,
                       NULL AS Qty1,
                       NULL AS Qty2,
                       NULL AS Qty3,
                       NULL AS Qty4,
                       NULL AS Qty5,
                       CASE WHEN t0.PlannedQty - isnull(t2.Quantity, 0.0) < 0.0 THEN 0.0
                            ELSE t0.PlannedQty - isnull(t2.Quantity, 0.0) END AS Qty6
                FROM [dbo].[OWOR] t0
                INNER JOIN [dbo].[WOR1] t1 ON t1.DocEntry = t0.DocEntry
                LEFT JOIN (SELECT a1.ItemCode,
                                  a1.BaseRef,
                                  sum(a1.Quantity) AS Quantity
                           FROM [dbo].[IGE1] a1
                           GROUP BY a1.ItemCode, a1.BaseRef) t2 ON t2.ItemCode = t0.ItemCode AND t2.BaseRef = t0.DocNum
                WHERE t0.Status = 'R' AND t0.[Type] = N'D' AND t0.PostDate <= @ToDate) tt0
           INNER JOIN [dbo].[OITW] tt1 ON tt1.ItemCode = tt0.ItemCode AND tt1.WhsCode = tt0.WhsCode
           INNER JOIN [dbo].[OITM] tt2 ON tt2.ItemCode = tt1.ItemCode
           GROUP BY tt0.ItemCode,
                    tt1.WhsCode,
                    tt1.OnHand,
                    tt2.U_OldItemNo,
                    tt2.ItemName) tt6 ON tt6.ItemCode = tt0.ItemCode AND tt6.WhsCode = tt0.LocCode
LEFT JOIN (SELECT t1.ItemCode,
                  t1.WhsCode,
                  sum(t1.Quantity - isnull(t2.Quantity, 0.0)) AS Quantity
           FROM [dbo].[OPOR] t0
           INNER JOIN [dbo].[POR1] t1 ON t1.DocEntry = t0.DocEntry
           LEFT JOIN (SELECT a1.ItemCode,
                             a1.BaseEntry,
                             a1.BaseLine,
                             a1.Quantity
                      FROM [dbo].[OPDN] a0
                      INNER JOIN [dbo].[PDN1] a1 ON a1.DocEntry = a0.DocEntry
                      WHERE a0.DocDate <= @ToDate) t2
                    ON t2.ItemCode = t1.ItemCode AND t2.BaseEntry = t1.DocEntry AND t2.BaseLine = t1.LineNum
           WHERE t0.DocDate <= @ToDate AND t1.LineStatus = 'O' AND t1.Quantity - isnull(t2.Quantity, 0.0) > 0.0
           GROUP BY t1.ItemCode, t1.WhsCode) tt7 ON tt7.ItemCode = tt0.ItemCode AND tt7.WhsCode = tt0.LocCode
ORDER BY tt0.LocCode, tt0.ItemCode

'''


SQL_A101 =  f'''
SET NOCOUNT ON;SET FMTONLY OFF;
DECLARE @De varchar(30)
set @De='{dtt}'

SELECT DB_NAME () AS "B1Database",	*,	@De AS "QueryDate" FROM	ETL_FN_A101 ( @De )

'''

SQL_A102 =  '''
SELECT   (SELECT a0.PrintHeadr
          FROM OADM a0) AS '公司'
         ,t3.WhsName AS '仓库名称'
         , t2.U_Category AS '类别'
         , t2.U_Brand AS '品牌'
         , t2.U_ProductType AS '品类'
         , t2.ItemCode AS 'SAP货号'
         , t2.U_OldItemNo AS '原来货号'
         , t2.ItemName AS '产品描述'
         , t5.Price AS '中国零售价'
         , t6.Price AS 'POSM价'
         , sum(t0.Quantity) AS '总数量'
         , sum(CASE WHEN t1.ExpDate IS NULL THEN t0.Quantity ELSE 0.0 END) AS '效期空'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 0 THEN t0.Quantity ELSE 0.0 END) AS '过期'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 90 AND datediff(d, getdate(), t1.ExpDate) > 0 THEN t0.Quantity ELSE 0.0 END) AS '0~3个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 180 AND datediff(d, getdate(), t1.ExpDate) > 90 THEN t0.Quantity ELSE 0.0 END) AS '3~6个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 270 AND datediff(d, getdate(), t1.ExpDate) > 180 THEN t0.Quantity ELSE 0.0 END) AS '6~9个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 360 AND datediff(d, getdate(), t1.ExpDate) > 270 THEN t0.Quantity ELSE 0.0 END) AS '9~12个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 450 AND datediff(d, getdate(), t1.ExpDate) > 360 THEN t0.Quantity ELSE 0.0 END) AS '12~15个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 540 AND datediff(d, getdate(), t1.ExpDate) > 450 THEN t0.Quantity ELSE 0.0 END) AS '15~18个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 630 AND datediff(d, getdate(), t1.ExpDate) > 540 THEN t0.Quantity ELSE 0.0 END) AS '18~21个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 720 AND datediff(d, getdate(), t1.ExpDate) > 630 THEN t0.Quantity ELSE 0.0 END) AS '21~24个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 810 AND datediff(d, getdate(), t1.ExpDate) > 720 THEN t0.Quantity ELSE 0.0 END) AS '25~27个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) <= 900 AND datediff(d, getdate(), t1.ExpDate) > 810 THEN t0.Quantity ELSE 0.0 END) AS '27~30个月'
         , sum(CASE WHEN datediff(d, getdate(), t1.ExpDate) > 900 THEN t0.Quantity ELSE 0.0 END) AS '大于30个月'
FROM     [dbo].[OBTQ] t0
         INNER JOIN [dbo].[OBTN] t1 ON t1.AbsEntry = t0.MdAbsEntry AND t1.ItemCode = t0.ItemCode
         INNER JOIN [dbo].[OITM] t2 ON t2.ItemCode = t0.ItemCode
         INNER JOIN [dbo].[OWHS] t3 ON t3.WhsCode = t0.WhsCode
         INNER JOIN [dbo].[@BRANDCODE] t4 ON t4.Code = t2.U_Brand
         INNER JOIN [dbo].[ITM1] t5 ON t5.ItemCode = t0.ItemCode AND t5.PriceList = N'2'
         INNER JOIN [dbo].[ITM1] t6 ON t6.ItemCode = t0.ItemCode AND t6.PriceList = N'11'
WHERE    t0.Quantity > 0.0 AND t2.U_Category = 'FG' AND t3.U_AreaCode <> '其他'
GROUP BY t3.WhsName, t2.U_Category, t2.U_Brand, t2.U_ProductType, t2.ItemCode, t5.Price, t6.Price, t2.U_OldItemNo, t2.ItemName

'''




##以下是合并成list--------------------------------------------------------------------------------------------------------------------

Jobs=[  [SQL_A042,'_Month1st_A042'],[SQL_A031,'_Month1st_A031']
       ,[SQL_A081,'_Month1st_A081'],[SQL_A091,'_Month1st_A091']
       ,[SQL_A034,'_Month1st_A034'],[SQL_A101,'_Month1st_A101']
       ,[SQL_A102,'_Month1st_A102']

]



#for job in Jobs:
#   print ('任务取数SQL'+job[0]+'\r\n'+'任务目标excel:'+job[1])
#

#多个JOBS用List处理；
#Jobs=[[SQL_A031,'_Month1st_A031'],[SQL_A031,'_Month1st_A032']
#
#]