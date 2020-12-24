# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\arc_r\multivariate_regression.py
# Compiled at: 2006-04-26 00:05:48
__doc__ = '\nArcRstats.py (version 0.5, 2005-06-13) - multivariate modeling script for ArcGIS\n\nThis script can be used with ArcGIS to produce predictive maps based on\ndifferent techniques using the free and robust R statistical package:\n    Generalized Linear Model (GLM)\n    Generalized Additive Model (GAM)\n    Classification and Regression Tree (CART)    \n\nThis script can be used within the ESRI ModelBuilder environment.  A basic script interface\nis included in the ArcRstats.tbx which can be viewed and used from ArcCatalog.  Dragging the\nrespective toolbox script (GLM, GAM or CART) into a new model allows you to connect the input\npoints and rasters as well as defining the output prediction raster and sampling tables.\nExample data and model runs are included in the toolbox, which you can run by simply pressing\nthe play button.\n\nModels are inherently flawed.  You are strongly advised to research the strengths and\nweaknesses of these different techniques as well as understanding their outputs, neither of\nwhich are explained with this tool.  The help for each of the R commands should be consulted.\nSee the out_mdl.r file (where out_mdl is the name of your output prediction raster) to re-create\nthe R session and try help(glm), help(gam) or help(rpart) after loading the necessary package,\nwhich is library(mgcv) for GAM and library(rpart) for CART.  Also look at the help for the\npredict.glm, predict.gam and predict.rpart functions.  A good habitat modeling review paper for\nmore background on these modeling techniques is:\n\n  Guisan, A., and N.E. Zimmermann. 2000, Predictive Habitat Distribution Models in Ecology: Ecol. Mod. 135 147-186.\n\nInputs / Outputs:\n    in_absence - any point feature class\n    in_presence - any point feature class\n    in_rasters - on or more rasters\n    out_mdl - output predicted raster\n\nRequires:\n    ArcGIS version 9 or higher (http://www.esri.com)\n        + Spatial Analyst extension\n    R version 2 or higher (http://www.r-project.org)\n        + COM(D) Server for R (http://cran.r-project.org/contrib/extra/dcom)\n    Python 2.1 or higher (http://www.python.org), included with ArcGIS 9 or higher\n        + win32com module (http://starship.python.net/crew/mhammond)\n\nTerm of Use:\n  This program is public domain under the GNU General Public License (www.gnu.org/copyleft/gpl.html).\n  We provide this software with absolutely no warranty.  If you use this, please cite with the following:\n\n    Best, B. D., S. Loarie, S. Qian, P. Halpin, D. Urban, 2005.  ArcRstats - multivariate habitat modeling with ArcGIS and R statistical software.\n      Available at http://www.nicholas.duke.edu/geospatial/software.\n\nAuthors:\n    Ben Best <bbest at duke dot edu>\n    Scott Loarie <srl6 at duke dot edu>\n    Song Qian <song at duke dot edu>\n    Patrick Halpin <phalpin at duke dot edu>\n    Dean Urban <deanu at duke dot edu>\n    \n    Duke University Geospatial Analysis Program\n    http://www.nicholas.duke.edu/geospatial\n\nVersions :\n    0.7 (2006-04-23):\n        - fixed factor(obs) for CART and logit function for GLM/GAM\n    0.6 (2005-08-02):\n        - fixed factor(obs) for CART and logit function for GLM/GAM\n    0.5 (2005-06-13):\n        - fixed for use with long path names by converting to short path names (especially for gp.Describe BUG)\n        - updated GLM to handle NAs more efficiently\n    0.4 (2005-05-23):\n        - updated terms of use with citation\n    0.3 (2005-05-19):\n        - fixed bug during GAM formula creation\n        - created basic help pdf doc\n    0.2 (2005-05-08):\n        - fixed projection of model output grid\n        - changed from tempfile grid output to *.asc\n        - cleaned up large variables from memory\n        - validated _Example models so output not already generated in ModelBuilder\n        - supplemented documentation\n    0.0.1 (2005-05-04):\n        - first beta version\n\nTODO : error check for ArcGIS, ArcGIS Spatial Analyst, R, and RCOM Server\nTODO : when feeding data to predict in R, remove unused coefficients from data frame (since NAs are excluded)\nTODO : check in_absence/presence for raster or point locations, not just "dataset"\nTODO : check for autodelete if exists in gp environment\nTODO : add ROC to GLM/GAM...\nTODO : work on other basic statistical tests, like T-tests, Moran\'s I stuff\nTODO : failover R, launch R and capture real error using the R package "session"\nTODO : check raster name length when creating reprojected (*_r) and integer (*_i) rasters\nTODO : handle big grids with map algebra statement for GLM and CART\nTODO : output error/deviance grids too\nTODO : setup listserve for sending updates to users\nTODO: write-up explanation for example dataset\n'
from win32com.client import Dispatch
import os, sys, re, time, shutil
debug = 0
if debug:
    fxn = 'glm'
    prefix = 'D:/projects/ArcRstats/'
    in_obs = prefix + 'sp_obs.shp'
    in_rnd = prefix + 'sp_rnd.shp'
    in_rnames = ['dem', 'aspect', 'tci', 'landcov']
    sep = ';' + prefix
    in_rasters = prefix + sep.join(in_rnames)
    out_mdl = prefix + 'out_' + fxn
    out_tbl_obs = out_mdl + '_smpl_obs.dbf'
    out_tbl_rnd = out_mdl + '_smpl_rnd.dbf'

