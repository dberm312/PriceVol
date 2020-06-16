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
    out = pd.DataFrame(np.linspace(0,1,26),index=np.zeros(26),columns = [labels[0]])
    for i in labels[1:]:
        out = out.join(pd.DataFrame(np.linspace(0,1,26),index=np.zeros(26),columns = [i]))
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