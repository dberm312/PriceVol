# -*- coding: utf-8 -*-
#Utils for PriceVols
import pandas as pd
import numpy as np
def makePort(labels):
    '''
    Parameters
    ----------
    labels : List
        List of Strings to label the portfolio Comps.

    Returns
    -------
    Pandas DataFrame of potential Portfolios.
    '''
    n=11
    out = pd.DataFrame(np.linspace(0,1,n),index=np.zeros(n),columns = [labels[0]])
    for i in labels[1:]:
        out = out.join(pd.DataFrame(np.linspace(0,1,n),index=np.zeros(n),columns = [i]))
    out = ((out.T/out.T.sum()).T).applymap(lambda x:np.round(x,3)).drop_duplicates().dropna()
    out.index = range(out.shape[0])
    return(out)

def portVol(r,vol,corr,p):
    '''
    Parameters
    ----------
     r : Pandas Series
         Series of expected returns for components in portfolio.
    Vol : Pandas Series
        Series of implied volitility for commonents in portfolio.
    corr : Pandas DataFrame
        Corrlation Matrix of components of portfolio.
    p : Pandas Series
        Series of given the percentage of .

    Returns
    -------
    Float Portfolio Variance.
    '''
    out = 0
    for i in r.index:
        out+= p[i]*vol[i]
        for j in r.index:
            out+=corr[i][j]*p[i]*p[j]*np.sqrt(vol[i])*np.sqrt(vol[j])
    return(out)

class Portfolio:
    def __init__(self,r,vol,corr,):
        '''
        Parameters
        ----------
        r : Pandas Series
            Series of expected returns for components in portfolio.
        vol : Pandas Series
            Series of implied volitility for commonents in portfolio.
        corr : Pandas DataFrame
            Corrlation Matrix of components of portfolio.
        '''
        self.r = r
        self.vol = vol
        self.corr = corr
        
        df = makePort(r.index)
        rs = r.dot(df.T)
        vs = []
        for i in df.index:
            vs.append(portVol(r,vol,corr,df.iloc[i]))
        df['return'] = rs
        df['vol'] = vs
        self.df = df
    def sharpe(self,rf):
        '''
        Parameters
        ----------
        rf : float
            Risk Free Intrest Rate.

        Returns
        -------
        Adds Sharp Ratio Column in DataFrame.

        '''
        self.rf = rf
        self.df['sharpe'] = (self.df['return']-rf)/(self.df['vol'])
    
    def components(self):
        temp = self.df[self.df[['corn','soyb','weat']].isin([1]).sum(1).astype(bool)]
        temp.index = temp[['corn','soyb','weat']].idxmax(1)
        temp = temp[['return','vol']]
        return(temp)
    
    def stats(self):
        maxreturn = pd.DataFrame(self.df.loc[self.df['return'].idxmax()])
        maxreturn.columns = ['maxreturn']
        minvol = pd.DataFrame(self.df.loc[self.df['vol'].idxmin()])
        minvol.columns = ['minvol']
        maxsharpe = pd.DataFrame(self.df.loc[self.df['sharpe'].idxmax()])
        maxsharpe.columns = ['maxsharpe']
        return(maxreturn.join(minvol).join(maxsharpe))