class RModel:
    __module__ = __name__

    def __init__(self):
        pass

    def msg(self, msg):
        self.gp.AddMessage(msg)
        print msg
        self.rlog.write('# %s\n' % msg)

    def rcmd(self, cmd):
        try:
            self.r.EvaluateNoReturn(cmd)
        except:
            self.msg('Unexpected error with R command...\n' + str(cmd) + '\n' + str(self.r.GetErrorText()) + '\n' + str(sys.exc_info()[0]))
            raise

        self.rlog.write(cmd + '\n')

    def initialize(self):
        global fxn
        global in_obs
        global in_rasters
        global in_rnd
        global out_mdl
        global out_tbl_obs
        global out_tbl_rnd
        self.fxn = fxn
        if debug:
            self.in_obs = in_obs
            self.in_rnd = in_rnd
            self.in_rasters = in_rasters
            self.out_mdl = out_mdl
            self.out_tbl_obs = out_tbl_obs
            self.out_tbl_rnd = out_tbl_rnd
        else:
            for i in range(0, len(sys.argv)):
                if isinstance(sys.argv[i], str):
                    sys.argv[i] = sys.argv[i].replace('\\', '/')

            self.in_obs = sys.argv[2]
            self.in_rnd = sys.argv[3]
            self.in_rasters = sys.argv[4]
            self.out_mdl = sys.argv[5]
            self.out_tbl_obs = sys.argv[6]
            self.out_tbl_rnd = sys.argv[7]
        self.cwd = os.path.dirname(self.out_mdl)
        self.samplesfile = self.out_mdl + '_samples.txt'
        self.rlogfile = self.out_mdl + '_log.r'
        self.rlog = open(self.rlogfile, 'w')
        self.rlog.write('# ' + self.fxn.upper() + ' started on ' + time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime()) + '\n')
        self.gp = Dispatch('esriGeoprocessing.GpDispatch.1')
        self.gp.CheckOutExtension('Spatial')
        self.gp.OverwriteOutput = 1
        self.r = Dispatch('StatConnectorSrv.StatConnector')
        self.r.Init('R')
        self.msg('  setup variables...')
        self.rasters = {}
        self.samples = {}
        self.samples['obs'] = []
        for path in self.in_rasters.split(';'):
            path = path.replace("'", '')
            name = os.path.basename(path)
            self.rasters[name] = path
            self.samples[name] = []

    def sample2r(self):
        self.msg('  sample rasters...')
        try:
            self.gp.Sample_sa((';').join(self.rasters.values()), self.in_obs, self.out_tbl_obs, 'NEAREST')
            self.gp.Sample_sa((';').join(self.rasters.values()), self.in_rnd, self.out_tbl_rnd, 'NEAREST')
        except:
            print 'ERROR: ' + self.gp.GetMessages()

        self.msg('  read in sampled presence tables...')
        rows = self.gp.SearchCursor(self.out_tbl_obs)
        row = rows.Next()
        while row:
            self.samples['obs'].append('present')
            for col in self.rasters.keys():
                self.samples[col].append(row.GetValue(col))

            row = rows.Next()

        self.msg('  read in sampled absence/random tables...')
        rows = self.gp.SearchCursor(self.out_tbl_rnd)
        row = rows.Next()
        while row:
            self.samples['obs'].append('absent')
            for col in self.rasters.keys():
                self.samples[col].append(row.GetValue(col))

            row = rows.Next()

        f = open(self.samplesfile, 'w')
        for i in range(len(self.samples['obs'])):
            rowdata = []
            for k in self.samples.keys():
                if i == 0:
                    rowdata.append(str(k))
                else:
                    v = str(self.samples[k][i])
                    rowdata.append(v)

            sep = ','
            f.write(sep.join(rowdata) + '\n')

        f.close()
        self.rcmd('dat <- read.table("' + self.samplesfile + '", header=TRUE, sep = ",", na.strings = "-9999.0")')
        del self.samples

    def grids2r(self):
        self.msg('  feed grid data to R for predicting with model...')
        cellwidth = 0
        self.cellsizes = {}
        self.extents = {}
        self.sprefs = {}
        for (n, p) in self.rasters.items():
            descr = self.gp.Describe(p)
            self.cellsizes[n] = str(descr.MeanCellWidth)
            self.extents[n] = str(descr.Extent)
            self.sprefs[n] = descr.SpatialReference
            if descr.MeanCellWidth > cellwidth:
                self.template = n

        self.msg('    template grid with largest cell size: ' + n)
        self.gp.Workspace = self.cwd
        self.gp.OutputCoordinateSystem = self.sprefs[self.template]
        self.gp.Extent = self.extents[self.template]
        self.msg('    resample other grids, if different cellsize/extent from template...')
        for (n, p) in self.rasters.items():
            if self.cellsizes[n] != self.cellsizes[self.template] or self.extents[n] != self.extents[self.template]:
                try:
                    if self.gp.Exists(p + '_r'):
                        self.gp.Delete(p + '_r')
                    self.gp.Resample(p, p + '_r', self.cellsizes[self.template], 'NEAREST')
                except:
                    print self.gp.GetMessages()
                else:
                    self.rasters[n] = p + '_r'

        self.msg('    output grids to temporary ASCII files and read into R...')
        self.rasters_asc = self.rasters.copy()
        for (n, p) in self.rasters.items():
            p_asc = p + '.asc'
            self.rasters_asc[n] = p_asc
            try:
                self.gp.RasterToASCII_conversion(p, p_asc)
            except:
                self.msg(self.gp.GetMessages())

            self.rcmd(n + ' <- read.table("' + self.rasters_asc[n].replace('\\', '/') + '", sep=" ", na.strings="-9999", skip=6)')
            self.rcmd(n + ' <- as.vector(data.matrix(' + n + '[-length(' + n + ')]))')
            self.header = {}
            if n == self.template:
                f = open(self.rasters_asc[n], 'r')
                self.header['ncols'] = re.match('([\\S]+)\\s+([\\S]+)', f.readline()).groups()[1]
                self.header['nrows'] = re.match('([\\S]+)\\s+([\\S]+)', f.readline()).groups()[1]
                self.header['xllcorner'] = re.match('([\\S]+)\\s+([\\S]+)', f.readline()).groups()[1]
                self.header['yllcorner'] = re.match('([\\S]+)\\s+([\\S]+)', f.readline()).groups()[1]
                self.header['cellsize'] = re.match('([\\S]+)\\s+([\\S]+)', f.readline()).groups()[1]
                self.header['NODATA_value'] = re.match('([\\S]+)\\s+([\\S]+)', f.readline()).groups()[1]
                f.close()

        self.out_mdl_ascii = self.out_mdl + '.asc'
        f = open(self.out_mdl_ascii, 'w')
        for (k, v) in self.header.items():
            f.write('%s %s\n' % (k, v))

        f.close()
        sep = ', '
        self.rcmd('datpred <- data.frame(cbind(' + sep.join(self.rasters.keys()) + '))')
        for n in self.rasters.keys():
            self.rcmd('rm(' + n + ')')

    def pred2gis(self):
        self.msg('  convert model prediction to grid...')
        self.rcmd('write.table(pred, file="' + self.out_mdl_ascii.replace('\\', '/') + '", append=TRUE, sep=" ", col.names=FALSE, row.names=FALSE, na="-9999")')
        try:
            if self.gp.Exists(self.out_mdl):
                self.gp.Delete(self.out_mdl)
            self.gp.ASCIIToRaster_conversion(self.out_mdl_ascii, self.out_mdl, 'FLOAT')
            self.gp.Toolbox = 'Management'
        except:
            print self.gp.GetMessages()

        prj = self.rasters[self.template] + '/prj.adf'
        if os.path.exists(prj):
            shutil.copyfile(prj, self.out_mdl + '/prj.adf')

    def plotsamples(self):
        self.rcmd('plotpre <- "' + self.out_mdl.replace('\\', '/') + '"')
        self.rcmd('datenv <- dat[,names(dat)!="obs"]')
        self.rcmd('png(paste(sep=, plotpre, "_plotpairs.png"))')
        self.rcmd('pairs(datenv, main="Correlations Between Variables")')
        self.rcmd('dev.off()')
        self.rcmd('for (c in names(datenv)){\n                        denspres <- density(na.exclude(dat[dat[["obs"]]==1, c]))\n                        densabs  <- density(na.exclude(dat[dat[["obs"]]==0, c]))\n                        xlim <- range(na.exclude(dat[, c]))\n                        ylim <- c(0,max(c(denspres$y, densabs$y)))\n                        #png(filename=filename, width=600, height=400, pointsize=1, bg="white", res=200)\n                        png(paste(sep=\'\', plotpre, \'_hist_\', c, \'.png\'))\n                        plot(denspres, type=\'l\', main=paste(c,\'Distribution\'), xlab=c, ylab=\'Density\', ylim=ylim, xlim=xlim)\n                        lines(densabs, lty=2)\n                        legend(x=xlim[1], y=ylim[2], legend=c(\'presence\', \'absence\'), lty=1:2)\n                        dev.off()\n                    }')

    def finalize(self):
        self.r.Close()
        self.rlog.close()
        del self.gp


