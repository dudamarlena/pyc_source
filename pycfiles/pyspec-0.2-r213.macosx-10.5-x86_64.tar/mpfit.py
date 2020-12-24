# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/EPD64.framework/Versions/7.0/lib/python2.7/site-packages/pyspec/mpfit.py
# Compiled at: 2011-02-13 14:08:59
"""
Perform Levenberg-Marquardt least-squares minimization, based on MINPACK-1.

                                                                   AUTHORS
  The original version of this software, called LMFIT, was written in FORTRAN
  as part of the MINPACK-1 package by XXX.

  Craig Markwardt converted the FORTRAN code to IDL.  The information for the
  IDL version is:
         Craig B. Markwardt, NASA/GSFC Code 662, Greenbelt, MD 20770
         craigm@lheamail.gsfc.nasa.gov
         UPDATED VERSIONs can be found on my WEB PAGE:
                http://cow.physics.wisc.edu/~craigm/idl/idl.html
        
  Mark Rivers created this Python version from Craig's IDL version.
        Mark Rivers, University of Chicago
        Building 434A, Argonne National Laboratory
        9700 South Cass Avenue, Argonne, IL 60439
        rivers@cars.uchicago.edu
        Updated versions can be found at http://cars.uchicago.edu/software
 
 Sergey Koposov converted the Mark's Python version from Numeric to numpy
        Sergey Koposov, Max Planck Institute for Astronomy
        Heidelberg, Germany, D-69117
        koposov@mpia.de
        Updated versions can be found at http://code.google.com/p/astrolibpy/source/browse/trunk/

                                                                 DESCRIPTION

 MPFIT uses the Levenberg-Marquardt technique to solve the
 least-squares problem.  In its typical use, MPFIT will be used to
 fit a user-supplied function (the "model") to user-supplied data
 points (the "data") by adjusting a set of parameters.  MPFIT is
 based upon MINPACK-1 (LMDIF.F) by More' and collaborators.

 For example, a researcher may think that a set of observed data
 points is best modelled with a Gaussian curve.  A Gaussian curve is
 parameterized by its mean, standard deviation and normalization.
 MPFIT will, within certain constraints, find the set of parameters
 which best fits the data.  The fit is "best" in the least-squares
 sense; that is, the sum of the weighted squared differences between
 the model and data is minimized.

 The Levenberg-Marquardt technique is a particular strategy for
 iteratively searching for the best fit.  This particular
 implementation is drawn from MINPACK-1 (see NETLIB), and is much faster
 and more accurate than the version provided in the Scientific Python package
 in Scientific.Functions.LeastSquares.
 This version allows upper and lower bounding constraints to be placed on each
 parameter, or the parameter can be held fixed.

 The user-supplied Python function should return an array of weighted
 deviations between model and data.  In a typical scientific problem
 the residuals should be weighted so that each deviate has a
 gaussian sigma of 1.0.  If X represents values of the independent
 variable, Y represents a measurement for each value of X, and ERR
 represents the error in the measurements, then the deviates could
 be calculated as follows:

   DEVIATES = (Y - F(X)) / ERR

 where F is the analytical function representing the model.  You are
 recommended to use the convenience functions MPFITFUN and
 MPFITEXPR, which are driver functions that calculate the deviates
 for you.  If ERR are the 1-sigma uncertainties in Y, then

   TOTAL( DEVIATES^2 )

 will be the total chi-squared value.  MPFIT will minimize the
 chi-square value.  The values of X, Y and ERR are passed through
 MPFIT to the user-supplied function via the FUNCTKW keyword.

 Simple constraints can be placed on parameter values by using the
 PARINFO keyword to MPFIT.  See below for a description of this
 keyword.

 MPFIT does not perform more general optimization tasks.  See TNMIN
 instead.  MPFIT is customized, based on MINPACK-1, to the
 least-squares minimization problem.

                                                           USER FUNCTION

 The user must define a function which returns the appropriate
 values as specified above.  The function should return the weighted
 deviations between the model and the data.  It should also return a status
 flag and an optional partial derivative array.  For applications which
 use finite-difference derivatives -- the default -- the user
 function should be declared in the following way:

   def myfunct(p, fjac=None, x=None, y=None, err=None)
        # Parameter values are passed in "p"
        # If fjac==None then partial derivatives should not be
        # computed.  It will always be None if MPFIT is called with default
        # flag.
        model = F(x, p)
        # Non-negative status value means MPFIT should continue, negative means
        # stop the calculation.
        status = 0
        return([status, (y-model)/err]

 See below for applications with analytical derivatives.

 The keyword parameters X, Y, and ERR in the example above are
 suggestive but not required.  Any parameters can be passed to
 MYFUNCT by using the functkw keyword to MPFIT.  Use MPFITFUN and
 MPFITEXPR if you need ideas on how to do that.  The function *must*
 accept a parameter list, P.

 In general there are no restrictions on the number of dimensions in
 X, Y or ERR.  However the deviates *must* be returned in a
 one-dimensional Numeric array of type Float.

 User functions may also indicate a fatal error condition using the
 status return described above. If status is set to a number between
 -15 and -1 then MPFIT will stop the calculation and return to the caller.

                                                        ANALYTIC DERIVATIVES

 In the search for the best-fit solution, MPFIT by default
 calculates derivatives numerically via a finite difference
 approximation.  The user-supplied function need not calculate the
 derivatives explicitly.  However, if you desire to compute them
 analytically, then the AUTODERIVATIVE=0 keyword must be passed to MPFIT.
 As a practical matter, it is often sufficient and even faster to allow
 MPFIT to calculate the derivatives numerically, and so
 AUTODERIVATIVE=0 is not necessary.

 If AUTODERIVATIVE=0 is used then the user function must check the parameter
 FJAC, and if FJAC!=None then return the partial derivative array in the
 return list.
   def myfunct(p, fjac=None, x=None, y=None, err=None)
        # Parameter values are passed in "p"
        # If FJAC!=None then partial derivatives must be comptuer.
        # FJAC contains an array of len(p), where each entry
        # is 1 if that parameter is free and 0 if it is fixed.
        model = F(x, p)
        Non-negative status value means MPFIT should continue, negative means
        # stop the calculation.
        status = 0
        if (dojac):
           pderiv = zeros([len(x), len(p)], Float)
           for j in range(len(p)):
                 pderiv[:,j] = FGRAD(x, p, j)
        else:
           pderiv = None
        return([status, (y-model)/err, pderiv]

 where FGRAD(x, p, i) is a user function which must compute the
 derivative of the model with respect to parameter P[i] at X.  When
 finite differencing is used for computing derivatives (ie, when
 AUTODERIVATIVE=1), or when MPFIT needs only the errors but not the
 derivatives the parameter FJAC=None.

 Derivatives should be returned in the PDERIV array. PDERIV should be an m x
 n array, where m is the number of data points and n is the number
 of parameters.  dp[i,j] is the derivative at the ith point with
 respect to the jth parameter.

 The derivatives with respect to fixed parameters are ignored; zero
 is an appropriate value to insert for those derivatives.  Upon
 input to the user function, FJAC is set to a vector with the same
 length as P, with a value of 1 for a parameter which is free, and a
 value of zero for a parameter which is fixed (and hence no
 derivative needs to be calculated).

 If the data is higher than one dimensional, then the *last*
 dimension should be the parameter dimension.  Example: fitting a
 50x50 image, "dp" should be 50x50xNPAR.

                   CONSTRAINING PARAMETER VALUES WITH THE PARINFO KEYWORD

 The behavior of MPFIT can be modified with respect to each
 parameter to be fitted.  A parameter value can be fixed; simple
 boundary constraints can be imposed; limitations on the parameter
 changes can be imposed; properties of the automatic derivative can
 be modified; and parameters can be tied to one another.

 These properties are governed by the PARINFO structure, which is
 passed as a keyword parameter to MPFIT.

 PARINFO should be a list of dictionaries, one list entry for each parameter.
 Each parameter is associated with one element of the array, in
 numerical order.  The dictionary can have the following keys
 (none are required, keys are case insensitive):

        'value' - the starting parameter value (but see the START_PARAMS
                         parameter for more information).

        'fixed' - a boolean value, whether the parameter is to be held
                         fixed or not.  Fixed parameters are not varied by
                         MPFIT, but are passed on to MYFUNCT for evaluation.

        'limited' - a two-element boolean array.  If the first/second
                           element is set, then the parameter is bounded on the
                           lower/upper side.  A parameter can be bounded on both
                           sides.  Both LIMITED and LIMITS must be given
                           together.

        'limits' - a two-element float array.  Gives the
                          parameter limits on the lower and upper sides,
                          respectively.  Zero, one or two of these values can be
                          set, depending on the values of LIMITED.  Both LIMITED
                          and LIMITS must be given together.

        'parname' - a string, giving the name of the parameter.  The
                           fitting code of MPFIT does not use this tag in any
                           way.  However, the default iterfunct will print the
                           parameter name if available.

        'step' - the step size to be used in calculating the numerical
                        derivatives.  If set to zero, then the step size is
                        computed automatically.  Ignored when AUTODERIVATIVE=0.

        'mpside' - the sidedness of the finite difference when computing
                          numerical derivatives.  This field can take four
                          values:

                                 0 - one-sided derivative computed automatically
                                 1 - one-sided derivative (f(x+h) - f(x)  )/h
                                -1 - one-sided derivative (f(x)   - f(x-h))/h
                                 2 - two-sided derivative (f(x+h) - f(x-h))/(2*h)

                         Where H is the STEP parameter described above.  The
                         "automatic" one-sided derivative method will chose a
                         direction for the finite difference which does not
                         violate any constraints.  The other methods do not
                         perform this check.  The two-sided method is in
                         principle more precise, but requires twice as many
                         function evaluations.  Default: 0.

        'mpmaxstep' - the maximum change to be made in the parameter
                                 value.  During the fitting process, the parameter
                                 will never be changed by more than this value in
                                 one iteration.

                                 A value of 0 indicates no maximum.  Default: 0.

        'tied' - a string expression which "ties" the parameter to other
                        free or fixed parameters.  Any expression involving
                        constants and the parameter array P are permitted.
                        Example: if parameter 2 is always to be twice parameter
                        1 then use the following: parinfo(2).tied = '2 * p(1)'.
                        Since they are totally constrained, tied parameters are
                        considered to be fixed; no errors are computed for them.
                        [ NOTE: the PARNAME can't be used in expressions. ]

        'mpprint' - if set to 1, then the default iterfunct will print the
                           parameter value.  If set to 0, the parameter value
                           will not be printed.  This tag can be used to
                           selectively print only a few parameter values out of
                           many.  Default: 1 (all parameters printed)

 Future modifications to the PARINFO structure, if any, will involve
 adding dictionary tags beginning with the two letters "MP".
 Therefore programmers are urged to avoid using tags starting with
 the same letters; otherwise they are free to include their own
 fields within the PARINFO structure, and they will be ignored.

 PARINFO Example:
 parinfo = [{'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]} 
                                                                                                for i in range(5)]
 parinfo[0]['fixed'] = 1
 parinfo[4]['limited'][0] = 1
 parinfo[4]['limits'][0]  = 50.
 values = [5.7, 2.2, 500., 1.5, 2000.]
 for i in range(5): parinfo[i]['value']=values[i]

 A total of 5 parameters, with starting values of 5.7,
 2.2, 500, 1.5, and 2000 are given.  The first parameter
 is fixed at a value of 5.7, and the last parameter is
 constrained to be above 50.

                                                                   EXAMPLE

   import mpfit
   import numpy.oldnumeric as Numeric
   x = arange(100, float)
   p0 = [5.7, 2.2, 500., 1.5, 2000.]
   y = ( p[0] + p[1]*[x] + p[2]*[x**2] + p[3]*sqrt(x) +
                 p[4]*log(x))
   fa = {'x':x, 'y':y, 'err':err}
   m = mpfit('myfunct', p0, functkw=fa)
   print 'status = ', m.status
   if (m.status <= 0): print 'error message = ', m.errmsg
   print 'parameters = ', m.params

   Minimizes sum of squares of MYFUNCT.  MYFUNCT is called with the X,
   Y, and ERR keyword parameters that are given by FUNCTKW.  The
   results can be obtained from the returned object m.

                                                        THEORY OF OPERATION

   There are many specific strategies for function minimization.  One
   very popular technique is to use function gradient information to
   realize the local structure of the function.  Near a local minimum
   the function value can be taylor expanded about x0 as follows:

          f(x) = f(x0) + f'(x0) . (x-x0) + (1/2) (x-x0) . f''(x0) . (x-x0)
                         -----   ---------------   -------------------------------  (1)
         Order  0th               1st                                     2nd

   Here f'(x) is the gradient vector of f at x, and f''(x) is the
   Hessian matrix of second derivatives of f at x.  The vector x is
   the set of function parameters, not the measured data vector.  One
   can find the minimum of f, f(xm) using Newton's method, and
   arrives at the following linear equation:

          f''(x0) . (xm-x0) = - f'(x0)                                                  (2)

   If an inverse can be found for f''(x0) then one can solve for
   (xm-x0), the step vector from the current position x0 to the new
   projected minimum.  Here the problem has been linearized (ie, the
   gradient information is known to first order).  f''(x0) is
   symmetric n x n matrix, and should be positive definite.

   The Levenberg - Marquardt technique is a variation on this theme.
   It adds an additional diagonal term to the equation which may aid the
   convergence properties:

          (f''(x0) + nu I) . (xm-x0) = -f'(x0)                            (2a)

   where I is the identity matrix.  When nu is large, the overall
   matrix is diagonally dominant, and the iterations follow steepest
   descent.  When nu is small, the iterations are quadratically
   convergent.

   In principle, if f''(x0) and f'(x0) are known then xm-x0 can be
   determined.  However the Hessian matrix is often difficult or
   impossible to compute.  The gradient f'(x0) may be easier to
   compute, if even by finite difference techniques.  So-called
   quasi-Newton techniques attempt to successively estimate f''(x0)
   by building up gradient information as the iterations proceed.

   In the least squares problem there are further simplifications
   which assist in solving eqn (2).  The function to be minimized is
   a sum of squares:

           f = Sum(hi^2)                                                                                 (3)

   where hi is the ith residual out of m residuals as described
   above.  This can be substituted back into eqn (2) after computing
   the derivatives:

           f'  = 2 Sum(hi  hi')
           f'' = 2 Sum(hi' hj') + 2 Sum(hi hi'')                                (4)

   If one assumes that the parameters are already close enough to a
   minimum, then one typically finds that the second term in f'' is
   negligible [or, in any case, is too difficult to compute].  Thus,
   equation (2) can be solved, at least approximately, using only
   gradient information.

   In matrix notation, the combination of eqns (2) and (4) becomes:

                hT' . h' . dx = - hT' . h                                                 (5)

   Where h is the residual vector (length m), hT is its transpose, h'
   is the Jacobian matrix (dimensions n x m), and dx is (xm-x0).  The
   user function supplies the residual vector h, and in some cases h'
   when it is not found by finite differences (see MPFIT_FDJAC2,
   which finds h and hT').  Even if dx is not the best absolute step
   to take, it does provide a good estimate of the best *direction*,
   so often a line minimization will occur along the dx vector
   direction.

   The method of solution employed by MINPACK is to form the Q . R
   factorization of h', where Q is an orthogonal matrix such that QT .
   Q = I, and R is upper right triangular.  Using h' = Q . R and the
   ortogonality of Q, eqn (5) becomes

                (RT . QT) . (Q . R) . dx = - (RT . QT) . h
                                         RT . R . dx = - RT . QT . h             (6)
                                                  R . dx = - QT . h

   where the last statement follows because R is upper triangular.
   Here, R, QT and h are known so this is a matter of solving for dx.
   The routine MPFIT_QRFAC provides the QR factorization of h, with
   pivoting, and MPFIT_QRSOLV provides the solution for dx.

                                                                 REFERENCES

   MINPACK-1, Jorge More', available from netlib (www.netlib.org).
   "Optimization Software Guide," Jorge More' and Stephen Wright,
         SIAM, *Frontiers in Applied Mathematics*, Number 14.
   More', Jorge J., "The Levenberg-Marquardt Algorithm:
         Implementation and Theory," in *Numerical Analysis*, ed. Watson,
         G. A., Lecture Notes in Mathematics 630, Springer-Verlag, 1977.

                                                   MODIFICATION HISTORY

   Translated from MINPACK-1 in FORTRAN, Apr-Jul 1998, CM
 Copyright (C) 1997-2002, Craig Markwardt
 This software is provided as is without any warranty whatsoever.
 Permission to use, copy, modify, and distribute modified or
 unmodified copies is granted, provided this copyright and disclaimer
 are included unchanged.

   Translated from MPFIT (Craig Markwardt's IDL package) to Python,
   August, 2002.  Mark Rivers
   Converted from Numeric to numpy (Sergey Koposov, July 2008)
"""
import numpy, types, scipy.lib.blas

