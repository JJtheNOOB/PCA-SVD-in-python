{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import random as rd\n",
    "from sklearn.decomposition import PCA\n",
    "from sklearn import preprocessing\n",
    "import matplotlib.pyplot as plt\n",
    "%matplotlib inline\n",
    "from sklearn.preprocessing import StandardScaler"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Generate the dataset\n",
    "genes = ['gene' + str(i) for i in range(1, 101)] #gene1, gene2, gene3...\n",
    "wk = ['wk' + str(i) for i in range(1, 6)] #wild sample\n",
    "ko = ['ko' + str(i) for i in range(1, 6)] #knock out sample\n",
    "\n",
    "data = pd.DataFrame(columns = [*wt, *ko], index = genes)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Fill the data with random values from poisson distributions\n",
    "for gene in genes:\n",
    "    data.loc[gene, 'wk1':'wk5'] = np.random.poisson(lam=rd.randrange(10,1000), size = 5)\n",
    "    data.loc[gene, 'ko1':'ko5'] = np.random.poisson(lam=rd.randrange(10,1000), size = 5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "       wk1  wk2  wk3  wk4  wk5  ko1  ko2  ko3  ko4  ko5\n",
      "gene1  789  805  777  820  782  816  802  787  838  786\n",
      "gene2  569  619  577  594  595  437  462  491  459  401\n",
      "gene3  738  754  828  762  760  190  191  218  177  182\n",
      "gene4  242  241  220  204  206  512  579  544  515  549\n",
      "gene5  592  618  637  706  627  364  381  308  350  372\n"
     ]
    }
   ],
   "source": [
    "print(data.head())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(100, 10)\n"
     ]
    }
   ],
   "source": [
    "print(data.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "D:\\Anacoda\\lib\\site-packages\\sklearn\\preprocessing\\data.py:625: DataConversionWarning: Data with input dtype int64 were all converted to float64 by StandardScaler.\n",
      "  return self.partial_fit(X, y)\n",
      "D:\\Anacoda\\lib\\site-packages\\sklearn\\base.py:462: DataConversionWarning: Data with input dtype int64 were all converted to float64 by StandardScaler.\n",
      "  return self.fit(X, **fit_params).transform(X)\n"
     ]
    }
   ],
   "source": [
    "#center and scale the data, mean would be 0 for each gene and std would be 1\n",
    "#scaled_data = preprocessing.scale(data.T) #Transpose the data\n",
    "scaled_data = StandardScaler().fit_transform(data.T)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Do the PCA\n",
    "pca = PCA()\n",
    "pca.fit(scaled_data)\n",
    "pca.data = pca.transform(scaled_data)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Percentage variance of each pca component stands for\n",
    "per_var = np.round(pca.explained_variance_ratio_*100, decimals = 1)\n",
    "#Create labels for the scree plot\n",
    "labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#Plot the data\n",
    "plt.bar(x=range(1, len(per_var)+1), height=per_var, tick_label = labels)\n",
    "plt.ylabel('percentage of Explained Variance')\n",
    "plt.xlabel('Principle Component')\n",
    "plt.title('Scree plot')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Almost all the variance is explained by the PC1 and PC2 component"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "#draw a pca plot\n",
    "pca_df = pd.DataFrame(pca.data, index = [*wt, *ko], columns = labels)\n",
    "plt.scatter(pca_df.PC1, pca_df.PC2)\n",
    "plt.ylabel('PC2 - {0}%'.format(per_var[1]))\n",
    "plt.xlabel('PC1 - {0}%'.format(per_var[0]))\n",
    "plt.title('My PC graph')\n",
    "\n",
    "for sample in pca_df.index:\n",
    "    plt.annotate(sample, (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))\n",
    "\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "WT samples and KO samples are correlated to each other"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "gene89    0.106856\n",
      "gene66    0.106827\n",
      "gene24    0.106822\n",
      "gene27    0.106799\n",
      "gene43   -0.106799\n",
      "gene84   -0.106784\n",
      "gene34   -0.106769\n",
      "gene15    0.106764\n",
      "gene58   -0.106760\n",
      "gene79    0.106747\n",
      "dtype: float64\n"
     ]
    }
   ],
   "source": [
    "loading_scores = pd.Series(pca.components_[0], index=genes) #pd series with loading scores in PC1\n",
    "sorted_loading_scores = loading_scores.abs().sort_values(ascending = False)\n",
    "\n",
    "top_10_genes = sorted_loading_scores[0:10].index.values\n",
    "\n",
    "print(loading_scores[top_10_genes])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "These genes are responsible for spliting the samples"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