class GLM(RModel):
    __module__ = __name__

    def __init__(self):
        self.initialize()
        self.sample2r()
        self.plotsamples()
        self.msg('  generate GLM in R...')
        self.rcmd('dat$obs <- factor(dat$obs)')
        self.rcmd('dat <- na.exclude(dat)')
        self.rcmd('mdlall <- glm(obs ~ ., data=dat, family=binomial(link="logit"))')
        self.msg('  find best GLM model by AIC...')
        self.rcmd('library(MASS)')
        self.rcmd('mdl <- stepAIC(mdlall, trace=F)')
        self.rcmd('sink("' + self.out_mdl.replace('\\', '/') + '_summary.txt")')
        self.rcmd('cat("\nGLM all..\n\n")')
        self.rcmd('print(summary(mdlall))')
        self.rcmd('cat("\nGLM best model, with step-wise AIC selection of coefficients...\n\n")')
        self.rcmd('print(summary(mdl))')
        self.rcmd('sink()')
        self.grids2r()
        self.msg('  predict GLM in R...')
        self.rcmd('pred <- predict(mdl, newdata=datpred, na.action=na.pass, type="response")')
        self.rcmd('dim(pred) <- c(' + self.header['nrows'] + ', ' + self.header['ncols'] + ')')
        self.rcmd('save(dat, mdlall, mdl, datpred, pred, file = "' + self.out_mdl.replace('\\', '/') + '.rdata")')
        self.pred2gis()
        self.finalize()