class mpfit():
    statusNiceText = {0: 'Improper input parameters', 1: 'GOOD FIT : Both actual and predicted relative reductions in the sum of squares are at most ftol', 
       2: 'Relative error between two consecutive iterates is at most xtol', 
       3: 'Errors 1 and 2', 
       4: 'The cosine of the angle between fvec and any column of the jacobian is at most gtol in absolute value.', 
       5: 'The maximum number of iterations has been reached', 
       6: 'ftol is too small. No further reduction in the sum of squares is possible.', 
       7: 'xtol is too small. No further improvement in the approximate solution x is possible.', 
       8: 'gtol is too small. fvec is orthogonal to the columns of the jacobian to machine percision.'}
    blas_enorm, = scipy.lib.blas.get_blas_funcs(['nrm2'])

    def __init__(self, fcn, xall=None, functkw={}, parinfo=None, ftol=1e-10, xtol=1e-10, gtol=1e-10, damp=0.0, maxiter=200, factor=100.0, nprint=1, iterfunct='default', iterkw={}, nocovar=0, rescale=0, autoderivative=1, quiet=0, diag=None, epsfcn=None, debug=0):
        """
  Inputs:
        fcn:
           The function to be minimized.  The function should return the weighted
           deviations between the model and the data, as described above.

        xall:
           An array of starting values for each of the parameters of the model.
           The number of parameters should be fewer than the number of measurements.

           This parameter is optional if the parinfo keyword is used (but see
           parinfo).  The parinfo keyword provides a mechanism to fix or constrain
           individual parameters.

  Keywords:

         autoderivative:
                If this is set, derivatives of the function will be computed
                automatically via a finite differencing procedure.  If not set, then
                fcn must provide the (analytical) derivatives.
                   Default: set (=1)
                   NOTE: to supply your own analytical derivatives,
                                 explicitly pass autoderivative=0

         ftol:
                A nonnegative input variable. Termination occurs when both the actual
                and predicted relative reductions in the sum of squares are at most
                ftol (and status is accordingly set to 1 or 3).  Therefore, ftol
                measures the relative error desired in the sum of squares.
                   Default: 1E-10

         functkw:
                A dictionary which contains the parameters to be passed to the
                user-supplied function specified by fcn via the standard Python
                keyword dictionary mechanism.  This is the way you can pass additional
                data to your user-supplied function without using global variables.

                Consider the following example:
                   if functkw = {'xval':[1.,2.,3.], 'yval':[1.,4.,9.],
                                                 'errval':[1.,1.,1.] }
                then the user supplied function should be declared like this:
                   def myfunct(p, fjac=None, xval=None, yval=None, errval=None):

                Default: {}   No extra parameters are passed to the user-supplied
                                          function.

         gtol:
                A nonnegative input variable. Termination occurs when the cosine of
                the angle between fvec and any column of the jacobian is at most gtol
                in absolute value (and status is accordingly set to 4). Therefore,
                gtol measures the orthogonality desired between the function vector
                and the columns of the jacobian.
                   Default: 1e-10

         iterkw:
                The keyword arguments to be passed to iterfunct via the dictionary
                keyword mechanism.  This should be a dictionary and is similar in
                operation to FUNCTKW.
                   Default: {}  No arguments are passed.

         iterfunct:
                The name of a function to be called upon each NPRINT iteration of the
                MPFIT routine.  It should be declared in the following way:
                   def iterfunct(myfunct, p, iter, fnorm, functkw=None,
                                                 parinfo=None, quiet=0, dof=None, [iterkw keywords here])
                   # perform custom iteration update

                iterfunct must accept all three keyword parameters (FUNCTKW, PARINFO
                and QUIET).

                myfunct:  The user-supplied function to be minimized,
                p:              The current set of model parameters
                iter:    The iteration number
                functkw:  The arguments to be passed to myfunct.
                fnorm:  The chi-squared value.
                quiet:  Set when no textual output should be printed.
                dof:      The number of degrees of freedom, normally the number of points
                                  less the number of free parameters.
                See below for documentation of parinfo.

                In implementation, iterfunct can perform updates to the terminal or
                graphical user interface, to provide feedback while the fit proceeds.
                If the fit is to be stopped for any reason, then iterfunct should return a
                a status value between -15 and -1.  Otherwise it should return None
                (e.g. no return statement) or 0.
                In principle, iterfunct should probably not modify the parameter values,
                because it may interfere with the algorithm's stability.  In practice it
                is allowed.

                Default: an internal routine is used to print the parameter values.

                Set iterfunct=None if there is no user-defined routine and you don't
                want the internal default routine be called.

         maxiter:
                The maximum number of iterations to perform.  If the number is exceeded,
                then the status value is set to 5 and MPFIT returns.
                Default: 200 iterations

         nocovar:
                Set this keyword to prevent the calculation of the covariance matrix
                before returning (see COVAR)
                Default: clear (=0)  The covariance matrix is returned

         nprint:
                The frequency with which iterfunct is called.  A value of 1 indicates
                that iterfunct is called with every iteration, while 2 indicates every
                other iteration, etc.  Note that several Levenberg-Marquardt attempts
                can be made in a single iteration.
                Default value: 1

         parinfo
                Provides a mechanism for more sophisticated constraints to be placed on
                parameter values.  When parinfo is not passed, then it is assumed that
                all parameters are free and unconstrained.  Values in parinfo are never
                modified during a call to MPFIT.

                See description above for the structure of PARINFO.

                Default value: None  All parameters are free and unconstrained.

         quiet:
                Set this keyword when no textual output should be printed by MPFIT

         damp:
                A scalar number, indicating the cut-off value of residuals where
                "damping" will occur.  Residuals with magnitudes greater than this
                number will be replaced by their hyperbolic tangent.  This partially
                mitigates the so-called large residual problem inherent in
                least-squares solvers (as for the test problem CURVI,
                http://www.maxthis.com/curviex.htm).
                A value of 0 indicates no damping.
                   Default: 0

                Note: DAMP doesn't work with autoderivative=0

         xtol:
                A nonnegative input variable. Termination occurs when the relative error
                between two consecutive iterates is at most xtol (and status is
                accordingly set to 2 or 3).  Therefore, xtol measures the relative error
                desired in the approximate solution.
                Default: 1E-10

   Outputs:

         Returns an object of type mpfit.  The results are attributes of this class,
         e.g. mpfit.status, mpfit.errmsg, mpfit.params, npfit.niter, mpfit.covar.

         .status
                An integer status code is returned.  All values greater than zero can
                represent success (however .status == 5 may indicate failure to
                converge). It can have one of the following values:

                -16
                   A parameter or function value has become infinite or an undefined
                   number.  This is usually a consequence of numerical overflow in the
                   user's model function, which must be avoided.

                -15 to -1
                   These are error codes that either MYFUNCT or iterfunct may return to
                   terminate the fitting process.  Values from -15 to -1 are reserved
                   for the user functions and will not clash with MPFIT.

                0  Improper input parameters.

                1  Both actual and predicted relative reductions in the sum of squares
                   are at most ftol.

                2  Relative error between two consecutive iterates is at most xtol

                3  Conditions for status = 1 and status = 2 both hold.

                4  The cosine of the angle between fvec and any column of the jacobian
                   is at most gtol in absolute value.

                5  The maximum number of iterations has been reached.

                6  ftol is too small. No further reduction in the sum of squares is
                   possible.

                7  xtol is too small. No further improvement in the approximate solution
                   x is possible.

                8  gtol is too small. fvec is orthogonal to the columns of the jacobian
                   to machine precision.

         .fnorm
                The value of the summed squared residuals for the returned parameter
                values.

         .covar
                The covariance matrix for the set of parameters returned by MPFIT.
                The matrix is NxN where N is the number of  parameters.  The square root
                of the diagonal elements gives the formal 1-sigma statistical errors on
                the parameters if errors were treated "properly" in fcn.
                Parameter errors are also returned in .perror.

                To compute the correlation matrix, pcor, use this example:
                   cov = mpfit.covar
                   pcor = cov * 0.
                   for i in range(n):
                          for j in range(n):
                                 pcor[i,j] = cov[i,j]/sqrt(cov[i,i]*cov[j,j])

                If nocovar is set or MPFIT terminated abnormally, then .covar is set to
                a scalar with value None.

         .errmsg
                A string error or warning message is returned.

         .nfev
                The number of calls to MYFUNCT performed.

         .niter
                The number of iterations completed.

         .perror
                The formal 1-sigma errors in each parameter, computed from the
                covariance matrix.  If a parameter is held fixed, or if it touches a
                boundary, then the error is reported as zero.

                If the fit is unweighted (i.e. no errors were given, or the weights
                were uniformly set to unity), then .perror will probably not represent
                the true parameter uncertainties.

                *If* you can assume that the true reduced chi-squared value is unity --
                meaning that the fit is implicitly assumed to be of good quality --
                then the estimated parameter uncertainties can be computed by scaling
                .perror by the measured chi-squared value.

                   dof = len(x) - len(mpfit.params) # deg of freedom
                   # scaled uncertainties
                   pcerror = mpfit.perror * sqrt(mpfit.fnorm / dof)

                """
        self.niter = 0
        self.params = None
        self.covar = None
        self.perror = None
        self.status = 0
        self.debug = debug
        self.errmsg = ''
        self.nfev = 0
        self.damp = damp
        self.machar = machar(double=1)
        machep = self.machar.machep
        self.dof = 0
        if fcn == None:
            self.errmsg = "Usage: parms = mpfit('myfunt', ... )"
            return
        if iterfunct == 'default':
            iterfunct = self.defiter
        if self.damp != 0 and autoderivative == 0:
            self.errmsg = 'ERROR: keywords DAMP and AUTODERIVATIVE are mutually exclusive'
            return
        else:
            if xall is None and parinfo is None:
                self.errmsg = 'ERROR: must pass parameters in P or PARINFO'
                return
            if parinfo is not None:
                if type(parinfo) != types.ListType:
                    self.errmsg = 'ERROR: PARINFO must be a list of dictionaries.'
                    return
                if type(parinfo[0]) != types.DictionaryType:
                    self.errmsg = 'ERROR: PARINFO must be a list of dictionaries.'
                    return
                if xall is not None and len(xall) != len(parinfo):
                    self.errmsg = 'ERROR: number of elements in PARINFO and P must agree'
                    return
            if xall is None:
                xall = self.parinfo(parinfo, 'value')
                if xall is None:
                    self.errmsg = 'ERROR: either P or PARINFO(*)["value"] must be supplied.'
                    return
            xall = numpy.asarray(xall, float)
            npar = len(xall)
            self.fnorm = -1.0
            fnorm1 = -1.0
            ptied = self.parinfo(parinfo, 'tied', default='', n=npar)
            self.qanytied = 0
            for i in range(npar):
                ptied[i] = ptied[i].strip()
                if ptied[i] != '':
                    self.qanytied = 1

            self.ptied = ptied
            pfixed = self.parinfo(parinfo, 'fixed', default=0, n=npar)
            pfixed = pfixed == 1
            for i in range(npar):
                pfixed[i] = pfixed[i] or ptied[i] != ''

            step = self.parinfo(parinfo, 'step', default=0.0, n=npar)
            dstep = self.parinfo(parinfo, 'relstep', default=0.0, n=npar)
            dside = self.parinfo(parinfo, 'mpside', default=0, n=npar)
            maxstep = self.parinfo(parinfo, 'mpmaxstep', default=0.0, n=npar)
            minstep = self.parinfo(parinfo, 'mpminstep', default=0.0, n=npar)
            qmin = minstep != 0
            qmin[:] = False
            qmax = maxstep != 0
            if numpy.any(qmin & qmax & (maxstep < minstep)):
                self.errmsg = 'ERROR: MPMINSTEP is greater than MPMAXSTEP'
                return
            wh = numpy.nonzero((qmin != 0.0) | (qmax != 0.0))[0]
            qminmax = len(wh > 0)
            ifree = numpy.nonzero(pfixed != 1)[0]
            nfree = len(ifree)
            if nfree == 0:
                self.errmsg = 'ERROR: no free parameters'
                return
            self.params = xall.copy()
            x = self.params[ifree]
            limited = self.parinfo(parinfo, 'limited', default=[0, 0], n=npar)
            limits = self.parinfo(parinfo, 'limits', default=[0.0, 0.0], n=npar)
            if limited is not None and limits is not None:
                if numpy.any(limited[:, 0] & (xall < limits[:, 0]) | limited[:, 1] & (xall > limits[:, 1])):
                    self.errmsg = 'ERROR: parameters are not within PARINFO limits'
                    return
                if numpy.any(limited[:, 0] & limited[:, 1] & (limits[:, 0] >= limits[:, 1]) & (pfixed == 0)):
                    self.errmsg = 'ERROR: PARINFO parameter limits are not consistent'
                    return
                qulim = limited[:, 1][ifree]
                ulim = limits[:, 1][ifree]
                qllim = limited[:, 0][ifree]
                llim = limits[:, 0][ifree]
                if numpy.any((qulim != 0.0) | (qllim != 0.0)):
                    qanylim = 1
                else:
                    qanylim = 0
            else:
                qulim = numpy.zeros(nfree)
                ulim = x * 0.0
                qllim = qulim
                llim = x * 0.0
                qanylim = 0
            n = len(x)
            if n < 0 or ftol <= 0 or xtol <= 0 or gtol <= 0 or maxiter < 0 or factor <= 0:
                self.errmsg = 'ERROR: input keywords are inconsistent'
                return
            if rescale != 0:
                self.errmsg = 'ERROR: DIAG parameter scales are inconsistent'
                if len(diag) < n:
                    return
                if numpy.any(diag <= 0):
                    return
                self.errmsg = ''
            x = numpy.asarray(x, float)
            self.status, fvec = self.call(fcn, self.params, functkw)
            if self.status < 0:
                self.errmsg = 'ERROR: first call to "' + str(fcn) + '" failed'
                return
            m = len(fvec)
            if m < n:
                self.errmsg = 'ERROR: number of parameters must not exceed data'
                return
            self.dof = m - nfree
            self.fnorm = self.enorm(fvec)
            par = 0.0
            self.niter = 1
            qtf = x * 0.0
            self.status = 0
            while 1:
                self.params[ifree] = x
                if self.qanytied:
                    self.params = self.tie(self.params, ptied)
                if nprint > 0 and iterfunct is not None:
                    if (self.niter - 1) % nprint == 0:
                        mperr = 0
                        xnew0 = self.params.copy()
                        dof = numpy.max([len(fvec) - len(x), 0])
                        status = iterfunct(fcn, self.params, self.niter, (self.fnorm ** 2), functkw=functkw, parinfo=parinfo, quiet=quiet, dof=dof, **iterkw)
                        if status is not None:
                            self.status = status
                        if self.status < 0:
                            self.errmsg = 'WARNING: premature termination by ' + str(iterfunct)
                            return
                        if numpy.max(numpy.abs(xnew0 - self.params)) > 0:
                            if self.qanytied:
                                self.params = self.tie(self.params, ptied)
                            x = self.params[ifree]
                self.status = 2
                catch_msg = 'calling MPFIT_FDJAC2'
                fjac = self.fdjac2(fcn, x, fvec, step, qulim, ulim, dside, epsfcn=epsfcn, autoderivative=autoderivative, dstep=dstep, functkw=functkw, ifree=ifree, xall=self.params)
                if fjac is None:
                    self.errmsg = 'WARNING: premature termination by FDJAC2'
                    return
                if qanylim:
                    catch_msg = 'zeroing derivatives of pegged parameters'
                    whlpeg = numpy.nonzero(qllim & (x == llim))[0]
                    nlpeg = len(whlpeg)
                    whupeg = numpy.nonzero(qulim & (x == ulim))[0]
                    nupeg = len(whupeg)
                    if nlpeg > 0:
                        for i in range(nlpeg):
                            sum0 = sum(fvec * fjac[:, whlpeg[i]])
                            if sum0 > 0:
                                fjac[:, whlpeg[i]] = 0

                    if nupeg > 0:
                        for i in range(nupeg):
                            sum0 = sum(fvec * fjac[:, whupeg[i]])
                            if sum0 < 0:
                                fjac[:, whupeg[i]] = 0

                fjac, ipvt, wa1, wa2 = self.qrfac(fjac, pivot=1)
                catch_msg = 'rescaling diagonal elements'
                if self.niter == 1:
                    if rescale == 0 or len(diag) < n:
                        diag = wa2.copy()
                        diag[diag == 0] = 1.0
                    wa3 = diag * x
                    xnorm = self.enorm(wa3)
                    delta = factor * xnorm
                    if delta == 0.0:
                        delta = factor
                catch_msg = 'forming (q transpose)*fvec'
                wa4 = fvec.copy()
                for j in range(n):
                    lj = ipvt[j]
                    temp3 = fjac[(j, lj)]
                    if temp3 != 0:
                        fj = fjac[j:, lj]
                        wj = wa4[j:]
                        wa4[j:] = wj - fj * sum(fj * wj) / temp3
                    fjac[(j, lj)] = wa1[j]
                    qtf[j] = wa4[j]

                fjac = fjac[0:n, 0:n]
                fjac.shape = [n, n]
                temp = fjac.copy()
                for i in range(n):
                    temp[:, i] = fjac[:, ipvt[i]]

                fjac = temp.copy()
                catch_msg = 'computing the scaled gradient'
                gnorm = 0.0
                if self.fnorm != 0:
                    for j in range(n):
                        l = ipvt[j]
                        if wa2[l] != 0:
                            sum0 = sum(fjac[0:j + 1, j] * qtf[0:j + 1]) / self.fnorm
                            gnorm = numpy.max([gnorm, numpy.abs(sum0 / wa2[l])])

                if gnorm <= gtol:
                    self.status = 4
                    break
                if maxiter == 0:
                    self.status = 5
                    break
                if rescale == 0:
                    diag = numpy.choose(diag > wa2, (wa2, diag))
                while 1:
                    catch_msg = 'calculating LM parameter (MPFIT_)'
                    fjac, par, wa1, wa2 = self.lmpar(fjac, ipvt, diag, qtf, delta, wa1, wa2, par=par)
                    wa1 = -wa1
                    if qanylim == 0 and qminmax == 0:
                        alpha = 1.0
                        wa2 = x + wa1
                    else:
                        alpha = 1.0
                        if qanylim:
                            catch_msg = 'checking for a step out of bounds'
                            if nlpeg > 0:
                                wa1[whlpeg] = numpy.clip(wa1[whlpeg], 0.0, numpy.max(wa1))
                            if nupeg > 0:
                                wa1[whupeg] = numpy.clip(wa1[whupeg], numpy.min(wa1), 0.0)
                            dwa1 = numpy.abs(wa1) > machep
                            whl = numpy.nonzero((dwa1 != 0.0) & qllim & (x + wa1 < llim))[0]
                            if len(whl) > 0:
                                t = (llim[whl] - x[whl]) / wa1[whl]
                                alpha = numpy.min([alpha, numpy.min(t)])
                            whu = numpy.nonzero((dwa1 != 0.0) & qulim & (x + wa1 > ulim))[0]
                            if len(whu) > 0:
                                t = (ulim[whu] - x[whu]) / wa1[whu]
                                alpha = numpy.min([alpha, numpy.min(t)])
                        if qminmax:
                            nwa1 = wa1 * alpha
                            whmax = numpy.nonzero((qmax != 0.0) & (maxstep > 0))[0]
                            if len(whmax) > 0:
                                mrat = numpy.max(numpy.abs(nwa1[whmax]) / numpy.abs(maxstep[ifree[whmax]]))
                                if mrat > 1:
                                    alpha = alpha / mrat
                        wa1 = wa1 * alpha
                        wa2 = x + wa1
                        sgnu = (ulim >= 0) * 2.0 - 1.0
                        sgnl = (llim >= 0) * 2.0 - 1.0
                        ulim1 = ulim * (1 - sgnu * machep) - (ulim == 0) * machep
                        llim1 = llim * (1 + sgnl * machep) + (llim == 0) * machep
                        wh = numpy.nonzero((qulim != 0) & (wa2 >= ulim1))[0]
                        if len(wh) > 0:
                            wa2[wh] = ulim[wh]
                        wh = numpy.nonzero((qllim != 0.0) & (wa2 <= llim1))[0]
                        if len(wh) > 0:
                            wa2[wh] = llim[wh]
                        wa3 = diag * wa1
                        pnorm = self.enorm(wa3)
                        if self.niter == 1:
                            delta = numpy.min([delta, pnorm])
                        self.params[ifree] = wa2
                        mperr = 0
                        catch_msg = 'calling ' + str(fcn)
                        self.status, wa4 = self.call(fcn, self.params, functkw)
                        if self.status < 0:
                            self.errmsg = 'WARNING: premature termination by "' + fcn + '"'
                            return
                        fnorm1 = self.enorm(wa4)
                        catch_msg = 'computing convergence criteria'
                        actred = -1.0
                        if 0.1 * fnorm1 < self.fnorm:
                            actred = -(fnorm1 / self.fnorm) ** 2 + 1.0
                        for j in range(n):
                            wa3[j] = 0
                            wa3[0:(j + 1)] = wa3[0:j + 1] + fjac[0:j + 1, j] * wa1[ipvt[j]]

                    temp1 = self.enorm(alpha * wa3) / self.fnorm
                    temp2 = numpy.sqrt(alpha * par) * pnorm / self.fnorm
                    prered = temp1 * temp1 + temp2 * temp2 / 0.5
                    dirder = -(temp1 * temp1 + temp2 * temp2)
                    ratio = 0.0
                    if prered != 0:
                        ratio = actred / prered
                    if ratio <= 0.25:
                        if actred >= 0:
                            temp = 0.5
                        else:
                            temp = 0.5 * dirder / (dirder + 0.5 * actred)
                        if 0.1 * fnorm1 >= self.fnorm or temp < 0.1:
                            temp = 0.1
                        delta = temp * numpy.min([delta, pnorm / 0.1])
                        par = par / temp
                    elif par == 0 or ratio >= 0.75:
                        delta = pnorm / 0.5
                        par = 0.5 * par
                    if ratio >= 0.0001:
                        x = wa2
                        wa2 = diag * x
                        fvec = wa4
                        xnorm = self.enorm(wa2)
                        self.fnorm = fnorm1
                        self.niter = self.niter + 1
                    if numpy.abs(actred) <= ftol and prered <= ftol and 0.5 * ratio <= 1:
                        self.status = 1
                    if delta <= xtol * xnorm:
                        self.status = 2
                    if numpy.abs(actred) <= ftol and prered <= ftol and 0.5 * ratio <= 1 and self.status == 2:
                        self.status = 3
                    if self.status != 0:
                        break
                    if self.niter >= maxiter:
                        self.status = 5
                    if numpy.abs(actred) <= machep and prered <= machep and 0.5 * ratio <= 1:
                        self.status = 6
                    if delta <= machep * xnorm:
                        self.status = 7
                    if gnorm <= machep:
                        self.status = 8
                    if self.status != 0:
                        break
                    if ratio >= 0.0001:
                        break
                    if ~numpy.all(numpy.isfinite(wa1) & numpy.isfinite(wa2) & numpy.isfinite(x)) or ~numpy.isfinite(ratio):
                        errmsg = "ERROR: parameter or function value(s) have become \n\t\t\t\t\t\t'infinite; check model function for over- 'and underflow"
                        self.status = -16
                        break

                if self.status != 0:
                    break

            catch_msg = 'in the termination phase'
            if len(self.params) == 0:
                return
            if nfree == 0:
                self.params = xall.copy()
            else:
                self.params[ifree] = x
            if nprint > 0 and self.status > 0:
                catch_msg = 'calling ' + str(fcn)
                status, fvec = self.call(fcn, self.params, functkw)
                catch_msg = 'in the termination phase'
                self.fnorm = self.enorm(fvec)
            if self.fnorm is not None and fnorm1 is not None:
                self.fnorm = numpy.max([self.fnorm, fnorm1])
                self.fnorm = self.fnorm ** 2.0
            self.covar = None
            self.perror = None
            if self.status > 0 and nocovar == 0 and n is not None and fjac is not None and ipvt is not None:
                sz = fjac.shape
                if n > 0 and sz[0] >= n and sz[1] >= n and len(ipvt) >= n:
                    catch_msg = 'computing the covariance matrix'
                    cv = self.calc_covar(fjac[0:n, 0:n], ipvt[0:n])
                    cv.shape = [n, n]
                    nn = len(xall)
                    self.covar = numpy.zeros([nn, nn], dtype=float)
                    for i in range(n):
                        self.covar[(ifree, ifree[i])] = cv[:, i]

                    catch_msg = 'computing parameter errors'
                    self.perror = numpy.zeros(nn, dtype=float)
                    d = numpy.diagonal(self.covar)
                    wh = numpy.nonzero(d >= 0)[0]
                    if len(wh) > 0:
                        self.perror[wh] = numpy.sqrt(d[wh])
            return

    def __str__(self):
        return {'params': self.params, 'niter': self.niter, 
           'params': self.params, 
           'covar': self.covar, 
           'perror': self.perror, 
           'status': self.status, 
           'debug': self.debug, 
           'errmsg': self.errmsg, 
           'nfev': self.nfev, 
           'damp': self.damp}.__str__()

    def defiter(self, fcn, x, iter, fnorm=None, functkw=None, quiet=0, iterstop=None, parinfo=None, format=None, pformat='%.10g', dof=1):
        if self.debug:
            print 'Entering defiter...'
        if quiet:
            return
        else:
            if fnorm is None:
                status, fvec = self.call(fcn, x, functkw)
                fnorm = self.enorm(fvec) ** 2
            nprint = len(x)
            print 'Iter ', '%6i' % iter, '   CHI-SQUARE = ', '%.10g' % fnorm, ' DOF = ', '%i' % dof
            for i in range(nprint):
                if parinfo is not None and parinfo[i].has_key('parname'):
                    p = '   ' + parinfo[i]['parname'] + ' = '
                else:
                    p = '   P' + str(i) + ' = '
                if parinfo is not None and parinfo[i].has_key('mpprint'):
                    iprint = parinfo[i]['mpprint']
                else:
                    iprint = 1
                if iprint:
                    print p + pformat % x[i] + '  '

            return 0

    def parinfo(self, parinfo=None, key='a', default=None, n=0):
        if self.debug:
            print 'Entering parinfo...'
        if n == 0 and parinfo is not None:
            n = len(parinfo)
        if n == 0:
            values = default
            return values
        else:
            values = []
            for i in range(n):
                if parinfo is not None and parinfo[i].has_key(key):
                    values.append(parinfo[i][key])
                else:
                    values.append(default)

            test = default
            if type(default) == types.ListType:
                test = default[0]
            if isinstance(test, types.IntType):
                values = numpy.asarray(values, int)
            elif isinstance(test, types.FloatType):
                values = numpy.asarray(values, float)
            return values

    def call(self, fcn, x, functkw, fjac=None):
        if self.debug:
            print 'Entering call...'
        if self.qanytied:
            x = self.tie(x, self.ptied)
        self.nfev = self.nfev + 1
        if fjac is None:
            status, f = fcn(x, fjac=fjac, **functkw)
            if self.damp > 0:
                f = numpy.tanh(f / self.damp)
            return [status, f]
        else:
            return fcn(x, fjac=fjac, **functkw)
            return

    def enorm(self, vec):
        ans = mpfit.blas_enorm(vec)
        return ans

    def fdjac2(self, fcn, x, fvec, step=None, ulimited=None, ulimit=None, dside=None, epsfcn=None, autoderivative=1, functkw=None, xall=None, ifree=None, dstep=None):
        if self.debug:
            print 'Entering fdjac2...'
        machep = self.machar.machep
        if epsfcn is None:
            epsfcn = machep
        if xall is None:
            xall = x
        if ifree is None:
            ifree = numpy.arange(len(xall))
        if step is None:
            step = x * 0.0
        nall = len(xall)
        eps = numpy.sqrt(numpy.max([epsfcn, machep]))
        m = len(fvec)
        n = len(x)
        if autoderivative == 0:
            mperr = 0
            fjac = numpy.zeros(nall, dtype=float)
            fjac[ifree] = 1.0
            status, fp = self.call(fcn, xall, functkw, fjac=fjac)
            if len(fjac) != m * nall:
                print 'ERROR: Derivative matrix was not computed properly.'
                return
            fjac.shape = [
             m, nall]
            fjac = -fjac
            if len(ifree) < nall:
                fjac = fjac[:, ifree]
                fjac.shape = [m, n]
                return fjac
        fjac = numpy.zeros([m, n], dtype=float)
        h = eps * numpy.abs(x)
        if step is not None:
            stepi = step[ifree]
            wh = numpy.nonzero(stepi > 0)[0]
            if len(wh) > 0:
                h[wh] = stepi[wh]
        if len(dstep) > 0:
            dstepi = dstep[ifree]
            wh = numpy.nonzero(dstepi > 0)[0]
            if len(wh) > 0:
                h[wh] = numpy.abs(dstepi[wh] * x[wh])
        h[h == 0] = eps
        mask = dside[ifree] == -1
        if len(ulimited) > 0 and len(ulimit) > 0:
            mask = mask | (ulimited != 0) & (x > ulimit - h)
            wh = numpy.nonzero(mask)[0]
            if len(wh) > 0:
                h[wh] = -h[wh]
        for j in range(n):
            xp = xall.copy()
            xp[ifree[j]] = xp[ifree[j]] + h[j]
            status, fp = self.call(fcn, xp, functkw)
            if status < 0:
                return
            if numpy.abs(dside[ifree[j]]) <= 1:
                fjac[0:, j] = (fp - fvec) / h[j]
            else:
                xp[ifree[j]] = xall[ifree[j]] - h[j]
                mperr = 0
                status, fm = self.call(fcn, xp, functkw)
                if status < 0:
                    return
                fjac[0:, j] = (fp - fm) / (2 * h[j])

        return fjac

    def qrfac(self, a, pivot=0):
        if self.debug:
            print 'Entering qrfac...'
        machep = self.machar.machep
        sz = a.shape
        m = sz[0]
        n = sz[1]
        acnorm = numpy.zeros(n, dtype=float)
        for j in range(n):
            acnorm[j] = self.enorm(a[:, j])

        rdiag = acnorm.copy()
        wa = rdiag.copy()
        ipvt = numpy.arange(n)
        minmn = numpy.min([m, n])
        for j in range(minmn):
            if pivot != 0:
                rmax = numpy.max(rdiag[j:])
                kmax = numpy.nonzero(rdiag[j:] == rmax)[0]
                ct = len(kmax)
                kmax = kmax + j
                if ct > 0:
                    kmax = kmax[0]
                    if kmax != j:
                        temp = ipvt[j]
                        ipvt[j] = ipvt[kmax]
                        ipvt[kmax] = temp
                        rdiag[kmax] = rdiag[j]
                        wa[kmax] = wa[j]
            lj = ipvt[j]
            ajj = a[j:, lj]
            ajnorm = self.enorm(ajj)
            if ajnorm == 0:
                break
            if a[(j, lj)] < 0:
                ajnorm = -ajnorm
            ajj = ajj / ajnorm
            ajj[0] = ajj[0] + 1
            a[j:, lj] = ajj
            if j + 1 < n:
                for k in range(j + 1, n):
                    lk = ipvt[k]
                    ajk = a[j:, lk]
                    if a[(j, lj)] != 0:
                        a[j:, lk] = ajk - ajj * sum(ajk * ajj) / a[(j, lj)]
                        if pivot != 0 and rdiag[k] != 0:
                            temp = a[(j, lk)] / rdiag[k]
                            rdiag[k] = rdiag[k] * numpy.sqrt(numpy.max([1.0 - temp ** 2, 0.0]))
                            temp = rdiag[k] / wa[k]
                            if 0.05 * temp * temp <= machep:
                                rdiag[k] = self.enorm(a[j + 1:, lk])
                                wa[k] = rdiag[k]

            rdiag[j] = -ajnorm

        return [
         a, ipvt, rdiag, acnorm]

    def qrsolv(self, r, ipvt, diag, qtb, sdiag):
        if self.debug:
            print 'Entering qrsolv...'
        sz = r.shape
        m = sz[0]
        n = sz[1]
        for j in range(n):
            r[j:n, j] = r[j, j:n]

        x = numpy.diagonal(r)
        wa = qtb.copy()
        for j in range(n):
            l = ipvt[j]
            if diag[l] == 0:
                break
            sdiag[j:] = 0
            sdiag[j] = diag[l]
            qtbpj = 0.0
            for k in range(j, n):
                if sdiag[k] == 0:
                    break
                if numpy.abs(r[(k, k)]) < numpy.abs(sdiag[k]):
                    cotan = r[(k, k)] / sdiag[k]
                    sine = 0.5 / numpy.sqrt(0.25 + 0.25 * cotan * cotan)
                    cosine = sine * cotan
                else:
                    tang = sdiag[k] / r[(k, k)]
                    cosine = 0.5 / numpy.sqrt(0.25 + 0.25 * tang * tang)
                    sine = cosine * tang
                r[(k, k)] = cosine * r[(k, k)] + sine * sdiag[k]
                temp = cosine * wa[k] + sine * qtbpj
                qtbpj = -sine * wa[k] + cosine * qtbpj
                wa[k] = temp
                if n > k + 1:
                    temp = cosine * r[k + 1:n, k] + sine * sdiag[k + 1:n]
                    sdiag[(k + 1):n] = -sine * r[k + 1:n, k] + cosine * sdiag[k + 1:n]
                    r[k + 1:n, k] = temp

            sdiag[j] = r[(j, j)]
            r[(j, j)] = x[j]

        nsing = n
        wh = numpy.nonzero(sdiag == 0)[0]
        if len(wh) > 0:
            nsing = wh[0]
            wa[nsing:] = 0
        if nsing >= 1:
            wa[nsing - 1] = wa[(nsing - 1)] / sdiag[(nsing - 1)]
            for j in range(nsing - 2, -1, -1):
                sum0 = sum(r[j + 1:nsing, j] * wa[j + 1:nsing])
                wa[j] = (wa[j] - sum0) / sdiag[j]

        x[ipvt] = wa
        return (r, x, sdiag)

    def lmpar(self, r, ipvt, diag, qtb, delta, x, sdiag, par=None):
        if self.debug:
            print 'Entering lmpar...'
        dwarf = self.machar.minnum
        machep = self.machar.machep
        sz = r.shape
        m = sz[0]
        n = sz[1]
        nsing = n
        wa1 = qtb.copy()
        rthresh = numpy.max(numpy.abs(numpy.diagonal(r))) * machep
        wh = numpy.nonzero(numpy.abs(numpy.diagonal(r)) < rthresh)[0]
        if len(wh) > 0:
            nsing = wh[0]
            wa1[(wh[0]):] = 0
        if nsing >= 1:
            for j in range(nsing - 1, -1, -1):
                wa1[j] = wa1[j] / r[(j, j)]
                if j - 1 >= 0:
                    wa1[0:j] = wa1[0:j] - r[0:j, j] * wa1[j]

        x[ipvt] = wa1
        iter = 0
        wa2 = diag * x
        dxnorm = self.enorm(wa2)
        fp = dxnorm - delta
        if fp <= 0.1 * delta:
            return [r, 0.0, x, sdiag]
        parl = 0.0
        if nsing >= n:
            wa1 = diag[ipvt] * wa2[ipvt] / dxnorm
            wa1[0] = wa1[0] / r[(0, 0)]
            for j in range(1, n):
                sum0 = sum(r[0:j, j] * wa1[0:j])
                wa1[j] = (wa1[j] - sum0) / r[(j, j)]

            temp = self.enorm(wa1)
            parl = fp / delta / temp / temp
        for j in range(n):
            sum0 = sum(r[0:j + 1, j] * qtb[0:j + 1])
            wa1[j] = sum0 / diag[ipvt[j]]

        gnorm = self.enorm(wa1)
        paru = gnorm / delta
        if paru == 0:
            paru = dwarf / numpy.min([delta, 0.1])
        par = numpy.max([par, parl])
        par = numpy.min([par, paru])
        if par == 0:
            par = gnorm / dxnorm
        while 1:
            iter = iter + 1
            if par == 0:
                par = numpy.max([dwarf, paru * 0.001])
            temp = numpy.sqrt(par)
            wa1 = temp * diag
            r, x, sdiag = self.qrsolv(r, ipvt, wa1, qtb, sdiag)
            wa2 = diag * x
            dxnorm = self.enorm(wa2)
            temp = fp
            fp = dxnorm - delta
            if numpy.abs(fp) <= 0.1 * delta or parl == 0 and fp <= temp and temp < 0 or iter == 10:
                break
            wa1 = diag[ipvt] * wa2[ipvt] / dxnorm
            for j in range(n - 1):
                wa1[j] = wa1[j] / sdiag[j]
                wa1[(j + 1):n] = wa1[j + 1:n] - r[j + 1:n, j] * wa1[j]

            wa1[n - 1] = wa1[(n - 1)] / sdiag[(n - 1)]
            temp = self.enorm(wa1)
            parc = fp / delta / temp / temp
            if fp > 0:
                parl = numpy.max([parl, par])
            if fp < 0:
                paru = numpy.min([paru, par])
            par = numpy.max([parl, par + parc])

        return [
         r, par, x, sdiag]

    def tie(self, p, ptied=None):
        if self.debug:
            print 'Entering tie...'
        if ptied is None:
            return
        else:
            for i in range(len(ptied)):
                if ptied[i] == '':
                    continue
                cmd = 'p[' + str(i) + '] = ' + ptied[i]
                exec cmd

            return p

    def calc_covar(self, rr, ipvt=None, tol=1e-14):
        if self.debug:
            print 'Entering calc_covar...'
        if numpy.rank(rr) != 2:
            print 'ERROR: r must be a two-dimensional matrix'
            return -1
        else:
            s = rr.shape
            n = s[0]
            if s[0] != s[1]:
                print 'ERROR: r must be a square matrix'
                return -1
            if ipvt is None:
                ipvt = numpy.arange(n)
            r = rr.copy()
            r.shape = [n, n]
            l = -1
            tolr = tol * numpy.abs(r[(0, 0)])
            for k in range(n):
                if numpy.abs(r[(k, k)]) <= tolr:
                    break
                r[(k, k)] = 1.0 / r[(k, k)]
                for j in range(k):
                    temp = r[(k, k)] * r[(j, k)]
                    r[(j, k)] = 0.0
                    r[0:j + 1, k] = r[0:j + 1, k] - temp * r[0:j + 1, j]

                l = k

            if l >= 0:
                for k in range(l + 1):
                    for j in range(k):
                        temp = r[(j, k)]
                        r[0:j + 1, j] = r[0:j + 1, j] + temp * r[0:j + 1, k]

                    temp = r[(k, k)]
                    r[0:k + 1, k] = temp * r[0:k + 1, k]

            wa = numpy.repeat([r[(0, 0)]], n)
            for j in range(n):
                jj = ipvt[j]
                sing = j > l
                for i in range(j + 1):
                    if sing:
                        r[(i, j)] = 0.0
                    ii = ipvt[i]
                    if ii > jj:
                        r[(ii, jj)] = r[(i, j)]
                    if ii < jj:
                        r[(jj, ii)] = r[(i, j)]

                wa[jj] = r[(j, j)]

            for j in range(n):
                r[0:j + 1, j] = r[j, 0:j + 1]
                r[(j, j)] = wa[j]

            return r


class machar():

    def __init__(self, double=1):
        if double == 0:
            info = numpy.finfo(numpy.float32)
        else:
            info = numpy.finfo(numpy.float64)
        self.machep = info.eps
        self.maxnum = info.max
        self.minnum = info.tiny
        self.maxlog = numpy.log(self.maxnum)
        self.minlog = numpy.log(self.minnum)
        self.rdwarf = numpy.sqrt(self.minnum * 1.5) * 10
        self.rgiant = numpy.sqrt(self.maxnum) * 0.1