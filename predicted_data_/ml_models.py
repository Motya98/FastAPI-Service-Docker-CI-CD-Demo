from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, Lars, OrthogonalMatchingPursuit
from sklearn.linear_model import ARDRegression, BayesianRidge, HuberRegressor, QuantileRegressor, RANSACRegressor
from sklearn.linear_model import TheilSenRegressor, GammaRegressor, PoissonRegressor, TweedieRegressor, PassiveAggressiveRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, BaggingRegressor
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.neural_network import BernoulliRBM
from sklearn.svm import SVR


class Models:
    models = {
            'LinearRegression': {
                'model': LinearRegression(),
                'param_grid': {},
            },
            'Ridge': {
                'model': Ridge(),
                'param_grid': {
                    'alpha': [i + 0.0001 for i in range(0, 20)],
                    'max_iter': [1000000],
                    'solver': ['auto']
                }
            },
            'Lasso': {
                'model': Lasso(),
                'param_grid': {
                    'alpha': [0.1, 1, 5, 10, 20, 30, 40, 50, 100, 500, 1000],
                    'max_iter': [1000000]
                },
            },
            'Elastic': {
                'model': ElasticNet(),
                'param_grid': {
                    'alpha': [0.1, 1, 5],
                    'l1_ratio': [0.1, 0.5, 0.7, 0.9, 0.95, 1.0],
                    'max_iter': [1000000]
                }
            },
            'K_Neighbours': {
                'model': KNeighborsRegressor(),
                'param_grid': {
                    'n_neighbors': [i for i in range(1, 30)],
                    'algorithm': ['auto']
                }
            },
            'DecisionTree': {
                'model': DecisionTreeRegressor(),
                'param_grid': {
                    'max_leaf_nodes': [100]
                }
            },
            'RandomForestRegressor': {
                'model': RandomForestRegressor(),
                'param_grid': {
                    'criterion': ['squared_error'],
                    'max_depth': [100],
                    'n_estimators': [100, 160],
                    'max_features': [1]
                }
            },
            'SVR': {
                'model': SVR(),
                'param_grid': {}
            },
            'GradientBoostingRegressor': {
                'model': GradientBoostingRegressor(),
                'param_grid': {
                    'n_estimators': [50, 100, 150, 200],
                    'max_depth': [10000]
                },
            },
            'AdaBoostRegressor': {
                'model': AdaBoostRegressor(),
                'param_grid': {
                    'n_estimators': [50, 100, 150, 200]
                },
            },
            'KernelRidge': {
                'model': KernelRidge(),
                'param_grid': {
                    'alpha': [i + 0.0001 for i in range(0, 20)],
                }
            },
            'Lars': {
                'model': Lars(),
                'param_grid': {}
            },
            'OrthogonalMatchingPursuit': {
                'model': OrthogonalMatchingPursuit(),
                'param_grid': {}
            },
            'ARDRegression': {
                'model': ARDRegression(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'BayesianRidge': {
                'model': BayesianRidge(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'HuberRegressor': {
                'model': HuberRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'QuantileRegressor': {
                'model': QuantileRegressor(),
                'param_grid': {}
            },
            'RANSACRegressor': {
                'model': RANSACRegressor(),
                'param_grid': {}
            },
            'TheilSenRegressor': {
                'model': TheilSenRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'GammaRegressor': {
                'model': GammaRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'PoissonRegressor': {
                'model': PoissonRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'TweedieRegressor': {
                'model': TweedieRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'PassiveAggressiveRegressor': {
                'model': PassiveAggressiveRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'RadiusNeighborsRegressor': {
                'model': PassiveAggressiveRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                }
            },
            'BaggingRegressor': {
                'model': BaggingRegressor(),
                'param_grid': {
                    'n_estimators': [50, 100, 150, 200]
                },
            },
            'ExtraTreesRegressor': {
                'model': ExtraTreesRegressor(),
                'param_grid': {
                    'n_estimators': [50, 100, 150, 200]
                },
            },
            'HistGradientBoostingRegressor': {
                'model': HistGradientBoostingRegressor(),
                'param_grid': {
                    'max_iter': [10000],
                    'max_leaf_nodes': [1000],
                    'max_depth': [10000]
                },
            },
            'BernoulliRBM': {
                'model': BernoulliRBM(),
                'param_grid': {},
            },
        }


if __name__ == '__main__':
    print(dict(Models.models.items()))