class GLM2(RModel):
    __module__ = __name__

    def __init__(self):
        self.initialize()
        self.sample2r()
        self.msg('  generate GLM in R...')
        self.rcmd('dat$obs <- factor(dat$obs)')
        self.rcmd('dat <- na.exclude(dat)')
        self.rcmd('mdlall <- glm(obs ~ ., data=dat, family=binomial(link="logit"))')
        self.msg('  find best GLM model by AIC...')
        self.rcmd('library(MASS)')
        self.rcmd('mdl <- stepAIC(mdlall, trace=F)')
        self.rcmd('sink("' + self.out_mdl + '_summary.txt")')
        self.rcmd('cat("\nGLM all..\n\n")')
        self.rcmd('print(summary(mdlall))')
        self.rcmd('cat("\nGLM best model, with step-wise AIC selection of coefficients...\n\n")')
        self.rcmd('print(summary(mdl))')
        self.rcmd('sink()')
        self.msg('  extract GLM coefficients from R...')
        coeffs = {}
        coeffs_d = self.r.Evaluate('summary(mdl)$coefficients')
        coeffs_r = self.r.Evaluate('rownames(summary(mdl)$coefficients)')
        coeffs_c = self.r.Evaluate('colnames(summary(mdl)$coefficients)')
        for i in range(0, len(coeffs_r)):
            coeffs[coeffs_r[i]] = dict([ (coeffs_c[j], coeffs_d[i][j]) for j in range(0, len(coeffs_c)) ])

        in_rasters = []
        expression = []
        for r in coeffs.keys():
            if r == '(Intercept)':
                expression.append(str(coeffs[r]['Estimate']))
            else:
                expression.append('(' + str(coeffs[r]['Estimate']) + ' * ' + self.rasters[r] + ')')

        in_expression = (' + ').join(expression)
        try:
            self.gp.SingleOutputMapAlgebra_sa(in_expression, self.out_mdl)
        except:
            print 'ERROR: ' + self.gp.GetMessages()

        self.rcmd('save(file="' + self.out_mdl + '.rdata")')


