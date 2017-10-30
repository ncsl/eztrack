'''
gaussianmodels.py
@By: Adam Li
@Date: 10/16/17

@Description: Class designed for holding the gaussian weighting function


@Methods:

'''

# Imports necessary for this function
import numpy as np
import math
import os
import logging.config
import yaml

from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import GridSearchCV

class TrainingModel():
    def __init__(self, listofpatients, origins=None):
        self.listofpats = listofpatients
        self.loo = LeaveOneOut()
        self.origins = origins

        print "The number of splits based on patients is: ", self.loo.get_n_splits(listofpatients)

    def train(self, params):
        # doascores is a Nx1 vector of degree of agreements
        # ezlikelihoods is a NxC matrix of likelihoods for N patients for C data points

        # split ezlikelihoods and doascores
        for train_index, test_index in loo.split(listofpatients):
            pat_train, pat_test = listofpatients[train_index], listofpatients[test_index]
            
            # create training and testing matrices of data
            X_train = []
            X_test = []
            y_train = []
            y_test = []

            # evaluate ranked EVC of each patients
            for pat in pat_train:
                # get the patieeg

                # initialize Gaussian weightmodel

                # evaluate model and compute weight

                # compute doa
            for pat in pat_test:

          # perform fitting evaluation on certain gaussian weighting function

    def gridsearch(self):
        # perform grid search on params by passing them over and over into training


class GaussianWeightModel(TrainingModel):
    def __init__(self, numchans, numseiz, numheatmapcolors=20, logger=None, default_path='logging_mvarmodels.yaml'):
        # super(MVARModel, self).__init__(winsize, stepsize)
        TrainingModel.__init__(self)

        # initialize logger configuration for Linear Model
        if not logger:
            self.setup_logging(default_path=default_path)

        self.numchans = numchans
        self.numseiz = numseiz
        self.numheatmapcolors = numheatmapcolors

        # create and initialize logger
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info('Initialized Gaussian Weighting function!')

    def setup_logging(self, default_path='logging_linearmodels.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
        """Setup logging configuration for any loggers created
        """
        path = default_path
        value = os.getenv(env_key, None)

        # set path to the logger file
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)

    def initgaussianfuncs(self):
        # creates gaussian weighting function in '4' quadrants
        origins = np.array([[-250, -25],
                            [-100, -100],
                            [-270, -80],
                            [130, -60]])

        # initialize exponential multiplying factors
        mf1 = 2e-2
        mf2 = 2.4 * mf1
        mf3 = 4 * mf2
        mf4 = 1e-3 * mf3
        mf = [mf1 mf2 mf3 mf4]

        # elliptical axes multipliers for 2D Gaussian distribution
        ax_mf = np.array([[1, 1], 
                        [0.2, 1],
                        [1, 8],
                        [1, 1]])

    def computeinversecov(self, pcamat, ax_mf, mf):
        # get covariance matrix of pca matrix
        covmat = np.cov(pcamat)

        # create separate cov matrices for each quadrant
        invcovmat_1 = np.linalg.inv(covmat);
        invcovmat_1[0, 0] = ax_mf[0, 0] * invcovmat_1[0, 0]
        invcovmat_1[1, 1] = ax_mf[0, 1] * invcovmat_1[1, 1]
        
        invcovmat_2 = invcovmat_1
        invcovmat_2[0,0] = ax_mf[1,0] * invcovmat_2[0,0]
        invcovmat_2[1,1] = ax_mf[1,1] * mf[0] * invcovmat_2[1,1]/mf[1];

        invcovmat_3 = invcovmat_2
        invcovmat_3[0,0] = ax_mf[2,0] * mf[1] * invcovmat_2[0,0] / mf[2]
        invcovmat_3[1,1] = ax_mf[2,1] * invcovmat_2[1,1]

        invcovmat_4 = invcovmat_3
        invcovmat_4[0,0] = ax_mf[3,0] * mf[0] * invcovmat_1[0,0] / mf[3]
        invcovmat_4[1,1] = ax_mf[3,1] * mf[2] * invcovmat_3[1,1] / mf[3]

        # create 3d array to return
        inv_cov_mat = np.concatenate((inv_cov_mat1[...,np.newaxis], \
            inv_cov_mat2[...,np.newaxis], \
            inv_cov_mat3[...,np.newaxis], \
            inv_cov_mat4[...,np.newaxis]), axis=2)

        return inv_cov_mat

    def computepcaweights(self, pcamat, origin, mf, invcovmat):
        gaussian = np.zeros((self.numchans, 1))

        for i in range(0, self.numchans):
            gaussian[i] = self.computechanweights(pcamat, origin, mf, invcovmat)

        pcaweights = np.sum(gaussian, axis=1) / self.numseiz

        return pcaweights

    def computechanweights(self, pcapoint, origin, mf, invcovmat):
        # create heaviside functions to determine where the point lies
        heavisidepoints = np.array([[origin[0] - pcapoint[0], origin[1] - pcapoint[1]],
                                    [pcapoint[0] - origin[0], origin[1] - pcapoint[1]],
                                    [pcapoint[0] - origin[0], pcapoint[1] - origin[1]],
                                    [origin[0] - pcapoint[0], pcapoint[1] - origin[1]],
            ])
        hfunc = np.heaviside(heavisidepoints, 0.5)

        # compute weight of the point
        weight = 0
        for i in range(0, len(mf)):
            weight += np.exp(-mf[i] * (pcapoint - origin) * invcovmat[:,:,i] * (pcapoint - origin).T) * \
                hfunc[i, 0] * hfunc[i, 1]

        return weight

    def computepatdoa(self, weights, ezindices):
        # compute degree of agreement between the weights and indices

    def score(self, X, y):
        