class GAM(RModel):
    __module__ = __name__

    def __init__(self):
        self.initialize()
        self.sample2r()
        self.plotsamples()
        self.msg('  generate GAM formula...')
        terms = []
        for k in self.rasters.keys():
            terms.append('s(' + k + ', bs="ts")')

        sep = ' + '
        formula = 'obs ~ ' + sep.join(terms)
        self.msg('  generate GAM in R...')
        self.rcmd('dat$obs <- factor(dat$obs)')
        self.rcmd('library(mgcv)')
        self.rcmd('mdl <- gam(' + formula + ', data=dat, family=binomial(link="logit"))')
        self.rcmd('sink("' + self.out_mdl.replace('\\', '/') + '_summary.txt")')
        self.rcmd('cat("\nGAM..\n\n")')
        self.rcmd('print(summary(mdl))')
        self.rcmd('sink()')
        self.rcmd('png("' + self.out_mdl.replace('\\', '/') + '_plot.png")')
        self.rcmd('plot(mdl,pages=1,residuals=TRUE,all.terms=TRUE,shade=TRUE,shade.col="gray")')
        self.rcmd('dev.off()')
        self.grids2r()
        self.msg('  predict with GAM in R...')
        self.rcmd('rowsna <- sort(unique(which(is.na(datpred), arr.ind=TRUE)[,1]))')
        self.rcmd('datpred <- na.exclude(datpred)')
        self.rcmd('pred <- predict(mdl, newdata=datpred, type="response", block.size=0.5, newdata.guaranteed=FALSE)')
        self.rcmd('for (row in rowsna){\n                        pred <- append(pred, NA, row-1)\n                    }')
        self.rcmd('dim(pred) <- c(' + self.header['nrows'] + ', ' + self.header['ncols'] + ')')
        self.rcmd('save(dat, mdl, datpred, pred, file = "' + self.out_mdl.replace('\\', '/') + '.rdata")')
        self.pred2gis()
        self.finalize()


class CART(RModel):
    __module__ = __name__

    def __init__(self):
        self.initialize()
        self.sample2r()
        self.plotsamples()
        self.msg('  generate CART in R...')
        self.rcmd('dat$obs <- factor(dat$obs)')
        self.rcmd('library(rpart)')
        self.rcmd('mdlall <- rpart(obs ~ ., data=dat, control=rpart.control(cp=0), method="class")')
        self.rcmd('mdlall.cp <- mdlall$cptable[mdlall$cptable[,4] == min(mdlall$cptable[,4]), 1]')
        self.msg('  trim CART (complexity parameter with minimum cross-validation error)...')
        self.rcmd('mdl <- rpart(obs ~ ., data=dat, control=rpart.control(cp=mdlall.cp), na.action=na.pass, method="class")')
        self.msg('  plot CART tree from R...')
        self.rcmd('png("' + self.out_mdl.replace('\\', '/') + '_tree.png")')
        self.rcmd('plot(mdl)')
        self.rcmd('text(mdl, use.n=TRUE)')
        self.rcmd('dev.off()')
        self.rcmd('sink("' + self.out_mdl.replace('\\', '/') + '_summary.txt")')
        self.rcmd('cat("\nFull CART (cp=0)...\n\n")')
        self.rcmd('print(summary(mdlall))')
        self.rcmd('cat("\n\nModified CART (using",str(mdlall.cp),"as complexity parameter from Full CART)...\n\n")')
        self.rcmd('print(summary(mdl))')
        self.rcmd('sink()')
        self.grids2r()
        self.msg('  predict CART in R...')
        self.rcmd('pred <- predict(mdl, newdata=datpred, na.action=na.pass, type="prob")[,2]')
        self.rcmd('dim(pred) <- c(' + self.header['nrows'] + ', ' + self.header['ncols'] + ')')
        self.rcmd('save(dat, mdl, datpred, pred, file = "' + self.out_mdl.replace('\\', '/') + '.rdata")')
        self.pred2gis()
        self.finalize()


class CART2(RModel):
    __module__ = __name__

    def __init__(self):
        self.initialize()
        self.rcmd('dat <- read.table("' + self.samplesfile + '", header=TRUE, sep = ",", na.strings = "-9999.0")')
        self.msg('  generate CART in R...')
        self.rcmd('library(rpart)')
        self.rcmd('mdl <- rpart(obs ~ ., data=dat, method="class")')
        self.rcmd('inodes = rownames(mdl$frame[mdl$frame$var=="<leaf>",])')
        self.rcmd('lnodes = length(inodes)')
        self.rcmd('paths = path.rpart(mdl, inodes, print.it=F)')
        self.rcmd('formulas = character(lnodes)')
        self.r.SetSymbol('raster.names', self.rasters.keys())
        self.r.SetSymbol('raster.paths', self.rasters.values())
        self.rcmd('for (i in 1:lnodes){\n                        ps = paths[[i]][-1]\n                        for (j in 1:length(ps)){\n                            for (k in 1:length(raster.names)){\n                                ps[j] = sub(raster.names[k],raster.paths[k], ps[j])\n                            }\n                        }\n                        formulas[i] = paste(ps, collapse=" & ")\n                      }')
        formulas = self.r.Evaluate('formulas')
        algebra = ''
        for i in range(0, len(formulas)):
            f = formulas[i]
            algebra += 'con(' + f + ',' + str(i + 1) + ','

        algebra += '0' + ')' * len(formulas)
        try:
            self.gp.SingleOutputMapAlgebra_sa(algebra, self.out_mdl)
        except:
            print 'ERROR: ' + self.gp.GetMessages()


if __name__ == '__main__':
    if not debug:
        fxn = sys.argv[1]
    if fxn == 'glm':
        GLM()
    elif fxn == 'glm2':
        GLM2()
    elif fxn == 'gam':
        GAM()
    elif fxn == 'cart':
        CART()
    elif fxn == 'cart2':
        CART2()